import boto3

client = boto3.client('ce')  # Cost Explorer

response = client.get_cost_and_usage(
    TimePeriod={
        'Start': '2025-08-01',
        'End': '2025-08-05'
    },
    Granularity='DAILY',
    Metrics=['UnblendedCost'],
    Filter={
        "Dimensions": {
            "Key": "SERVICE",
            "Values": ["Amazon Bedrock"]
        }
    }
)

print(response)
