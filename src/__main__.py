from .corpusreader import CorpusReader


if __name__ == "__main__":
    try:
        root_dir: str = "vllm-0.10.1/"
        accepted_extensions: list[str] = [".py", ".md"]
        corpus_reader = CorpusReader(root_dir, accepted_extensions)
        file_paths = corpus_reader.search_accepted_files()
        i = 0
        print("\n//// SOME FILEPATHS ////")
        for i, file_path in enumerate(file_paths[:5]):
            print(f"({i + 1}) - {file_path}")
        print(f"Total paths found: {len(file_paths)}")
        first_file_content = corpus_reader.save_file_as_str(file_paths[0])
        print("\n//// FIRST FILE CONTENT ////")
        print(first_file_content)
    except Exception as e:
        print(f"An error occurred: {e}")
