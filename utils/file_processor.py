import os
from pathlib import Path
from .text_splitter import TextSplitter


class FileProcessor:
    def __init__(self):
        self.text_splitter = TextSplitter()

    def process_markdown_files(self, directory_path):
        md_files = list(Path(directory_path).glob("**/*.md"))

        all_chunks = []
        all_metadatas = []

        for file_path in md_files:
            if file_path.is_file():
                chunks, metadatas = self._process_single_file(file_path)
                all_chunks.extend(chunks)
                all_metadatas.extend(metadatas)

        return all_chunks, all_metadatas

    def _process_single_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            chunks = self.text_splitter.split_text(content)

            metadatas = [{
                "source": str(file_path),
                "chunk_index": i,
                "total_chunks": len(chunks)
            } for i in range(len(chunks))]

            return chunks, metadatas

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return [], []
