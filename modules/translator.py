
import json  
import copy  # 객체 복사에 사용
import re  # 정규 표현식 처리를 위한 모듈
import numpy as np  

from modules.utils import make_client  # 사용자 정의 유틸리티 함수 가져오기
import modules.prompts as P  # 사용자 정의 프롬프트 모듈 가져오기

from sklearn.metrics.pairwise import cosine_similarity  # 코사인 유사도를 계산하기 위한 함수
from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # LangChain에서 제공하는 OpenAI 관련 기능 가져오기
from langchain.prompts import ChatPromptTemplate  # LangChain의 ChatPromptTemplate 클래스
from langchain_community.vectorstores import FAISS  # FAISS 기반 벡터 저장소 사용
from langchain_core.output_parsers import StrOutputParser  # LangChain의 문자열 출력 파서
from langchain.schema import Document  # LangChain 문서 객체
from langchain.chains import LLMChain  # LangChain에서 체인을 정의하기 위한 클래스

# 전역 변수 선언 (FAISS 기반 검색기)
retriever = None

# FAISS 인덱스를 생성하고 설정하는 함수
def setup_vector_store(rag_data_list : list[dict], embeddings):
    # 문서 목록 초기화
    documents = []
    for rag_data in rag_data_list:  # 데이터 리스트 반복
        # Document 객체 생성 및 추가 (문서 내용과 메타데이터 포함)
        documents.append(Document(page_content=rag_data["input"], metadata={"output": rag_data["output"]}))

    # FAISS 벡터 저장소 생성
    vectorstore = FAISS.from_documents(documents, embeddings)
    # 검색기로 변환 후 반환
    return vectorstore.as_retriever()

# 두 임베딩 벡터 간의 유사도를 계산하는 함수
def compute_similarity(embedding1, embedding2):
    # 첫 번째 임베딩을 2차원 배열로 변환
    embedding1 = np.array(embedding1).reshape(1, -1)
    # 두 번째 임베딩을 2차원 배열로 변환
    embedding2 = np.array(embedding2).reshape(1, -1)
    # 코사인 유사도 계산 후 반환
    return cosine_similarity(embedding1, embedding2)[0][0]

# 검색과 유사도 계산을 수행하는 함수 정의
def search_documents_with_similarity(retriever, query, embeddings, num_results=3, similarity_threshold=0.85):
    # 쿼리 문장을 임베딩으로 변환
    query_embedding = embeddings.embed_query(query)
    # 검색 결과에서 num_results 만큼 문서를 가져옴
    results = retriever.get_relevant_documents(query, k=num_results)
    # 유사한 결과를 저장할 리스트 초기화
    relevant_results = []
    for idx, result in enumerate(results):  # 검색 결과를 반복
        # 각 문서의 내용을 임베딩으로 변환
        doc_embedding = embeddings.embed_query(result.page_content)
        # 쿼리와 문서 간 유사도 계산
        similarity_score = compute_similarity(query_embedding, doc_embedding)
        # 유사도가 설정된 임계값 이상일 경우 결과에 추가
        if similarity_score >= similarity_threshold:
            relevant_results.append((result, similarity_score))
    # 유사도가 높은 결과 반환
    return relevant_results

# ChatPromptTemplate 초기화
def initialize_retriever(db_dir: str, embeddings):
    # 전역 변수 retriever 사용
    global retriever
    with open(db_dir, "r", encoding="utf-8") as db_raw:  # JSON 데이터베이스 파일 열기
        db_json = json.load(db_raw)  # JSON 파일 읽기
        retriever = setup_vector_store(db_json, embeddings)  # 벡터 저장소 설정

# LaTeX 문자열을 번역하는 함수 정의
def translate_latex_line(latex_str: str, db_dir: str, use_RAG=False) -> str:
    if(use_RAG):  # RAG(Retrieval-Augmented Generation)를 사용할 경우
        # 프롬프트 템플릿 설정
        prompt = ChatPromptTemplate.from_template(P.rag_sys_prompt)
        # ChatGPT 모델 초기화
        model = ChatOpenAI(openai_api_key="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")
        # 문자열 출력 파서 초기화
        output_parser = StrOutputParser()
        # 체인(Chain) 초기화 (프롬프트와 모델 연결)
        chain = LLMChain(llm=model, prompt=prompt, output_parser=output_parser)

        # OpenAI 임베딩 생성
        embeddings = OpenAIEmbeddings(api_key="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")

        # 전역 변수 retriever 사용
        global retriever
        if use_RAG:  # RAG 사용 여부 확인
            if retriever is None:  # 검색기가 초기화되지 않았을 경우
                embeddings = OpenAIEmbeddings(api_key="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")
                initialize_retriever(db_dir, embeddings)  # 검색기 초기화

        try:
            if len(latex_str) == 1:  # 입력이 한 글자일 경우 에러 메시지 반환
                return "An error occurred: Single character query is not allowed."

            # 문서 검색 및 유사도 계산
            search_result = search_documents_with_similarity(retriever, latex_str, embeddings, num_results=5)

            if search_result and len(search_result) > 0:  # 검색 결과가 있을 경우
                # 결과를 입력 및 출력 문자열로 구성
                context_list = [
                    f"Input: {res[0].page_content}, Output: {res[0].metadata.get('output', 'No output found')}"
                    for res in search_result
                ]
                context = "\n".join(context_list)  # 컨텍스트 문자열 생성
            else:  # 검색 결과가 없을 경우
                context = ""

            question = latex_str.strip()  # 입력 문자열에서 공백 제거
            inputs = {"context": context, "question": question}  # 체인 입력 구성
            return chain.run(inputs)  # 체인 실행 및 결과 반환
        except Exception as e:  # 에러 발생 시 처리
            return "An error occurred during chain execution."
    else: # RAG를 사용하지 않을 때
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
