from src.basemodels import MinimalSource
from src.config import CHUNK_OVERLAP


class ChunkerError(Exception):
    pass


class BaseChunker:
    def __init__(self, max_chunk_size: int) -> None:
        """Sets the maximum allowed chunk size in characters."""
        self.max_chunk_size = max_chunk_size

    def chunk(self, file_path: str, content: str) -> list[MinimalSource]:
        """Splits content into chunks. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")


class TextChunker(BaseChunker):
    def chunk(
            self, file_path: str,
            content: str
            ) -> list[MinimalSource]:
        if len(content) <= self.max_chunk_size:
            # devolver el chunk.
            return
    


@staticmethod
def pre_chunk(
    content: str,
    separator: str,
    offset: int = 0,
    end: int | None = None,
) -> list[tuple[int, int]]:
    if end is None or end > len(content):
        end = len(content)

    positions: list[tuple[int, int]] = []

    if separator == "":
        raise ChunkerError("Chunker separator is empty")

    while offset < end:
        sep_pos = content.find(separator, offset, end)

        if sep_pos >= 0:
            end_part = sep_pos + len(separator)
            positions.append((offset, end_part))
            offset = end_part
        else:
            positions.append((offset, end))
            break

    return positions



def build_max_chunk_size_ranges(
    positions: list[tuple[int, int]],
    max_chunk_size: int  # este metodo no es estatico esta variable sería self.max_chunk_size
) -> list[tuple[int, int]]:
    if not positions:
        return []

    max_chunk_size_ranges: list[tuple[int, int]] = []
    a, b = positions[0]

    for x, y in positions[1:]:
        if y - a <= max_chunk_size:
            b = y
        else:
            max_chunk_size_ranges.append((a, b))
            a, b = x, y

    max_chunk_size_ranges.append((a, b))
    return max_chunk_size_ranges





texto = "holitas bolitas . si seño . si"
lista_ret = pre_chunk(texto, "", 0)
print(lista_ret)

