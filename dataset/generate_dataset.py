"""
ChainGuard AI - Dataset Generator
Generates a realistic Ethereum Transaction & Wallet Fraud Dataset based on standard
Kaggle and academic Ethereum fraud detection benchmarks.
"""

import numpy as np
import pandas as pd
import os

def generate_ethereum_dataset(num_samples=6000, random_state=42):
    np.random.seed(random_state)
    
    # 70% Legitimate (Normal Users), 30% Fraudulent (Scams, Phishing, Drainers)
    num_normal = int(num_samples * 0.70)
    num_fraud = num_samples - num_normal
    
    data = []
    
    # 1. Generate Normal / Safe Accounts
    for i in range(num_normal):
        # Normal accounts: longer lifespan, varied transactions, steady balance
        time_diff = np.random.exponential(scale=200000) + 1440  # 1 day to a year+
        sent_tnx = int(np.random.negative_binomial(5, 0.1)) + 1
        received_tnx = int(np.random.negative_binomial(8, 0.1)) + 1
        created_contracts = 1 if np.random.rand() < 0.05 else 0
        unique_recv = min(received_tnx, int(np.random.uniform(1, received_tnx + 1)))
        unique_sent = min(sent_tnx, int(np.random.uniform(1, sent_tnx + 1)))
        
        avg_recv = float(np.random.exponential(scale=1.5) + 0.01)
        max_recv = float(avg_recv * np.random.uniform(1.2, 5.0))
        min_recv = float(avg_recv * np.random.uniform(0.01, 0.5))
        
        avg_sent = float(np.random.exponential(scale=1.2) + 0.01)
        max_sent = float(avg_sent * np.random.uniform(1.2, 4.0))
        min_sent = float(avg_sent * np.random.uniform(0.01, 0.5))
        
        total_recv = float(received_tnx * avg_recv)
        total_sent = float(sent_tnx * avg_sent)
        # Normal users usually keep a portion of their balance
        balance = max(0.001, total_recv - total_sent + np.random.uniform(0.05, 2.0))
        is_contract = 1 if np.random.rand() < 0.25 else 0
        gas_price_gwei = float(np.random.normal(loc=25, scale=8))
        gas_price_gwei = max(10.0, gas_price_gwei)
        drainer_signal = float(np.random.beta(1, 10)) # Very low signal
        
        data.append({
            'time_diff_first_last': time_diff,
            'sent_tnx': sent_tnx,
            'received_tnx': received_tnx,
            'created_contracts': created_contracts,
            'unique_received_from': unique_recv,
            'unique_sent_to': unique_sent,
            'min_val_received': min_recv,
            'max_val_received': max_recv,
            'avg_val_received': avg_recv,
            'min_val_sent': min_sent,
            'max_val_sent': max_sent,
            'avg_val_sent': avg_sent,
            'total_ether_sent': total_sent,
            'total_ether_received': total_recv,
            'total_ether_balance': balance,
            'is_contract_interaction': is_contract,
            'gas_price_gwei': gas_price_gwei,
            'drainer_risk_factor': drainer_signal,
            'is_fraud': 0  # Safe
        })
        
    # 2. Generate Fraud / Scam Accounts (Drainers, Phishing, Fake Airdrops)
    for i in range(num_fraud):
        # Scammer characteristics:
        # - Very short lifespan (newly created wallet or fast exit)
        # - Rapid incoming funds immediately swept out to mixer/central wallet
        # - Remaining balance often near 0
        # - High transaction velocity in short bursts
        # - High gas price to speed up draining
        time_diff = np.random.exponential(scale=5000) + 10  # minutes or hours
        received_tnx = int(np.random.uniform(2, 60))
        sent_tnx = int(np.random.uniform(1, 15))  # fewer sweeps to collector wallet
        created_contracts = 1 if np.random.rand() < 0.35 else 0 # fake token / drainer contract
        unique_recv = received_tnx # each victim is a distinct address
        unique_sent = int(np.random.uniform(1, 3)) # sent only to 1 or 2 mixer/deposit wallets
        
        avg_recv = float(np.random.exponential(scale=2.5) + 0.1)
        max_recv = float(avg_recv * np.random.uniform(2.0, 10.0))
        min_recv = float(avg_recv * np.random.uniform(0.001, 0.1))
        
        # Scammers sweep almost 99% of what they receive
        total_recv = float(received_tnx * avg_recv)
        total_sent = float(total_recv * np.random.uniform(0.92, 0.999))
        avg_sent = total_sent / max(1, sent_tnx)
        max_sent = float(avg_sent * np.random.uniform(1.2, 2.5))
        min_sent = float(avg_sent * 0.5)
        
        # Remaining balance is nearly 0 after cashout
        balance = float(np.random.uniform(0.0001, 0.05))
        is_contract = 1 if np.random.rand() < 0.65 else 0
        # High gas price used by drainers to quickly sweep funds before victim notices
        gas_price_gwei = float(np.random.normal(loc=85, scale=25))
        gas_price_gwei = max(35.0, gas_price_gwei)
        drainer_signal = float(np.random.beta(6, 2)) # High risk signal
        
        data.append({
            'time_diff_first_last': time_diff,
            'sent_tnx': sent_tnx,
            'received_tnx': received_tnx,
            'created_contracts': created_contracts,
            'unique_received_from': unique_recv,
            'unique_sent_to': unique_sent,
            'min_val_received': min_recv,
            'max_val_received': max_recv,
            'avg_val_received': avg_recv,
            'min_val_sent': min_sent,
            'max_val_sent': max_sent,
            'avg_val_sent': avg_sent,
            'total_ether_sent': total_sent,
            'total_ether_received': total_recv,
            'total_ether_balance': balance,
            'is_contract_interaction': is_contract,
            'gas_price_gwei': gas_price_gwei,
            'drainer_risk_factor': drainer_signal,
            'is_fraud': 1  # Fraud / Scam
        })
        
    df = pd.DataFrame(data)
    # Shuffle the dataset
    df = df.sample(frac=1.0, random_state=random_state).reset_index(drop=True)
    
    output_path = os.path.join(os.path.dirname(__file__), 'ethereum_fraud_dataset.csv')
    df.to_csv(output_path, index=False)
    print(f"Dataset generated successfully at: {output_path}")
    print(f"Total samples: {len(df)} (Normal: {num_normal}, Fraudulent: {num_fraud})")
    return df

if __name__ == '__main__':
    generate_ethereum_dataset()
