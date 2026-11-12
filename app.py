"""
ChainGuard AI - Web Application & Security Engine
Backend: Flask REST API + Hybrid PyTorch/NumPy Deep Learning Inference Engine
"""

import os
import sys
import json
import numpy as np

from flask import Flask, render_template, request, jsonify, send_from_directory

base_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(base_dir, 'model')
sys.path.append(model_dir)

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(base_dir, 'static'), filename)

# Global model and scaler variables
MODEL = None
SCALER = None
SCALER_PARAMS = None
NPZ_WEIGHTS = None
METRICS = None
FEATURE_COLS = []
USE_TORCH = False

def load_ai_engine():
    global MODEL, SCALER, SCALER_PARAMS, NPZ_WEIGHTS, METRICS, FEATURE_COLS, USE_TORCH
    
    # 1. Load Metrics
    metrics_path = os.path.join(model_dir, 'training_metrics.json')
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r') as f:
            METRICS = json.load(f)
            FEATURE_COLS = METRICS.get('feature_columns', [])

    # 2. Load Scaler (pkl or json)
    scaler_params_path = os.path.join(model_dir, 'scaler_params.json')
    if os.path.exists(scaler_params_path):
        with open(scaler_params_path, 'r') as f:
            SCALER_PARAMS = json.load(f)
            
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    if os.path.exists(scaler_path):
        try:
            import pickle
            with open(scaler_path, 'rb') as f:
                SCALER = pickle.load(f)
        except Exception:
            pass

    # 3. Load Model: Try PyTorch first, fallback to exact NumPy forward pass
    weights_npz_path = os.path.join(model_dir, 'model_weights.npz')
    if os.path.exists(weights_npz_path):
        NPZ_WEIGHTS = np.load(weights_npz_path)

    try:
        import torch
        from model import ChainGuardNet
        model_weights_path = os.path.join(model_dir, 'chainguard_model.pth')
        if os.path.exists(model_weights_path):
            MODEL = ChainGuardNet(input_dim=len(FEATURE_COLS) if FEATURE_COLS else 18)
            MODEL.load_state_dict(torch.load(model_weights_path, map_location=torch.device('cpu')))
            MODEL.eval()
            USE_TORCH = True
            print("ChainGuard AI Engine initialized with PyTorch backend.")
    except Exception as e:
        print(f"PyTorch not available or skipped ({e}). Using optimized NumPy Deep Learning engine.")
        USE_TORCH = False

# Known sample addresses for live demonstration
PRESET_PROFILES = {
    "0xd8da6bf26964af9d7eed9e03e53415d37aa96045": {
        "name": "Vitalik Buterin (vitalik.eth)",
        "type": "Safe Public Figure",
        "description": "Long-standing high reputation wallet with years of diversified on-chain activity.",
        "features": {
            "time_diff_first_last": 31536000.0,
            "sent_tnx": 1250,
            "received_tnx": 8420,
            "created_contracts": 12,
            "unique_received_from": 5200,
            "unique_sent_to": 890,
            "min_val_received": 0.001,
            "max_val_received": 500.0,
            "avg_val_received": 14.2,
            "min_val_sent": 0.01,
            "max_val_sent": 320.0,
            "avg_val_sent": 8.5,
            "total_ether_sent": 10625.0,
            "total_ether_received": 119564.0,
            "total_ether_balance": 240.5,
            "is_contract_interaction": 1,
            "gas_price_gwei": 22.5,
            "drainer_risk_factor": 0.01
        }
    },
    "0x28c6c06298d514db089934071355e5743bf21d60": {
        "name": "Binance 14 (Exchange Hot Wallet)",
        "type": "High-Volume Exchange Wallet",
        "description": "Massive institutional liquidity pool with millions of legitimate transactions.",
        "features": {
            "time_diff_first_last": 18000000.0,
            "sent_tnx": 95000,
            "received_tnx": 180000,
            "created_contracts": 0,
            "unique_received_from": 92000,
            "unique_sent_to": 78000,
            "min_val_received": 0.005,
            "max_val_received": 2500.0,
            "avg_val_received": 18.0,
            "min_val_sent": 0.01,
            "max_val_sent": 3000.0,
            "avg_val_sent": 15.0,
            "total_ether_sent": 1425000.0,
            "total_ether_received": 3240000.0,
            "total_ether_balance": 1815000.0,
            "is_contract_interaction": 0,
            "gas_price_gwei": 28.0,
            "drainer_risk_factor": 0.02
        }
    },
    "0x98c47b520445d4c94f5c9e47cb5c8a38b2d131f4": {
        "name": "Inferno / Angel Drainer Associated Address",
        "type": "Malicious Phishing Drainer",
        "description": "Recently created wallet used in phishing campaigns. Automatically sweeps incoming victim funds to wash wallets within minutes.",
        "features": {
            "time_diff_first_last": 120.0,
            "sent_tnx": 6,
            "received_tnx": 42,
            "created_contracts": 0,
            "unique_received_from": 42,
            "unique_sent_to": 1,
            "min_val_received": 0.05,
            "max_val_received": 8.4,
            "avg_val_received": 1.25,
            "min_val_sent": 4.5,
            "max_val_sent": 25.0,
            "avg_val_sent": 8.7,
            "total_ether_sent": 52.2,
            "total_ether_received": 52.5,
            "total_ether_balance": 0.002,
            "is_contract_interaction": 1,
            "gas_price_gwei": 140.0,
            "drainer_risk_factor": 0.96
        }
    },
    "0x4e8d3568c0b561c28c68ff8701918a287a99f123": {
        "name": "Fake Airdrop Scam Smart Contract",
        "type": "Honeypot / Malicious Contract",
        "description": "Mimics an ERC-20 token claim. Exploits permit/transferFrom approvals to siphon wallet assets upon interaction.",
        "features": {
            "time_diff_first_last": 45.0,
            "sent_tnx": 2,
            "received_tnx": 19,
            "created_contracts": 1,
            "unique_received_from": 19,
            "unique_sent_to": 1,
            "min_val_received": 0.01,
            "max_val_received": 4.2,
            "avg_val_received": 0.85,
            "min_val_sent": 3.0,
            "max_val_sent": 13.0,
            "avg_val_sent": 8.0,
            "total_ether_sent": 16.0,
            "total_ether_received": 16.15,
            "total_ether_balance": 0.005,
            "is_contract_interaction": 1,
            "gas_price_gwei": 115.0,
            "drainer_risk_factor": 0.94
        }
    }
}

def generate_address_features(address):
    addr_clean = address.lower().strip()
    if addr_clean in PRESET_PROFILES:
        return PRESET_PROFILES[addr_clean]["features"], PRESET_PROFILES[addr_clean]["name"]
        
    seed = sum(ord(c) for c in addr_clean)
    np.random.seed(seed)
    
    is_suspicious = (seed % 3 == 0)
    
    if is_suspicious:
        name = "Unverified High-Velocity Address"
        features = {
            "time_diff_first_last": float(np.random.uniform(30, 2800)),
            "sent_tnx": int(np.random.uniform(1, 10)),
            "received_tnx": int(np.random.uniform(5, 50)),
            "created_contracts": 1 if (seed % 2 == 0) else 0,
            "unique_received_from": int(np.random.uniform(5, 45)),
            "unique_sent_to": 1,
            "min_val_received": 0.01,
            "max_val_received": 6.0,
            "avg_val_received": 1.1,
            "min_val_sent": 1.0,
            "max_val_sent": 15.0,
            "avg_val_sent": 5.0,
            "total_ether_sent": 25.0,
            "total_ether_received": 25.2,
            "total_ether_balance": 0.008,
            "is_contract_interaction": 1,
            "gas_price_gwei": float(np.random.uniform(70, 130)),
            "drainer_risk_factor": float(np.random.uniform(0.75, 0.98))
        }
    else:
        name = "Standard Ethereum User Wallet"
        features = {
            "time_diff_first_last": float(np.random.uniform(50000, 1000000)),
            "sent_tnx": int(np.random.uniform(15, 120)),
            "received_tnx": int(np.random.uniform(20, 200)),
            "created_contracts": 0,
            "unique_received_from": int(np.random.uniform(10, 80)),
            "unique_sent_to": int(np.random.uniform(10, 60)),
            "min_val_received": 0.05,
            "max_val_received": 12.0,
            "avg_val_received": 1.4,
            "min_val_sent": 0.02,
            "max_val_sent": 8.0,
            "avg_val_sent": 1.1,
            "total_ether_sent": 45.0,
            "total_ether_received": 58.0,
            "total_ether_balance": 13.0,
            "is_contract_interaction": 0,
            "gas_price_gwei": float(np.random.uniform(18, 32)),
            "drainer_risk_factor": float(np.random.uniform(0.01, 0.15))
        }
        
    return features, name

def run_deep_learning_inference(features_dict):
    global MODEL, SCALER, SCALER_PARAMS, NPZ_WEIGHTS, USE_TORCH
    if MODEL is None and NPZ_WEIGHTS is None:
        load_ai_engine()
        
    feature_vector = [features_dict.get(col, 0.0) for col in FEATURE_COLS]
    X_raw = np.array([feature_vector], dtype=np.float32)
    
    # Scale features
    if SCALER is not None:
        X_scaled = SCALER.transform(X_raw)
    elif SCALER_PARAMS is not None:
        mean = np.array(SCALER_PARAMS['mean'], dtype=np.float32)
        scale = np.array(SCALER_PARAMS['scale'], dtype=np.float32)
        X_scaled = (X_raw - mean) / scale
    else:
        X_scaled = X_raw

    # Forward pass
    if USE_TORCH and MODEL is not None:
        import torch
        with torch.no_grad():
            input_tensor = torch.tensor(X_scaled, dtype=torch.float32)
            prob, _ = MODEL(input_tensor)
            risk_probability = float(prob.item())
    else:
        w = NPZ_WEIGHTS
        x = X_scaled
        # Layer 1
        x = np.dot(x, w['fc1.weight'].T) + w['fc1.bias']
        x = (x - w['bn1.running_mean']) / np.sqrt(w['bn1.running_var'] + 1e-5) * w['bn1.weight'] + w['bn1.bias']
        x = np.maximum(0, x)
        # Layer 2
        x = np.dot(x, w['fc2.weight'].T) + w['fc2.bias']
        x = (x - w['bn2.running_mean']) / np.sqrt(w['bn2.running_var'] + 1e-5) * w['bn2.weight'] + w['bn2.bias']
        x = np.maximum(0, x)
        # Layer 3
        x = np.dot(x, w['fc3.weight'].T) + w['fc3.bias']
        x = (x - w['bn3.running_mean']) / np.sqrt(w['bn3.running_var'] + 1e-5) * w['bn3.weight'] + w['bn3.bias']
        x = np.maximum(0, x)
        # Output Layer
        x = np.dot(x, w['fc_out.weight'].T) + w['fc_out.bias']
        risk_probability = float(1.0 / (1.0 + np.exp(-x))[0, 0])
        
    risk_score = round(risk_probability * 100, 1)
    
    if risk_score < 30:
        level = "SAFE"
        color = "#10B981"
        badge = "badge-safe"
    elif risk_score < 70:
        level = "SUSPICIOUS / CAUTION"
        color = "#F59E0B"
        badge = "badge-warning"
    else:
        level = "DANGEROUS / SCAM DETECTED"
        color = "#EF4444"
        badge = "badge-danger"
        
    reasons = []
    if features_dict.get("drainer_risk_factor", 0) > 0.6:
        reasons.append({
            "severity": "HIGH",
            "title": "Malicious Drainer Signature",
            "desc": "Transaction pattern matches known phishing drainers that attempt to siphon token allowances."
        })
        
    if features_dict.get("time_diff_first_last", 99999) < 1440:
        reasons.append({
            "severity": "HIGH",
            "title": "Freshly Created Address",
            "desc": "This address was created very recently (< 24 hours ago). Scammers frequently discard wallets after each attack."
        })
        
    sent = features_dict.get("total_ether_sent", 0)
    recv = features_dict.get("total_ether_received", 0)
    if recv > 0 and (sent / recv) > 0.95 and features_dict.get("total_ether_balance", 0) < 0.05:
        reasons.append({
            "severity": "MEDIUM",
            "title": "Rapid Fund Siphon (Zero Holding)",
            "desc": "Over 95% of incoming funds are immediately forwarded to another wallet, leaving near-zero residual balance."
        })
        
    if features_dict.get("gas_price_gwei", 20) > 60:
        reasons.append({
            "severity": "MEDIUM",
            "title": "Abnormally High Gas Price",
            "desc": f"Gas bid ({features_dict.get('gas_price_gwei')} Gwei) is significantly higher than network median. Often used by bots to frontrun victims."
        })
        
    if features_dict.get("is_contract_interaction", 0) == 1 and features_dict.get("created_contracts", 0) > 0:
        reasons.append({
            "severity": "INFO",
            "title": "Smart Contract Deployment",
            "desc": "This entity directly deploys unverified code or interactions on Ethereum."
        })
        
    if not reasons:
        reasons.append({
            "severity": "LOW",
            "title": "Organic Historical Activity",
            "desc": "Healthy account age, balanced transactions, and standard holding duration. No drainer patterns identified."
        })
        
    return {
        "risk_score": risk_score,
        "risk_level": level,
        "badge_class": badge,
        "color": color,
        "confidence": round((risk_probability if risk_probability >= 0.5 else (1 - risk_probability)) * 100, 1),
        "reasons": reasons
    }

# Auto-initialize on import
load_ai_engine()

@app.route('/')
def index():
    return render_template('index.html', metrics=METRICS)

@app.route('/api/presets')
def get_presets():
    return jsonify({
        addr: {
            "address": addr,
            "name": info["name"],
            "type": info["type"],
            "description": info["description"]
        } for addr, info in PRESET_PROFILES.items()
    })

@app.route('/api/metrics')
def get_metrics():
    return jsonify(METRICS)

@app.route('/api/scan', methods=['POST'])
def scan_transaction():
    data = request.get_json() or {}
    address = data.get('address', '').strip()
    custom_features = data.get('features', None)
    
    if custom_features:
        target_features = custom_features
        target_name = "Custom Transaction Simulation"
    elif address:
        target_features, target_name = generate_address_features(address)
    else:
        target_features, target_name = generate_address_features("0xd8da6bf26964af9d7eed9e03e53415d37aa96045")
        
    analysis = run_deep_learning_inference(target_features)
    analysis["target_name"] = target_name
    analysis["address"] = address if address else "Simulated Transaction"
    analysis["features"] = target_features
    
    return jsonify(analysis)

if __name__ == '__main__':
    print("ChainGuard AI Server running at: http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)
