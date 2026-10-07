from flask import Flask, jsonify, send_from_directory
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

STOCKS = {
    'amazon': 'AMZN',
    'microsoft': 'MSFT',
    'adobe': 'ADBE',
    'pfizer': 'PFE',
    'johnson': 'JNJ',
    'vertex': 'VRTX',
    'hdfc': 'HDFCBANK.NS',
    'bajaj': 'BAJFINANCE.NS',
    'muthoot': 'MUTHOOTFIN.NS'
}

@app.route('/')
def home():
    return send_from_directory('.', 'login.html')

@app.route('/<path:filename>')
def serve_files(filename):
    return send_from_directory('.', filename)

def generate_chart(symbol, period, filename):
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    plt.figure(figsize=(10, 4))
    plt.plot(hist.index, hist['Close'], color='blue')
    plt.title(f'{symbol} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.tight_layout()
    os.makedirs('static/charts', exist_ok=True)
    path = f'static/charts/{filename}.png'
    plt.savefig(path)
    plt.close()

def format_large_number(val):
    if val is None:
        return 'N/A'
    if val >= 1_000_000_000_000:
        return f'{val/1_000_000_000_000:.2f} Trillion'
    if val >= 1_000_000_000:
        return f'{val/1_000_000_000:.2f} Billion'
    if val >= 1_000_000:
        return f'{val/1_000_000:.2f} Million'
    return str(val)

@app.route('/stock/<name>')
def stock(name):
    if name not in STOCKS:
        return "Stock not found", 404

    symbol = STOCKS[name]
    ticker = yf.Ticker(symbol)
    info = ticker.info

    # Generate charts
    generate_chart(symbol, '1mo', f'{name}_1m')
    generate_chart(symbol, '1y', f'{name}_1y')
    generate_chart(symbol, '5y', f'{name}_5y')

    # Get financial data safely
    price = info.get('currentPrice') or info.get('regularMarketPrice')
    market_cap = format_large_number(info.get('marketCap'))
    pe_ratio = round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else 'N/A'
    dividend = info.get('dividendYield')
    dividend = f"{round(dividend, 4)}%" if dividend else '-'
    analyst_rating = info.get('recommendationKey', 'N/A').replace('_', ' ').title()
    price_target = info.get('targetMeanPrice', 'N/A')
    revenue = format_large_number(info.get('totalRevenue'))
    net_income = format_large_number(info.get('netIncomeToCommon'))
    eps = info.get('trailingEps', 'N/A')

    return jsonify({
        'name': name,
        'symbol': symbol,
        'price': price,
        'market_cap': market_cap,
        'pe_ratio': pe_ratio,
        'dividend': dividend,
        'analyst_rating': analyst_rating,
        'price_target': price_target,
        'revenue': revenue,
        'net_income': net_income,
        'eps': eps,
        'chart_1m': f'/static/charts/{name}_1m.png',
        'chart_1y': f'/static/charts/{name}_1y.png',
        'chart_5y': f'/static/charts/{name}_5y.png'
    })

if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)