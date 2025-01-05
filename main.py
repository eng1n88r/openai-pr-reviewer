import os
import json
import openai
import requests
from github import Github
from flask import Flask, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_available_models():
    openai.organization = os.environ['OPENAI_ORG_ID']
    openai.api_key = os.environ['OPENAI_API_KEY']
    models = openai.Model.list()

    for model in models.data:
        print(model.id)


def get_file_content(file):
    if file.patch is not None:
        return file.patch
    elif file.status == "added":
        raw_file_response = requests.get(file.raw_url)
        raw_file_response.raise_for_status()
        return raw_file_response.text
    else:
        return None


app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_json()
    print(payload)
    return '', 200

    """
    if payload and payload.get('action') == 'opened':
        process_pull_request(payload)
    return '', 200
    """


def process_pull_request(payload):
    # 1. Authenticate with GitHub
    github_token = os.environ['GITHUB_TOKEN']
    g = Github(github_token)

    # 2. Select and access repositories
    user = g.get_user()
    repos = [repo for repo in user.get_repos()]

    # Select a repository (e.g., by name)
    selected_repo = next(repo for repo in repos if repo.name == 'bing_pointer')

    # 3. Monitor pull requests (PRs)
    # For this example, we'll just fetch existing PRs
    prs = selected_repo.get_pulls(state='open')

    # 4. Retrieve PR details and code changes
    for pr in prs:
        print(f"Processing PR {pr.number}: {pr.title}")

        # Retrieve PR details and code changes (diff)
        pr_diff = pr.get_files()

        # 5. Send code to Codex API
        # You'll need to set up your OpenAI API key first
        openai.api_key = os.environ['OPENAI_API_KEY']

        # code_changes = "\n".join([file.patch for file in pr_diff])
        code_changes = "\n".join([get_file_content(file) for file in pr_diff if get_file_content(file) is not None])
        # code_changes = "\n".join([file.patch for file in pr_diff if file.patch is not None])

        prompt = f"Review the following .NET code changes for best practices, performance, and potential issues:\n\n{code_changes}"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # 6. Process Codex API response
        feedback = response.choices[0].text.strip()

        # 7. Post feedback to the PR as a comment
        pr.create_issue_comment(feedback)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
