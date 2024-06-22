import argparse
import pandas as pd
import random
import os
import csv
import re
from tqdm import tqdm

from dotenv import load_dotenv

from api.remote import generate_response_api
from api.local import generate_response_local
from prompt import prompt_template

load_dotenv()

parser = argparse.ArgumentParser(description='Run LLM locally or from an API provider')
parser.add_argument('--mode', choices=['local', 'remote'], default='remote', required=True,
                    help='Choose the mode to run the LLM')
args = parser.parse_args()

model = os.environ['MODEL']

datasets = ['data/stereoset.csv', 'data/beauty_dataset.csv']
types = [(True, False), (False, False), (True, True)]

for dataset_path in datasets:
    dataset = pd.read_csv(dataset_path)
    dataset = dataset[:1]
    dataset_name = dataset_path.split('/')[-1].split('.')[0]

    if 'beauty' in dataset_name:
        beauty = True
    else:
        beauty = False

    for few_shot, echo_shot in types:

        for col, data in tqdm(dataset.iterrows(), total=len(dataset), desc="Processing"):
            option_list = [str(data['anti_stereotype']), str(data['stereotype']), str(data['unrelated'])]
            random.shuffle(option_list)

            query = prompt_template.create_prompt(data['context'], option_list, few_shot=few_shot, echo_shot=echo_shot, beauty=beauty)
            try: 
                if args.mode == 'local':
                    response = generate_response_local(model, query)
                else:
                    response = generate_response_api(model, query)
                dataset.loc[col, 'raw_response'] = response

                match = re.search(r'My Final Answer: (.+)', response)
                if match:
                    final_answer = match.group(1)
                    dataset.loc[col, 'response'] = final_answer
                else:
                    dataset.loc[col, 'response'] = "error"
            except Exception as e:
                print("An error occurred", e)
                dataset.loc[col, 'response'] = "error"


        output_dir = f'results/{model}'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if few_shot:
            file_name = f'{output_dir}/few_shot_echo_shot_{dataset_name}.csv' if echo_shot else f'{output_dir}/few_shot_{dataset_name}.csv'
        else:
            file_name = f'{output_dir}/zero_shot_{dataset_name}.csv'
        dataset.to_csv(file_name, quoting=csv.QUOTE_NONNUMERIC)
