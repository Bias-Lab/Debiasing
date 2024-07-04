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
datasets = ['stereoset']
models = ['llama3', 'mistral', 'gemma']

types = ['without_system_2', 'without_debiasing', 'without_cot', 'all_together', 'without_detailed_cot', 'without_persona']

for model in models:
    for dataset in datasets:
        dataset_path = f'results/{model}/{dataset}.csv'
        dataset = pd.read_csv(dataset_path)

        for col, data in tqdm(dataset.iterrows(), total=len(dataset), desc="Processing"):
            option_list = [str(data['anti_stereotype']), str(data['stereotype']), str(data['unrelated'])]
            random.shuffle(option_list)
            for type in types:
                prompt = prompt_template.create_review_prompt(data[f'{type}-raw_response'], option_list)
                response = generate_review_local(review_model, prompt).strip('"').strip('"""')
                dataset.at[col, f'{type}-response'] = response

        dataset.to_csv(dataset_path, quoting=csv.QUOTE_NONNUMERIC, index=False)


