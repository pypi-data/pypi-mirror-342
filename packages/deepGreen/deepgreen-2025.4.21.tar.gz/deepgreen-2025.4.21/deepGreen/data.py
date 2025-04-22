import torch
import lightning as L

class Dataset(L.LightningDataModule):
    def __init__(self, ds, input_vns, output_vns, train_frac=0.7, val_frac=0.1, test_frac=0.2,
                 batch_size=12, num_workers=4):
        super().__init__()
        self.ds = ds
        self.input_vns = input_vns
        self.output_vns = output_vns
        assert batch_size % 12 == 0, 'Batch size must be divisible by 12.'
        self.batch_size = batch_size
        self.num_workers = num_workers

        assert abs(train_frac + val_frac + test_frac - 1.0) < 1e-6, 'Train, val, and test fractions must sum to 1.'
        self.train_frac = train_frac
        self.val_frac = val_frac
        self.test_frac = test_frac

    def setup(self, stage=None):
        self.x = torch.stack([torch.from_numpy(self.ds[vn].values) for vn in self.input_vns], dim=1)
        self.y = torch.stack([torch.from_numpy(self.ds[vn].values) for vn in self.output_vns], dim=1)

        if 'year' in self.ds.dims:
            self.x = self.x.view(-1, 12, self.x.shape[1])  # shape: (N, 12, C_in)

        dataset = torch.utils.data.TensorDataset(self.x, self.y)

        # Compute dataset indices
        ds_idx = list(range(len(dataset)))
        test_size = int(len(dataset) * self.test_frac)
        train_valid_size = len(dataset) - test_size
        
        # Split train+val and test sets
        self.train_valid_idx = ds_idx[:train_valid_size]
        self.test_idx = ds_idx[train_valid_size:]
        
        train_valid_set = torch.utils.data.Subset(dataset, self.train_valid_idx)
        self.test_set = torch.utils.data.Subset(dataset, self.test_idx)
        
        # Further split into train and validation sets
        train_size = int(self.train_frac / (self.train_frac + self.val_frac) * train_valid_size)
        val_size = train_valid_size - train_size
        self.train_set, self.valid_set = torch.utils.data.random_split(train_valid_set, [train_size, val_size])

    def train_dataloader(self):
        return torch.utils.data.DataLoader(self.train_set, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=True)

    def val_dataloader(self):
        return torch.utils.data.DataLoader(self.valid_set, batch_size=self.batch_size, num_workers=self.num_workers)

    def test_dataloader(self):
        return torch.utils.data.DataLoader(self.test_set, batch_size=self.batch_size, num_workers=self.num_workers)
