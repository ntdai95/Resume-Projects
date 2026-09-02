import requests
import streamlit as st


API = "http://127.0.0.1:8000"
st.title("Ocean Data ML Platform with RAG")
tab1, tab2, tab3 = st.tabs(["Forecast", "Search", "Ask"])
with tab1:
    st.header("Forecast")
    hour = st.slider("Hour", 0, 23, 12)
    day = st.slider("Day of Year", 1, 365, 150)
    lag1 = st.number_input("Lag 1", value=13.0)
    lag3 = st.number_input("Lag 3", value=13.0)
    lag6 = st.number_input("Lag 6", value=13.0)
    if st.button("Predict"):
        r = requests.post(f"{API}/predict", json={"hour": hour, "dayofyear": day, "lag_1": lag1, 
                                                  "lag_3": lag3, "lag_6": lag6})
        st.json(r.json())

with tab2:
    query = st.text_input("Search query")
    if st.button("Search"):
        r = requests.get(f"{API}/search", params={"q": query})
        st.json(r.json())

with tab3:
    question = st.text_input("Ask a question")
    if st.button("Ask"):
        r = requests.post(f"{API}/ask", json={"question": question})
        st.json(r.json())