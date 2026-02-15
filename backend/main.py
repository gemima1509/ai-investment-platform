from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once when server starts
import os
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "lstm_model.h5")

model = load_model(MODEL_PATH)


@app.get("/")
def home():
    return {"message": "AI Investment Backend Running"}


@app.get("/analyze/{stock}")
def analyze(stock: str):

    # Download stock data
    df = yf.download(stock, period="5y", progress=False)

    if df is None or df.empty:
        return {"error": "Invalid stock symbol"}

    data = df[['Close']]

    # Scale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    X = []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i - 60:i])

    if len(X) == 0:
        return {"error": "Not enough data"}

    X = np.array(X)
    X_input = X[-1].reshape(1, 60, 1)

    # Predict
    predicted_scaled = model.predict(X_input)
    predicted_price = scaler.inverse_transform(predicted_scaled)[0][0]

    current_price = data.values[-1][0]

    # Basic risk calculation
    prices = data.values.flatten()
    returns = np.diff(prices) / prices[:-1]
    risk = float(np.std(returns))

    # Simple decision logic
    if predicted_price > current_price:
        decision = "BUY"
    else:
        decision = "SELL"

    confidence = float((predicted_price - current_price) / current_price * 100)

    return {
        "stock": stock.upper(),
        "current_price": round(float(current_price), 2),
        "predicted_price": round(float(predicted_price), 2),
        "risk": round(risk, 4),
        "confidence": round(confidence, 2),
        "decision": decision
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)