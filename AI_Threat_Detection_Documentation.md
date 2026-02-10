# Artificial Intelligence–Based Threat Detection

## 1. Introduction to the AI Component

● Core intelligence layer for real-time network traffic classification  
● Analyzes flow-based features to distinguish benign from malicious traffic  
● Enables pattern-based detection beyond traditional signature methods  
● Integrates with FastAPI to provide automated threat response capabilities

## 2. Problem Formulation

● Multi-class classification of network flows into 7 attack categories  
● Input: 13 flow-based numerical features (duration, protocols, bytes, packets, rates)  
● Output: Attack label with confidence percentage score  
● Target classes: Benign, DoS, Exploits, Fuzzers, Reconnaissance, Generic, Shellcode

## 3. Data Understanding and Sources

● Flow-based network data capturing bidirectional connection statistics  
● 10,000 Zeek-generated real network traffic samples  
● CIC-IDS2017 public intrusion detection dataset  
● Combined datasets ensure realistic training and production generalization

## 4. Selected Datasets

● CIC-IDS2017: 5-day network captures with modern attack scenarios  
● Covers DoS, DDoS, Brute Force, XSS, SQL Injection, Port Scan, Botnet  
● Sampled 10,000 Benign flows + all attack samples for balance  
● Zeek dataset (10,000 samples) merged for real-world validation

## 5. Unified Feature Schema

● 13 standardized features across all data sources  
● Features: duration, protocol_tcp, protocol_udp, src_port, dst_port, orig_bytes, resp_bytes, orig_pkts, resp_pkts, bytes_per_second, packets_per_second, packet_length_mean, packet_length_std  
● Column naming aligned with Zeek conventions  
● Fixed feature ordering enforced for consistent inference

## 6. Feature Engineering Process

● Selected 13 most informative features from 80+ original CIC-IDS2017 features  
● Removed timestamps, IP addresses, and redundant features  
● One-hot encoded Protocol field (6=TCP, 17=UDP) into binary features  
● Computed rate-based and statistical derived features  
● Applied StandardScaler for feature normalization

## 7. Label Processing and Class Definition

● Unified CIC-IDS2017 and Zeek label formats  
● Mapped attack subcategories to 7 main classes  
● Applied LabelEncoder for string-to-numeric conversion  
● Balanced dataset: 10,000 Benign + all attack samples  
● Ensured consistent label encoding/decoding across pipeline

## 8. Model Selection and Justification

● Evaluated Decision Trees, Random Forest, Gradient Boosting, Neural Networks  
● Selected Random Forest for tabular data performance  
● Provides feature importance and decision path interpretability  
● Robust to overfitting on imbalanced multi-class problems  
● Optimal balance of accuracy, speed, and explainability

## 9. Model Training Strategy

● 80-20 train-test split with stratification  
● Cross-validation for hyperparameter tuning  
● Optimized n_estimators, max_depth, min_samples_split, min_samples_leaf  
● Ensemble averaging prevents overfitting  
● Final model trained on full training set

## 10. Model Evaluation

● Metrics: Accuracy, Precision, Recall, F1-Score, Confusion Matrix  
● Per-class performance analysis via confusion matrix  
● High precision minimizes false positives for IPS deployment  
● High recall ensures comprehensive attack detection  
● Identified misclassification patterns for improvement

## 11. Model Output Design

● Predicted class decoded to human-readable attack label  
● Confidence score from predict_proba() probability distribution  
● Confidence >90%: high certainty; 70-90%: moderate; <70%: ambiguous  
● Configurable threshold for IPS decision-making  
● Full probability distribution returned for all classes

## 12. Real-Time Inference Integration

● Single-flow prediction in <100ms  
● Pydantic model validates input structure  
● Preprocessing pipeline ensures consistent feature scaling  
● Model loaded once at startup for low latency  
● Robust to typical network traffic variations

## 13. Deployment Interface

● RESTful FastAPI endpoint: POST /detection-attack  
● Input: JSON with 13 numerical features  
● Output: JSON with attack_type and confidence_percentage  
● Designed for SIEM and network monitoring tool integration  
● Error handling with descriptive status messages

## 14. Validation Using Real Network Traffic

● Merged 10,000 Zeek samples with CIC-IDS2017 for training  
● Validated predictions against known attack labels  
● Model maintains high accuracy on Zeek data  
● Demonstrates generalization beyond training distribution  
● Confirmed real-world applicability

## 15. Limitations of the AI Component

● Limited to attack types present in CIC-IDS2017 training data  
● Performance depends on similarity to training distribution  
● Requires complete flow information (may delay long-connection detection)  
● Potential vulnerability to adversarial evasion techniques  
● Novel attack patterns may not be detected

## 16. Contribution of the AI Module

● Detects complex attack patterns beyond rule-based systems  
● Reduces false positives through multi-feature analysis  
● Enables risk-based automated blocking via confidence scores  
● Transforms security from reactive to proactive behavioral analysis  
● Foundation for continuous learning and model improvement
