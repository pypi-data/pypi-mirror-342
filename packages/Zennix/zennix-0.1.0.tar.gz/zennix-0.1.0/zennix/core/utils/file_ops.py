import os
import json
from typing import Union
from datetime import datetime
import dataclasses

def save_file(
    content: Union[str, dict],
    output_path: str,
    filename: str = "output.txt",
    timestamp: bool = True,
    prettify_json: bool = True
):
    """
    Saves content (str, dict, or dataclass) to a file with optional timestamp in filename.
    
    Args:
        content: The content to save. Can be str, dict, or dataclass.
        output_path: Target folder path.
        filename: Base filename.
        timestamp: Whether to append timestamp to filename.
        prettify_json: If content is dict and ext is .json, prettify it.
    """
    # Automatically convert dataclass to dict
    if dataclasses.is_dataclass(content):
        content = dataclasses.asdict(content)

    name, ext = os.path.splitext(filename)

    # Add timestamp to filename if needed
    if timestamp:
        time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{time_str}{ext}"

    full_path = os.path.join(output_path, filename)
    os.makedirs(output_path, exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        if isinstance(content, dict) and ext == ".json":
            json.dump(content, f, indent=4 if prettify_json else None)
        else:
            f.write(content)

    print(f"✅ Saved: {full_path}")
    return full_path
