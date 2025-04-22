import os

def show_code(filename):
    file_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    if not os.path.exists(file_path):
        return f"File {filename} not found."

    with open(file_path, 'r') as f:
        content = f.read()

    print(content)  # shows the code in Jupyter output
    return content   # also returns content if needed
