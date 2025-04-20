# import os
# import pkg_resources

# def get_file_path(filename):
#     """Get the path to a file within the package."""
#     return pkg_resources.resource_filename(__name__, f"{filename}")

# def save_text(filename, content):
#     """Save text content to a file."""
#     path = os.path.join(os.path.dirname(__file__), filename)
#     with open(path, 'w') as f:
#         f.write(content)
#     return f"Saved file: {filename}"

# def read_text(filename):
#     """Read text content from a file."""
#     try:
#         path = get_file_path(filename)
#         with open(path, 'r') as f:
#             return f.read()
#     except FileNotFoundError:
#         return f"{filename} not found."

# def list_files():
#     """List all .txt files in the package directory."""
#     package_files = pkg_resources.resource_listdir(__name__, "")
#     return [f for f in package_files if f.endswith('.txt')]

import os
import pkg_resources

def get_file_path(filename):
    """Get the path to a file within the package."""
    try:
        # Use pkg_resources to get the path of a file inside the package
        return pkg_resources.resource_filename(__name__, f"{filename}")
    except FileNotFoundError:
        return f"{filename} not found."

def save_text(filename, content):
    """Save text content to a file (locally, not inside the package)."""
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'w') as f:
        f.write(content)
    return f"Saved file: {filename}"

def read_text(filename):
    """Read text content from a file within the package."""
    try:
        # Access the file path within the installed package
        path = get_file_path(filename)
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"{filename} not found."

def list_files():
    """List all .txt files in the package directory."""
    # Using pkg_resources to list files in the package directory
    package_files = pkg_resources.resource_listdir(__name__, "")
    return [f for f in package_files if f.endswith('.txt')]
