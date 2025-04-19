#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import logging

import numpy as np
import pandas as pd
from scipy import sparse

from random import sample
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Normal
from torch.utils.data import DataLoader, TensorDataset, Subset

from tqdm import tqdm

log = logging.getLogger(__file__)

def logsumexp(inputs, dim=None, keepdim=False):
    """PyTorch version of tf.math.reduce_logsumexp"""
    if dim is None:
        inputs = inputs.view(-1)
        dim = 0
    s, _ = torch.max(inputs, dim=dim, keepdim=True)
    outputs = s + (inputs - s).exp().sum(dim=dim, keepdim=True).log()
    if not keepdim:
        outputs = outputs.squeeze(dim)
    return outputs

def total_correlation(marginal_entropies, joint_entropy):
    """Calculate total correlation from marginal and joint entropies"""
    return torch.sum(marginal_entropies) - joint_entropy

class VAE(nn.Module):
    """
    General VAE (beta = 0) and beta-TCVAE class 
    """
    def __init__(self, num_cells_train, x_dimension, z_dimension=10, **kwargs):
        super().__init__()
        self.num_cells_train = num_cells_train
        self.x_dim = x_dimension
        self.z_dim = z_dimension
        self.learning_rate = kwargs.get("learning_rate", 1e-3)
        self.dropout_rate = kwargs.get("dropout_rate", 0.2)
        self.beta = kwargs.get("beta", 0.0)
        self.alpha = kwargs.get("alpha", 1.0)
        self.inflate_to_size1 = kwargs.get("inflate_size_1", 256)
        self.inflate_to_size2 = kwargs.get("inflate_size_2", 512)
        self.disc_internal_size2 = kwargs.get("disc_size_2", 512)
        self.disc_internal_size3 = kwargs.get("disc_size_3", 256)
        self.if_BNTrainingMode = kwargs.get("BNTrainingMode", True)
        
        self.device = kwargs.get("device", 'cuda' if torch.cuda.is_available() else 'cpu')
        
        # Build encoder network
        self.encoder_layers = nn.ModuleList([
            nn.Linear(self.x_dim, self.inflate_to_size2),
            nn.BatchNorm1d(self.inflate_to_size2),
            nn.LeakyReLU(),
            nn.Dropout(self.dropout_rate),
            nn.Linear(self.inflate_to_size2, self.inflate_to_size1),
            nn.BatchNorm1d(self.inflate_to_size1),
            nn.ReLU(),
            nn.Dropout(self.dropout_rate)
        ])
        
        self.mu_encoder = nn.Linear(self.inflate_to_size1, self.z_dim)
        self.logvar_encoder = nn.Linear(self.inflate_to_size1, self.z_dim)
        
        # Build decoder network
        self.decoder_layers = nn.ModuleList([
            nn.Linear(self.z_dim, self.inflate_to_size1),
            nn.BatchNorm1d(self.inflate_to_size1),
            nn.LeakyReLU(),
            nn.Dropout(self.dropout_rate),
            nn.Linear(self.inflate_to_size1, self.inflate_to_size2),
            nn.BatchNorm1d(self.inflate_to_size2),
            nn.LeakyReLU(),
            nn.Dropout(self.dropout_rate)
        ])
        
        self.mu_decoder = nn.Linear(self.inflate_to_size2, self.x_dim)
        
        self.to(self.device)
        
        self.optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        
        self.train_loss = []
        self.valid_loss = []
        self.training_time = 0.0
        
    def encoder(self, x):
        """Encoder of VAE"""
        h = x
        for layer in self.encoder_layers:
            h = layer(h)
        
        mu = self.mu_encoder(h)
        logvar = F.softplus(self.logvar_encoder(h))
        
        return mu, logvar
    
    def decoder(self, z):
        """Decoder of VAE"""
        h = z
        for layer in self.decoder_layers:
            h = layer(h)
        
        mu_x = self.mu_decoder(h)
        std_x = torch.ones_like(mu_x)
        
        return mu_x, std_x
    
    def reparameterize(self, mu, logvar):
        """Sample from the posterior using the reparameterization trick"""
        std = torch.sqrt(logvar)
        eps = torch.randn_like(std)
        return mu + eps * std
    
    def sample_z(self, batch_size):
        """Sample from the standard normal prior"""
        return torch.randn(batch_size, self.z_dim, device=self.device)
    
    def log_prob_z_prior(self, z):
        """Log probabilities of z under the prior"""
        return Normal(0, 1).log_prob(z).sum(dim=1)
    
    def log_prob_z_posterior(self, z, mu, logvar):
        """Log probabilities of z under the posterior"""
        return Normal(mu, torch.sqrt(logvar)).log_prob(z).sum(dim=1)
    
    def log_prob_x(self, x, mu_x, std_x):
        """Log probabilities of x under the reconstruction"""
        return Normal(mu_x, std_x).log_prob(x).sum(dim=1)
    
    def compute_qz_entropies(self, z_samples, mu, logvar, is_mss=False):
        """
        Compute entropies for q(z) and q(z_j)
        If is_mss is True, use Minibatch Stratified Sampling
        """
        batch_size = z_samples.size(0)
    
        if is_mss:
            # MSS implementation
            dataset_size = torch.tensor(self.num_cells_train, dtype=torch.float, device=self.device)
        
            # Computing the weights
            output = torch.zeros((batch_size - 1, 1), device=self.device)
            output = torch.cat([torch.ones((1, 1), device=self.device), output], dim=0)
            outpart_1 = torch.zeros((batch_size, 1), device=self.device)
            outpart_3 = torch.zeros((batch_size, batch_size - 2), device=self.device)
            output = torch.cat([outpart_1, output], dim=1)
            part_4 = -torch.cat([output, outpart_3], dim=1) / dataset_size
        
            part_1 = torch.ones((batch_size, batch_size), device=self.device) / (batch_size - 1)
            part_2 = torch.ones((batch_size, batch_size), device=self.device)
            part_2 = -torch.tril(part_2, diagonal=1) / dataset_size
        
            part_3 = torch.eye(batch_size, device=self.device) * (2 / dataset_size - 1 / (batch_size - 1))
        
            weights = torch.log(part_1 + part_2 + part_3 + part_4 + 1e-8)  # Add small epsilon for numerical stability
        else:
            # Regular entropy estimation
            weights = -torch.log(torch.tensor(batch_size, dtype=torch.float, device=self.device))
            weights = weights.expand(batch_size)  # Make it a vector of size batch_size
    
        # Compute log probabilities for each dimension separately
        std = torch.sqrt(logvar)
    
        # Create matrices for broadcasting
        z_expand = z_samples.unsqueeze(1)  # [batch_size, 1, z_dim]
        mu_expand = mu.unsqueeze(0)        # [1, batch_size, z_dim]
        std_expand = std.unsqueeze(0)      # [1, batch_size, z_dim]
    
        # Calculate log probability matrices
        log_p_z = -0.5 * (
        (z_expand - mu_expand)**2 / std_expand**2 + 
        torch.log(2 * torch.tensor(np.pi, device=self.device) * std_expand**2)
            )  # [batch_size, batch_size, z_dim]
    
        # Sum over z dimensions for joint distribution
        log_q_z_joint = log_p_z.sum(dim=2)  # [batch_size, batch_size]
    
        if not is_mss:
            # For standard entropy estimation, weights should be reshaped correctly
            # to broadcast with log_q_z_joint and log_p_z
            joint_logqz = logsumexp(log_q_z_joint + weights.view(-1, 1), dim=1)
            marginal_logqz = logsumexp(log_p_z + weights.view(-1, 1, 1), dim=1)
        else:
            # For MSS, weights is a matrix
            joint_logqz = logsumexp(log_q_z_joint + weights, dim=1)
            # Reshape weights to broadcast correctly with log_p_z
            weights_expand = weights.unsqueeze(2)  # [batch_size, batch_size, 1]
            marginal_logqz = logsumexp(log_p_z + weights_expand, dim=1)
    
        # Calculate entropies
        joint_entropy = -torch.mean(joint_logqz)
        marginal_entropies = -torch.mean(marginal_logqz, dim=0)
    
        return marginal_entropies, joint_entropy
    
    def forward(self, x):
        """Forward pass through the VAE"""
        mu, logvar = self.encoder(x)
        z = self.reparameterize(mu, logvar)
        mu_x, std_x = self.decoder(z)
        
        # Calculate entropies for total correlation
        z_mss_marginal_entropy, z_mss_joint_entropy = self.compute_qz_entropies(z, mu, logvar, is_mss=True)
        z_marginal_entropy, z_joint_entropy = self.compute_qz_entropies(z, mu, logvar, is_mss=False)
        
        z_tc = total_correlation(z_marginal_entropy, z_joint_entropy)
        z_mss_tc = total_correlation(z_mss_marginal_entropy, z_mss_joint_entropy)
        
        # Calculate loss components
        kl_loss = -torch.mean(self.log_prob_z_prior(z)) + torch.mean(self.log_prob_z_posterior(z, mu, logvar))
        rec_loss = -torch.mean(self.log_prob_x(x, mu_x, std_x))
        
        # Total loss
        loss = self.alpha * kl_loss + rec_loss + self.beta * z_mss_tc
        
        return {
            'loss': loss,
            'kl_loss': kl_loss,
            'rec_loss': rec_loss,
            'tc_loss': z_mss_tc,
            'z': z,
            'mu': mu,
            'logvar': logvar,
            'mu_x': mu_x,
            'std_x': std_x
        }
    
    def encode(self, x_data):
        """Encode data to latent samples"""
        self.eval()
        with torch.no_grad():
            x_tensor = torch.tensor(x_data, dtype=torch.float32, device=self.device)
            mu, logvar = self.encoder(x_tensor)
            z = self.reparameterize(mu, logvar)
        return z.cpu().numpy()
    
    def encode_mean(self, x_data):
        """Encode data to latent means"""
        self.eval()
        with torch.no_grad():
            x_tensor = torch.tensor(x_data, dtype=torch.float32, device=self.device)
            mu, _ = self.encoder(x_tensor)
        return mu.cpu().numpy()
    
    def decode(self, z_data):
        """Decode from latent values to data"""
        self.eval()
        with torch.no_grad():
            z_tensor = torch.tensor(z_data, dtype=torch.float32, device=self.device)
            mu_x, _ = self.decoder(z_tensor)
        return mu_x.cpu().numpy()
    
    def reconstruct(self, data, if_latent=False):
        """Reconstruct data from original data or latent samples"""
        self.eval()
        with torch.no_grad():
            if if_latent:
                z = torch.tensor(data, dtype=torch.float32, device=self.device)
            else:
                z = torch.tensor(self.encode(data), dtype=torch.float32, device=self.device)
            
            mu_x, _ = self.decoder(z)
        return mu_x.cpu().numpy()
    
    def avg_vector(self, data):
        """Encode data to the latent sample means"""
        latent = self.encode(data)
        latent_avg = np.average(latent, axis=0)
        return latent_avg
    
    @property
    def model_parameter(self):
        """Report the number of training parameters"""
        total_param = sum(p.numel() for p in self.parameters() if p.requires_grad)
        return f"There are {total_param} parameters in VAE."
    
    def save_model(self, model_save_path, epoch):
        """Save the trained model to the model_save_path"""
        os.makedirs(model_save_path, exist_ok=True)
        model_save_name = os.path.join(model_save_path, f"model_epoch_{epoch}.pt")
        
        torch.save({
            'epoch': epoch,
            'model_state_dict': self.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'training_time': self.training_time,
            'train_loss': self.train_loss,
            'valid_loss': self.valid_loss
        }, model_save_name)
        
        np.save(os.path.join(model_save_path, "training_time.npy"), self.training_time)
        np.save(os.path.join(model_save_path, "train_loss.npy"), self.train_loss)
        np.save(os.path.join(model_save_path, "valid_loss.npy"), self.valid_loss)
    
    def restore_model(self, model_path):
        """Restore model from model_path"""
        checkpoint = torch.load(model_path)
        self.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.training_time = checkpoint.get('training_time', 0.0)
        self.train_loss = checkpoint.get('train_loss', [])
        self.valid_loss = checkpoint.get('valid_loss', [])
    
    def train_np(self, train_data, use_validation=False, valid_data=None, 
                 use_test_during_train=False, test_data=None,
                 test_every_n_epochs=100, test_size=3000, 
                 inception_score_data=None, n_epochs=25, batch_size=128, 
                 early_stop_limit=20, threshold=0.0025, shuffle=True, 
                 save=False, model_save_path=None, output_save_path=None, verbose=False):
        """Train VAE with train_data (numpy array) and optional valid_data (numpy array) for n_epochs."""
        log.info("--- Training ---")
        if use_validation and valid_data is None:
            raise Exception("valid_data is None but use_validation is True.")

        patience = early_stop_limit
        min_delta = threshold
        patience_cnt = 0

        # Convert data to PyTorch datasets and dataloaders
        train_tensor = torch.tensor(train_data, dtype=torch.float32)
        train_dataset = TensorDataset(train_tensor)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle)
        
        if use_validation:
            valid_tensor = torch.tensor(valid_data, dtype=torch.float32)
            valid_dataset = TensorDataset(valid_tensor)
            valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False)
        
        # Setup for test during training if requested
        if use_test_during_train:
            from sklearn.decomposition import PCA
            # Assuming these classes are defined elsewhere in your code
            # You might need to implement or adapt these classes
            # genmetric = MetricVisualize()
            # RFE = RandomForestError()
            
            pca_data_50 = PCA(n_components=50, random_state=42)
            genmetrics_pd = pd.DataFrame({'epoch': [], 'is_real_mu': [], 'is_real_std': [], 
                                          'is_fake_mu': [], 'is_fake_std': [], 'rf_error': []})
            pca_data_fit = pca_data_50.fit(train_data)
        
        for epoch in tqdm(range(1, n_epochs + 1)):
            begin = time.time()
            
            # Training phase
            self.train()
            train_loss = 0.0
            
            for x_batch, in train_loader:
                x_batch = x_batch.to(self.device)
                
                self.optimizer.zero_grad()
                result = self(x_batch)
                loss = result['loss']
                loss.backward()
                self.optimizer.step()
                
                train_loss += loss.item() * x_batch.size(0)
            
            train_loss /= len(train_tensor)
            
            # Validation phase if needed
            valid_loss = 0.0
            if use_validation:
                self.eval()
                with torch.no_grad():
                    for x_batch, in valid_loader:
                        x_batch = x_batch.to(self.device)
                        result = self(x_batch)
                        loss = result['loss']
                        valid_loss += loss.item() * x_batch.size(0)
                
                valid_loss /= len(valid_tensor)
            
            self.train_loss.append(train_loss)
            self.valid_loss.append(valid_loss)
            self.training_time += (time.time() - begin)
            
            # Testing for generation metrics
            if (epoch - 1) % test_every_n_epochs == 0 and use_test_during_train:
                # This part would need to be adapted based on your custom metrics classes
                if test_data is None:
                    reset_test_data = True
                    sampled_indices = sample(range(len(train_tensor)), test_size)
                    test_data_subset = train_data[sampled_indices, :]
                    gen_data = self.reconstruct(test_data_subset)
                    
                    if inception_score_data is not None:
                        inception_score_subdata = inception_score_data[sampled_indices]
                        # You would need to adapt your metrics calculation here
                        # mean_is_real, std_is_real = genmetric.InceptionScore(...)
                        # mean_is_fake, std_is_fake = genmetric.InceptionScore(...)
                        mean_is_real = std_is_real = mean_is_fake = std_is_fake = 0.0
                    else:
                        mean_is_real = std_is_real = mean_is_fake = std_is_fake = 0.0
                else:
                    assert test_data.shape[0] == test_size
                    reset_test_data = False
                    gen_data = self.reconstruct(test_data)
                    
                    if inception_score_data is not None:
                        inception_score_subdata = inception_score_data
                        # mean_is_real, std_is_real = genmetric.InceptionScore(...)
                        # mean_is_fake, std_is_fake = genmetric.InceptionScore(...)
                        mean_is_real = std_is_real = mean_is_fake = std_is_fake = 0.0
                    else:
                        mean_is_real = std_is_real = mean_is_fake = std_is_fake = 0.0
                
                # errors_d = list(RFE.fit(test_data, gen_data, pca_data_fit, if_dataPC=True, output_AUC=False)['avg'])[0]
                errors_d = 0.0  # Placeholder, replace with actual metric
                
                genmetrics_pd = pd.concat([genmetrics_pd, pd.DataFrame(
                    [[epoch, mean_is_real, std_is_real, mean_is_fake, std_is_fake, errors_d]], 
                    columns=['epoch', 'is_real_mu', 'is_real_std', 'is_fake_mu', 'is_fake_std', 'rf_error'])])
                
                if save:
                    genmetrics_pd.to_csv(os.path.join(output_save_path, "GenerationMetrics.csv"))
                
                if reset_test_data:
                    test_data = None
            
            if verbose:
                print(f"Epoch {epoch}: Train Loss: {train_loss} Valid Loss: {valid_loss}")
            
            # Early stopping
            if use_validation and epoch > 1:
                if self.valid_loss[epoch - 2] - self.valid_loss[epoch - 1] > min_delta:
                    patience_cnt = 0
                else:
                    patience_cnt += 1
                
                if patience_cnt > patience:
                    if save:
                        self.save_model(model_save_path, epoch)
                        log.info(f"Model saved in file: {model_save_path}. Training stopped earlier at epoch: {epoch}.")
                        if verbose:
                            print(f"Model saved in file: {model_save_path}. Training stopped earlier at epoch: {epoch}.")
                        if use_test_during_train:
                            genmetrics_pd.to_csv(os.path.join(model_save_path, "GenerationMetrics.csv"))
                    break
        
        if save:
            self.save_model(model_save_path, epoch)
            log.info(f"Model saved in file: {model_save_path}. Training finished.")
            if verbose:
                print(f"Model saved in file: {model_save_path}. Training finished.")
            if use_test_during_train:
                genmetrics_pd.to_csv(os.path.join(model_save_path, "GenerationMetrics.csv"))
    
    def train_np_crossValidate(self, train_data, seed=123, use_test_during_train=False,
                              test_every_n_epochs=100, test_size=3000, n_epochs=25, 
                              batch_size=128, early_stop_limit=20, threshold=0.0025, 
                              shuffle=True, save=False, model_save_path=None,
                              output_save_path=None, verbose=False, cv_prop=0.8):
        """
        Train VAE with train_data (numpy array) using cross-validation for n_epochs.
        Force to use validation.
        """
        log.info("--- Training with Cross-Validation ---")
        
        patience = early_stop_limit
        min_delta = threshold
        patience_cnt = 0
        
        n_data = train_data.shape[0]
        n_train = int(n_data * cv_prop)
        n_test = n_data - n_train
        
        # Random split of train and validation datasets
        np.random.seed(seed)
        permutation = np.random.permutation(n_data)
        indices_test, indices_train = permutation[:n_test], permutation[n_test:]
        
        train_data_train = train_data[indices_train]
        train_data_test = train_data[indices_test]
        
        # Convert to PyTorch datasets and dataloaders
        train_tensor = torch.tensor(train_data_train, dtype=torch.float32)
        train_dataset = TensorDataset(train_tensor)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle)
        
        test_tensor = torch.tensor(train_data_test, dtype=torch.float32)
        test_dataset = TensorDataset(test_tensor)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=shuffle)
        
        # Setup for metrics tracking
        if use_test_during_train:
            from sklearn.decomposition import PCA
            # RFE = RandomForestError()
            
            pca_data_50 = PCA(n_components=50, random_state=42)
            genmetrics_pd = pd.DataFrame({'epoch': [], 'rf_train': [], 'rf_test': []})
            pca_data_fit = pca_data_50.fit(train_data)
        
        for epoch in tqdm(range(1, n_epochs + 1)):
            begin = time.time()
            
            # Training phase
            self.train()
            train_loss = 0.0
            
            for x_batch, in train_loader:
                x_batch = x_batch.to(self.device)
                
                self.optimizer.zero_grad()
                result = self(x_batch)
                loss = result['loss']
                loss.backward()
                self.optimizer.step()
                
                train_loss += loss.item() * x_batch.size(0)
            
            train_loss /= len(train_tensor)
            
            # Validation phase
            valid_loss = 0.0
            self.eval()
            with torch.no_grad():
                for x_batch, in test_loader:
                    x_batch = x_batch.to(self.device)
                    result = self(x_batch)
                    loss = result['loss']
                    valid_loss += loss.item() * x_batch.size(0)
            
            valid_loss /= len(test_tensor)
            
            self.train_loss.append(train_loss)
            self.valid_loss.append(valid_loss)
            self.training_time += (time.time() - begin)
            
            # Testing for generation metrics
            if (epoch - 1) % test_every_n_epochs == 0 and use_test_during_train:
                # Sample data for metrics
                sampled_indices_train = sample(range(len(train_tensor)), test_size)
                test_data_train = train_data_train[sampled_indices_train]
                gen_data_train = self.reconstruct(test_data_train)
                
                sampled_indices_test = sample(range(len(test_tensor)), test_size)
                test_data_test = train_data_test[sampled_indices_test]
                gen_data_test = self.reconstruct(test_data_test)
                
                # Calculate metrics (placeholders - implement your specific metrics)
                # errors_train = list(RFE.fit(test_data_train, gen_data_train, pca_data_fit, if_dataPC=True, output_AUC=False)['avg'])[0]
                # errors_test = list(RFE.fit(test_data_test, gen_data_test, pca_data_fit, if_dataPC=True, output_AUC=False)['avg'])[0]
                errors_train = errors_test = 0.0  # Replace with actual metrics
                
                genmetrics_pd = pd.concat([genmetrics_pd, pd.DataFrame(
                    [[epoch, errors_train, errors_test]], columns=['epoch', 'rf_train', 'rf_test'])])
                
                if save:
                    genmetrics_pd.to_csv(os.path.join(output_save_path, "GenerationMetrics.csv"))
            
            if verbose:
                print(f"Epoch {epoch}: Train Loss: {train_loss} Valid Loss: {valid_loss}")
            
            # Early stopping
            if epoch > 1:
                if self.valid_loss[epoch - 2] - self.valid_loss[epoch - 1] > min_delta:
                    patience_cnt = 0
                else:
                    patience_cnt += 1
                
                if patience_cnt > patience:
                    if save:
                        self.save_model(model_save_path, epoch)
                        log.info(f"Model saved in file: {model_save_path}. Training stopped earlier at epoch: {epoch}.")
                        if verbose:
                            print(f"Model saved in file: {model_save_path}. Training stopped earlier at epoch: {epoch}.")
                        if use_test_during_train:
                            genmetrics_pd.to_csv(os.path.join(model_save_path, "GenerationMetrics.csv"))
                    break
        
        if save:
            self.save_model(model_save_path, epoch)
            log.info(f"Model saved in file: {model_save_path}. Training finished.")
            if verbose:
                print(f"Model saved in file: {model_save_path}. Training finished.")
            if use_test_during_train:
                genmetrics_pd.to_csv(os.path.join(model_save_path, "GenerationMetrics.csv"))