import sys
import json
import os
from process_pdf import process_pdf

def get_pdf_files(input_dir):
    return [f for f in os.listdir(input_dir) if f.endswith('.pdf')]

def get_json_files(output_dir):
    return [f.replace('.json', '') for f in os.listdir(output_dir) if f.endswith('.json')]

if __name__ == '__main__':
    input_dir = 'database/input'
    output_dir = 'database/output'

    pdf_files = get_pdf_files(input_dir)
    json_files = get_json_files(output_dir)

    for pdf_file in pdf_files:
        pdf_name = os.path.splitext(pdf_file)[0]
        if pdf_name not in json_files:
            pdf_file_path = os.path.join(input_dir, pdf_file)
            output_file_path = os.path.join(output_dir, f'{pdf_name}.json')
            data = process_pdf(pdf_file_path)
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f'Processed {pdf_file} and saved to {output_file_path}')
        else:
            print(f'Skipping {pdf_file}, corresponding JSON file already exists.')
