import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

def mysql_data():
    try:
        connection = mysql.connector.connect(
            host='bw59sqe4chjztk4k1mri-mysql.services.clever-cloud.com',
            user='uemwk5cbfvpokdi0',
            password='qAiIhXVCUKdob2tTzO9F',
            database='bw59sqe4chjztk4k1mri'
        )
        if connection.is_connected():
            return connection
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def impress_data(connection):
    query = f"SELECT Date, SUM(Impressions) AS Total_Impressions, SUM(Engagements) AS Total_Engagements FROM posts WHERE Date >= DATE_SUB(NOW(), INTERVAL 365 DAY) GROUP BY Date"
    try:
        data = pd.read_sql_query(query, connection)
        return data
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def visualize(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data['Total_Impressions'], label='Impressions', marker='o')
    plt.plot(data['Date'], data['Total_Engagements'], label='Engagements', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('LinkedIn Impressions and Engagements Over Time')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def linear_regression_forecast(data, target_column):
    # Assuming 'Date' is a datetime type, if not, convert it using pd.to_datetime
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.set_index('Date')

    # Create a feature for the number of days
    data['Days'] = (data.index - data.index.min()).days

    # Split the data into training and testing sets
    train, test = train_test_split(data, test_size=0.2, shuffle=False)

    # Train a linear regression model
    model = LinearRegression()
    model.fit(train[['Days']], train[target_column])

    # Predict for future dates
    future_days = np.arange(data['Days'].max() + 1, data['Days'].max() + 366)
    future_dates = pd.to_datetime(data.index.min()) + pd.to_timedelta(future_days, unit='D')
    future_data = pd.DataFrame({'Days': future_days, 'Date': future_dates})
    future_data = future_data.set_index('Date')

    # Make predictions
    future_data[target_column] = model.predict(future_data[['Days']])

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data[target_column], label='Observed ' + target_column, marker='o')
    plt.plot(future_data.index, future_data[target_column], color='red', label='Forecasted ' + target_column, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title(f'LinkedIn {target_column} Forecast using Linear Regression')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def main():
    connection = mysql_data()
    if connection:
        data = impress_data(connection)
        if data is not None:
            visualize(data)
            linear_regression_forecast(data, 'Total_Impressions')
            linear_regression_forecast(data, 'Total_Engagements')
        connection.close()

if __name__ == "__main__":
    main()