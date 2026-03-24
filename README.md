# ML-Based SOC: Web Attack Detection System

Overview
This project is a Machine Learning-based Security Operations Center (SOC) system designed to detect web attacks such as SQL Injection (SQLi) and Cross-Site Scripting (XSS), including obfuscated inputs.

---
## Highlights
- Achieved ~99% accuracy in attack detection  
- Detects obfuscated XSS using character-level n-grams  
- Real-time logging with IP and geolocation  
- Visualization of global attack patterns  

---

## Approach

### 1. Preprocessing
- Basic filtering for normal inputs
- Removal of HTML tags to handle obfuscated payloads

### 2. Feature Extraction
- Word-level n-grams → detect SQL injection patterns  
- Character-level n-grams → detect obfuscated XSS attacks  
- TF-IDF vectorization to convert text into numerical features  

### 3. Model
- Multinomial Logistic Regression classifier  
- Classes:
  - Normal  
  - SQL Injection  
  - XSS  

---

## Results

- Accuracy: **~99%**
- High precision, recall, and F1-score across all classes  

---

## Model Performance

Confusion Matrix
## <img width="555" height="449" alt="confusion_matrix" src="https://github.com/user-attachments/assets/fc30257b-c323-4b5e-a8db-a105ef38c9e7" />

### Insights
- Very low misclassification across all classes  
- Strong detection of obfuscated XSS payloads  
- Minor confusion between normal and SQL inputs  

---

## Features

- Detects SQL Injection and XSS attacks  
- Handles obfuscated attack payloads  
- Logs attacker details:
  - IP address  
  - Geolocation  
  - Timestamp  
  - Proxy/VPN detection  
- Real-time visualization of global attack patterns  

---

## Tech Stack
- Python  
- Scikit-learn  
- Flask  
- TF-IDF Vectorizer  
- N-grams  

---

## Dataset
- Custom dataset of normal, SQL injection, and XSS payloads  
- Includes obfuscated attack samples for robust detection  

---

## Future Improvements
- Deep learning models (LSTM/Transformers)  
- Adversarial attack resistance  
- Integration with real-world traffic logs  

---

## Author
**Chadive Revanth Sai Reddy**
