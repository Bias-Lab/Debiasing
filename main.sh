#!/bin/bash

# Llama3
echo "/bye" | ollama run llama3
export MODEL=llama3
nohup python3 main.py --mode=local &

pid=$!
wait $pid
echo "Running llama3 done"

git add .
git commit -m "add llama3 data"

# Mistral
echo "/bye" | ollama run mistral
export MODEL=mistral
nohup python3 main.py --mode=local &

pid=$!
wait $pid
echo "Running mistral done"

git add .
git commit -m "add mistral data"
