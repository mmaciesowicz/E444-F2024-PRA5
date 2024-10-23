'''
Attribution:
ChatGPT. Accessed 10/23/2024 with prompt: how can i create a pytest testcase testing REST server (AWS Elastic Beanstalk server by providing 100 api calls each for 4 test cases. Record the timestamps in a csv file and create a boxplot to visualize the performance results and calculate average performance. Used as a starting point for the test cases.
'''

import pytest
from application import application, load_model
import requests
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the model and vectorizer as they are needed for mock tests
loaded_model, vectorizer = load_model()

# AWS Elastic Beanstalk URL for the REST API
AWS_BASE_URL = "http://pra5-env.eba-eky39tyb.us-east-1.elasticbeanstalk.com/"

@pytest.fixture
def client():
    with application.test_client() as client:
        yield client

# -------------- Local Flask App Tests ----------------

def test_real_news(client):
    # Example of real news input
    real_news_1 = "This is real news"
    response = client.post('/', data={'sentence': real_news_1})
    assert response.status_code == 200
    assert b"Prediction" in response.data
    assert b"REAL" in response.data

    real_news_2 = "Summer is hot."
    response = client.post('/', data={'sentence': real_news_2})
    assert response.status_code == 200
    assert b"Prediction" in response.data
    assert b"REAL" in response.data

def test_fake_news(client):
    # Example of fake news input
    fake_news_1 = "This is fake news"
    response = client.post('/', data={'sentence': fake_news_1})
    assert response.status_code == 200
    assert b"Prediction" in response.data
    assert b"FAKE" in response.data

    fake_news_2 = "Summer is cold"
    response = client.post('/', data={'sentence': fake_news_2})
    assert response.status_code == 200
    assert b"Prediction" in response.data
    assert b"FAKE" in response.data

# -------------- AWS Elastic Beanstalk Performance Tests ----------------

# Helper function to send POST request to AWS Elastic Beanstalk and return response time
def make_aws_api_call(sentence):
    start_time = time.time()
    response = requests.post(AWS_BASE_URL, data={'sentence': sentence})
    end_time = time.time()
    
    # Check if the response is successful
    assert response.status_code == 200
    assert "Prediction" in response.text
    return end_time - start_time  # Return the duration of the request

# Parametrize to test real and fake news for performance
@pytest.mark.parametrize("test_case", [
    ("REAL", ["This is real news", "Summer is hot"]),
    ("FAKE", ["This is fake news", "Summer is cold"]),
])
def test_aws_performance(test_case):
    label, examples = test_case
    duration_averages = []

    # Perform 100 API calls
    for example in examples:
        results = []
        print(example)
        for i in range(100):
            duration = make_aws_api_call(example)
            results.append(duration)
        promptNoSpace = example.replace(" ", "_")
        # Write results to CSV file
        csv_filename = f'performance_results_{label}_{promptNoSpace}.csv'
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Request_Number', 'Duration'])  # CSV header
            for i, duration in enumerate(results):
                writer.writerow([i+1, duration])

        # Load CSV data into Pandas DataFrame
        df = pd.read_csv(csv_filename)

        # Generate boxplot
        plt.boxplot(df['Duration'])
        plt.title(f'{promptNoSpace} API Request Durations')
        plt.ylabel('Duration (seconds)')
        plt.savefig(f'{promptNoSpace}_boxplot.png')  # Save boxplot as an image
        plt.show()

        # Calculate average performance and print
        avg_duration = df['Duration'].mean()
        duration_averages.append(avg_duration)
        print(f"Average duration for prompt: {example} ({label} news): {avg_duration} seconds")
    
    total_average_duration = np.mean(avg_duration)
    print(f"Total average duration for the system: {total_average_duration} seconds")
