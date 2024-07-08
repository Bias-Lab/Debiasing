import argparse
import pandas as pd
import random
import os
import csv
from tqdm import tqdm

from dotenv import load_dotenv

from api.local import generate_review_local
from prompt import prompt_template

load_dotenv()

review_model = os.environ['MODEL']

# datasets = ['data/stereoset.csv', 'data/beauty_dataset.csv']
datasets = ['few_shot_stereoset']
models = ['llama3', 'mistral']


for model in models:
    for dataset in datasets:
        dataset_path = f'results/{model}/{dataset}.csv'
        dataset = pd.read_csv(dataset_path)

        for col, data in tqdm(dataset.iterrows(), total=len(dataset), desc="Processing"):
            option_list = [str(data['anti_stereotype']), str(data['stereotype']), str(data['unrelated'])]

            random.shuffle(option_list)

            prompt = prompt_template.create_review_prompt(data[f'raw_response'], option_list)

            response = generate_review_local(review_model, prompt).strip('"').strip('"""')
            dataset.at[col, f'response'] = response

        dataset.to_csv(dataset_path, quoting=csv.QUOTE_NONNUMERIC, index=False)
