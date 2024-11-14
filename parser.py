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

# Set flag to indicate when to stop parsing
stop_parsing = False

# Loop through <p> tags to identify questions
for question in soup.find_all("p"):
    # Check if we're entering an unrelated section
    if question.find_previous("nav", {"class": "navigation post-navigation"}) or \
       question.find_previous("div", {"id": "comments", "class": "comments-area"}) or \
       question.find_previous("div", {"class": "wpdiscuz_top_clearing"}):
        stop_parsing = True
    
    # Skip parsing if we've reached the stop point
    if stop_parsing:
        continue
    
    strong_tag = question.find("strong")
    if strong_tag and "Explanation" not in strong_tag.text:
        next_sibling = question.find_next_sibling()
        if next_sibling and next_sibling.name == "ul":
            question_text = strong_tag.get_text(strip=True)
            
            # Extract answers
            answers = []
        
            for li in next_sibling.find_all("li"):
                answer_text = li.get_text(strip=True)
                # Check for the span tag inside any child of li (even inside a <b>)
                span_tag = li.find("span", style=True)

                # Check if the color is correct, handling both color formats
                is_correct = False

                if span_tag:
                    # Get the style attribute
                    style = span_tag['style'].lower()

                    # Check for both possible color formats
                    if "color: rgb(255, 0, 0)" in style or "color: #ff0000" in style:
                        is_correct = True
                
                answers.append({
                    "answer": answer_text,
                    "is_correct": is_correct
                })
              
            
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
                "explanation": explanation,
                "image": image_src
            })

# Save to JSON file
with open("questions_data.json", "w", encoding="utf-8") as json_file:
    json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

print("Data saved to questions_data.json")
