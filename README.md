# ML-Based SOC: Web Attack Detection System

## Overview

This project is a Machine Learning-based Security Operations Center (SOC) system designed to detect web attacks such as SQL Injection (SQLi) and Cross-Site Scripting (XSS), including obfuscated inputs.

---

## Highlights

* Achieved ~99% accuracy in attack detection
* Detects obfuscated XSS using character-level n-grams
* Real-time logging with IP and geolocation
* Visualization of global attack patterns

---

## Approach

### Preprocessing

* Basic filtering for normal inputs
* Removal of HTML tags to handle obfuscated payloads

### Feature Extraction

* Word-level n-grams → detect SQL injection patterns
* Character-level n-grams → detect obfuscated XSS attacks
* TF-IDF vectorization

### Model

* Multinomial Logistic Regression
* Classes: Normal, SQL Injection, XSS

---

## Results

* Accuracy: **~99%**
* High precision, recall, and F1-score

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

* Detects SQL Injection and XSS attacks
* Handles obfuscated payloads
* Logs attacker details:

  * IP address
  * Geolocation
  * Timestamp
  * Proxy/VPN detection
* Real-time attack visualization

---

## Tech Stack

* Python
* Flask
* Scikit-learn
* TF-IDF Vectorizer
* N-grams

---

## How to Run

```bash
git clone https://github.com/RevanthSai24/ml-soc-attack-detection.git
cd ml-soc-attack-detection
pip install -r requirements.txt
python init_db.py
python app.py
```

### Access

* API: http://127.0.0.1:5000/predict
* Map: http://127.0.0.1:5000/attack-map

---

## Public Access (ngrok)

By default, the app runs on localhost, so geolocation may not work.

To enable real-world testing:

```bash
ngrok http 5000
```

This allows:

* External access
* Real IP detection
* Accurate map visualization

---

## Testing

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/predict" `
-Method POST `
-Body '{"username":"admin'' OR 1=1--","password":"test"}' `
-ContentType "application/json"
```

---

## Dataset

Custom dataset including normal, SQLi, and XSS payloads with obfuscation.

---

## Future Improvements

* Deep learning models (LSTM/Transformers)
* Adversarial attack resistance
* Real traffic integration

---

## Author

**Chadive Revanth Sai Reddy**
