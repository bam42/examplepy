import pytest
import boto3
import json
import os
import psycopg2
import time
from faker import Faker

os.environ['AWS_SECRET_ACCESS_KEY'] = 'xyz'
os.environ['AWS_ACCESS_KEY_ID'] = '123'

fake = Faker()
db_conn = psycopg2.connect(
    database="example",
    user='example',
    password='example_pwd',
    host="localhost",
    port=5432
)
cur = db_conn.cursor()

sns = boto3.client('sns', endpoint_url='http://localhost:4566', region_name='us-east-1')
topic_arn = 'arn:aws:sns:us-east-1:000000000000:tester1-topic'

def send_sns_message(message):
    response = sns.publish(
        TopicArn=topic_arn,
        MessageAttributes={
            fake.word(): {
                'DataType': 'String',
                'StringValue': fake.sentence()
            },
            fake.word(): {
                'DataType': 'String',
                'StringValue': fake.sentence()
            },
        },
        Message=json.dumps({
            'default': json.dumps({
                'message': message
            }),
        }),
        MessageStructure='json',
        Subject=fake.name()
    )

def find_message_in_db(message):
    cur.execute("SELECT * FROM example.records WHERE message = %s", (message,))
    return cur.fetchall()

def wait_for_expect(condition_func, timeout=10, interval=0.5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(interval)
    return False

def test_verify_sns_message_written_to_db():
    expected_message = fake.sentence()
    send_sns_message(expected_message)

    assert wait_for_expect(lambda: len(find_message_in_db(expected_message)) == 1)
