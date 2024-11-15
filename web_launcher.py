import gradio as gr
import base64
from io import BytesIO
from PIL import Image
import openai
import json
from modules.OCR import OCR_image
from modules.parser import parse_latex
from modules.translator import translate_latex
from modules.merger import latex_merge_latex, final_merge_latex

def process_image(image_path):
    print(image_path)
    o_r = OCR_image(image_path)
    p_r,question,file_name = parse_latex(o_r)
    t_r = translate_latex(p_r,"",False)
    m_r = latex_merge_latex(t_r)
    f_r = final_merge_latex(file_name,question,m_r)

    def to_json(json_d: dict) -> str:
        return json.dumps(json_d,indent=4,ensure_ascii=False)
    
    return f_r,to_json(o_r),to_json(p_r),to_json(t_r),to_json(m_r)


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="filepath")
            submit_button = gr.Button("Submit")
        with gr.Tab("Main Outputs"):
            main_output1 = gr.Textbox(label="Summarized Text",lines=20)
        with gr.Tab("OCR"):
            OCR_result = gr.Textbox(label="Result of OCR image",lines=20)
        with gr.Tab("Parsed"):
            Parsed_result = gr.Textbox(label="Result of parse Inequality & Fraction",lines=20)
        with gr.Tab("Translate"):
            Translated_result = gr.Textbox(label="Result of translate each latex",lines=20)
        with gr.Tab("Merged"):
            Merged_result = gr.Textbox(label="Result of re-locate latex",lines=20)

    submit_button.click(
        fn=process_image,
        inputs=image_input,
        outputs=[main_output1,OCR_result,Parsed_result,Translated_result,Merged_result]
    )

demo.launch()