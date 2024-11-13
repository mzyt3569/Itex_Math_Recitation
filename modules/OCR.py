import json
import os 
def OCR_image(img_name: str) -> dict:
    img_name = os.path.basename(img_name)
    
    with open('./result_final.json','r',encoding='utf-8') as f:
        entire_data = json.load(f)
    for question in entire_data:
        fn = str(question["File"])
        if img_name in fn:
            return question