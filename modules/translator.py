import json
import copy
import re
import numpy as np

from modules.utils import make_client
import modules.prompts as P

from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain.chains import LLMChain

retriever = None

# FAISS 인덱스 생성 및 설정
def setup_vector_store(rag_data_list : list[dict], embeddings):
    documents = []
    for rag_data in rag_data_list:
        documents.append(Document(page_content=rag_data["input"], metadata={"output": rag_data["output"]}))

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
def initialize_retriever(db_dir: str, embeddings):
    global retriever
    with open(db_dir, "r", encoding="utf-8") as db_raw:
        db_json = json.load(db_raw)
        retriever = setup_vector_store(db_json, embeddings)

def translate_latex_line(latex_str: str, db_dir: str, use_RAG=False) -> str:
    if(use_RAG):
        # RAG를 쓸때.
        prompt = ChatPromptTemplate.from_template(P.rag_sys_prompt)
        model = ChatOpenAI(openai_api_key="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")
        output_parser = StrOutputParser()
        chain = LLMChain(llm=model, prompt=prompt, output_parser=output_parser)

        # We defined Embeddings
        embeddings = OpenAIEmbeddings(api_key="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")

        # We defined retriever
        global retriever
        if use_RAG:
            if retriever is None:
                embeddings = OpenAIEmbeddings(api_key="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")
                initialize_retriever(db_dir, embeddings)

        try:
            if len(latex_str) == 1: return "An error occurred: Single character query is not allowed."

            search_result = search_documents_with_similarity(retriever, latex_str, embeddings, num_results=5)

            if search_result and len(search_result) > 0:
                context_list = [
                    f"Input: {res[0].page_content}, Output: {res[0].metadata.get('output', 'No output found')}"
                    for res in search_result
                ]
                context = "\n".join(context_list)
            else:
                context = ""

            question = latex_str.strip()
            inputs = {"context": context, "question": question}
            return chain.run(inputs)
        except Exception as e:
            return "An error occurred during chain execution."
    else:
        # RAG를 사용하지 않을 때
        client = make_client("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")
        latex_prompt = [{"role" : "user", "content" : latex_str}]

        completion_latex = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=4096,
            temperature=0,
            messages=P.latex2kor_shot + latex_prompt
        )
        translate_latex = completion_latex.choices[0].message.content
        return translate_latex

def translate_latex(parsed_latex: dict, db_dir: str, use_rag: bool) -> dict:
    #간단하게 json을 모두 순회하면서 각 라텍스를 번역합니다.
    
    client = make_client("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")

    translated_latex = copy.deepcopy(parsed_latex)

    for key,val in translated_latex.items():
        if "Origin" in val:
            val["Origin"] = translate_latex_line(val["Origin"],db_dir,use_rag)

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