import os
from llama_parse import LlamaParse
from dotenv import load_dotenv

load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")


def extract_raw_markdown(file_path: str) -> str:
    parser = LlamaParse(
        api_key=LLAMA_API_KEY,
        result_type="markdown",
        premium_mode=True,
        continuous_mode=True,
        verbose=False
    )

    documents = parser.load_data(file_path)
    return "\n".join(doc.text for doc in documents)
