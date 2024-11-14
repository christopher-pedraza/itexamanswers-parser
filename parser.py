from bs4 import BeautifulSoup

# Load the HTML file
with open("html-files/CyberOps Associate (version 1.0) - Course Final Exam Answers.html", "r", encoding="utf-8") as file:
    content = file.read()

soup = BeautifulSoup(content, "lxml")

# Initialize list to store questions
questions_data = []

# Loop through <p> tags to identify questions
for question in soup.find_all("p"):
    strong_tag = question.find("strong")
    if strong_tag:
        # Check if the <p><strong> is followed by a <ul>, indicating a question
        next_sibling = question.find_next_sibling()
        if next_sibling and next_sibling.name == "ul":
            question_text = strong_tag.get_text(strip=True)
            
            # Extract answers
            answers = []
            correct_answer = None
            for li in next_sibling.find_all("li"):
                answer_text = li.get_text(strip=True)
                answers.append(answer_text)
                # Check for the correct answer based on color styling
                if li.find("span", style="color: rgb(255, 0, 0);"):
                    correct_answer = answer_text
            
            # Extract explanation if available
            explanation_div = question.find_next("div", class_="message_box success")
            explanation = explanation_div.get_text(strip=True) if explanation_div else None
            
            # Extract associated image if available
            image_tag = question.find_next("img")
            image_src = image_tag["src"] if image_tag else None
            
            # Append the parsed question data
            questions_data.append({
                "question": question_text,
                "answers": answers,
                "correct_answer": correct_answer,
                "explanation": explanation,
                "image": image_src
            })

# Example output
for q in questions_data:
    print(f"Question: {q['question']}")
    print(f"Answers: {q['answers']}")
    print(f"Correct Answer: {q['correct_answer']}")
    print(f"Explanation: {q['explanation']}")
    print(f"Image: {q['image']}")
    print("-----")
