import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from sklearn.cluster import KMeans
import numpy as np
url = 'https://drive.google.com/file/d/1yq6aIqR3sUd1MLrWCTwPDpS6pBFlxpPl/view?usp=sharing'
df = pd.read_csv('https://drive.google.com/uc?export=download&id='+url[32:65], delimiter=',')
# 페이지 설정
st.set_page_config(
    page_title="배달 위치 군집 분석",
    page_icon="🗺️",
    layout="wide"
)

# 타이틀
st.title("🗺️ 배달 위치 군집 분석")
st.markdown("서울 지역 배달 위치를 K-means 클러스터링으로 분석합니다.")

# 사이드바에 컨트롤 패널
st.sidebar.header("설정")

# 데이터 로드 함수
@st.cache_data
def load_data():
    """배달 데이터를 로드합니다."""
    # CSV 데이터 (실제 사용 시에는 파일에서 읽어옵니다)
    data = """Num,Latitude,Longitude
