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

# Open a debug log file
debug_file = open("debug_log.txt", "w", encoding="utf-8")

# Debugging helper function
def debug_element(tag, prefix=""):
    """Writes tag name and its content to the debug log."""
    debug_file.write(f"{prefix}DEBUG: Tag: {tag.name}, Content: {tag.get_text(strip=True)[:50]}\n")

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

    # Debugging: Check current <p> tag content
    debug_element(question)

    # Check if the paragraph contains a question based on typical content structure
    if question.find("strong") and "Explanation" not in question.text:
        # Extract question text
        question_text = question.get_text(strip=True)
        
        # Debugging: Write detected question to log
        debug_file.write(f"DEBUG: Detected question: {question_text}\n")

        # Default values
        answers = []
        explanation = None
        images = []

        # Loop through all following elements to gather answers, images, and explanation
        for sibling in question.find_all_next():
            # Stop if we reach a new question or an unrelated section
            if sibling.name == "p" and sibling.find("strong") and "Explanation" not in sibling.text:
                break
            if sibling.find_previous("nav", {"class": "navigation post-navigation"}) or \
               sibling.find_previous("div", {"id": "comments", "class": "comments-area"}) or \
               sibling.find_previous("div", {"class": "wpdiscuz_top_clearing"}):
                stop_parsing = True
                break

            # Debugging: Write sibling content being processed
            debug_element(sibling, "    ")

            # Collect answers if in <ul> list
            if sibling.name == "ul":
                for li in sibling.find_all("li"):
                    answer_text = li.get_text(strip=True)
                    # Check if this answer is correct by examining the <span> tag color
                    span_tag = li.find("span", style=True)
                    is_correct = False
                    if span_tag and "style" in span_tag.attrs:
                        style = span_tag['style'].lower()
                        if "color: rgb(255, 0, 0)" in style or "color: #ff0000" in style:
                            is_correct = True
                    answers.append({
                        "answer": answer_text,
                        "is_correct": is_correct
                    })

            # Collect answers if in <p> tags with <br> elements
            if sibling.name == "p" and sibling.find("br"):
                answer_lines = sibling.get_text(strip=True).split("\n")
                for line in answer_lines:
                    answer_text = line.strip()
                    if answer_text:
                        # Check if this answer is correct by examining inline styles
                        span_tag = sibling.find("span", style=True)
                        is_correct = False
                        if span_tag and "style" in span_tag.attrs:
                            style = span_tag['style'].lower()
                            if "color: rgb(255, 0, 0)" in style or "color: #ff0000" in style:
                                is_correct = True
                        answers.append({
                            "answer": answer_text,
                            "is_correct": is_correct
                        })

            # Collect images
            if sibling.name == "img":
                images.append(sibling["src"])

            # Extract explanation when encountering a div with class "message_box success"
            if sibling.name == "div" and "message_box" in sibling.get("class", []) and "success" in sibling.get("class", []):
                explanation = sibling.get_text(strip=True)
                # Write explanation to debug
                debug_file.write(f"DEBUG: Detected explanation: {explanation}\n")
                break  # Explanations are unique per question, so we can stop looking for more explanations.

        # Append the parsed question data, ensuring all fields are present
        questions_data.append({
            "question": question_text,
            "answers": answers if answers else None,
            "explanation": explanation,
            "images": images if images else None  # Store images as a list
        })

# Close debug file
debug_file.close()

# Save to JSON file
with open("questions_data.json", "w", encoding="utf-8") as json_file:
    json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

print("Data saved to questions_data.json and debug_log.txt")
