import json
import copy
import re
import numpy as np

from utils import make_client
import prompts as P

from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain.chains import LLMChain

api_key = "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"
embeddings = OpenAIEmbeddings(openai_api_key=api_key) # 나중에 utils에 집어넣겠음.

file_path = '/content/drive/MyDrive/Colab_Content/db.json' #이것도 나중에 고칠 예정.

# FAISS 인덱스 생성 및 설정
def setup_vector_store(translated_latex):
    documents = [
        Document(page_content=str(val["Origin"]), metadata=val)
        for key, val in translated_latex.items()
    ]
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore.as_retriever()

# 유사도 계산 함수
def compute_similarity(embedding1, embedding2):
    embedding1 = np.array(embedding1).reshape(1, -1)
    embedding2 = np.array(embedding2).reshape(1, -1)
    return cosine_similarity(embedding1, embedding2)[0][0]

# 검색 및 유사도 계산 함수 정의
def search_documents_with_similarity(retriever, query, embeddings, num_results=3, similarity_threshold=0.85):
    query_embedding = embeddings.embed_query(query)
    results = retriever.get_relevant_documents(query, k=num_results)
    relevant_results = []
    for idx, result in enumerate(results):
        doc_embedding = embeddings.embed_query(result.page_content)
        similarity_score = compute_similarity(query_embedding, doc_embedding)
        if similarity_score >= similarity_threshold:
            relevant_results.append((result, similarity_score))
    return relevant_results

# ChatPromptTemplate 설정
template = """
Context: {context}
Question: {question}
Answer: 당신은 LateX를 한국어로 음독하는 역할을 수행합니다.
위의 Context를 참고하여 Question을 올바르게 한글로 음독해 주세요.
context는 참고만 하고 음독하지 말고, question의 latex(영어 및 수식)만을 한국어로 음독해 주세요.
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI(openai_api_key=api_key)
output_parser = StrOutputParser()
chain = LLMChain(llm=model, prompt=prompt, output_parser=output_parser)

#json File읽어와서 vector에 저장하는 방식인거 같아서 대충 이렇게 해놨음.
ret_temp = None
with open(file_path, encoding='utf-8') as json_file:
    db_latex = json.load(json_file)
    ret_temp = setup_vector_store(db_latex)

def run_chain(query, retriever) -> str:
    try:
        query_str = str(query)
        if len(query_str) == 1:
            return "An error occurred: Single character query is not allowed."
        search_result = search_documents_with_similarity(retriever, query_str, embeddings, num_results=5)
        if search_result and len(search_result) > 0:
            context_list = [
                f"Input: {res[0].page_content}, Output: {res[0].metadata.get('output', 'No output found')}"
                for res in search_result
            ]
            context = "\n".join(context_list)
        else:
            context = ""
        question = str(query_str).strip()
        inputs = {"context": context, "question": question}
        return chain.run(inputs)
    except Exception as e:
        print(f"Error during chain execution: {str(e)}")
        return "An error occurred during chain execution."


def translate_latex(parsed_latex: dict,db_dir: str) -> dict:
    client = make_client("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")

    translated_latex = copy.deepcopy(parsed_latex)

    for key,val in translated_latex.items():
        if "Origin" in val:
            will_translate_latex = val["Origin"]
            translater_latex = run_chain(will_translate_latex,ret_temp)
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

    return translated_latex