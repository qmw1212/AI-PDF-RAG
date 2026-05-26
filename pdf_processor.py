"""PDF文本提取和分块模块"""
from typing import List
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PDFProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def extract_text(self, pdf_file) -> str:
        """从PDF文件中提取文本"""
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    def split_text(self, text: str) -> List[str]:
        """将文本分割成块"""
        chunks = self.text_splitter.split_text(text)
        return chunks

    def process_pdf(self, pdf_file) -> List[str]:
        """处理PDF：提取文本并分块"""
        text = self.extract_text(pdf_file)
        chunks = self.split_text(text)
        return chunks
