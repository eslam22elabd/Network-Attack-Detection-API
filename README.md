# Network Attack Detection API 🛡️

A FastAPI-based application that uses Machine Learning to detect network attacks in real-time.

## 🚀 Features
- **Real-time Prediction**: Classifies network traffic as Benign or specific attack types (DoS, Exploits, Reconnaissance, etc.).
- **Confidence Score**: Returns the probability of the prediction along with full class probabilities.
- **REST API**: Simple and fast interface built with FastAPI.

## 🛠️ Installation

1. **Install dependencies:**
   
   ```bash
   download anaconda
   python==3.14.0
   pip install -r requirments.txt
   ```
## You must put all files in same directory
## 🏃‍♂️ Usage

Run the server using uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### `POST /detection-attack`

Detects the type of network attack based on traffic features.

**Input Sample (JSON):**
```json
{
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
```

**Response Sample:**
```json
{
  "prediction": {
    "attack_type": "Benign",
    "confidence_percentage": "98.5%"
  }
}
```

## 📊 Features Used
The model uses the following network flow features:
- `duration`
- `protocol_tcp`, `protocol_udp`
- `src_port`, `dst_port`
- `orig_bytes`, `resp_bytes`
- `orig_pkts`, `resp_pkts`
- `bytes_per_second`, `packets_per_second`
- `packet_length_mean`, `packet_length_std`
76: 
77: ## ⚠️ Note on Data Files
78: The raw dataset file `Data/CICFlowMeter.csv` is approximately 2GB in size and is excluded from this repository via `.gitignore` to comply with GitHub's file size limits and to optimize repository performance. 
79: 
80: However, the processed datasets and sampling logic are included in the `Data/` and `notebooks/` folders respectively, allowing for full reproducibility of the model training process.
