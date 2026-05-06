import os
import hashlib

class Uploader:
    """
    Handles file validation and hashing before processing.
    """
    
    ALLOWED_EXTENSIONS = {'.log', '.txt', '.csv', '.json', '.access'}
    
    @staticmethod
    def is_valid_file(file_path: str) -> bool:
        _, ext = os.path.splitext(file_path)
        return ext.lower() in Uploader.ALLOWED_EXTENSIONS

    @staticmethod
    def calculate_hash(file_path: str, algorithm: str = 'sha256') -> str:
        """
        Calculates SHA-256 hash for forensic integrity.
        """
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(65536)
                    if not data:
                        break
                    sha256.update(data)
            return sha256.hexdigest()
        except IOError:
            return ""
