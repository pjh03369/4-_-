import streamlit as st
import requests
from bs4 import BeautifulSoup

# 폰트를 설정하기 위한 HTML 코드 추가
st.markdown(
    """
    <style>
    .title {
        font-family: 'Arial', sans-serif; /* 원하는 폰트로 설정 */
        font-size: 30px;  /* 제목 크기 */
        color: #FF5733;  /* 제목 색상 */
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 제목에 클래스 적용
#st.markdown('<p class="title"><b style="font-size:2em;">무</b>작정 <b style="font-size:2em;">신</b>나게 <b style="font-size:2em;">사</b>보자!</p>', unsafe_allow_html=True)
st.markdown('<p class="title"> <b style="font-size:2em;">무</b>조건  <b style="font-size:2em;">신</b>상  <b style="font-size:2.3em;">4</b>죠</p>', unsafe_allow_html=True)


# 로고 이미지 URL
logo_url = "https://image.msscdn.net/display/images/2024/07/19/3a7caf3364184181a3cae5741f91464f.png"

# 사이드바 상단에 로고 추가
st.sidebar.image(logo_url, use_container_width=True)

# 1. 월에 따른 평균 온도 설정
def get_average_temperature(month):
    month_to_temp = {
        '1월': -5,   
        '2월': 0,    
        '3월': 5,    
        '4월': 10,   
        '5월': 15,   
        '6월': 25,   
        '7월': 30,   
        '8월': 30,   
        '9월': 25,   
        '10월': 15,  
        '11월': 5,   
        '12월': 0    
    }
    return month_to_temp.get(month, 20)

# 2. 온도에 따라 계절을 자동으로 판별하는 함수
def get_season_by_temperature(temperature):
    if temperature < 2:
        return "winter"
    elif 2 <= temperature <= 10:
        return "spring"  # 봄을 추가
    elif 11 <= temperature <= 20:
        return "autumn"  # 가을을 추가
    else:
        return "winter"



# 4. 사용자가 선택할 수 있는 월 (사이드바에 배치)
selected_month = st.sidebar.selectbox("Select the month you want", 
                                      ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'])

# 5. 사용자가 온도를 선택할 수 있도록 슬라이더 추가 (사이드바에 배치)
selected_temperature = st.sidebar.slider("Select your desired temperature (°C)", -30, 40, get_average_temperature(selected_month))

# 7. 가격 범위 선택 (사이드바에 배치)
price_range = st.sidebar.selectbox("Select your price range", 
                                   ["0 ~ 500,000 won", "10,000 ~ 30,000 won", "30,000 ~ 50,000 won", "50,000 ~ 100,000 won", "100,000 won"])


def get_season_and_recommendation(temperature):
    season = get_season_by_temperature(temperature)  # 온도에 따라 계절을 자동 판별
    
    if season == "겨울":
        recommendation = "두꺼운 코트, 장갑, 목도리"
    elif season == "봄":  # 봄에 대한 추천 아이템 추가
        recommendation = "가벼운 자켓, 스웨터"
    elif season == "가을":  # 가을에 대한 추천 아이템 추가
        recommendation = "가벼운 자켓, 스웨터"
    else:  # 여름
        recommendation = "반팔 티셔츠, 반바지, 선글라스"
    
    return season, recommendation  # season과 recommendation을 반환

# 9. 가격대별 추천 아이템 (가격대에 맞게 아이템을 추천)
def get_item_recommendations(season, price_range):
    items_by_season = {
        "여름": {
            "0 ~ 10,000원": ["반팔 티셔츠", "반바지", "모자", "슬리퍼"],
            "10,000 ~ 30,000원": ["반팔 티셔츠", "반바지", "선글라스", "모자"],
            "30,000 ~ 50,000원": ["디자이너 반팔 티셔츠", "고급 선글라스", "휴양지 스타일 의류"],
            "50,000 ~ 100,000원": ["고급 반팔 티셔츠", "프리미엄 선글라스", "트렌디한 의류"],
            "100,000원 이상": ["디자이너 반팔 티셔츠", "디자이너 반바지", "고급 선글라스"]
        },
        "겨울": {
            "0 ~ 10,000원": ["두꺼운 코트", "장갑", "목도리", "부츠"],
            "10,000 ~ 30,000원": ["울코트", "패딩 자켓", "방한 장갑", "스카프"],
            "30,000 ~ 50,000원": ["명품 패딩", "디자이너 코트", "고급 장갑"],
            "50,000 ~ 100,000원": ["프리미엄 패딩", "고급 장갑", "프리미엄 스카프"],
            "100,000원 이상": ["디자이너 패딩", "럭셔리 코트", "고급 장갑"]
        },
        "봄":{
            "0 ~ 10,000원": ["가벼운 자켓", "청바지", "스웨터"],
            "10,000 ~ 30,000원": ["가벼운 자켓", "스웨터", "코듀로이 팬츠"],
            "30,000 ~ 50,000원": ["디자이너 자켓", "고급 스웨터", "프리미엄 팬츠"],
            "50,000 ~ 100,000원": ["프리미엄 자켓", "고급 스웨터", "디자이너 팬츠"],
            "100,000원 이상": ["디자이너 자켓", "고급 스웨터", "프리미엄 팬츠"]
        },
        "가을": {
            "0 ~ 10,000원": ["가벼운 자켓", "청바지", "스웨터"],
            "10,000 ~ 30,000원": ["가벼운 자켓", "스웨터", "코듀로이 팬츠"],
            "30,000 ~ 50,000원": ["디자이너 자켓", "고급 스웨터", "프리미엄 팬츠"],
            "50,000 ~ 100,000원": ["프리미엄 자켓", "고급 스웨터", "디자이너 팬츠"],
            "100,000원 이상": ["디자이너 자켓", "고급 스웨터", "프리미엄 팬츠"]
        }
    }

    # 해당 계절과 가격 범위에 맞는 아이템 리스트
    recommended_items = items_by_season.get(season, {}).get(price_range, [])
    
    return recommended_items

# 10. 계절과 추천 아이템 출력
season, recommendation = get_season_and_recommendation(selected_temperature)

# 11. 가격대에 맞는 아이템 추천
recommended_items = get_item_recommendations(season, price_range)

# 12. 결과 출력
#st.write(f"추천 계절: {season}")
#st.write(f"온도에 따른 패션 아이템: {recommendation}")
#st.write(f"선택 가격대에 맞는 패션 아이템: {', '.join(recommended_items)}")

import requests
from bs4 import BeautifulSoup
import streamlit as st

# 예시 데이터 설정
season = "Winter"
recommendation = "Coat"
recommended_items = ["Coat", "Gloves", "Scarf"]


# Create a dictionary 
options_dict = {
    "상의": "top",
    "하의": "bottom",
    "원피스": "onepiece",
    "아웃터": "outerwear",
    "신발": "shoes",
    "가방": "bag",
    #"모자": "hat",
    "양발": "socks",
    "머플러": "muffler",
    "안경": "glasses",
    "악세사리": "accessories",
    #"쥬얼리": "jewelry",
    #"벨트": "belt"
}

options_key = list(options_dict.keys())

# 선택된 항목을 sidebar에서 받기
def get_selection_type_eng(selection):
    if selection:
        return options_dict.get(selection, None)
    return None

selection = st.segmented_control(
    "Directions", options_key, selection_mode="single"
)

# 선택된 항목에 해당하는 영어 값을 가져오기
selection_type_eng = get_selection_type_eng(selection)


# 선택 옵션 표시
options2 = ["클래식", "디자인", "편안함", "운동화", "발", "안정적", "스타일리시", "의상", "활용도", "외출", "운동", "깔끔", "미니멀", "스타일", "쿠셔닝", "경량", "심플", "세련됨", "안정감", "활동", "튼튼", "실용적", "발목", "내구성", "블랙", "운동성", "트레일", "러닝", "그립력", "캐주얼", "고급스러움", "실버", "방수", "하이킹", "화이트", "자연", "색감", "여름", "통기성", "시원", "밑창", "여성스러움", "라이프스타일", "일상", "활동적", "밑창", "편안함", "디자인", "세련됨", "경량", "컬러", "기능", "초콜릿", "데일리", "모던", "스포츠", "다크 스모크", "그레이", "빨간색", "슬라이드"]
selection_tag_b = st.sidebar.pills("Directions", options2, selection_mode="multi")
selection_tag = " ".join(selection_tag_b)
#st.markdown(f"Your selected options: {selection_tag}.{selection_type_eng}")
import streamlit as st
import requests
from bs4 import BeautifulSoup

# 채팅 입력 받기
prompt = st.chat_input("Say something")


if prompt:
    # 사용자의 입력 메시지를 오른쪽에 표시 (사용자의 채팅)
    st.markdown(f'<div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">'
                f'<div style="background-color: #262730; padding: 10px; border-radius: 20px; max-width: 80%; word-wrap: break-word;">'
                f'{prompt}</div></div>', unsafe_allow_html=True)
    
    # POST 요청을 보낼 URL
    url = "https://secure-mayfly-instantly.ngrok-free.app/query"  # 실제 URL로 변경
    
    # 서버에 보낼 데이터
    data = {
        "query": prompt +' '+ selection_type_eng + ' ' + selection_tag
    }

    # 요청 헤더 설정 (User-Agent 추가)
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # POST 요청 보내기
    response = requests.post(url, json=data, headers=headers)
    
    # 응답 처리
    if response.status_code == 200:
        # 서버에서 반환된 결과
        result = response.json().get('result', 'No result found')
        
        # 응답 메시지를 왼쪽에 표시 (서버의 응답)
        st.markdown(f'<div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">'
                    f'<div style="background-color: #ff4b4b; padding: 10px; border-radius: 20px; max-width: 80%; word-wrap: break-word;">'
                    f'{result}</div></div>', unsafe_allow_html=True)
        
        # 링크가 있을 경우 처리
        if "https://" in result:  # 링크가 포함된 경우
            # 링크 추출
            start_index = result.find("https://")
            end_index = result.find(" ", start_index)
            if end_index == -1:  # 공백이 없으면 링크 끝까지
                link = result[start_index:]
            else:
                link = result[start_index:end_index]

            # OG 태그 파싱을 위한 요청
            try:
                # User-Agent 헤더 추가하여 요청
                response = requests.get(link, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')

                # OG 이미지, 설명, URL 정보 추출
                og_image = soup.find("meta", property="og:image")
                og_description = soup.find("meta", property="og:description")
                og_url = soup.find("meta", property="og:url")

                # OG 이미지 처리
                if og_image:
                    image_url = og_image['content']
                    st.markdown(f'<img src="{image_url}" style="border-radius: 20px; width: 100%; max-width: 500px; margin-bottom: 10px" />', unsafe_allow_html=True)
                else:
                    st.write("No OG image found.")  # OG 이미지가 없을 경우 알림

                # OG 설명 처리
                if og_description:
                    #description = og_description['content']
                    product_url = og_url['content']
                    st.markdown(f'<div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">'
                                f'<div style="background-color: #ff4b4b; padding: 10px; border-radius: 20px; max-width: 80%; word-wrap: break-word;">'
                                f'<strong>Description:</strong> {product_url}</div></div>', unsafe_allow_html=True)
                else:
                    st.write("No description found.")


            except Exception as e:
                st.write(f"Failed to retrieve OG tags. Error: {str(e)}")

    else:
        # 요청 실패 시 오류 메시지 출력
        st.write(f"Error: {response.status_code}, {response.text}")



# streamlit run .py        