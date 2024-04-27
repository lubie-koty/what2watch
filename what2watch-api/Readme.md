# API Setup

## Movie recommender needs the dataset inside of the data folder (https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset/data)

## Crucial files are: movies_metadata.csv, credits.csv, keywords.csv

# Running the API

```shell
poetry run uvicorn app.main --host 0.0.0.0 --port 5000
```
