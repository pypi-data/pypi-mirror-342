class FileHandler:
    @staticmethod
    def read_file(file_path, encoding='utf-8', fallback_encodings=['latin-1', 'utf-16', 'cp1252']):
        """Read text from a file with automatic encoding detection and fallback."""
        for enc in [encoding] + fallback_encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError(f"Could not decode {file_path} with any of the provided encodings")

    @staticmethod
    def write_file(file_path, content, encoding='utf-8', errors='replace'):
        """Write text to a file with specified encoding and error handling."""
        with open(file_path, 'w', encoding=encoding, errors=errors) as f:
            f.write(content)

# class FileHandler:
#     @staticmethod
#     def read_file(file_path):
#         """Read text from a file with UTF-8 encoding."""
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return f.read()

#     @staticmethod
#     def write_file(file_path, content):
#         """Write text to a file with UTF-8 encoding."""
#         with open(file_path, 'w', encoding='utf-8') as f:
#             f.write(content)