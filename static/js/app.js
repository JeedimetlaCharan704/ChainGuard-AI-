/**
 * ChainGuard AI - Frontend Controller & Web3 MetaMask Connector
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initial scan with default safe address
    triggerScan();
    
    // Bind wallet button
    const connectWalletBtn = document.getElementById('connectWalletBtn');
    if (connectWalletBtn) {
        connectWalletBtn.addEventListener('click', connectMetaMask);
    }
});

// MetaMask Connector
async function connectMetaMask() {
    const walletBtnText = document.getElementById('walletBtnText');
    const addressInput = document.getElementById('addressInput');

    if (typeof window.ethereum !== 'undefined') {
        try {
            walletBtnText.innerText = "Connecting...";
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            
            if (accounts.length > 0) {
                const userAddr = accounts[0];
                walletBtnText.innerText = `${userAddr.substring(0, 6)}...${userAddr.substring(userAddr.length - 4)}`;
                addressInput.value = userAddr;
                
                // Immediately scan the connected wallet
                triggerScan();
            }
        } catch (error) {
            console.error("MetaMask connection rejected:", error);
            walletBtnText.innerText = "Connect MetaMask";
            alert("MetaMask connection was cancelled or rejected.");
        }
    } else {
        // Fallback for systems/browsers without MetaMask installed (ideal for College Viva / Lab)
        walletBtnText.innerText = "0x71C...3a9F (Simulated)";
        addressInput.value = "0x71C356eF736F5a8927878d655f448b1d4D863a9F";
        alert("MetaMask extension not found in this browser. Running in 'Simulated Web3' mode for lab/viva testing!");
        triggerScan();
    }
}

// 1-Click Demo Profile Loader
function loadDemo(address) {
    const addressInput = document.getElementById('addressInput');
    addressInput.value = address;
    triggerScan();
}

// Trigger Deep Learning Analysis via Flask API
async function triggerScan() {
    const addressInput = document.getElementById('addressInput');
    const scanBtn = document.getElementById('scanBtn');
    const scanBtnText = document.getElementById('scanBtnText');
    const address = addressInput.value.trim();

    if (!address) {
        alert("Please enter a valid Ethereum address or pick a quick test profile.");
        return;
    }

    scanBtn.disabled = true;
    scanBtnText.innerText = "Analyzing...";

    try {
        const response = await fetch('/api/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ address: address })
        });

        const data = await response.json();
        renderAnalysisResults(data);

    } catch (err) {
        console.error("Error analyzing address:", err);
        alert("Analysis failed. Please make sure the Flask backend is running.");
    } finally {
        scanBtn.disabled = false;
        scanBtnText.innerText = "Analyze with AI";
    }
}

// Scan with Custom Tweaked Parameters
async function scanCustomParameters() {
    const time_diff = parseFloat(document.getElementById('p_time_diff').value) || 1000;
    const sent_tnx = parseInt(document.getElementById('p_sent_tnx').value) || 10;
    const recv_tnx = parseInt(document.getElementById('p_recv_tnx').value) || 10;
    const balance = parseFloat(document.getElementById('p_balance').value) || 1.0;
    const gas = parseFloat(document.getElementById('p_gas').value) || 25;
    const drainer = parseFloat(document.getElementById('p_drainer').value) || 0.05;

    const customFeatures = {
        "time_diff_first_last": time_diff,
        "sent_tnx": sent_tnx,
        "received_tnx": recv_tnx,
        "created_contracts": 0,
        "unique_received_from": recv_tnx,
        "unique_sent_to": sent_tnx,
        "min_val_received": 0.01,
        "max_val_received": 5.0,
        "avg_val_received": 1.0,
        "min_val_sent": 0.01,
        "max_val_sent": 4.0,
        "avg_val_sent": 0.9,
        "total_ether_sent": sent_tnx * 0.9,
        "total_ether_received": recv_tnx * 1.0,
        "total_ether_balance": balance,
        "is_contract_interaction": 0,
        "gas_price_gwei": gas,
        "drainer_risk_factor": drainer
    };

    try {
        const response = await fetch('/api/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ features: customFeatures })
        });

        const data = await response.json();
        renderAnalysisResults(data);
    } catch (err) {
        console.error("Custom parameter scan failed:", err);
    }
}

// Render Results into UI Elements
function renderAnalysisResults(data) {
    const riskScoreEl = document.getElementById('riskScore');
    const riskBadgeEl = document.getElementById('riskBadge');
    const confidenceScoreEl = document.getElementById('confidenceScore');
    const gaugeCircle = document.getElementById('gaugeCircle');
    const targetTypeBadge = document.getElementById('targetTypeBadge');
    const targetNameEl = document.getElementById('targetName');
    const reasonsListEl = document.getElementById('reasonsList');
    const recommendationText = document.getElementById('recommendationText');

    const score = data.risk_score;
    riskScoreEl.innerText = `${score}%`;
    confidenceScoreEl.innerText = `${data.confidence}%`;
    targetNameEl.innerText = data.target_name || data.address;

    // Update circular gauge
    gaugeCircle.style.background = `conic-gradient(${data.color} ${score}%, #1f293d ${score}%)`;

    // Update verdict badge
    riskBadgeEl.className = `status-verdict ${data.badge_class}`;
    if (score < 30) {
        riskBadgeEl.innerText = "SAFE TO PROCEED";
        targetTypeBadge.innerText = "Verified Safe / Standard";
        targetTypeBadge.className = "badge badge-safe";
        recommendationText.innerText = "Safe to interact. Deep Neural Network detected no drainer patterns or suspicious exit velocity.";
    } else if (score < 70) {
        riskBadgeEl.innerText = "CAUTION ADVISED";
        targetTypeBadge.innerText = "Unverified Activity";
        targetTypeBadge.className = "badge badge-warning";
        recommendationText.innerText = "Exercise caution. Address exhibits abnormal spikes or newly created characteristics.";
    } else {
        riskBadgeEl.innerText = "DANGER: HIGH SCAM RISK";
        targetTypeBadge.innerText = "Malicious Drainer / Scam";
        targetTypeBadge.className = "badge badge-danger";
        recommendationText.innerText = "DO NOT SIGN! Address has high probability of being a wallet drainer or malicious phishing contract.";
    }

    // Render Explainable AI reasons
    reasonsListEl.innerHTML = '';
    data.reasons.forEach(r => {
        const sevClass = r.severity === 'HIGH' ? 'sev-high' : (r.severity === 'MEDIUM' ? 'sev-medium' : 'sev-low');
        const item = document.createElement('div');
        item.className = `reason-item ${sevClass}`;
        item.innerHTML = `
            <div class="reason-item-header">
                <span class="reason-title">${r.title}</span>
                <span class="reason-badge ${r.severity}">${r.severity}</span>
            </div>
            <p class="reason-desc">${r.desc}</p>
        `;
        reasonsListEl.appendChild(item);
    });
}
