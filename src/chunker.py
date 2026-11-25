from src.basemodels import MinimalSource, Chunk


SEPARATORS: list[str] = ["\n#", "\n\n", "\n", "```", ". ", ", ", " "] # esto puede ser un atributo mejor, o ke


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
        content_len = len(self.content)
        if content_len <= self.max_chunk_size:
            return [(0, content_len)]
        if self.content == "":
            return []
        ranges: list[tuple[int, int]] = self.split_recursively(
            (0, content_len), SEPARATORS
            )
        merged: list[tuple[int, int]] = self.merge_small_ranges(ranges)
        return [Chunk(file_path, a, b, content[a:b]) for (a, b) in merged]

    def split_recursively(
            self,
            zone: tuple[int, int],
            separators: list[str]
            ) -> list[tuple[int, int]]:
        start, end = zone
        if end - start <= self.max_chunk_size:
            return [zone]
        if separators == []:
            return self.hard_split(start, end)
        parts: list[int, int] = self.split_by_separator(
            self.content, separators[0], start, end
            )
        result = []
        for (a, b) in parts:
            if b - a <= self.max_chunk_size:
                result.append((a, b))
            else:
                result.extend(
                    self.split_recursively(self.content, (a, b), separators[1:])
                    )
        return result

    def hard_split(self, start: int, end: int) -> list[tuple[int, int]]:
        ranges: list[tuple[int, int]] = []
        while start < end:
            stop = min(start + self.max_chunk_size, end)
            ranges.append(start, stop)
            start = stop
        return ranges

    def split_by_separator( # Falta organizar que end part +1
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

    def merge_small_ranges(
            self,
            positions: list[tuple[int, int]],
            ) -> list[tuple[int, int]]:
        if not positions:
            return []

        small_ranges: list[tuple[int, int]] = []
        a, b = positions[0]

        for x, y in positions[1:]:
            if y - a <= self.max_chunk_size:
                b = y
            else:
                small_ranges.append((a, b))
                a, b = x, y

        small_ranges.append((a, b))
        return small_ranges





    texto = "holitas bolitas . si seño . si"
    lista_ret = pre_chunk(texto, "", 0)
    print(lista_ret)

