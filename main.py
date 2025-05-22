import sys
import re
import requests
import json

def extract_quiz_id(quiz_url: str) -> str:
    match = re.search(r'/quiz/([a-zA-Z0-9]+)', quiz_url)
    if not match:
        raise ValueError("Unable to extract quiz ID from URL.")
    return match.group(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <quiz_url>")
        sys.exit(1)

    quiz_url = sys.argv[1]
    try:
        quiz_id = extract_quiz_id(quiz_url)
    except ValueError as e:
        print(e)
        sys.exit(1)

    api_url = f"https://quizizz.com/_quizserver/main/v2/quiz/{quiz_id}?convertQuestions=false&includeFsFeatures=true&sanitize=read&questionMetadata=true&includeUserHydratedVariants=true"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            quiz = data.get("data", {}).get("quiz", {})
            created_by = quiz.get("createdBy", {})
            info = quiz.get("info", {})
            print("\n=== Quiz creator ===")
            print(f"ID: {created_by.get('_id')}")
            print(f"First name: {created_by.get('firstName')}")
            print(f"Last name: {created_by.get('lastName')}")
            print(f"Email: {created_by.get('email')}")
            print(f"Country: {created_by.get('country')}")
            print(f"Occupation: {created_by.get('occupation')}")
            print(f"User profile: https://quizizz.com/profile/{created_by.get('_id')}?section=library")
            print(f"Quiz language: {info.get('lang')}")
            print(f"Google profile image: {created_by.get('media')}")
        except json.JSONDecodeError:
            print("Error: response is not valid JSON.")
    else:
        print(f"HTTP error {response.status_code} during request.")

if __name__ == "__main__":
    main()
