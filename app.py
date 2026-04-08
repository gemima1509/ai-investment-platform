import streamlit as st

st.set_page_config(
    page_title="NexusTrade",
    page_icon="📈"
)





import streamlit as st
import numpy as np
import joblib
from tensorflow.keras.models import load_model
#Load Model and Scaler
model = load_model("backend/lstm_model.h5")
scaler = joblib.load("backend/scaler.pkl")
st.title("NexusTrade AI Dashboard")
st.write("Enter last 90 days stock values (comma separated):")
user_input = st.text_area("Stock Data (90 values)")
if st.button("Predict"):
  try:
    values = list(map(float, user_input.split(",")))
    if len(values) != 90:
        st.error("Please enter exactly 90 values.")
  else:
       data = np.array(values).reshape(-1,1)
       scaled = scaler.transform(data)
       scaled = scaled.reshape(1, 90, 1)
       prediction = model.predict(scaled)
       prediction = scaler.inverse_transform(prediction)
       st.success(f"Predicted Next Value: {prediction[0][0]: 2f}")
  except:
      st.error("Invalid input. Please enter numbers separated by commas.")
