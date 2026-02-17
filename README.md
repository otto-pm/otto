# Otto: An AI Powered Project Management Solution

![Otto Logo](https://via.placeholder.com/150/007bff/ffffff?text=OttoAI)

Otto is an advanced AI-powered project management solution designed to streamline development workflows, enhance code understanding, and automate documentation generation. It leverages Retrieval-Augmented Generation (RAG) to provide intelligent assistance for developers, offering features like Q&A over codebases, automated documentation, and code completion. By integrating directly with your repositories, Otto aims to reduce manual effort, improve code quality, and accelerate project delivery.

## Table of Contents

1.  [Features](#features)
2.  [Installation](#installation)
3.  [Usage](#usage)
    *   [RAG CLI](#rag-cli)
    *   [Backend API](#backend-api)
4.  [API Reference](#api-reference)
    *   [Backend Endpoints](#backend-endpoints)
    *   [Ingest Service Classes & Functions](#ingest-service-classes--functions)
5.  [Configuration](#configuration)
6.  [Contributing](#contributing)
7.  [License](#license)

---

## 1. Features

Otto provides a comprehensive suite of features to assist developers and project managers:

*   **AI-Powered Codebase Q&A**: Ask natural language questions about your repository and get accurate, context-aware answers.
*   **Automated Documentation Generation**:
    *   Generate various types of documentation: API, User Guides, Technical Specifications, and READMEs.
    *   Target specific code sections, functions, or entire modules for documentation.
    *   Support for streaming responses for real-time feedback.
*   **GitHub Integration**:
    *   Option to push generated documentation directly to your GitHub repository as a new branch and Pull Request, attributed to the user.
    *   Leverages user's GitHub permissions for seamless integration.
*   **Local Documentation Management**: Save all generated documentation locally as Markdown files for easy review and integration into existing documentation systems.
*   **Code Completion & Assistance**: (High-level feature, details to be expanded) Provides intelligent suggestions and assistance for code development.
*   **Repository Ingestion & Processing**: Efficiently ingest, process, and embed repository content to build a rich knowledge base for RAG services.
*   **Modular Architecture**: Built with a FastAPI backend for robust API services and a dedicated ingest service for processing code.
*   **Documentation Readiness Assessment**: Tools to analyze code chunks for their suitability in generating high-quality documentation.

## 2. Installation

To get Otto up and running, follow these steps. This project is primarily written in Python.

### Prerequisites

*   Python 3.9+
*   `git`
*   `pip` (Python package installer)

### Step-by-Step Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/otto-pm/otto.git
    cd otto
    ```

2.  **Set up Virtual Environment:**
    It's recommended to use a virtual environment to manage dependencies.

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    Otto consists of a `backend` and an `ingest-service`. Install dependencies for both.

    ```bash
    # Install common dependencies
    pip install -r requirements.txt

    # Install backend dependencies
    pip install -r backend/requirements.txt

    # Install ingest-service dependencies
    pip install -r ingest-service/requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory of the project and populate it with the necessary environment variables. See the [Configuration](#configuration) section for details.

    ```bash
    touch .env
    ```

5.  **Run the Services:**

    *   **Start the Ingest Service (if running independently or for local testing):**
        (This might be integrated into the backend or run as a separate worker process)

        ```bash
        # Example: if ingest-service has a direct runnable entrypoint
        python ingest-service/main.py
        ```

    *   **Start the Backend API:**

        ```bash
        cd backend
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        ```
        The API will be accessible at `http://localhost:8000`.

## 3. Usage

Otto can be interacted with via a command-line interface (CLI) for RAG services or directly through its Backend API.

### RAG CLI

The `ingest-service/scripts/rag_cli.py` script provides a convenient way to interact with Otto's RAG capabilities.

#### 4.1. Q&A Service

Answer questions about your codebase:

```bash
# Ask a question about a specific repository
python ingest-service/scripts/rag_cli.py owner/repo \
  --service qa \
  --question "How does the OCR service handle errors?"

# With streaming (see response in real-time)
python ingest-service/scripts/rag_cli.py owner/repo \
  --service qa \
  --question "What caching mechanism is used?" \
  --stream

# Filter by language
python ingest-service/scripts/rag_cli.py owner/repo \
  --service qa \
  --question "How is authentication implemented?" \
  --language python
```

**Example:**

```bash
python ingest-service/scripts/rag_cli.py malav2002/ai-portfolio-analyzer \
  --service qa \
  --question "How does the OCR service handle errors?" \
  --stream
```

#### 4.2. Documentation Generation

Generate professional documentation for various targets and types:

```bash
# Generate API documentation for a specific target within a repo
python ingest-service/scripts/rag_cli.py owner/repo \
  --service doc \
  --target "portfolio analysis API" \
  --doc-type api \
  --stream

# Generate a user guide for a specific topic
python ingest-service/scripts/rag_cli.py owner/repo \
  --service doc \
  --target "getting started" \
  --doc-type user_guide \
  --stream

# Generate technical documentation for a specific component
python ingest-service/scripts/rag_cli.py owner/repo \
  --service doc \
  --target "OCR service architecture" \
  --doc-type technical \
  --stream

# Generate a README for the entire repository
python ingest-service/scripts/rag_cli.py owner/repo \
  --service doc \
  --target "repository overview" \
  --doc-type readme \
  --stream

# Generate documentation and push it to GitHub
python ingest-service/scripts/rag_cli.py owner/repo \
  --service doc \
  --target "new feature X" \
  --doc-type api \
  --push-to-github \
  --stream

# Generate documentation and save it locally (default behavior, but can be explicit)
python ingest-service/scripts/rag_cli.py owner/repo \
  --service doc \
  --target "utility functions" \
  --doc-type technical \
  --save-local
```

### Backend API

The Otto backend exposes a FastAPI interface for programmatic interaction.

#### Ingesting and Processing Repositories

Before using RAG services, repositories need to be ingested and processed.

*   `POST /ingest`: Ingest a repository.
*   `POST /process`: Process ingested repository content.
*   `POST /embed`: Embed processed content for vector search.

#### Asking Questions

*   `POST /qa/ask`: Ask a question about an embedded repository.

#### Generating Documentation

To generate documentation via the API, send a `POST` request to the `/docs/generate` endpoint.

**Endpoint:** `POST /docs/generate`

**Request Body (GenerateDocsRequest):**

```json
{
  "repo_full_name": "owner/repo",
  "target": "What to document (e.g., 'User authentication module', 'API endpoints')",
  "doc_type": "api",  // or "user_guide", "technical", "readme"
  "push_to_github": false,
  "save_local": true
}
```

**Example `curl` request:**

```bash
curl -X POST "http://localhost:8000/docs/generate" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_GITHUB_TOKEN_OR_AUTH_TOKEN" \
     -d '{
           "repo_full_name": "your-github-username/your-repo-name",
           "target": "User management API",
           "doc_type": "api",
           "push_to_github": true,
           "save_local": true
         }'
```

**Response (GenerateDocsResponse):**

```json
{
  "generated_docs": {
    "file_path": "/path/to/generated/docs/api/user-management-api_20231027_103000.md",
    "content_preview": "## User Management API\n\nThis document describes the API for managing users..."
  },
  "pr_link": "https://github.com/your-github-username/your-repo-name/pull/123",
  "message": "Documentation generated successfully."
}
```
*When `push_to_github` is `true`, a new branch is created under the user's account, and a PR attributed to the user is opened, leveraging the user's permissions.*

## 4. API Reference

This section details key classes, functions, and API endpoints within Otto.

### Backend Endpoints

The FastAPI backend (`backend/app/routes/rag.py`) exposes the following primary endpoints:

*   **`POST /ingest`**
    *   **Description**: Initiates the ingestion process for a specified GitHub repository.
    *   **Request Body**: `IngestRepositoryRequest` (e.g., `repo_full_name: str`).
    *   **Returns**: `IngestRepositoryResponse`.
*   **`POST /process`**
    *   **Description**: Processes the raw ingested content, typically involving chunking and cleaning.
    *   **Request Body**: `ProcessRepositoryRequest` (e.g., `repo_full_name: str`).
    *   **Returns**: `ProcessRepositoryResponse`.
*   **`POST /embed`**
    *   **Description**: Generates embeddings for the processed content, preparing it for RAG queries.
    *   **Request Body**: `EmbedRepositoryRequest` (e.g., `repo_full_name: str`).
    *   **Returns**: `EmbedRepositoryResponse`.
*   **`POST /qa/ask`**
    *   **Description**: Answers a question about the codebase using RAG.
    *   **Request Body**: `AskQuestionRequest` (e.g., `repo_full_name: str`, `question: str`, `stream: bool`).
    *   **Returns**: `AskQuestionResponse` (or a streaming response).
*   **`POST /docs/generate`**
    *   **Description**: Generates documentation for a specified target within a repository.
    *   **Request Body**: `GenerateDocsRequest`
        *   `repo_full_name: str`: The full name of the GitHub repository (e.g., `owner/repo`).
        *   `target: str`: The specific part of the code or topic to document (e.g., "User authentication module", "API endpoints").
        *   `doc_type: str = "api"`: Type of documentation to generate (`"api"`, `"user_guide"`, `"technical"`, `"readme"`).
        *   `push_to_github: bool = False`: If `True`, pushes the generated documentation as a PR to GitHub.
        *   `save_local: bool = True`: If `True`, saves the documentation locally.
    *   **Returns**: `GenerateDocsResponse`
        *   `generated_docs: Dict`: Contains `file_path` and `content_preview`.
        *   `pr_link: Optional[str]`: URL to the created Pull Request if `push_to_github` was `True`.
        *   `message: str`: Status message.
*   **`POST /code/complete`**
    *   **Description**: Provides code completion or assistance based on context.
    *   **Request Body**: `CompleteCodeRequest` (e.g., `repo_full_name: str`, `file_path: str`, `code_context: str`).
    *   **Returns**: `CompleteCodeResponse`.

### Ingest Service Classes & Functions

The `ingest-service` contains the core logic for RAG and documentation generation.

#### `class RAGServices` (`ingest-service/src/rag/rag_services.py`)

This class encapsulates the core RAG functionalities.

*   **`generate_documentation(self, target: str, repo_path: str, doc_type: str = 'api', stream: bool = False, push_to_github: bool = False, save_local: bool = True) -> Dict`**
    *   **Description**: Generates professional documentation based on the provided parameters.
    *   **Args**:
        *   `target: str`: What specific part of the code or topic to document.
        *   `repo_path: str`: The local path to the repository.
        *   `doc_type: str = 'api'`: The type of documentation to generate (`'api'`, `'user_guide'`, `'technical'`, `'readme'`).
        *   `stream: bool = False`: If `True`, enables streaming the response.
        *   `push_to_github: bool = False`: If `True`, pushes the generated documentation to GitHub.
        *   `save_local: bool = True`: If `True`, saves the documentation locally as a `.md` file.
    *   **Returns**: `Dict` containing the generated documentation content and file paths.

#### `class DocumentationManager` (`ingest-service/src/utils/file_manager.py`)

Manages the local saving of generated documentation files.

*   **`__init__(self, output_dir: str = "./docs")`**
    *   **Description**: Initializes the documentation manager, ensuring the output directory exists.
    *   **Args**:
        *   `output_dir: str = "./docs"`: The base directory where documentation will be saved.
*   **`save_documentation(self, content: str, name: str, doc_type: str, repo_name: Optional[str] = None) -> str`**
    *   **Description**: Saves the provided documentation content to a file within the configured output directory.
    *   **Args**:
        *   `content: str`: The documentation content to save.
        *   `name: str`: The name for the document (used to form the filename).
        *   `doc_type: str`: The type of documentation (`'api'`, `'user_guide'`, `'technical'`, `'readme'`). This creates a subdirectory for organization.
        *   `repo_name: Optional[str] = None`: An optional repository name to further organize files.
    *   **Returns**: `str` representing the absolute path to the saved file.

#### `function assess_documentation_readiness` (`ingest-service/scripts/analyze_chunk_quality.py`)

*   **Description**: Analyzes a list of code chunks to determine their suitability for documentation generation. It checks for semantic chunks (functions/classes) and chunks with sufficient context (imports, content length).
*   **Args**:
    *   `chunks: List[Dict]`: A list of code chunks, each represented as a dictionary with metadata.
*   **Returns**: Prints readiness assessment and returns a boolean indicating if chunks are good for documentation.

## 5. Configuration

Otto relies on several environment variables for its operation, especially for connecting to external services like GitHub and LLM providers. Create a `.env` file in the project root and populate it as follows:

```ini
# --- GitHub Integration ---
# Required for pushing PRs, fetching repository content, etc.
GITHUB_TOKEN="your_github_personal_access_token"
# Ensure this token has appropriate permissions (repo scope for PRs, read access for content)

# --- LLM Provider Configuration (e.g., OpenAI, Anthropic, Google Gemini) ---
# Choose your preferred LLM provider.
# For OpenAI:
OPENAI_API_KEY="sk-your_openai_api_key"
# For Anthropic:
# ANTHROPIC_API_KEY="sk-your_anthropic_api_key"
# For Google Cloud (if using Gemini via GCP):
# GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/gcp-service-account-key.json"

# --- Google Cloud Project Settings (if using GCP services like Storage) ---
# These are inferred from the backend/app/routes/rag.py
PROJECT_ID="your-gcp-project-id"
BUCKET_RAW="your-gcp-raw-data-bucket-name"
BUCKET_PROCESSED="your-gcp-processed-data-bucket-name"

# --- Ingest Service Path ---
# Path to the ingest service, used by the backend to locate it.
INGEST_SERVICE_PATH="./ingest-service"

# --- Documentation Manager Output Directory ---
# Default directory for saving generated documentation locally.
# Can be overridden in DocumentationManager.__init__
DOCS_OUTPUT_DIR="./docs"
```

**Important Notes:**
*   **GitHub Token**: Ensure your GitHub Personal Access Token has the necessary scopes (e.g., `repo` for full control over private repositories, `public_repo` for public ones, `workflow` if you need to trigger GitHub Actions).
*   **LLM API Keys**: Keep your API keys secure and never commit them to version control.
*   **GCP Credentials**: If `GOOGLE_APPLICATION_CREDENTIALS` is set, it should point to a JSON key file for a service account with permissions to access the specified GCP buckets and other services.

## 6. Contributing

We welcome contributions to Otto! If you're interested in improving the project, please follow these guidelines.

### How to Contribute

1.  **Fork the Repository**: Start by forking the `otto-pm/otto` repository to your GitHub account.
2.  **Clone Your Fork**: Clone your forked repository to your local machine.
    ```bash
    git clone https://github.com/YOUR_USERNAME/otto.git
    cd otto
    ```
3.  **Create a New Branch**: Create a new branch for your feature or bug fix.
    ```bash
    git checkout -b feature/your-feature-name
    # or
    git checkout -b bugfix/issue-description
    ```
4.  **Make Your Changes**: Implement your changes, ensuring they adhere to the project's coding standards.
    *   Write clear, concise, and well-documented code.
    *   Add or update unit tests for your changes.
    *   Ensure all existing tests pass.
5.  **Commit Your Changes**: Commit your changes with a descriptive commit message.
    ```bash
    git commit -m "feat: Add new feature X"
    # or
    git commit -m "fix: Resolve navigation bug"
    ```
6.  **Push to Your Fork**: Push your new branch to your forked repository on GitHub.
    ```bash
    git push origin feature/your-feature-name
    ```
7.  **Create a Pull Request**: Go to the original `otto-pm/otto` repository on GitHub and open a new Pull Request from your branch.
    *   Provide a clear title and detailed description of your changes.
    *   Reference any related issues.

### Code Style

*   We generally follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
*   Use type hints for all function arguments and return values.
*   Include docstrings for all modules, classes, and functions.

### Testing

*   All new features should be accompanied by appropriate unit and integration tests.
*   Run tests using `pytest`.

## 7. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2023 otto-pm

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```