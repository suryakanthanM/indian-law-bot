from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

def extract_and_chunk_pdf(file_path: str):
    """Reads a PDF and splits it into smaller text chunks."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    # Split the text into chunks of 1000 characters
    # with a 200 character overlap so we don't cut a sentence in half
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    chunks = text_splitter.split_text(text)
    return chunks