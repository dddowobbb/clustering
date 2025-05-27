import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import folium
from streamlit_folium import st_folium

st.title("📍 배송 위치 기반 군집 분석 (Folium 지도 시각화)")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/dddowobbb/clustering/main/Delivery%20-%20Delivery.csv"
    df = pd.read_csv(url)
    return df

df = load_data()
st.subheader("데이터 미리보기")
st.dataframe(df)

# 위치 컬럼 지정
lat_col = "Latitude"
lon_col = "Longitude"

# 군집 수 선택
n_clusters = st.sidebar.slider("군집 수 (K)", min_value=2, max_value=10, value=3)

# 군집 분석용 데이터프레임 구성
loc_df = df[[lat_col, lon_col]].dropna().copy()

# 표준화 후 클러스터링
scaler = StandardScaler()
X_scaled = scaler.fit_transform(loc_df[[lat_col, lon_col]])

kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
labels = kmeans.fit_predict(X_scaled)

# 클러스터 결과 추가
loc_df["Cluster"] = labels

# 지도 중심 계산
center_lat = loc_df[lat_col].mean()
center_lon = loc_df[lon_col].mean()

# Folium 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

# 색상 목록
cluster_colors = [
    "red", "blue", "green", "purple", "orange",
    "darkred", "lightblue", "pink", "gray", "cadetblue"
]

# 마커 추가
for _, row in loc_df.iterrows():
    folium.CircleMarker(
        location=[row[lat_col], row[lon_col]],
        radius=5,
        color=cluster_colors[int(row["Cluster"]) % len(cluster_colors)],
        fill=True,
        fill_opacity=0.7,
        popup=f"Cluster {row['Cluster']}"
    ).add_to(m)

# 지도 출력
st.subheader("🌍 군집 결과 지도")
st_folium(m, width=700, height=500)
