import os

import openai
from github import Github

g = Github(os.getenv("GITHUB_TOKEN"))
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_review_with_openai(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # use GPT-4 model
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant. Your job is to review the following diff and spot any bugs. Leave review comments so the author can fix their bugs."},
            {"role": "user", "content": text},
        ],
    )
    try:
        return response.choices[0].message['content']
    except Exception as e:
        raise Exception(f"Failed to get review with OpenAI {response}: {e}")

def reviewPR():
    repo = g.get_repo(f"{os.getenv('GITHUB_REPOSITORY')}")
    pr_number = os.getenv('GITHUB_REF').split('/')[-2]
    pr = repo.get_pull(int(pr_number))

    feedback = get_review_with_openai(pr.body)

    pr.create_review(body=feedback, event="COMMENT")


if __name__ == "__main__":
    reviewPR()
