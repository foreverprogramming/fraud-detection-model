from fastapi import FastAPI, HTTPException, UploadFile, Response
import numpy as np
import pandas as pd
import random
import xgboost as xgb
import pickle

def load_data(path):
    df = pd.read_csv(path)
    if "TARGET" not in df.columns:
        raise KeyError("No existe la columna TARGET")

    X = df.drop(columns=["TARGET"])
    y = df["TARGET"].astype(int)

    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    return X, y, numeric_cols

app = FastAPI(title="NeoPay AntiFraude API", version="0.1.0")
model = pickle.load(open('src/model.pkl', 'rb'))

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_version": model.version,
    }

@app.get("/version")
def version():
    return {"model_version": model.version}

@app.post("/reload_model")
def reload_model():
    new_version = model.reload()
    return {"status": "reloaded", "model_version": new_version}

@app.post("/predict")
def predict(file: UploadFile):
    try:
        # ¡OJO! El orden debe coincidir con el usado al entrenar el modelo real
        df = pd.read_csv(file.file)
        df['ID'] = np.arange(len(df))
        df = df.set_index('ID')
        proba = model.predict_proba(df)
        label = [1 if p > 0.5 else 0 for p in proba[:, 1]]
        return Response(
            content = pd.DataFrame({"probability": proba[:, 1], "label": label}).to_csv(index=False),
            media_type="text/csv"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))