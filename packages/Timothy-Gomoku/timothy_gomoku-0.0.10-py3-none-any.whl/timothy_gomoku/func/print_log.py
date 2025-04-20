from datetime import datetime

def print_log(log: str, log_path: str = None):
    """
    Print the log message with a timestamp.
    
    Args:
        log (str): The log message to print.
    """

    # Generate log
    log_content = ""
    current_time = datetime.now().isoformat()
    log_content = f"[{current_time}] {log}"

    # Print to console
    print(log_content)

    # Add to file if log_path is provided
    if log_path:
        with open(log_path, "a") as f:
            f.write(log_content + "\n")

__all__ = ["print_log"]