import os
import math


class InvalidFileType(ValueError):
    """Custom exception for invalid file types."""
    pass


class HTTPError(Exception):
    """Base class for HTTP errors."""
    pass


class NotFoundError(HTTPError):
    """Exception raised for 404 Not Found errors."""
    def __init__(self, message="Resource not found"):
        super().__init__(f"404 Not Found: {message}")


class InternalServerError(HTTPError):
    """Exception raised for 500 Internal Server errors."""
    def __init__(self, message="Internal server error"):
        super().__init__(f"500 Internal Server Error: {message}")


class TimeoutError(HTTPError):
    """Exception raised when a request times out."""
    def __init__(self, message="The request timed out"):
        super().__init__(f"Timeout Error: {message}")


# Define common video and photo file extensions
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm']
PHOTO_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.heif']


# A default target chunk size when chunking is required/chosen (e.g., 10 MiB).
DEFAULT_CHUNK_SIZE_BYTES = 10 * 1024 * 1024  # 10 MiB
MAX_CHUNK_SIZE_BYTES = 60 * 1024 * 1024  # 60 MiB
# Maximum number of chunks allowed by the API.
MAX_CHUNKS_COUNT = 1000


def get_file(file_path):
    """
    Reads a file, checks its type and size, and prepares it for chunking.

    Args:
        file_path (str): The path to the file.

    Returns:
        dict: A dictionary containing file information, including chunks.

    Raises:
        FileNotFoundError: If the file does not exist.
        InvalidFileType: If the file is not a recognized video or photo type.
        Exception: For other errors during file processing.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: File not found at {file_path}")

    _, file_extension = os.path.splitext(file_path)
    file_extension_lower = file_extension.lower()

    if file_extension_lower not in VIDEO_EXTENSIONS and file_extension_lower not in PHOTO_EXTENSIONS:
        raise InvalidFileType(f"Error: File '{os.path.basename(file_path)}' is not a recognized video or photo type.")

    try:
        file_size_bytes = os.path.getsize(file_path)
        if file_size_bytes < 0:
            raise ValueError("File size cannot be negative.")

        calculated_chunk_size_bytes = 0
        total_chunks = 0

        if file_size_bytes == 0:
            calculated_chunk_size_bytes = 0
            total_chunks = 0
        elif file_size_bytes < DEFAULT_CHUNK_SIZE_BYTES:
            calculated_chunk_size_bytes = file_size_bytes
            total_chunks = 1
            chunk_size = file_size_bytes
        else:
            target_chunk_size = DEFAULT_CHUNK_SIZE_BYTES
            provisional_chunks = math.ceil(file_size_bytes / target_chunk_size)

            if provisional_chunks <= MAX_CHUNKS_COUNT:
                calculated_chunk_size_bytes = target_chunk_size
                if (file_size_bytes < MAX_CHUNK_SIZE_BYTES):
                    total_chunks = 1
                    chunk_size = file_size_bytes
                else:
                    total_chunks = min(provisional_chunks, MAX_CHUNKS_COUNT)
                    chunk_size = DEFAULT_CHUNK_SIZE_BYTES
            else:
                required_chunk_size = math.ceil(file_size_bytes / MAX_CHUNKS_COUNT)
                calculated_chunk_size_bytes = max(required_chunk_size, DEFAULT_CHUNK_SIZE_BYTES)
                total_chunks = min(math.ceil(file_size_bytes / calculated_chunk_size_bytes), MAX_CHUNKS_COUNT)
                chunk_size = DEFAULT_CHUNK_SIZE_BYTES
            

        if file_size_bytes > 0 and calculated_chunk_size_bytes <= 0:
            raise ValueError("Calculated chunk size is invalid (must be > 0 for non-empty files).")

        def convert_size(size_bytes):
            """Converts bytes to a human-readable format (e.g., KB, MB)."""
            if size_bytes <= 0:
                return "0 B"
            size_name = ("B", "KB", "MB", "GB", "TB")
            i = int(math.floor(math.log(size_bytes, 1024)))
            i = min(i, len(size_name) - 1)
            p = math.pow(1024, i)
            s = round(size_bytes / p, 2)
            return f"{s} {size_name[i]}"

        file_size_readable = convert_size(file_size_bytes)
        chunk_size_readable = convert_size(calculated_chunk_size_bytes)

        # Add chunk range info
        chunks_info = []
        chunk_count = total_chunks - 1 if total_chunks > 1 else total_chunks

        with open(file_path, "rb") as f:
            for i in range(chunk_count):
                start = i * chunk_size
                if (i + 1 == chunk_count):
                    end = file_size_bytes - 1
                else:
                    end = min(start + chunk_size, file_size_bytes) - 1
                chunk_data = f.read(end - start + 1)
                chunks_info.append({'start': start, 'end': end, 'content_range': f"bytes {start}-{end}/{file_size_bytes}", "chunk_data": chunk_data})

        file_info = {
            'file_size': file_size_bytes,
            'chunk_size': chunk_size,
            'total_chunks': chunk_count,
            'file_size_bytes': file_size_bytes,
            'file_size_readable': file_size_readable,
            'chunk_size_bytes': calculated_chunk_size_bytes,
            'chunk_size_readable': chunk_size_readable,
            'file_path': file_path,
            'file_data': chunks_info,
        }
        return file_info

    except (FileNotFoundError, InvalidFileType, ValueError) as e:
        raise Exception(f"Error: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while processing the file: {e}")


def handle_response(response):
    """
    Handles the HTTP response from the TikTok API.

    Args:
        response (requests.Response): The HTTP response object.

    Returns:
        dict: The JSON response from the API if successful.

    Raises:
        NotFoundError: If the response indicates a 404 error.
        InternalServerError: If the response indicates a 500 error.
        TimeoutError: If the request times out (status code 408).
        HTTPError: For other HTTP errors.
    """
    # Check for HTTP errors based on response status code
    if hasattr(response, 'status_code'):
        if response.status_code == 404:
            raise NotFoundError("The requested resource was not found.")
        elif response.status_code == 500:
            raise InternalServerError("The server encountered an error.")
        elif response.status_code == 408:  # Example for timeout
            raise TimeoutError("The request timed out.")
        elif response.status_code != 200:
            error_message = f"HTTP Error: {response.status_code}"
            if hasattr(response, 'text'):
                error_message += f" - {response.text}"
            raise HTTPError(error_message)
        else:
            # Handle successful response
            if hasattr(response, 'raise_for_status'):
                response.raise_for_status()
            if hasattr(response, 'json'):
                return response.json()
            else:
                return response.text  # Or handle other response types
    else:
        raise HTTPError("Invalid response object provided.")