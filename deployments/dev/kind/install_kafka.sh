#!/bin/bash

# kubectl create namespace kafka
# kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
# kubectl wait --for=condition=Established --timeout=60s crd/kafkas.kafka.strimzi.io

# kubectl apply -f manifests/kafka-e11b.yaml

kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -

# 1. Operator + CRDs
kubectl apply -n kafka -f https://strimzi.io/install/latest?namespace=kafka

# 2. Block until operator fully rolled out (max 2 min)
kubectl rollout status -n kafka deployment/strimzi-cluster-operator --timeout=120s

# 3. Apply your Kafka cluster custom resource
kubectl apply -n kafka -f manifests/kafka-e11b.yaml