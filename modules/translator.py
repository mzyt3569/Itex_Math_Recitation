import json
import copy
import re

from utils import make_client
import prompts as P

def translate_latex(parsed_latex: dict) -> dict:
    client = make_client("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")

    translated_latex = copy.deepcopy(parsed_latex)

    for key,val in translated_latex.items():
        if "Origin" in val:
            latex_prompt = [{"role" : "user", "content" : val["Origin"]}]
            completion_latex = client.chat.completions.create(
                model="gpt-4o",
                max_tokens=4096,
                temperature=0,
                messages=P.latex2kor_shot + latex_prompt
            )
            translater_latex = completion_latex.choices[0].message.content
            val["Origin"] = translater_latex

        if "Inequal_list" in val:
            inequal_list = val["Inequal_list"]
            for inequal_idx,inequal_val in inequal_list.items():
                while True:
                    inequal_prompt = [{"role" : "user", "content" : inequal_val}] # Make inequality to user prompt
                    completion_inequal = client.chat.completions.create(
                        model="gpt-4o",
                        max_tokens=4096,
                        temperature=0,
                        messages=P.inequal2kor_shot + inequal_prompt
                    )

                    translate_process_inequal = completion_inequal.choices[0].message.content # GPT will translate it with process.
                    matched_inequal = re.search(r"Merged : (.*)", translate_process_inequal) # Our interests is final answer.
                    if matched_inequal:
                        translate_inequal = matched_inequal.group(1) # transform match into string.
                        inequal_list[inequal_idx] = translate_inequal # change original to translated one.
                        break

        if "Frac_list" in val:
            frac_list = val["Frac_list"]
            for frac_idx,frac_val in frac_list.items():
                while True:
                    frac_prompt = [{"role" : "user", "content" : frac_val}]

                    completion_frac = client.chat.completions.create(
                        model="gpt-4o",
                        max_tokens=4096,
                        temperature=0,
                        messages=P.frac2kor_shot + frac_prompt
                    )

                    translate_process_frac = completion_frac.choices[0].message.content
                    matched_frac = re.search(r"Merged : (.*)", translate_process_frac)
                    if matched_frac:
                        translate_frac = matched_frac.group(1)
                        frac_list[frac_idx] = translate_frac
                        break

    # if is_debug: 
    #     print("TRANSLATED!!!!!!!!!!!!!!!!!!!!")
    #     print(json.dumps(translated_latex,indent=4,ensure_ascii=False))              
    #     print("\n")
    return translated_latex