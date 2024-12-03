# 무조건 신상 4죠

## 1️⃣ 프로젝트 개요
패션은 단순히 옷을 입는 것을 넘어, 개인의 정체성과 개성을 표현하는 중요한 수단입니다. 옷을 통해 자신의 가치관, 취향, 분위기를 드러낼 수 있으며, 이를 통해 다른 사람들에게 강렬한 첫인상을 남길 수 있습니다. 
하지만 여러가지 이유때문에 패션에 대해 무관심하거나, 어려워하는 사람들, 소위 “패알못”들은  끊임없이 빠르게 변화하는 트렌드에 대처하기 힘들어 패션테러를 일으켜 우리를 안타깝게 만듭니다. 
그래서 저희는  국내 대표 패션 플랫폼인 무신사에서 제공해 주는 데이터를 바탕으로 사용자의 취향과 실질적인 니즈에 맞춘 가격, 온도 및 계절, 리뷰 기반 추천 서비스를 제공하는 챗봇을 기획했습니다.

---

<br><br>
## 2️⃣ TEAM BYTEBITE (사일런스)

| 이름  | 역할      | 업무         |
|-----|---------|------------|
| 박지호 | 팀장      | 문서화, PT 및 발표  |
| 정재석 | 서기     | Streamlit 인터페이스 디자인  |
| 김건태 | 팀원 | 데이터 전처리 |
| 이규혁 | 팀원      | 웹 크롤링 |
| 김민철 | 팀원      |  API 및 모델 학습, 서비스 기능 테스트 |

<br><br>

## 3️⃣ 프로젝트 일정
| 날짜            | 업무                 |
|---------------|--------------------|
| 11.22 ~ 11.24 | 아이디어 회의          |
| 11.25 | 프로젝트 주제 결정 및 역할 분담          |
| 11.25 ~ 11.28 | 각자 역할에 맞는 작업 수행 |
| 11.29 | 여러 이슈 수집 및 해결방안 모색 |
| 11.30 ~ 12.02 | 데이터 전처리 관련 추가 업무 |
| 12.03 | 추가기능 구현 및 프론트엔드 수정 |
| 12.04 | 프로젝트 완성 및 발표 |

<br><br>

## 4️⃣ 기능 소개
```
여러가지 카테고리를 통해 무신사에서 크롤링 한 데이터를 바탕으로 사용자가 원하는 패션아이템(이미지, url, 리뷰요약)을 추천합니다
- 월별
- 온도별
- 가격별
- 키워드별
- 패션 아이템 카테고리별
```
<br><br>

## 5️⃣ 사용 기술 
🖥️ 프론트엔드
- Streamlit
- Python
<br>📀 백엔드
- jhgan/ko-sbert-nli
- Python
- 구글 Gemini
- API(무신사)
- ngrok
- <br>💬 협업도구
- GitHub
- Slack
- Notion
## 6️⃣ 서비스 아키텍쳐
- 🏗️ 서비스 아키텍쳐
<br><br>
![서비스아키텍쳐](https://github.com/user-attachments/assets/c70fe23b-a75a-4c80-ae1e-ae6c4d88d18f)
<br><br>
- 🖼️ 와이어프레임
<br><br>
![와이어프레임](https://github.com/user-attachments/assets/8d2f3cf4-2469-4346-be27-60bea26ee6cd)

<br><br>

## 7️⃣ 프로젝트 파일 구조

```
📦
├─ .streamlit
 └─ config.toml # 설정 파일 (모델 경로 및 환경 변수 등)
├─ data
 └─ data_sample.csv # 데이터 샘플 (CSV 형식)
├─ faiss_index
 └─ index.faiss # FAISS 인덱스 파일 (벡터 검색용)
 └─ index.pkl # 추가 데이터 또는 인덱스 객체 (피클 형식)
├── app.py                 # Streamlit 기반의 사용자 인터페이스를 제공하는 파일
├── api.py                 # FastAPI 서버와 RAG 모델 연결을 처리하는 파일
├── rag.py                 # RAG(검색 및 생성) 모델 로직 정의
├── README.md              # 프로젝트 개요 및 설명 문서
└── rag_CVS_전처리_디버그.ipynb  # 데이터 전처리 및 디버깅 노트북
```

