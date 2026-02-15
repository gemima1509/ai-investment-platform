import numpy as np
import pickle
import yfinance as yf
from tensorflow.keras.models import load_model

# Load model
model = load_model("lstm_model.h5")

# Load scaler
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)


def predict_stock(ticker):
    # Download latest data
    df = yf.download(ticker, period="120d")
    
    if df.empty:
        return None

    data = df["Close"].values.reshape(-1, 1)

    # Scale using saved scaler
    scaled_data = scaler.transform(data)

    # Use last 90 days
    last_90 = scaled_data[-90:]
    X_input = np.reshape(last_90, (1, 90, 1))

    # Predict
    prediction = model.predict(X_input)
    predicted_price = scaler.inverse_transform(prediction)[0][0]

    current_price = data[-1][0]

    risk = abs(predicted_price - current_price) / current_price
    confidence = max(0, 1 - risk)

    decision = "BUY" if predicted_price > current_price else "SELL"

    return {
        "stock": ticker,
        "current_price": round(float(current_price), 2),
        "predicted_price": round(float(predicted_price), 2),
        "risk": round(float(risk), 4),
        "confidence": round(float(confidence), 2),
        "decision": decision
    }