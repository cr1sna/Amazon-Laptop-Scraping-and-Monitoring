import pandas as pd
import os
import json
import requests


def get_past_data():
    if os.path.exists('history.csv'):
        print('Found')
        df = pd.read_csv('history.csv')
    else:
        print('not Found')
        df = pd.DataFrame({'asin':[],'price':[]})
    return df

def save_data(df):
    df.to_csv('history.csv',index=False)


def send_notification(message):
    
    # send slack message 
    webhook_url = 'https://hooks.slack.com/services/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'
    slack_data = {'text':message}

    response = requests.post(
        webhook_url ,
        data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        print(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    else:
        print('Notification sent.')