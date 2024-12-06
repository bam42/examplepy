import boto3
import json
import psycopg2
import time
import signal
import sys
import os


def main():
    db_conn = psycopg2.connect(
        database="example",
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        host=os.environ['DB_HOST'],
        port=5432
    )
    cur = db_conn.cursor()

    sqs = boto3.resource('sqs', endpoint_url=os.environ['AWS_ENDPOINT'], region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName='tester1-queue')

    while True:
        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20  # Use long polling
        )

        for message in messages:
            print(f"Received message: {message}")

            message.delete()

            bodyMessage = json.loads(json.loads(message.body)['Message'])
            print(bodyMessage)

            cur.execute("INSERT INTO example.records (message) VALUES (%s)", (bodyMessage['message'],))
            db_conn.commit()

def interrupt_handler(signum, frame, ask=True):
    print(f'Handling signal {signum} ({signal.Signals(signum).name}).')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, interrupt_handler)

    main()
