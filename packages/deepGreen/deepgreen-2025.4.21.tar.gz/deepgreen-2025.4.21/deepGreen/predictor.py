import os
import xarray as xr
import numpy as np
import torch
from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error,
    mean_absolute_percentage_error,
)

from . import utils

class Predictor:
    def __init__(self, model, data, ckpt_fpath):
        self.model = model
        self.data = data
        self.ckpt_fpath = ckpt_fpath
        self.ckpt = torch.load(self.ckpt_fpath, weights_only=True)
        self.model.load_state_dict(self.ckpt['state_dict'])

    def run(self, pred_fpath=None, truth_fpath=None):
        x = torch.stack([data[0] for data in self.data.test_set])
        y = torch.stack([data[1] for data in self.data.test_set])
        y = self.data.denormalize(y)
        y_hat = self.data.denormalize(self.model(x))

        self.ds_truth = xr.Dataset()
        self.ds_pred = xr.Dataset()

        for vn in self.data.output_vns:
            ds_template = self.data.ds[vn][self.data.test_idx[0]:self.data.test_idx[-1]+1]
            self.ds_truth[vn] = ds_template.copy()
            self.ds_pred[vn] = ds_template.copy()
            self.ds_truth[vn].values = y.squeeze(1).detach().numpy()
            self.ds_pred[vn].values = y_hat.squeeze(1).detach().numpy()

        if truth_fpath is not None:
            if os.path.exists(truth_fpath): os.remove(truth_fpath)
            dirpath = os.path.dirname(truth_fpath)
            if not os.path.exists(dirpath): os.makedirs(dirpath, exist_ok=True)
            self.ds_truth.to_netcdf(truth_fpath)
            utils.p_success(f'Truth saved at: "{truth_fpath}"')

        if pred_fpath is not None:
            if os.path.exists(pred_fpath): os.remove(pred_fpath)
            dirpath = os.path.dirname(pred_fpath)
            if not os.path.exists(dirpath): os.makedirs(dirpath, exist_ok=True)
            self.ds_pred.to_netcdf(pred_fpath)
            utils.p_success(f'Prediction saved at: "{pred_fpath}"')

    def plot_clim(self, vn):
        try:
            import x4c
        except ImportError:
            raise ImportError('x4c is required for this method. Please install x4c via: pip install x4c-exp.')

        x4c.set_style('journal', font_scale=1.0)

        ax_dict={
            'T_ann': (0, 0), 'P_ann': (0, 1),
            'T_DJF': (1, 0), 'P_DJF': (1, 1),
            'T_MAM': (2, 0), 'P_MAM': (2, 1),
            'T_JJA': (3, 0), 'P_JJA': (3, 1),
            'T_SON': (4, 0), 'P_SON': (4, 1),
        }
        proj_dict = {lb: 'Robinson' for lb in ax_dict.keys()}
        proj_kws_dict = {lb: dict(central_longitude=180) for lb in ax_dict.keys()}

        fig, ax = x4c.subplots(
            nrow=5, ncol=2,
            figsize=(10, 18),
            ax_loc=ax_dict,
            wspace=0.1, hspace=0.1,
            projs=proj_dict,
            projs_kws=proj_kws_dict,
            annotation=True, annotation_kws={'style': '', 'loc_x': 0}
        )

        ds_dict = {
            'Truth': self.ds_truth,
            'Prediction': self.ds_pred,
        }

        months_dict = {
            'DJF': [12, 1, 2],
            'MAM': [3, 4, 5],
            'JJA': [6, 7, 8],
            'SON': [9, 10, 11],
        }

        add_colorbar = False
        for name, ds in ds_dict.items():
            _, im = ds[vn].mean('time').x.plot(
                ax=ax[f'{name[0]}_ann'],
                cmap='PiYG',
                levels=np.linspace(-40, 0, 21),
                add_colorbar=add_colorbar,
                cbar_kwargs={'ticks': np.linspace(-40, 0, 11)},
                title=f'{name}: Annual Mean',
                return_im=True,
            )

            for label, months in months_dict.items():
                ds[vn].x.annualize(months=months).mean('time').x.plot(
                    ax=ax[f'{name[0]}_{label}'],
                    cmap='PiYG',
                    levels=np.linspace(-40, 0, 21),
                    add_colorbar=add_colorbar,
                    cbar_kwargs={'ticks': np.linspace(-40, 0, 11)},
                    title=f'{name}: {label}',
                )

        cbar = fig.colorbar(im, ax=list(ax.values()), orientation='horizontal', ticks=np.linspace(-40, 0, 11), aspect=15, pad=0.02, shrink=0.5)
        cbar.set_label(r'$\delta^{18}$O$_p$ [‰]')
        return fig, ax


    def valid_metric(self, vn, metric='R2', **plot_kws):
        try:
            import x4c
        except ImportError:
            raise ImportError('x4c is required for this method. Please install x4c via: pip install x4c-exp.')

        metric_dict = {
            'R2': r2_score,
            'MAE': mean_squared_error,
            'MSE': mean_squared_error,
            'RMSE': mean_squared_error,
            'MAE': mean_absolute_error,
            'MAPE': mean_absolute_percentage_error,
        }

        x4c.set_style('journal', font_scale=1.0)
        valid_map = xr.apply_ufunc(
            metric_dict[metric],
            self.ds_truth[vn],
            self.ds_pred[vn],
            input_core_dims=[['time'], ['time']],  # Apply along the 'time' dimension
            vectorize=True,
        )
        if metric == 'RMSE': valid_map = np.sqrt(valid_map)

        _plot_kws = {
            'R2': dict(
                cmap='RdBu_r',
                levels=np.linspace(0, 1, 21),
                cbar_kwargs={'ticks': np.linspace(0, 1, 6), 'label': '$R^2$'},
                title='$R^2$(Prediction, Truth)',
                extend='min',
            ),
            'MSE': dict(
                cmap='RdBu_r',
                levels=np.linspace(0, 1, 21),
                cbar_kwargs={'ticks': np.linspace(0, 1, 6), 'label': 'MSE'},
                title='MSE(Prediction, Truth)',
                extend='both',
            ),
            'RMSE': dict(
                cmap='RdBu_r',
                levels=np.linspace(0, 1, 21),
                cbar_kwargs={'ticks': np.linspace(0, 1, 6), 'label': 'RMSE'},
                title='RMSE(Prediction, Truth)',
                extend='both',
            ),
            'MAE': dict(
                cmap='RdBu_r',
                levels=np.linspace(0, 1, 21),
                cbar_kwargs={'ticks': np.linspace(0, 1, 6), 'label': 'MAE'},
                title='MAE(Prediction, Truth)',
                extend='both',
            ),
            'MAPE': dict(
                cmap='RdBu_r',
                levels=np.linspace(0, 1, 21),
                cbar_kwargs={'ticks': np.linspace(0, 1, 6), 'label': 'MAPE'},
                title='MAPE(Prediction, Truth)',
                extend='both',
            ),
        }
        _plot_kws[metric].update(plot_kws)
        fig, ax = valid_map.x.plot(
            **_plot_kws[metric],
        )

        return fig, ax