import os
import argparse

from modules.OCR import OCR_image
from modules.translator import translate_latex
from modules.parser import parse_latex
from modules.merger import latex_merge_latex,final_merge_latex
from modules import utils

def image_to_text(input_dir: str, output_dir: str, file_name: str, is_debug: bool) -> str:
    input_file_path = os.path.join(input_dir,file_name)
    output_file_path_wo_ext,_ = os.path.splitext(os.path.join(output_dir,file_name))
    output_file_path = output_file_path_wo_ext + ".txt"

    extracted_json = OCR_image(input_file_path) # First, We conduct OCR and makes result to json file.
    parsed_latex,question,file_name = parse_latex(extracted_json,is_debug) # We parse inequality and fraction

    if parsed_latex:
        translated_latex = translate_latex(parsed_latex,is_debug) # We translate all of latex parts.
        latex_merged_latex = latex_merge_latex(translated_latex,is_debug) # We merge parts into original latex
        merged_question = final_merge_latex(file_name,question,latex_merged_latex,is_debug) # We merge latex into korean question
        return merged_question
    else:
        return question

def text_to_speech(output_dir: str, file_name: str, output_text: str, is_debug: bool) -> None:
    output_file_path_wo_ext,_ = os.path.splitext(os.path.join(output_dir,file_name))
    output_file_path = output_file_path_wo_ext + ".mp3" # get the output file

    client = utils.make_client("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")
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=output_text
    ) # we just use openai's text to speech model.
    response.write_to_file(output_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',type=str,default="./src/input",help="directory of input images") # input directory
    parser.add_argument('-o', '--output',type=str,default="./src/output",help="directory of output results") # output directory
    parser.add_argument('--debug', action='store_true',default=False) # use debug for check each step.
    parser.add_argument('--full',action='store_true',default=False) # if full is set, we make text to speech.

    args = parser.parse_args()

    input_dir,output_dir,is_debug,is_full = args.input,args.output,args.debug,args.full
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    input_list = os.listdir(input_dir)

    for file_name in input_list:
        output_text = image_to_text(input_dir,output_dir,file_name,is_debug) # file write is actually conducted here.

        if is_full: text_to_speech(output_dir,file_name,output_text,is_debug) # is full is set, we conduct text to speech steps.    