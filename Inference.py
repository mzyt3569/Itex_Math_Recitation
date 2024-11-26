import os
import argparse
import csv
import json
from tqdm import tqdm 

from modules.OCR import OCR_image
from modules.translator import translate_latex
from modules.parser import parse_latex
from modules.merger import latex_merge_latex,final_merge_latex
from modules import utils

def image_to_text(
        input_dir: str,
        output_dir: str,
        file_name: str,
        is_debug: bool,
        writer,
        db_dir: str,
        use_rag: bool
    ) -> str:

    input_file_path = os.path.join(input_dir,file_name)
    output_file_path_wo_ext,_ = os.path.splitext(os.path.join(output_dir,file_name))
    output_file_path = output_file_path_wo_ext + ".txt"

    extracted_json = OCR_image(input_file_path) # First, We conduct OCR and makes result to json file.
    parsed_latex,question,file_name = parse_latex(extracted_json) # We parse inequality and fraction

    # if there's no question. we will consider it as error.
    if question is None:
        if is_debug: writer.writerow([extracted_json,parsed_latex])
        with open(output_file_path,"w",encoding="utf-8") as fw: fw.write("Error while process")
        return ""

    if parsed_latex:
        translated_latex = translate_latex(parsed_latex,db_dir,use_rag) # We translate all of latex parts.

        latex_merged_latex = latex_merge_latex(translated_latex) # We merge parts into original latex

        merged_question = final_merge_latex(file_name,question,latex_merged_latex) # We merge latex into korean question

        output = merged_question

        if is_debug: writer.writerow([
            file_name,
            question,
            json.dumps(parsed_latex,ensure_ascii=False,indent=4),
            json.dumps(translated_latex,ensure_ascii=False,indent=4),
            json.dumps(latex_merged_latex,ensure_ascii=False,indent=4),
            merged_question])        
    else: 
        output = question
        if is_debug: writer.writerow([file_name,question])

    with open(output_file_path,"w",encoding="utf-8") as fw: fw.write(output)
    return output

def text_to_speech(output_dir: str, file_name: str, output_text: str) -> None:
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
    parser.add_argument('-d', '--database',type=str,default="./db/db.json",help="rag database") # database directory
    parser.add_argument('-c', '--count',type=int,default=-1,help="count of processing images")
    parser.add_argument('--debug', action='store_true') # use debug for check each step.
    parser.add_argument('--full',action='store_true') # if full is set, we make text to speech.
    parser.add_argument('--rag', action='store_true') # if rag is set, we use rag when translate. else we just use some few-shots.

    args = parser.parse_args()

    input_dir,output_dir,is_debug,is_full,count,db_dir,use_rag = args.input,args.output,args.debug,args.full,args.count,args.database,args.rag
    
    # if output path does not exist, make it.
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    # we get the list of the input
    input_list = os.listdir(input_dir)

    # define count
    if count < 0: count = len(input_list)
    count = min(count,len(input_list))

    # csv file for debugging.
    csv_file = open('./logs/steps.csv','w',encoding='utf-8-sig',newline='')
    writer = csv.writer(csv_file)

    # process each image.
    for idx, file_name in tqdm(enumerate(input_list), total=count):
        if idx >= count: break

        output_text = image_to_text(input_dir,output_dir,file_name,is_debug,writer,db_dir,use_rag) # file write is actually conducted here.

        if is_full: text_to_speech(output_dir,file_name,output_text) # is full is set, we conduct text to speech steps.