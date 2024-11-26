import copy
import json
from modules.utils import make_client
import modules.prompts as P

def latex_merge_latex(translated_latex: dict) -> dict:
    # 분리되었던 분수와 부등식을 원래 라텍스에 집어넣는다.
    latex_merged_latex = copy.deepcopy(translated_latex)

    for key,val in latex_merged_latex.items():
        if "Origin" in val:
            original_latex = val["Origin"]
            if "Inequal_list" in val:
                inequal_list = val["Inequal_list"]
                for inequal_idx,inequal_val in reversed(inequal_list.items()):
                    original_latex = original_latex.replace(inequal_idx,f"[{inequal_val.strip()}]")

            if "Frac_list" in val:
                frac_list = val["Frac_list"]
                for frac_idx,frac_val in frac_list.items():
                    if frac_idx in original_latex:
                        original_latex = original_latex.replace(frac_idx,f"[{frac_val.strip()}]")

            val["Origin"] = original_latex

    return latex_merged_latex

def final_merge_latex(file_name: str, question: str, latex_merged_latex: dict) -> str:
    # 분리되었던 라텍스를 원래 문제에 집어넣는다.
    client = make_client("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")
    merged_question = question

    for key,val in latex_merged_latex.items():
        merged_question = merged_question.replace(f"[{key}]",f"[{val["Origin"].strip()}]")

    merge_prompt = [{"role": "user", "content": merged_question}]
    """
    merge_prompt = [
        {"role": "user", "content": [
            {"type": "text", "text": merged_question},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encode_image(file_name)}"}}]
        }
    ]
    """

    completion_merge = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=4096,
        temperature=0,
        messages=P.merge_shot + merge_prompt
    )
    merged_question = completion_merge.choices[0].message.content
    
    return merged_question