from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import joblib
import pandas as pd
import os

base_router = APIRouter()

# Determining the path of the artifacts
ARTIFACTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'artifacts')

# Loading pipeline, model, and label encoder
pipeline = joblib.load(os.path.join(ARTIFACTS_PATH, 'pipeline.pkl'))
model = joblib.load(os.path.join(ARTIFACTS_PATH, 'Random_forest.pkl'))
label_encoder = joblib.load(os.path.join(ARTIFACTS_PATH, 'label_encoder.pkl'))

print("✅ Models loaded successfully!")


# Pydantic model for input data
class NetworkTrafficInput(BaseModel):
    duration: float
    protocol_tcp: int
    protocol_udp: int
    src_port: int
    dst_port: int
    orig_bytes: float
    resp_bytes: float
    orig_pkts: int
    resp_pkts: int
    bytes_per_second: float
    packets_per_second: float
    packet_length_mean: float
    packet_length_std: float

    class Config:
        json_schema_extra = {
            "example": {
                "duration": 1000.0,
                "protocol_tcp": 1,
                "protocol_udp": 0,
                "src_port": 443,
                "dst_port": 8080,
                "orig_bytes": 5000.0,
                "resp_bytes": 3000.0,
                "orig_pkts": 10,
                "resp_pkts": 8,
                "bytes_per_second": 500.0,
                "packets_per_second": 5.0,
                "packet_length_mean": 250.0,
                "packet_length_std": 50.0
            }
        }


@base_router.post('/detection-attack')
async def detection_attack(data: NetworkTrafficInput):
    """
   Endpoint for network attack detection

     Receives network traffic data and returns the attack type along 
     with a confidence level.
    """
    try:
        # Convert the input to a DataFrame
        input_data = pd.DataFrame([{
            'duration': data.duration,
            'protocol_tcp': data.protocol_tcp,
            'protocol_udp': data.protocol_udp,
            'src_port': data.src_port,
            'dst_port': data.dst_port,
            'orig_bytes': data.orig_bytes,
            'resp_bytes': data.resp_bytes,
            'orig_pkts': data.orig_pkts,
            'resp_pkts': data.resp_pkts,
            'bytes_per_second': data.bytes_per_second,
            'packets_per_second': data.packets_per_second,
            'packet_length_mean': data.packet_length_mean,
            'packet_length_std': data.packet_length_std
        }])
        
        # Apply the preprocessing pipeline
        input_transformed = pipeline.transform(input_data)
        
        # Make prediction
        prediction_encoded = model.predict(input_transformed)[0]
        prediction_proba = model.predict_proba(input_transformed)[0]
        
        # Converting the prediction to the original label
        predicted_label = label_encoder.inverse_transform([prediction_encoded])[0]
        
        # Calculating the confidence
        confidence = float(prediction_proba[prediction_encoded] * 100)
        
        # Returning the result
        return {
            "prediction": {
                "attack_type": predicted_label,
                "confidence_percentage": f"{round(confidence, 2)}%"
            },

        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }