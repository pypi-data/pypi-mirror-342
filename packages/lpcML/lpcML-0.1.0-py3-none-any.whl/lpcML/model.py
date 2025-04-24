import torch
import torch.nn as nn
from torch.nn import functional as F
from torch.utils.data import Dataset
from torcheval.metrics.functional import r2_score
import pytorch_lightning as pl
import wandb

# Dataset class
class CustomDataset(Dataset):

    def __init__(self, data_in, data_out):
        self.data_in = data_in
        self.data_out = data_out

    def __len__(self):
        return len(self.data_in)

    def __getitem__(self, i):
        if torch.is_tensor(i):
            i = i.tolist()
        return self.data_in[i], self.data_out[i]





class mlp_hLPC(pl.LightningModule):
    '''Class for the multi-layer perceptron applied to predict the Eff of horizontal laser power convereters (hLPC)'''
    def __init__(self, config):
        super().__init__()
        self.layer_1 = config["layer_1"]
        self.layer_2 = config["layer_2"]
        self.lr = config["lr"]
        self.batch_size = config["batch_size"]
        self.momentum = config["momentum"]
        # self.std = config["weight_std"]
        self.encoder = nn.Sequential(
            nn.LazyLinear(self.layer_1),
            nn.Tanh(),
            nn.LazyLinear(self.layer_2),
            nn.Tanh(),
            nn.LazyLinear(1),
        )
        # Save the hyperparameters to use the trained NN
        self.save_hyperparameters()

    # Prediction/inference actions
    def forward(self,x):
        embedding = self.encoder(x)
        return embedding

    # Optimization algorithm
    def configure_optimizers(self):
        optimizer = torch.optim.SGD(self.parameters(), momentum=self.momentum, lr=self.lr,nesterov=False)
        lr_scheduler = {
            'scheduler': torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min',factor=0.1),
            'name': 'learning_rate_scheduler',
            'monitor': 'val/loss'
        }
        return [optimizer], [lr_scheduler]

    # Training loop with MSE as loss function, R2 metric to visualize
    def training_step(self, train_batch, batch_idx):
        x, y = train_batch
        x = x.view(x.size(0),-1)
        y = y.view(y.size(0),-1)
        y_hat = self.encoder(x)
        loss = F.mse_loss(y_hat, y)
        if len(y_hat)>2:
            r2 = r2_score(y_hat, y)
            if wandb.run is not None:
                wandb.log({"r2_train": r2, "loss_train": loss})
            self.log('train/r2', r2, on_step=True, on_epoch=True, logger=True)
        self.log('train/loss', loss, on_step=True, on_epoch=True, prog_bar=True, logger=True) # sending metrics to TensorBoard, add on_epoch=True to calculate epoch-level metrics
        return loss

    # Validation with MSE as loss function, R2 metric to visualize
    def validation_step(self, val_batch, batch_idx):
        x, y = val_batch
        x = x.view(x.size(0),-1)
        y = y.view(y.size(0),-1)
        y_hat = self.encoder(x)
        loss = F.mse_loss(y_hat, y)
        if len(y_hat)>2:
            r2 = r2_score(y_hat, y)
            if wandb.run is not None:
                wandb.log({"r2_val": r2, "loss_val": loss})
            self.log('val/r2', r2, on_step=True, prog_bar=False,on_epoch=True, logger=True)
        self.log('val/loss', loss, on_step=True, prog_bar=False,on_epoch=True, logger=True)

    # Test with MSE as loss function, R2 and RMSE metrics to visualize
    def test_step(self, test_batch, batch_idx):
        x, y = test_batch
        x = x.view(x.size(0),-1)
        y = y.view(y.size(0),-1)
        y_hat = self.encoder(x)
        loss = F.mse_loss(y_hat, y)
        rmse = torch.sqrt(loss)
        if len(y_hat)>2:
            r2 = r2_score(y_hat, y)
            if wandb.run is not None:
                wandb.log({"r2_test": r2, "loss_test": loss})
            self.log('test/r2', r2, on_step=True, on_epoch=True, logger=True)
        self.log('test/loss', loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        self.log('test/rmse', rmse, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        print(f'Iste é o R2 do test: {r2}')