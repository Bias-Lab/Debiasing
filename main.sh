#!/bin/bash

# Llama3
echo "/bye" | ollama run llama3
export MODEL=llama3
nohup python3 main.py --mode=local &

pid=$!
wait $pid
echo "Running llama3 done"

git add .
git commit -m "add llama3 data no shot"

# Mistral
echo "/bye" | ollama run mistral
export MODEL=mistral
nohup python3 main.py --mode=local &

pid=$!
wait $pid
echo "Running mistral done"

git add .
git commit -m "add mistral data no shot"

# Gemma
echo "/bye" | ollama run gemma
export MODEL=gemma
nohup python3 main.py --mode=local &

pid=$!
wait $pid
echo "Running gemma done"

git add .
git commit -m "add gemma data no shot"

# Post process
export MODEL=llama3
python review.py

git add .
git commit -m "add review data change"

git push origin main