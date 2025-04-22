from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    api_key=os.getenv("BIANXIE")
    api_base = os.getenv("BIANXIE_BASE")

    llm = OpenAI(
        model="gpt-4o",
        api_key=api_key,
        api_base=api_base,
        temperature=0.1,
    )
    embed_model = OpenAIEmbedding(api_key=api_key,
                                api_base =api_base)
    Settings.embed_model = embed_model
    Settings.llm = llm
    Settings.text_splitter = SentenceSplitter(chunk_size=4096)
    return llm


if __name__ == "__main__":
    llm = get_llm()
    print(llm.complete('hello'))

    