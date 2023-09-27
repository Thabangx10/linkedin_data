import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


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
    plt.plot(data['Date'], data['Impressions'], label='Impressions', marker='o')
    plt.plot(data['Date'], data['Engagements'], label='Engagements', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('LinkedIn Impressions and Engagements Over Time')
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
        connection.close()

if __name__ == "__main__":
    main()

