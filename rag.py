import os

from fastapi import HTTPException

from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, StuffDocumentsChain 
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_community.vectorstores import FAISS
from langchain_community.document_transformers import LongContextReorder


# .env 파일을 불러오기
load_dotenv(r"C:\Users\241011\Documents\key.env")

# 환경 변수 중 하나를 확인 (예: 'KEY'라는 환경 변수 확인)
key = os.getenv("GOOGLE_API_KEY")  # 여기서 "KEY"는 .env 파일에 정의된 환경 변수의 이름입니다.

# HuggingFace 모델 캐시 경로 설정 (로컬에 저장)
os.environ["HF_HOME"] = r"C:\Users\241011\Documents\models"

model_name = "jhgan/ko-sbert-nli"  # 한국어 임베딩 모델
model_kwargs = {'device': 'cpu'}  # GPU에서 모델을 실행
encode_kwargs = {'normalize_embeddings': True}  # 임베딩 정규화

# HuggingFace 임베딩 객체 생성
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# 로컬에 저장된 FAISS 인덱스를 불러오기 (보안 상 신뢰할 수 있으면 True로 설정)
loaded_faiss = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# 검색기 설정 (가장 유사한 3개의 문서를 검색)
faiss_retriever = loaded_faiss.as_retriever(search_kwargs={"k": 3})


# 모델을 ChatGoogleGenerativeAI 객체로 설정 (여기서는 'gemini-pro' 모델 사용)
model = ChatGoogleGenerativeAI(model="gemini-pro")

# 사용자에게 질문을 하고 그에 대한 답변을 받을 수 있도록 ChatPromptTemplate 설정
prompt = ChatPromptTemplate.from_messages([("user", """
Even if it doesn't match exactly, it will tell you the most similar information. You must choose at least one.
 Answer: 하이페리엄 슬라이드 블랙은 세련되면서도 실용적인 디자인의 슬리퍼입니다. 블랙 컬러는 어떤 스타일에도 잘 어울려 데일리로 사용하기에 좋으며, 간편하게 착용할 수 있는 슬라이드 형식이 매력적입니다. 발을 편안하게 감싸는 디자인과 부드러운 쿠셔닝 덕분에 장시간 착용해도 편안함을 유지하며, 여름철 외출이나 물가에서 활동할 때 유용하게 활용할 수 있습니다. 가벼운 외출이나 여행, 바캉스에 적합한 이 슬라이드는 간편하면서도 스타일리시한 선택이 될 것입니다. 가격은 22,000원이고, 브랜드는 블렌도프입니다. 링크는 https://www.musinsa.com/products/1564155 입니다."\n
 Answer: 스피드캣 OG - 블랙은 클래식한 디자인과 탁월한 편안함을 자랑하는 운동화입니다. 발을 안정적으로 지지해주며, 스타일리시하면서도 어떤 의상에도 잘 어울립니다. 이 신발은 일상적인 외출뿐만 아니라 간단한 운동에도 적합해 활용도가 높습니다. 가격은 159,000원이고, 브랜드는 킨입니다. 링크는 https://www.musinsa.com/products/2378989 입니다."\n
 Answer: 어센틱 블랙은 심플하면서도 세련된 디자인을 자랑하는 신발입니다. 편안하고 실용적인 착용감 덕분에 일상적인 외출에 자주 활용할 수 있으며, 다양한 스타일에 잘 어울립니다. 가격은 13,000원이고, 브랜드는 인볼입니다. 링크는 https://www.musinsa.com/products/3489258 입니다."\n
Question: {question}
""")])


# 디버깅용 RunnablePassthrough 클래스 (입력과 출력을 그대로 넘겨주는 역할)
class prompt_debug(RunnablePassthrough):
    def invoke(self, *args, **kwargs):
        # 디버그 출력을 원한다면 출력할 수 있습니다
        # print("Debug Output:", output)
        output = super().invoke(*args, **kwargs)  # 입력과 출력을 그대로 넘김
        return output

# 문서들의 포맷을 재구성하는 함수 (예: 긴 문서를 재정렬하여 더 나은 형태로 처리)
def format_docs(docs):
    # print("docs:", docs)  # 원본 문서 출력 (디버깅 시)
    reordering = LongContextReorder()  # 긴 문서에서 중요한 내용만 우선적으로 처리
    reordered_docs = reordering.transform_documents(docs)  # 문서 재정렬
    # print("reordered_docs:", reordered_docs)  # 재정렬된 문서 출력 (디버깅 시)
    
    # 문서 내용을 "\n\n"로 구분하여 하나의 문자열로 변환
    formatted_docs = "\n\n".join(doc.page_content for doc in reordered_docs)
    
    return formatted_docs

# RAG 체인 구성: 검색기, 문서 포맷팅, 프롬프트 템플릿, 모델, 응답 파싱 등
rag_chain = (
        {"context": faiss_retriever | format_docs, "question": RunnablePassthrough()}  # 검색기와 포맷 처리
        | prompt  # 사용자 프롬프트 템플릿
        | prompt_debug()  # 디버그용 처리
        | model  # 모델을 통한 질문 응답
        | StrOutputParser()  # 응답 파싱
)

def generate_response(query_text: str):
    try:
        # rag_chain.invoke()를 사용하여 query_text를 처리합니다.
        result = rag_chain.invoke(query_text)  # query_text를 사용해 처리
        return result  # 결과 반환
    except Exception as e:
        # 예외가 발생하면 처리하고, 적절한 메시지 반환
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
    
