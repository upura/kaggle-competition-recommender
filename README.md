# Kaggle Competition Reccomender

![demo](demo.gif)

## Environment

```bash
source env/bin/activate
pip install -r requirements.txt
streamlit run kaggler-ja-faq/kaggler-ja-faq.py
```

## Data

https://www.kaggle.com/sishihara/competition-recommendation-by-matrix-factorization

## Recommend algorithm

- Non-Negative Matrix Factorization (NMF) by [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html)
- Target values are whether a user participates in a competition.
