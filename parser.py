import requests
from bs4 import BeautifulSoup
import json

# Load HTML content from the URL
url = "https://itexamanswers.net/cyberops-associate-version-1-0-final-exam-answers.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Data extraction parameters
questions_data = []
parsing_questions = False  # Start parsing only after detecting actual question format

# Loop through <p> tags and detect questions accurately
for element in soup.find_all(["p", "ul", "div"]):
    # Detect the start of questions section by finding the first <p><strong> that appears as a question
    if element.name == "p" and element.find("strong") and not parsing_questions:
        parsing_questions = True  # Start parsing questions after this point

    # Skip elements until the question section starts
    if not parsing_questions:
        continue

    # Initialize variables for each question
    if element.name == "p" and element.find("strong"):
        # Detect question
        question_text = element.get_text(strip=True)
        answers = []
        correct_answer = None
        explanation = None
        image_url = None

        # Check for an image after the question (if any)
        next_sibling = element.find_next_sibling()
        if next_sibling and next_sibling.name == "img":
            image_url = next_sibling["src"]

        # Locate the answer <ul> and parse each <li> as an answer option
        answer_list = element.find_next("ul")
        if answer_list:
            for li in answer_list.find_all("li"):
                answer_text = li.get_text(strip=True)
                # Check for the correct answer by red color style
                if "color: rgb(255, 0, 0)" in str(li):
                    correct_answer = answer_text
                answers.append(answer_text)

        # Extract explanation in the following <div> with the success class
        explanation_div = element.find_next("div", class_="message_box success")
        if explanation_div:
            explanation = explanation_div.get_text(strip=True)

        # Append question data to the list
        questions_data.append({
            "question": question_text,
            "answers": answers,
            "correct_answer": correct_answer,
            "explanation": explanation,
            "image": image_url
        })

# Save parsed data to a JSON file
with open("parsed_questions.json", "w", encoding="utf-8") as file:
    json.dump(questions_data, file, indent=4, ensure_ascii=False)

print("Data has been parsed and saved to 'parsed_questions.json'")