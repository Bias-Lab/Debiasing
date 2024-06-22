#!/bin/bash

# Llama3
echo "/bye" | ollama run llama3
export MODEL=llama3
nohup python3 main.py --mode=local &
echo "Running llama3 done"

pid=$!

wait $pid

git add .
git commit -m "add llama3 data"

# Gemma
echo "/bye" | ollama run gemma
export MODEL=gemma
nohup python3 main.py --mode=local &
echo "Running gemma done"

pid=$!

wait $pid

git add .
git commit -m "add gemma data"

# Mistral
echo "/bye" | ollama run mistral
export MODEL=mistral
nohup python3 main.py --mode=local &
echo "Running mistral done"

pid=$!
wait $pid

git add .
git commit -m "add mistral data"

# Phi3
echo "/bye" | ollama run phi3
export MODEL=phi3
nohup python3 main.py --mode=local &
echo "Running phi3 done"

pid=$!
wait $pid

git add .
git commit -m "add phi3 data"

# Qwen2
echo "/bye" | ollama run qwen2
export MODEL=qwen2
nohup python3 main.py --mode=local &
echo "Running qwen2 done"

pid=$!
wait $pid

git add .
git commit -m "add mistral data"

# Commit the changes and push to github
git push origin main

