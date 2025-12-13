# Deployment Guide

## Local Development

### Prerequisites
- Python 3.10+
- pip or poetry

### Installation

\`\`\`bash
# Clone repository
git clone <repo-url>
cd aurora-quant

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run backtest
python main.py
\`\`\`

### Running the Dashboard

\`\`\`bash
streamlit run dashboard/app.py
\`\`\`

Access at `http://localhost:8501`

## Docker Deployment

### Build Image

\`\`\`bash
docker build -t aurora-quant:latest .
\`\`\`

### Run Container

\`\`\`bash
docker run -d \
  --name aurora-quant \
  -p 8501:8501 \
  -v $(pwd)/storage:/app/storage \
  aurora-quant:latest
\`\`\`

### Docker Compose

\`\`\`bash
docker-compose up -d
\`\`\`

## Production Deployment

### Linux Server Setup

\`\`\`bash
# Update system
sudo apt update && apt upgrade -y

# Install Python 3.10+
sudo apt install python3.10 python3.10-venv

# Clone and setup
git clone <repo-url> /opt/aurora-quant
cd /opt/aurora-quant
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

### Systemd Service

Create `/etc/systemd/system/aurora-quant.service`:

\`\`\`ini
[Unit]
Description=Aurora Quant Trading Platform
After=network.target

[Service]
Type=simple
User=aurora
WorkingDirectory=/opt/aurora-quant
ExecStart=/opt/aurora-quant/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
\`\`\`

Enable and start:

\`\`\`bash
sudo systemctl enable aurora-quant
sudo systemctl start aurora-quant
\`\`\`

### Monitoring

\`\`\`bash
# View logs
sudo journalctl -u aurora-quant -f

# Check status
sudo systemctl status aurora-quant
\`\`\`

## Environment Variables

\`\`\`bash
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
DATABASE_URL=sqlite:///storage/market_data.db
LOG_LEVEL=INFO
\`\`\`
