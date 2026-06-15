import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(
    page_title="좋아하는 과목으로 찾는 진로 탐색기",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 좋아하는 과목으로 찾는 진로 탐색기")
st.write("좋아하는 과목을 선택하면 어울리는 진로를 추천합니다.")

# 진로 데이터
career_data = {
    "수학": [
        ("데이터 분석가", "데이터를 분석하여 문제를 해결하는 직업", "통계학과"),
        ("인공지능 개발자", "AI 모델을 개발하는 직업", "컴퓨터공학과"),
        ("금융 전문가", "금융 데이터를 분석하는 직업", "경제학과")
    ],
    "과학": [
        ("연구원", "과학적 탐구를 수행", "자연과학계열"),
        ("의사", "질병을 진단하고 치료", "의예과"),
        ("환경 전문가", "환경 문제 해결", "환경공학과")
    ],
    "국어": [
        ("작가", "글을 창작하는 직업", "국어국문학과"),
        ("기자", "뉴스를 취재하는 직업", "신문방송학과"),
        ("교사", "교육 활동 수행", "교육학과")
    ],
    "영어": [
        ("통역사", "언어를 번역 및 통역", "통번역학과"),
        ("외교관", "국가 간 외교 업무", "국제학과"),
        ("항공 승무원", "항공 서비스 제공", "항공서비스학과")
    ],
    "사회": [
        ("공무원", "행정 업무 수행", "행정학과"),
        ("변호사", "법률 서비스 제공", "법학계열"),
        ("사회복지사", "복지 서비스 제공", "사회복지학과")
    ],
    "기술·가정": [
        ("제품 디자이너", "제품을 설계하고 디자인", "산업디자인학과"),
        ("메이커 교육 전문가", "창작 활동 교육", "기술교육과"),
        ("엔지니어", "기술 문제 해결", "공학계열")
    ],
    "정보": [
        ("소프트웨어 개발자", "프로그램 개발", "컴퓨터공학과"),
        ("보안 전문가", "정보 보호", "정보보호학과"),
        ("게임 개발자", "게임 제작", "게임공학과")
    ],
    "미술": [
        ("그래픽 디자이너", "시각 디자인 제작", "디자인학과"),
        ("일러스트레이터", "그림 창작", "미술학과"),
        ("웹디자이너", "웹 화면 디자인", "디지털디자인학과")
    ],
    "음악": [
        ("작곡가", "음악 창작", "작곡과"),
        ("음향 엔지니어", "음향 기술 담당", "음향제작과"),
        ("음악교사", "음악 교육", "음악교육과")
    ],
    "체육": [
        ("체육교사", "체육 교육", "체육교육과"),
        ("운동처방사", "건강 관리 지원", "스포츠과학과"),
        ("스포츠 마케터", "스포츠 산업 기획", "스포츠산업학과")
    ]
}

st.subheader("1️⃣ 좋아하는 과목 선택")

subjects = st.multiselect(
    "좋아하는 과목을 선택하세요",
    list(career_data.keys())
)

st.subheader("2️⃣ 관심 분야 선택")

interest = st.selectbox(
    "관심 분야",
    ["선택 안 함", "공학", "교육", "의료", "예술", "IT", "사회", "경영"]
)

if st.button("🔍 진로 추천 받기"):

    if not subjects:
        st.warning("과목을 하나 이상 선택하세요.")
    else:

        result = []

        for subject in subjects:
            result.extend(career_data[subject])

        career_score = {}

        for career, desc, major in result:
            career_score[career] = career_score.get(career, 0) + 1

        sorted_careers = sorted(
            career_score.items(),
            key=lambda x: x[1],
            reverse=True
        )

        st.success("추천 결과가 생성되었습니다.")

        output_data = []

        for career, score in sorted_careers:

            for item in result:
                if item[0] == career:
                    desc = item[1]
                    major = item[2]
                    break

            st.markdown("---")
            st.subheader(f"⭐ {career}")
            st.write(f"추천 점수: {score}")
            st.write(f"설명: {desc}")
            st.write(f"관련 학과: {major}")

            output_data.append({
                "직업": career,
                "추천점수": score,
                "설명": desc,
                "관련학과": major
            })

        csv = pd.DataFrame(output_data).to_csv(
            index=False,
            encoding="utf-8-sig"
        )

        st.download_button(
            "📥 결과 다운로드",
            csv,
            file_name="career_recommendation.csv",
            mime="text/csv"
        )

st.markdown("---")

st.subheader("🎲 랜덤 진로 탐색")

if st.button("랜덤 진로 보기"):
    import random

    all_careers = []

    for careers in career_data.values():
        all_careers.extend(careers)

    selected = random.choice(all_careers)

    st.info(f"""
    직업: {selected[0]}
    
    설명: {selected[1]}
    
    관련 학과: {selected[2]}
    """)

st.markdown("---")
st.caption("진로 탐색 참고용 앱입니다.")
