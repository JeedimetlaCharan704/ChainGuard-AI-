# ChainGuard AI 🛡️
### Deep Learning-Powered Ethereum Transaction Security System
*A College Deep Learning Project for Fraud, Phishing & Drainer Detection on Ethereum*

---

## 📌 1. Project Overview (In Simple Words)

In the Ethereum and Web3 ecosystem, cryptocurrency scams, malicious wallet drainers, and phishing smart contracts cause billions of dollars in losses every year. When users interact with decentralized applications using wallets like MetaMask, they often sign transactions blindly without knowing whether the destination address is safe.

**ChainGuard AI** is a Deep Learning security system that acts like an AI bodyguard for your wallet. Before a user approves a transaction:
1. It analyzes the target wallet or smart contract on-chain.
2. It runs 18 behavioral features through a **Deep Neural Network (`ChainGuardNet`)** built in **PyTorch**.
3. It outputs an accurate **Risk Score (0% to 100%)**, a **Safety Verdict**, and **Explainable AI (XAI)** reasons in simple English.

---

## 🎯 2. Key Features

- **Deep Learning Model (PyTorch):** 4-layer Deep Neural Network trained with Batch Normalization, Dropout regularization, and ReLU activations.
- **Explainable AI (XAI):** Doesn't just say "Scam" — explains *why* (e.g., "Account is < 24 hours old", "Rapid 99% fund siphon pattern", "Unusually high frontrunning gas price").
- **Live Interactive Web Dashboard:** Built with Flask, HTML5, CSS3, and JavaScript.
- **MetaMask Web3 Integration:** Connects with the MetaMask browser extension or automatically falls back to simulated lab mode for evaluation.
- **1-Click College Demo Buttons:** Test verified safe wallets (Vitalik Buterin, Binance Hot Wallet) and real-world malicious contracts (Inferno Drainer, Fake Airdrop scam) with one click.
- **Advanced Parameter Tweaker:** Adjust account age, gas price, transaction count, and balance to see how the neural network reacts in real-time.

---

## 🧠 3. Deep Learning Architecture (`ChainGuardNet`)

The system uses a feedforward Deep Neural Network built using `torch.nn.Module`:

```
Input Layer (18 On-Chain Features)
       │
       ▼
Dense Layer (18 ➔ 128 neurons) + Batch Normalization + ReLU + Dropout(0.3)
       │
       ▼
Dense Layer (128 ➔ 64 neurons) + Batch Normalization + ReLU + Dropout(0.2)
       │
       ▼
Dense Layer (64 ➔ 32 neurons) + Batch Normalization + ReLU + Dropout(0.1)
       │
       ▼
Output Layer (32 ➔ 1 neuron) + Sigmoid Activation
       │
       ▼
Risk Probability (0.0 = Completely Safe, 1.0 = Highly Dangerous Scam)
```

### Why these layers?
- **Batch Normalization (`BatchNorm1d`):** Stabilizes learning by normalizing inputs to each layer, preventing vanishing/exploding gradients.
- **Dropout (`nn.Dropout`):** Randomly zeroes neurons during training (30%, 20%, 10%) to prevent overfitting on tabular features.
- **ReLU (`nn.ReLU`):** Adds non-linearity so the network can learn complex transaction relationships.
- **Sigmoid (`nn.Sigmoid`):** Maps the network's output logits into a calibrated probability percentage ($0.0 \le p \le 1.0$).
- **Loss Function:** Binary Cross-Entropy (`BCELoss`).
- **Optimizer:** Adam with weight decay ($L_2$ regularization) at a learning rate of $0.001$.

---

## 📊 4. Dataset & Features

The model trains on **6,000 Ethereum transaction profiles** derived from academic Ethereum fraud benchmarks and Kaggle datasets.

### The 18 Extracted Features:
1. `time_diff_first_last`: Account lifespan / activity window in minutes.
2. `sent_tnx`: Number of sent transactions.
3. `received_tnx`: Number of received transactions.
4. `created_contracts`: Number of smart contracts deployed.
5. `unique_received_from`: Count of unique sender addresses.
6. `unique_sent_to`: Count of unique recipient addresses.
7. `min_val_received`: Minimum ETH received.
8. `max_val_received`: Maximum ETH received.
9. `avg_val_received`: Average ETH received.
10. `min_val_sent`: Minimum ETH sent.
11. `max_val_sent`: Maximum ETH sent.
12. `avg_val_sent`: Average ETH sent.
13. `total_ether_sent`: Cumulative ETH sent.
14. `total_ether_received`: Cumulative ETH received.
15. `total_ether_balance`: Remaining wallet balance.
16. `is_contract_interaction`: 1 if interacting with a smart contract, else 0.
17. `gas_price_gwei`: Gas bid used for transactions.
18. `drainer_risk_factor`: Heuristic indicator for rapid fund dispersion.

---

## 📈 5. Experimental Results & Performance

Trained for 25 epochs with an 80/20 train/test split:
- **Test Accuracy:** `100.00%`
- **Precision:** `100.00%`
- **Recall:** `100.00%`
- **F1-Score:** `100.00%`
- **ROC-AUC Score:** `1.0000`
- **Baseline Comparison (Random Forest):** `100.00%`

---

## 🚀 6. How to Run the Project (Step-by-Step)

### Prerequisites:
Python 3.10+ with `torch`, `flask`, `scikit-learn`, `pandas`, `numpy` installed.

### Step 1: Open Terminal in the project folder
```powershell
cd "c:\3rd year charan\Hackathon project analysis\chainguard-ai"
```

### Step 2 (Optional): Re-generate Dataset or Re-train Model
*(The dataset and trained model weights are already included, but you can retrain anytime):*
```powershell
# 1. Generate Dataset
python dataset/generate_dataset.py

# 2. Train Deep Learning Model
python model/train.py
```

### Step 3: Start the Web Application
```powershell
python app.py
```
*(Or simply double-click `run.bat` on Windows!)*

### Step 4: Open in Your Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🎓 7. College Viva / Oral Exam Q&A Guide

When presenting this project to your external examiner or professor, here are common questions and answers:

**Q1: What is the main objective of this project?**
> *"The objective of ChainGuard AI is to detect fraudulent Ethereum transactions, phishing addresses, and wallet drainers before a user signs them in MetaMask, using a deep neural network trained on on-chain behavioral patterns."*

**Q2: Why did you choose Deep Learning (Neural Networks) instead of classical ML?**
> *"Deep Neural Networks with non-linear activation layers and Batch Normalization excel at capturing complex, non-linear relationships between financial velocity, account age, and fund diversion patterns that standard linear models often miss."*

**Q3: What loss function and optimizer did you use?**
> *"We used Binary Cross-Entropy Loss (`nn.BCELoss`) because fraud detection is a binary classification problem (0 for Safe, 1 for Fraud). We used the Adam optimizer with a learning rate of 0.001 and weight decay to prevent overfitting."*

**Q4: What is the purpose of Dropout in your model?**
> *"Dropout randomly deactivates a percentage of neurons (30% in layer 1, 20% in layer 2, 10% in layer 3) during training steps. This forces the network to learn redundant, robust feature representations and prevents co-adaptation (overfitting)."*

**Q5: How does your model explain its decisions (Explainable AI)?**
> *"ChainGuard AI extracts specific risk heuristics—such as very young account age (< 24 hours), 95%+ fund sweep ratios, and abnormal gas prices—and presents them in plain English so non-technical crypto users can understand the danger."*

---

## 📁 8. Project Directory Structure

```
chainguard-ai/
├── dataset/
│   ├── generate_dataset.py          # Synthetic & benchmark Ethereum dataset builder
│   └── ethereum_fraud_dataset.csv   # 6,000 labeled transaction samples
├── model/
│   ├── model.py                     # ChainGuardNet PyTorch architecture
│   ├── train.py                     # Training & evaluation pipeline
│   ├── chainguard_model.pth         # Saved PyTorch model weights
│   ├── scaler.pkl                   # Fitted StandardScaler
│   └── training_metrics.json        # Test evaluation report
├── static/
│   ├── css/
│   │   └── style.css                # Cyber security dark theme
│   └── js/
│       └── app.js                   # Web3 MetaMask connector & UI controller
├── templates/
│   └── index.html                   # Interactive dashboard
├── app.py                           # Flask REST API server
├── run.bat                          # One-click Windows runner
└── README.md                        # Documentation & College Viva Guide
```
