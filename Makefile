MLFLOW_HOST = 127.0.0.1
MLFLOW_PORT = 8000
MLFLOW_LOCAL_FOLDER = ./data/mlflow

.PHONY: clean-all clean run server

clean-all:
	rm -r -f data/*

clean:
	rm -r -f ./data/*/experiments

run:
	python main.py --parallel=1

server:
	mlflow server \
	--host $(MLFLOW_HOST) \
	--port $(MLFLOW_PORT) \
	--backend-store-uri $(MLFLOW_LOCAL_FOLDER)