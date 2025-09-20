_default:
  @just --list

alias b := build
[doc('docker build')]
build:
  @docker build -t rhythm .

alias m := mlflow-server
[doc('mlflow server')]
mlflow-server:
  @uv run mlflow server

alias s := serve
[doc('docker compose up')]
serve:
  @docker compose up api mlflow

alias p := predict
[doc('make simple prediction')]
predict:
  @curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2 }'

