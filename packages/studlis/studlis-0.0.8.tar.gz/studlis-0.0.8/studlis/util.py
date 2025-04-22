#import regex as re
import re

def ensure_valid_name(text):
    # Only allow letters, numbers ._ and space, and replace all other characters with _
    name=re.sub(r"[^\w\s. _]", "_", text.strip(), flags=re.UNICODE)
    if len(name)<2 or len(name)>128:
        return "Resource name must be between 2 and 128 characters"
    return name

def path_valid(path):
    return re.match(r'^\/[\w\s. _/]{5,265}$', path) is not None