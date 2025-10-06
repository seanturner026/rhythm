_default:
  @just --list

alias b := build
[doc('docker build')]
build:
  @docker build -t rhythm .

alias s := serve
[doc('docker compose up')]
serve:
  @docker compose up api mlflow

alias p := predict
[doc('make simple prediction')]
predict:
  @curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{"feature_1": 1.0, "feature_2": 2.0, "feature_3": 3.0, "feature_4": 4.0}'
