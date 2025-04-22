def extract_first_traceback(traceback_text):
    """
    Extracts and returns the first traceback block from a traceback string.

    Parameters:
        traceback_text (str): The full traceback string.

    Returns:
        str: The first traceback block, including the error message.
    """
    lines = traceback_text.splitlines()
    first_tb_lines = []
    in_first_tb = False

    for line in lines:
        if line.startswith("Traceback (most recent call last):"):
            if not in_first_tb:
                in_first_tb = True
                first_tb_lines.append(line)
            elif in_first_tb:
                # Encountered another traceback start, stop at the first one
                break
        elif in_first_tb:
            # Stop if we reach the "During handling..." line
            if (
                "During handling of the above exception, another exception occurred:"
                in line
            ):
                break
            first_tb_lines.append(line)

    return "\n".join(first_tb_lines)
