# Stock Wiser

Stock Wiser is a Flask-based stock information dashboard. It serves static login, registration, and stock-category pages, and provides a JSON endpoint with market data and generated price charts for selected companies.

## Features

- Stock pages for selected US and Indian-listed companies
- Company metrics from Yahoo Finance via `yfinance`
- Generated closing-price charts for 1-month, 1-year, and 5-year periods
- Static HTML and CSS pages for sign-in, registration, stock categories, and stock details

## Requirements

- Python 3.10 or newer
- Internet access for Yahoo Finance data and Google Fonts

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>.

## Stock data endpoint

Request `/stock/<name>` to retrieve JSON data and generate chart images. Supported names are `amazon`, `microsoft`, `adobe`, `pfizer`, `johnson`, `vertex`, `hdfc`, `bajaj`, and `muthoot`.

For example: <http://127.0.0.1:5000/stock/microsoft>

The charts are written to `static/charts/` when the endpoint is requested. Yahoo Finance data availability and fields may vary.

## Notes

The login and registration pages are static UI only; this project does not currently implement user accounts, authentication, or persistent portfolios. Stock data is for informational purposes and is not investment advice.
