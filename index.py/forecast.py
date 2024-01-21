import os
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Get the current working directory
current_directory = os.getcwd()

# List all files in the current directory
all_files = os.listdir(current_directory)

# Find the first CSV file (assuming there is only one CSV file)
csv_files = [file for file in all_files if file.endswith('.csv')]

if not csv_files:
    print("No CSV files found in the current directory.")
else:
    # Take the first CSV file found
    csv_file_path = os.path.join(current_directory, csv_files[0])

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, parse_dates=['Date'])

    # Plot Impressions and Engagements
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Impressions'], label='Impressions', marker='o')
    plt.plot(df['Date'], df['Engagements'], label='Engagements', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('LinkedIn Impressions and Engagements Over Time')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

    # Seasonal decomposition
    decomposition_impressions = sm.tsa.seasonal_decompose(df['Impressions'], period=12)
    trend_impressions = decomposition_impressions.trend
    seasonal_impressions = decomposition_impressions.seasonal
    residual_impressions = decomposition_impressions.resid

    decomposition_engagements = sm.tsa.seasonal_decompose(df['Engagements'], period=12)
    trend_engagements = decomposition_engagements.trend
    seasonal_engagements = decomposition_engagements.seasonal
    residual_engagements = decomposition_engagements.resid

    # Plot seasonal decomposition
    plt.figure(figsize=(12, 8))

    plt.subplot(4, 1, 1)
    plt.plot(df['Date'], df['Impressions'], label='Original Impressions')
    plt.legend()

    plt.subplot(4, 1, 2)
    plt.plot(df['Date'], trend_impressions, label='Trend Impressions')
    plt.legend()

    plt.subplot(4, 1, 3)
    plt.plot(df['Date'], seasonal_impressions, label='Seasonal Impressions')
    plt.legend()

    plt.subplot(4, 1, 4)
    plt.plot(df['Date'], residual_impressions, label='Residual Impressions')
    plt.legend()

    plt.tight_layout()
    plt.show()

    # ARIMA model for Impressions
    model_impressions = sm.tsa.ARIMA(df['Impressions'], order=(1, 1, 1))
    results_impressions = model_impressions.fit()

    # Forecast next 365 days for Impressions
    forecast_steps = 365
    forecast_impressions = results_impressions.get_forecast(steps=forecast_steps)
    forecast_index = pd.date_range(df['Date'].max(), periods=forecast_steps + 1, freq='D')[1:]

    # Plotting for Impressions
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Impressions'], label='Observed Impressions', marker='o')
    plt.plot(forecast_index, forecast_impressions.predicted_mean, color='red', label='Forecasted Impressions', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('LinkedIn Impressions Forecast using ARIMA with Seasonal Decomposition')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
