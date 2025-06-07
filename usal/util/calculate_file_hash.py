import hashlib


async def calculate_file_hash(file_path: str) -> str:
    hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash.update(chunk)
        return hash.hexdigest()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: Cannot read file: {file_path}")
    except IsADirectoryError:
        raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}") from e
