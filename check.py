import os
import json

def check_questions(folder_path):
    total_questions = 0
    valid_questions = 0
    file_results = {}

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                questions = json.load(file)
                
                file_total = 0
                file_valid = 0

                for question in questions:
                    total_questions += 1
                    file_total += 1
                    if question['answers'] is None:
                        print("No answers for question: ", question['question'])
                    elif not any(answer['is_correct'] for answer in question['answers']):
                        print("All incorrect answers for question: ", question['question'])
                    else:
                        valid_questions += 1
                        file_valid += 1

                file_results[file_name] = (file_valid, file_total)

    for file_name, (file_valid, file_total) in file_results.items():
        print(f"File: {file_name} - Valid questions: {file_valid}/{file_total}")

    best_file = max(file_results, key=lambda x: file_results[x][0])
    print(f"\nFile with the most valid questions: {best_file} ({file_results[best_file][0]}/{file_results[best_file][1]})")

if __name__ == "__main__":
    folder_path = './output/'  # Replace with the path to the folder containing JSON files
    check_questions(folder_path)
