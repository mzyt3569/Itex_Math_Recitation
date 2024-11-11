import openai
import base64
import re

def make_client(key: str):
    return openai.OpenAI(api_key=key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def find_index(latex_string,op_list):
    indices = []
    for op in op_list:
        matches = [m.span() for m in re.finditer(re.escape(op),latex_string)]
        indices.extend(matches)
    indices.sort(key=lambda x:(x[0],x[1]))
    return indices

def find_first(string: str, pattern_list: list[str], tail=False) -> int:
    for idx in range(len(pattern_list)):
        if tail: pattern = pattern_list[idx] + r'\s*$'
        else: pattern = r'^\s*' + pattern_list[idx]
        if re.search(pattern,string): return idx
    return -1