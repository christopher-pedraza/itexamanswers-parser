import json

def check_questions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        questions = json.load(file)
        
        for question in questions:
            if question['answers'] is None:
                print("No answers for question: ", question['question'])
            elif not any(answer['is_correct'] for answer in question['answers']):
                print("All incorrect answers for question: ", question['question'])

if __name__ == "__main__":
    file_path = './ccna_1_final_exam.json'  # Replace with the path to the JSON file
    check_questions(file_path)
