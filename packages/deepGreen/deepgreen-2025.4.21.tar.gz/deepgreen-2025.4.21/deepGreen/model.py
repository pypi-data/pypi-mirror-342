import torch
import lightning as L
from . import utils

class GrowthModel(L.LightningModule):
    def __init__(self, T1=None, T2=None, M1=None, M2=None, mode='TMEint', phi=None, I_0=1, I_f=12,
                 optimizer='AdamW', lr=1e-2):
        super().__init__()
        # Initialize learnable parameters
        self.T1 = torch.nn.Parameter(torch.tensor(T1, requires_grad=True)) if T1 is not None else T1
        self.T2 = torch.nn.Parameter(torch.tensor(T2, requires_grad=True)) if T2 is not None else T2
        self.M1 = torch.nn.Parameter(torch.tensor(M1, requires_grad=True)) if M1 is not None else M1
        self.M2 = torch.nn.Parameter(torch.tensor(M2, requires_grad=True)) if M2 is not None else M2
        self.phi = torch.tensor(phi) if phi is not None else phi
        self.I_0 = I_0
        self.I_f = I_f
        self.criterion = torch.nn.MSELoss()
        self.lr = lr
        self.optimizer = optimizer
        self.mode = mode

    def normalize(self, V, V1, V2):
        gT = (V - V1) / (V2 - V1)
        return torch.clamp(gT, 0, 1)

    def forward(self, x):
        if self.mode == 'T':
            T = x[:, 0]
            return self.normalize(T, self.T1, self.T2)
        elif self.mode == 'M':
            M = x[:, 0]
            return self.normalize(M, self.M1, self.M2)
        elif self.mode == 'TM':
            T, M = x[:, 0], x[:, 1]
            gT = self.normalize(T, self.T1, self.T2)
            gM = self.normalize(M, self.M1, self.M2)
            return torch.min(gT, gM)
        elif self.mode == 'TME':
            T, M, gE = x[:, 0], x[:, 1], x[:, 2]
            gT = self.normalize(T, self.T1, self.T2)
            gM = self.normalize(M, self.M1, self.M2)
            res = torch.min(gT, gM) * gE
            return res
        elif self.mode == 'TMEint':
            if x.dim() == 3:
                T, M, gE = x[:, :, 0].flatten(), x[:, :, 1].flatten(), x[:, :, 2].flatten()
            elif x.dim() == 2:
                T, M, gE = x[:, 0], x[:, 1], x[:, 2]
            else:
                raise ValueError("Input tensor must be 2D or 3D.")

            gT = self.normalize(T, self.T1, self.T2)
            gM = self.normalize(M, self.M1, self.M2)
            Gr = torch.min(gT, gM) * gE
            nyrs = int(Gr.shape[0] // 12)
            Gr = Gr.view(nyrs, 12).T  # Reshape to (n_months, nyrs)
            width = torch.full((nyrs,), float('nan'))

            if self.phi > 0:  # Northern Hemisphere
                if self.I_0 < 0:
                    startmo = 12 + self.I_0
                    endmo = self.I_f
                    # First year: average previous year contribution
                    width[0] = torch.sum(Gr[0:endmo, 0]) + torch.sum(torch.mean(Gr[startmo-1:12, :], dim=1))
                    past_year = Gr[startmo-1:12, :-1]   # shape: (n_months, nyrs-1)
                    this_year = Gr[0:endmo, 1:]         # shape: (n_months, nyrs-1)
                    width[1:] = torch.sum(past_year, dim=0) + torch.sum(this_year, dim=0)
                else:
                    startmo = self.I_0
                    endmo = self.I_f
                    width = torch.sum(Gr[startmo-1:endmo, :], dim=0)

            elif self.phi < 0:  # Southern Hemisphere
                startmo = 6 + self.I_0
                endmo = self.I_f - 6
                this_year = Gr[startmo-1:12, :-1]   # shape: (n_months, nyrs-1)
                next_year = Gr[0:endmo, 1:]         # shape: (n_months, nyrs-1)
                width[:-1] = torch.sum(this_year, dim=0) + torch.sum(next_year, dim=0)
                width[-1] = torch.sum(Gr[startmo-1:12, -1]) + torch.sum(torch.mean(Gr[0:endmo, :], dim=1))

            # Standardize to get tree-ring proxy series
            res = (width - torch.nanmean(width)) / utils.nanstd(width)
            return res

    def training_step(self, batch, batch_idx):
        x, y = batch
        predictions = self(x)
        loss = self.criterion(predictions, y.flatten())
        self.log('train_loss', loss, on_step=True, on_epoch=True, prog_bar=True, sync_dist=True)

        if 'T' in self.mode:
            self.log('T1', self.T1, on_step=True, on_epoch=True, prog_bar=True, sync_dist=True)
            self.log('T2', self.T2, on_step=True, on_epoch=True, prog_bar=True, sync_dist=True)

        if 'M' in self.mode or 'P' in self.mode:
            self.log('M1', self.M1, on_step=True, on_epoch=True, prog_bar=True, sync_dist=True)
            self.log('M2', self.M2, on_step=True, on_epoch=True, prog_bar=True, sync_dist=True)

        # Log gradients
        for name, param in self.named_parameters():
            if param.grad is not None:
                self.log(f"{name}_grad", param.grad.abs().mean())

        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        predictions = self(x)
        loss = self.criterion(predictions, y.flatten())
        self.log('valid_loss', loss, on_step=True, on_epoch=True, prog_bar=True, sync_dist=True)
        return loss

    def test_step(self, batch, batch_idx):
        x, y = batch
        predictions = self(x)
        loss = self.criterion(predictions, y.flatten())
        self.log('test_loss', loss, sync_dist=True)
        return loss
    
    def configure_optimizers(self):
        return torch.optim.__dict__[self.optimizer](self.parameters(), lr=self.lr)