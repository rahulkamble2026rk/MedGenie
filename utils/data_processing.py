
import pandas as pd
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

def load_and_process_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except pd.errors.ParserError:
        df = pd.read_csv(file_path, sep='\t', encoding='utf-8', on_bad_lines='skip')

    texts = df['description'].tolist() if 'description' in df.columns else df.iloc[:, 0].tolist()
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = [Document(page_content=text) for text in texts if text]  # Filter out None/empty
    documents = text_splitter.split_documents(documents)
    documents = documents[:100]  # Limit for testing
    return documents