import requests
from bs4 import BeautifulSoup
import json

# Load HTML content from the URL
url = "https://itexamanswers.net/cyberops-associate-version-1-0-final-exam-answers.html"
response = requests.get(url)
response.raise_for_status()  # Check for HTTP errors

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, "lxml")

# Initialize list to store questions
questions_data = []
stop_parsing = False

# Loop through <p> tags to identify questions
for question in soup.find_all("p"):
    # Check if we've reached an unrelated section and should stop parsing
    if question.find_previous("nav", {"class": "navigation post-navigation"}) or \
       question.find_previous("div", {"id": "comments", "class": "comments-area"}) or \
       question.find_previous("div", {"class": "wpdiscuz_top_clearing"}):
        stop_parsing = True
    
    # Skip parsing if we've reached the stop point
    if stop_parsing:
        continue
    
    strong_tag = question.find("strong")
    if strong_tag and "Explanation" not in strong_tag.text:
        # Extract question text
        question_text = strong_tag.get_text(strip=True)
        
        # Default values
        answers = []
        explanation = None
        images = []

        # Loop through everything following this question to gather answers and images
        for sibling in question.find_all_next():
            # Stop if we reach a new question or an unrelated section
            if sibling.name == "p" and sibling.find("strong") and "Explanation" not in sibling.text:
                break
            if sibling.find_previous("nav", {"class": "navigation post-navigation"}) or \
               sibling.find_previous("div", {"id": "comments", "class": "comments-area"}) or \
               sibling.find_previous("div", {"class": "wpdiscuz_top_clearing"}):
                stop_parsing = True
                break

            # Collect answers if we encounter an <ul> list
            if sibling.name == "ul":
                for li in sibling.find_all("li"):
                    answer_text = li.get_text(strip=True)
                    # Check if this answer is correct by examining the <span> tag color
                    span_tag = li.find("span", style=True)
                    is_correct = False
                    if span_tag:
                        style = span_tag['style'].lower()
                        if "color: rgb(255, 0, 0)" in style or "color: #ff0000" in style:
                            is_correct = True
                    answers.append({
                        "answer": answer_text,
                        "is_correct": is_correct
                    })

            # Collect images if they are in <img> tags
            if sibling.name == "p" and sibling.find("img"):
                img_tag = sibling.find("img")
                if img_tag:
                    images.append(img_tag["src"])
                    print(f"Image found for question '{question_text}': {img_tag['src']}")  # Debug print

            # Collect explanation if available
            if sibling.name == "div" and "message_box success" in sibling.get("class", []):
                explanation = sibling.get_text(strip=True)

        # Append the parsed question data, ensuring all fields are present
        questions_data.append({
            "question": question_text,
            "answers": answers if answers else None,
            "explanation": explanation,
            "images": images if images else None  # Store images as a list
        })

# Save to JSON file
with open("questions_data.json", "w", encoding="utf-8") as json_file:
    json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

print("Data saved to questions_data.json")
