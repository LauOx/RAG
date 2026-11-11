import os


class CorpusReaderError(Exception):
    """Custom error for CorpusReader"""


class CorpusReader:
    """Busca en la carpeta path y devuelve las rutas
    de los archivos válidos para buscar la respuesta
    recibe el root_dir de la carpeta y la lista de los tipos
    de archivos aceptados"""

    def __init__(self, root_dir: str, file_extensions: list[str]) -> None:
        """Inicializa el CorpusReader con el path del folder"""
        self.root_dir: str = root_dir
        self.accepted_extensions: tuple[str, ...] = tuple(file_extensions)

    def search_accepted_files(self) -> list[str]:
        """Devuelve la lista de los paths de los archivos
        aceptados para la busqueda"""
        try:
            file_paths: list[str] = [
                os.path.join(dirpath, filename)
                for dirpath, _, filenames in os.walk(self.root_dir)
                for filename in filenames
                if filename.endswith(self.accepted_extensions)
            ]
        except Exception as e:
            raise CorpusReaderError("An error occurred while exploring the root_dir "
                  f"'{self.root_dir}': {e}")
        if len(file_paths) == 0:
            raise CorpusReaderError(
                f"No files with extension {self.accepted_extensions} "
                f"were found in root_dir '{self.root_dir}'")
        return sorted(file_paths)

    @staticmethod
    def save_file_as_str(file_path: str) -> str:
        """Guarda el texto del archivo como str"""
        try: 
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (OSError, UnicodeDecodeError) as e:
            raise CorpusReaderError("An error occurred while trying to read "
                        f"the file '{file_path}'") from e
        return content


# root_dir debería estar comprobado que no es vacío desde
# antes de inicializar el CorpusReader
