from base64 import b64encode

def get_base64(bin_file: str) -> str:
    """
    Reads a binary file and returns its base64 encoded string.

    Args:
        bin_file (str): Path to the binary file.

    Returns:
        str: Base64 encoded string of the file content.
    """
    with open(bin_file, "rb") as f:
        data = f.read()
    return b64encode(data).decode()