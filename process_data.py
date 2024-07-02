import os
import pandas as pd


def process_csv_files(folder_path):
    print('Processing folder:', folder_path)
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            try:
                data = pd.read_csv(file_path)
                for index, row in data.iterrows():
                    answer_start = row['raw_response'].find('My Final Answer')
                    answer = row['raw_response'][answer_start:].lower()
                    # "anti_stereotype","stereotype","unrelated"
                    if row['anti_stereotype'].lower() in answer:
                        data.loc[index, 'response'] = row['anti_stereotype']
                    elif row['stereotype'].lower() in answer:
                        data.loc[index, 'response'] = row['stereotype']
                    elif row['unrelated'].lower() in answer:
                        data.loc[index, 'response'] = row['unrelated']
                    else:
                        print('Error:', row['index'])
                        data.loc[index, 'response'] = 'no answer'
                # del data['raw_response']
                data.to_csv(file_path, index=False)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

main_folder_path = 'results'
for folder in os.listdir(main_folder_path):
    folder_path = os.path.join(main_folder_path, folder)
    process_csv_files(folder_path)
