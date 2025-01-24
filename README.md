```shell
uv venv
uv pip compile requirements/base.in > requirements/requirements.txt
uv pip install -r requirements/requirements.txt

source .venv/bin/activate
python3 -m rhythm.pipelines.train

docker build -t rhythm .
docker compose up

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
