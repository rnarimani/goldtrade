# Gold Trade Analysis Tool

A comprehensive tool for analyzing gold market prices and investment opportunities, including physical gold, coins, and digital gold tokens.

## Overview

This tool helps investors make informed decisions by:
- Tracking real-time prices from multiple sources
- Calculating price premiums and bubbles
- Providing investment recommendations
- Visualizing market data through an interactive dashboard

## Features

### Price Monitoring
- **Global Gold Price**: Real-time price per ounce in USD
- **Local Gold Price**: 18k gold price per gram in Tomans
- **Gold Coins**:
  - Emami Full Coin
  - Half Azadi Coin
  - Quarter Azadi Coin
- **Digital Gold**:
  - PAXG (Pax Gold)
  - XAUT (Tether Gold)
- **Exchange Rate**: USD/IRR

### Analysis Tools
- Gold price premium/discount calculation
- Coin bubble analysis
- Market timing indicators
- Investment rankings
- Comparative analysis between different gold assets

### Interactive Dashboard
- Real-time data updates
- Interactive charts and gauges
- Price comparison tools
- Investment recommendations
- Market trend visualization

## Technical Details

### Price Premium Calculation

### Coin Weights
- Emami Full Coin: 8.133 grams
- Half Azadi: 4.068 grams
- Quarter Azadi: 2.034 grams

### Gold Purity
- 18k Gold: 0.750 (75% pure gold)
- Coins: 0.900 (90% pure gold)

## Sample Output

### Market Status

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rnarimani/goldtrade.git
cd goldtrade
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface
For basic price analysis:
```bash
python coin_price_calculator.py
```

### Interactive Dashboard
To launch the web dashboard:
```bash
streamlit run dashboard.py
```

## Dashboard Features

### Market Overview Tab
- Global gold price gauge
- Digital gold comparison chart
- Exchange rate trends
- Price premium indicators

### Coin Analysis Tab
- Bubble comparison chart
- Price history
- Investment recommendations
- Risk analysis

### Investment Recommendations Tab
- Ranked investment options
- Market timing signals
- Risk/reward analysis
- Storage and liquidity considerations

## Data Sources
- Gold and coin prices: bon-bast.com
- Digital gold prices: MEXC Exchange
- Exchange rates: bon-bast.com

## Project Structure
```
goldtrade/
├── coin_price_calculator.py   # Core analysis engine
├── dashboard.py              # Streamlit dashboard
├── requirements.txt         # Package dependencies
└── README.md               # Documentation
```

## Dependencies
- Python 3.8+
- Selenium
- Streamlit
- Plotly
- Pandas
- Requests
- Colorama
- Tabulate

## Error Handling
- Automatic retry on connection failures
- Fallback data sources
- Comprehensive error logging
- User-friendly error messages

## Performance Optimization
- Data caching
- Parallel price fetching
- Efficient calculations
- Optimized web scraping

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

### Development Guidelines
1. Fork the repository
2. Create your feature branch
3. Write clear commit messages
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## License
This project is licensed under the MIT License.

## Disclaimer
This tool is for informational purposes only. Always conduct your own research before making investment decisions. The calculations and recommendations are based on mathematical models and historical data, which may not predict future market behavior.

## Support
For issues or feature requests, please open an issue on GitHub.

## Future Enhancements
- Historical price analysis
- Price prediction models
- Mobile app version
- API integration
- Additional digital tokens
- Multi-currency support

## Acknowledgments
- bon-bast.com for providing market data
- MEXC Exchange for digital gold prices
- Streamlit for dashboard framework
- Open source community