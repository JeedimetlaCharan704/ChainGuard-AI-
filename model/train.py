"""
ChainGuard AI - Model Training Script
Trains the Deep Neural Network (ChainGuardNet) on Ethereum Fraud data,
evaluates metrics (Accuracy, Precision, Recall, F1, ROC-AUC),
and saves the trained model and scaler.
"""

import os
import pickle
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

from model import ChainGuardNet

def train_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(base_dir)
    dataset_path = os.path.join(project_dir, 'dataset', 'ethereum_fraud_dataset.csv')
    
    print("=" * 60)
    print("        CHAINGUARD AI - DEEP LEARNING MODEL TRAINING")
    print("=" * 60)
    print(f"Loading dataset from: {dataset_path}")
    
    df = pd.read_csv(dataset_path)
    feature_cols = [c for c in df.columns if c != 'is_fraud']
    X = df[feature_cols].values
    y = df['is_fraud'].values
    
    print(f"Total Samples: {len(X)} | Features count: {len(feature_cols)}")
    print(f"Target distribution -> Safe: {np.sum(y == 0)}, Fraud: {np.sum(y == 1)}")
    
    # Train / Test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    # Feature Scaling (Standardization: mean=0, std=1)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler
    scaler_path = os.path.join(base_dir, 'scaler.pkl')
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Feature scaler saved to: {scaler_path}")
    
    # Convert to PyTorch Tensors
    train_dataset = TensorDataset(
        torch.tensor(X_train_scaled, dtype=torch.float32),
        torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    )
    test_dataset = TensorDataset(
        torch.tensor(X_test_scaled, dtype=torch.float32),
        torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)
    )
    
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    
    # Initialize Model, Loss Function, Optimizer
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Training using device: {device}")
    
    model = ChainGuardNet(input_dim=len(feature_cols)).to(device)
    criterion = nn.BCELoss() # Binary Cross-Entropy
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
    
    # Training Loop
    epochs = 25
    print("\nStarting Deep Learning Training (25 Epochs)...")
    print("-" * 60)
    
    history = {'epoch': [], 'loss': [], 'val_accuracy': []}
    
    for epoch in range(1, epochs + 1):
        model.train()
        epoch_loss = 0.0
        
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            
            optimizer.zero_grad()
            probs, _ = model(batch_X)
            loss = criterion(probs, batch_y)
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item() * len(batch_X)
            
        epoch_loss = epoch_loss / len(train_dataset)
        
        # Validation accuracy check
        model.eval()
        with torch.no_grad():
            X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32).to(device)
            val_probs, _ = model(X_test_tensor)
            val_preds = (val_probs.cpu().numpy() >= 0.5).astype(int)
            val_acc = accuracy_score(y_test, val_preds)
            
        history['epoch'].append(epoch)
        history['loss'].append(round(epoch_loss, 4))
        history['val_accuracy'].append(round(val_acc * 100, 2))
        
        if epoch % 5 == 0 or epoch == 1:
            print(f"Epoch [{epoch:02d}/{epochs}] -> Loss: {epoch_loss:.4f} | Validation Accuracy: {val_acc*100:.2f}%")
            
    print("-" * 60)
    print("Deep Learning Training Completed!")
    
    # Final Evaluation on Test Set
    model.eval()
    with torch.no_grad():
        test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32).to(device)
        test_probs, _ = model(test_tensor)
        dl_probs = test_probs.cpu().numpy().flatten()
        dl_preds = (dl_probs >= 0.5).astype(int)
        
    dl_acc = accuracy_score(y_test, dl_preds)
    dl_prec = precision_score(y_test, dl_preds)
    dl_rec = recall_score(y_test, dl_preds)
    dl_f1 = f1_score(y_test, dl_preds)
    dl_auc = roc_auc_score(y_test, dl_probs)
    dl_cm = confusion_matrix(y_test, dl_preds).tolist()
    
    # Baseline comparison (Random Forest) for academic benchmarking
    print("\nTraining Baseline Machine Learning Model (Random Forest) for comparison...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train_scaled, y_train)
    rf_preds = rf.predict(X_test_scaled)
    rf_probs = rf.predict_proba(X_test_scaled)[:, 1]
    
    rf_acc = accuracy_score(y_test, rf_preds)
    rf_f1 = f1_score(y_test, rf_preds)
    
    print("\n" + "=" * 60)
    print("                    EVALUATION RESULTS")
    print("=" * 60)
    print(f"Deep Learning (ChainGuardNet) Accuracy : {dl_acc * 100:.2f}%")
    print(f"Deep Learning Precision                : {dl_prec * 100:.2f}%")
    print(f"Deep Learning Recall                   : {dl_rec * 100:.2f}%")
    print(f"Deep Learning F1-Score                 : {dl_f1 * 100:.2f}%")
    print(f"Deep Learning ROC-AUC Score            : {dl_auc:.4f}")
    print(f"Baseline (Random Forest) Accuracy      : {rf_acc * 100:.2f}%")
    print("=" * 60)
    
    # Save Model Weights
    model_save_path = os.path.join(base_dir, 'chainguard_model.pth')
    torch.save(model.state_dict(), model_save_path)
    print(f"Trained Deep Learning model saved to: {model_save_path}")
    
    # Save Metrics & Feature Columns to JSON
    metrics = {
        'model_name': 'ChainGuardNet (Deep Neural Network)',
        'accuracy': round(dl_acc * 100, 2),
        'precision': round(dl_prec * 100, 2),
        'recall': round(dl_rec * 100, 2),
        'f1_score': round(dl_f1 * 100, 2),
        'roc_auc': round(dl_auc, 4),
        'confusion_matrix': dl_cm,
        'baseline_rf_accuracy': round(rf_acc * 100, 2),
        'feature_columns': feature_cols,
        'training_history': history
    }
    
    metrics_path = os.path.join(base_dir, 'training_metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"Evaluation report and metrics saved to: {metrics_path}")
    print("=" * 60)

if __name__ == '__main__':
    train_model()
