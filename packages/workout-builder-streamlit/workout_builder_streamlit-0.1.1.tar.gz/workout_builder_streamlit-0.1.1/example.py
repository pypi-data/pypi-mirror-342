import streamlit as st 
from workout_builder_streamlit import workout_builder

st.set_page_config(page_title="Workout Builder", page_icon=":weight_lifter:", layout="wide")

st.title("Workout Builder")
data = workout_builder()
st.line_chart(data)