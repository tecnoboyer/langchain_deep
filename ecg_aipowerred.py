import boto3
from langchain_aws import ChatBedrock
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain

# 🔁 Shared boto3 client (single point of credentials + region config)
boto3_client = boto3.client('bedrock-runtime', region_name='us-east-1')

# 🧠 LLM: Claude v2.1 via ChatBedrock
def config_llm(client):
    model_kwargs = {
        "temperature": 0.5,
        "top_p": 1,
        "max_tokens": 512
    }

    llm = ChatBedrock(
        model_id="anthropic.claude-v1",
        client=client,
        model_kwargs=model_kwargs
    )
    return llm

# 📚 Vectorstore setup from PDF
def config_vector_db(filename, client):
    bedrock_embeddings = BedrockEmbeddings(client=client)
    loader = PyPDFLoader(filename)
    pages = loader.load_and_split()
    vectorstore = FAISS.from_documents(pages, bedrock_embeddings)
    return vectorstore

# 🔍 Search vectorstore
def vector_search(query):
    docs = vectorstore_faiss.similarity_search_with_score(query)
    info = ""
    for doc, score in docs:
        info += doc.page_content + "\n"
    return info

# ✅ Initialize once
llm = config_llm(boto3_client)
vectorstore_faiss = config_vector_db("social-media-training.pdf", boto3_client)

# 💬 Claude-style prompt
my_template = """
Human:
You are a conversational assistant designed to help answer questions from an employee.
You should reply to the human's question using the information provided below. Include all relevant information but keep your answers short. Only answer the question. Do not say things like "according to the training or handbook or according to the information provided...".

<Information>
{info}
</Information>

{input}

Assistant:
"""

# 🧱 Prompt template
prompt_template = PromptTemplate(
    input_variables=['input', 'info'],
    template=my_template
)

# 🔗 Chain setup
question_chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    output_key="answer"
)

# 🔄 Interactive loop
while True:
    question = input("\nAsk a question about the social media training manual:\n")
    info = vector_search(question)
    output = question_chain.invoke({'input': question, 'info': info})
    print("\nAnswer:\n", output['answer'])
