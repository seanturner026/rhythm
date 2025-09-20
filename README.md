```shell
just b
just s
uv run python3 -m rhythm.pipelines.train

docker compose up mlflow
curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }'
{"prediction":"setosa"}%
```
