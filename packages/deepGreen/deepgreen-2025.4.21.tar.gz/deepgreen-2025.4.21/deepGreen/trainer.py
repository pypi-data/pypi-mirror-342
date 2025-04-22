import os
import lightning as L
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

from . import utils

class ParameterHistoryCallback(L.Callback):
    def __init__(self, params=['T1', 'T2', 'M1', 'M2']):
        super().__init__()
        self.params = params

    def on_train_start(self, trainer, pl_module):
        """Initialize parameter history dictionary when training starts."""
        trainer.mode = getattr(pl_module, 'mode', None)
        trainer.optimizer = getattr(pl_module, 'optimizer', None)
        trainer.lr = getattr(pl_module, 'lr', None)
        trainer.param_history = {}
        for param in self.params:
            param_value = getattr(pl_module, param, None)
            if param_value is not None:
                trainer.param_history[param] = [param_value.item()]

    def on_train_epoch_end(self, trainer, pl_module):
        """Record parameter values at the end of each training epoch."""
        for param in self.params:
            param_value = getattr(pl_module, param, None)
            if param_value is not None:
                trainer.param_history[param].append(param_value.item())

class Trainer(L.Trainer):
    def __init__(self, log_dirpath='./logs', name='IsoGen', min_epochs=1, max_epochs=1000):
        utils.p_header(f'Name: {name}')

        early_stop = L.pytorch.callbacks.early_stopping.EarlyStopping(
            monitor='valid_loss',  # Metric to monitor
            patience=10,          # Wait 3 epochs without improvement
            mode='min',          # Minimize the monitored metric (e.g., loss)
            verbose=True,        # Log when training stops
            min_delta=0.001      # Optional: Minimum change to qualify as improvement
        )

        ckpt_callback = L.pytorch.callbacks.ModelCheckpoint(
            dirpath=log_dirpath, filename=name,
        )

        # Remove the checkpoint file if it exists
        self.ckpt_fpath = os.path.join(log_dirpath, f'{name}.ckpt')
        utils.p_header(f'Checkpoint path: {os.path.abspath(self.ckpt_fpath)}')

        if os.path.exists(self.ckpt_fpath):
            os.remove(self.ckpt_fpath)
        else:
            pass

        super().__init__(
            accelerator='gpu', devices=1, strategy='auto',
            min_epochs=min_epochs, max_epochs=max_epochs,
            default_root_dir=log_dirpath, callbacks=[early_stop, ckpt_callback, ParameterHistoryCallback()]
        )

    def plot(self):
        # Determine number of subplots based on mode
        if self.mode == 'T':
            fig, ax = plt.subplots(figsize=(5, 3))
            axes = [ax]
            param_groups = [('T1', 'T2')]
        elif self.mode == 'M':
            fig, ax = plt.subplots(figsize=(5, 3))
            axes = [ax]
            param_groups = [('M1', 'M2')]
        else:
            fig, axes = plt.subplots(nrows=2, figsize=(5, 6), sharex=True)
            param_groups = [('T1', 'T2'), ('M1', 'M2')]

        for ax, (param1, param2) in zip(axes, param_groups):
            for param in [param1, param2]:
                if param in self.param_history:
                    values = self.param_history[param]
                    (line,) = ax.plot(values, marker='o', label=param)  # Capture line object
                    color = line.get_color()  # Get line color

                    # Annotate initial value
                    ax.text(-0.5, values[0], f'{values[0]:.2f}', ha='right', va='center', fontsize=10, color=color,
                            bbox=dict(facecolor='white', edgecolor=color, boxstyle='round,pad=0.3'))

                    # Annotate final value with slight vertical offset
                    x_final, y_final = len(values) - 1, values[-1]
                    ax.text(x_final*1.05, y_final, f'{param}={y_final:.2f}', ha='left', va='center', fontsize=10, color=color,
                            bbox=dict(facecolor='white', edgecolor=color, boxstyle='round,pad=0.3'))

            ax.set_ylabel('Parameter Value')
            ax.set_title(f'Parameters: {param1}, {param2}; Optimizer: {self.optimizer}, lr={self.lr}')
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # Integer xticks

        axes[-1].set_xlabel('Epoch')  # X-axis label only on last subplot

        return fig, axes