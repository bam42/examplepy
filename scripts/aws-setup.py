import boto3
import os

os.environ['AWS_SECRET_ACCESS_KEY'] = 'xyz'
os.environ['AWS_ACCESS_KEY_ID'] = '123'

subscriptions = ['tester1']

sns_client = boto3.client('sns',
                            endpoint_url='http://localhost:4566',
                            region_name='us-east-1')

sqs_client = boto3.client('sqs',
                          endpoint_url='http://localhost:4566',
                          region_name='us-east-1')

queue_name = 'test-queue'

for subscription in subscriptions:
    queue_name = "{}-queue".format(subscription)
    response = sns_client.create_topic(Name="{}-topic".format(subscription))
    topic_arn = response['TopicArn']
    print(topic_arn)
    response = sqs_client.create_queue(QueueName=queue_name)
    queue_url = response['QueueUrl']
    response = sqs_client.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['QueueArn']
    )
    queue_arn = response['Attributes']['QueueArn']
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='sqs',
        Endpoint=queue_arn
    )

