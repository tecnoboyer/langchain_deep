import boto3
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage

# Initialize client
boto3_client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Proper configuration for Claude 2.1 (LangChain handles formatting internally)
chat_model = ChatBedrock(
    model_id="anthropic.claude-v2:1",
    client=boto3_client,
    model_kwargs={
        "temperature": 0.5,
        "top_p": 1,
        "max_tokens": 1000  # ✅ Correct key instead of `max_tokens_to_sample`
    }
)

# Standard LangChain message list (no need to manually format prompt)
messages = [HumanMessage(content="Write a welcome email for new hire John Doe")]
response = chat_model.invoke(messages)
print(response.content)
