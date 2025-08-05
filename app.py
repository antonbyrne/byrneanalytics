from flask import Flask, render_template, request ,redirect, url_for, flash
import pandas as pd

app = Flask(__name__)

app = Flask(__name__)
app.secret_key = 'byrne_group_byrne_analytics'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/visuals')
def visuals():
    return render_template('visuals.html')

@app.route('/unemployment')
def unemployment():
    import pandas as pd

    df = pd.read_csv('data/unemployment_ireland.csv')
    df['Month'] = pd.to_datetime(df['Month'], format='%Y %B')
    df = df.sort_values('Month')

    dates = df['Month'].dt.strftime('%Y-%m').tolist()
    rates = df['Unemployment Rate %'].round(2).tolist()

    return render_template('unemployment.html', dates=dates, rates=rates)

@app.route('/rent')
def rent():
    rent_df = pd.read_csv('data/rent_prices.csv')
    rent_df = rent_df.dropna()

    return render_template(
        'rent.html',
        years=rent_df['year'].tolist(),
        national_rent=rent_df['national'].tolist(),
        dublin_rent=rent_df['dublin'].tolist()
    )

@app.route('/mortgage')
def mortgage():
    mortgage_df = pd.read_csv('data/mortgage_rates.csv')
    mortgage_df = mortgage_df.dropna()

    years = mortgage_df['year'].tolist()
    rates = mortgage_df['avg_mortgage_rate'].tolist()

    return render_template('mortgage.html', years=years, rates=rates)

@app.route('/gdp')
def gdp_chart():
    import pandas as pd
    df = pd.read_csv('data/ireland_gdp.csv')
    df = df.dropna()

    years = df['Year'].astype(str).tolist()
    values = df['Nominal GDP'].astype(int).tolist()

    return render_template('gdp.html', years=years, values=values)

@app.route('/debt')
def debt():
    import pandas as pd

    df = pd.read_csv('data/debt.csv', usecols=['Year', 'Debt (Billion EUR)', 'Debt to Revenue (%)'])
    df.columns = df.columns.str.strip()
    df = df.dropna()

    years = df['Year'].astype(int).astype(str).tolist()
    debt_values = df['Debt (Billion EUR)'].astype(float).tolist()
    debt_percent = df['Debt to Revenue (%)'].str.replace('%', '').astype(float).tolist()

    return render_template('debt.html', years=years, debt_values=debt_values, debt_percent=debt_percent)

@app.route('/insights')
def insights():
    return render_template('insights.html')

@app.route('/articles/housing/<article>')
def housing_article(article):
    return render_template(f'articles/housing/{article}.html')

@app.route('/articles/salary/<article>')
def salary_article(article):
    return render_template(f'articles/salary/{article}.html')

@app.route('/articles/public/<article>')
def public_article(article):
    return render_template(f'articles/public/{article}.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        print(f"New Feedback:\nName: {name}\nEmail: {email}\nMessage: {message}")

        flash("Thanks for your feedback!", "success")
        return redirect(url_for('feedback'))

    return render_template('feedback.html')

import requests
from datetime import datetime
import yfinance as yf

@app.route('/fear-greed')
def fear_greed_index():
    return render_template('fear_greed/fear_greed.html')

@app.route('/fear-greed/sp500')
def sp500_index():
    import requests
    from datetime import datetime

    url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"Error: Could not fetch data. Status code: {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        return "Error: Invalid JSON response from CNN API"

    raw_values = data.get("fear_and_greed_historical", {}).get("data", [])
    if not raw_values:
        return "Error: No data found in response."


    dates = [datetime.fromtimestamp(entry.get("x") / 1000).strftime('%Y-%m-%d') for entry in raw_values]
    values = [entry.get("y") for entry in raw_values]

    return render_template('fear_greed/sp500.html', dates=dates[-30:], values=values[-30:])

@app.route('/fear-greed/crypto')
def crypto_index():
    response = requests.get("https://api.alternative.me/fng/?limit=30")
    data = response.json()['data']

    dates = [datetime.fromtimestamp(int(entry['timestamp'])).strftime('%Y-%m-%d') for entry in data]
    values = [int(entry['value']) for entry in data]

    dates.reverse()
    values.reverse()

    return render_template('fear_greed/crypto.html', dates=dates, values=values)

if __name__ == '__main__':
    app.run(debug=True)
