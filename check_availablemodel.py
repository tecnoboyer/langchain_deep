# Test your credentials
import boto3

try:
    bedrock = boto3.client('bedrock', region_name='us-east-1')
    models = bedrock.list_foundation_models()
    print("Available models:")
    for model in models['modelSummaries']:
        print(f"- {model['modelId']}")
except Exception as e:
    print(f"Credential error: {e}")