# OpenAI PR Reviewer

OpenAI PR Reviewer is a Python-based web application that utilizes OpenAI's Codex to review GitHub pull requests for best practices, performance, and potential issues. It integrates with GitHub to automatically process and review pull requests.

## Features
- Authenticate with GitHub
- Select and access repositories
- Monitor and retrieve pull requests
- Review code changes using OpenAI Codex API
- Post feedback to GitHub PRs as comments


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/eng1n88r/openai-pr-reviewer.git
   cd openai-pr-reviewer
   ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables for OpenAI and GitHub in `.env` file.


## Usage

1. Run the Flask web application:
    ```bash
    python main.p
    ```

2. Set up a webhook in your GitHub repository to point to `/webhook` endpoint of your running Flask app (e.g., http://yourserver.com/webhook).
3. Your application will now process pull requests and post feedback comments based on OpenAI Codex API responses.