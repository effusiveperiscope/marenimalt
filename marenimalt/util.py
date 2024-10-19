def sanitize_filename(input_string: str, max_length: int = 200) -> str:
    # Define a set of invalid characters
    invalid_chars = r'\/:*?"<>|'
    reserved_names = {
        "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4",
        "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3",
        "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }
    
    # Replace invalid characters with an underscore
    sanitized = re.sub(f"[{re.escape(invalid_chars)}]", "_", input_string)
    
    # Trim leading and trailing spaces or dots
    sanitized = sanitized.strip().strip(".")
    
    # Check if the sanitized name is a reserved name and alter it if necessary
    if sanitized.upper() in reserved_names:
        sanitized = f"{sanitized}_file"
    
    # Ensure the length of the filename does not exceed the specified max length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].strip().strip(".")
    
    # If the resulting filename is empty, use a default name
    return sanitized or "default_filename"

def wrap_text(text : str, width: int = 50) -> str:
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + len(current_line) <= width:
            current_line.append(word)
            current_length += len(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(" ".join(current_line))
    
    return "\n".join(lines)