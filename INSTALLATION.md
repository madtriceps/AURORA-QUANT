# Aurora Quant Installation & Setup

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

## Local Installation

### 1. Clone or Download

\`\`\`bash
git clone <repository-url>
cd aurora-quant
\`\`\`

### 2. Create Virtual Environment

\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

### 3. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Run Platform

\`\`\`bash
python main.py
\`\`\`

## Docker Installation

### Build Image

\`\`\`bash
docker build -t aurora-quant .
\`\`\`

### Run Container

\`\`\`bash
docker run -it aurora-quant
\`\`\`

### Using Docker Compose

\`\`\`bash
docker-compose up -d
docker-compose exec aurora-quant python main.py
\`\`\`

## Troubleshooting

### "No module named 'X'"

Ensure all dependencies are installed:
\`\`\`bash
pip install -r requirements.txt --upgrade
\`\`\`

### API Connection Errors

- Check internet connection
- Verify Binance API status
- Ensure yfinance can reach Yahoo Finance

### Insufficient Data Error

- Try running with `--days 7` for more historical data
- Check if market is open for equities

## Configuration

Edit `core/config.py` to adjust:
- Slippage percentages
- Risk profiles
- Indicator periods
- API endpoints
