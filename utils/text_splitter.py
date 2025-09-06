import re
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


class TextSplitter:
    def __init__(self):
        self.chunk_size = CHUNK_SIZE
        self.chunk_overlap = CHUNK_OVERLAP

    def split_text(self, text):
        sections = re.split(r'(?m)^(#+ .+)$', text)

        chunks = []
        current_chunk = []
        current_length = 0

        for i, section in enumerate(sections):
            if not section.strip():
                continue

            if re.match(r'^#+ .+$', section) and i > 0:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    overlap_start = max(0, len(current_chunk) - 2)
                    current_chunk = current_chunk[overlap_start:]
                    current_length = sum(len(s) for s in current_chunk) + len(current_chunk) - 1

                current_chunk.append(section)
                current_length += len(section)
            else:
                sentences = re.split(r'(?<=[.!?])\s+', section)

                for sentence in sentences:
                    sentence_length = len(sentence)

                    if current_length + sentence_length > self.chunk_size and current_chunk:
                        chunks.append(" ".join(current_chunk))
                        overlap_start = max(0, len(current_chunk) - 3)
                        current_chunk = current_chunk[overlap_start:]
                        current_length = sum(len(s) for s in current_chunk) + len(current_chunk) - 1

                    current_chunk.append(sentence)
                    current_length += sentence_length + 1

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks