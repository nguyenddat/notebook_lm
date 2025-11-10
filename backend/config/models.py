from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="AITeamVN/Vietnamese_Embedding_v2",
    model_kwargs={"device": "cpu", "trust_remote_code":True},
    encode_kwargs={"normalize_embeddings": True},
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")