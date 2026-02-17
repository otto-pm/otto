# Otto: AI-Powered Project Management & Documentation

![Otto Logo](https://img.shields.io/badge/Otto-AI%20Powered-blueviolet?style=for-the-badge&logo=openai)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 1. Project Title and Description

**Otto** is an advanced AI-powered project management solution designed to streamline development workflows, enhance code understanding, and automate critical tasks like documentation generation. Built primarily with Python, Otto leverages state-of-the-art Retrieval-Augmented Generation (RAG) techniques to interact intelligently with your codebase, providing insights, generating content, and facilitating collaboration.

At its core, Otto aims to reduce manual overhead for developers and project managers by intelligently analyzing code repositories. Its flagship feature, the AI-powered documentation service, can generate various types of professional documentation (API references, user guides, technical specifications, READMEs) directly from your source code, with options to save locally or integrate seamlessly with GitHub pull requests.

## 2. Features

Otto offers a robust set of features to empower your development process:

*   **AI-Powered Documentation Generation:**
    *   **Versatile Documentation Types:** Generate API documentation, user guides, technical specifications, or comprehensive READMEs.
    *   **Targeted Generation:** Focus documentation on specific functions, classes, modules, or entire repositories.
    *   **Streaming Responses:** Receive documentation content in real-time for immediate feedback and improved user experience.
    *   **GitHub Integration:** Automatically create new branches and open Pull Requests with the generated documentation, attributed to the user.
    *   **Local Saving:** Option to save generated documentation as Markdown files directly to your local filesystem.
*   **Intelligent Code Analysis:**
    *   Utilizes advanced chunking and semantic analysis to understand code context and dependencies.
    *   Assesses documentation readiness of code chunks to ensure high-quality output.
*   **Modular & Scalable Architecture:**
    *   Separation of concerns with an `ingest-service` for core AI logic and a `backend` API for external interaction.
    *   Built on FastAPI for high performance and easy API consumption.
*   **Repository Ingestion & Processing:** (Implied by RAG context)
    *   Ingest and process code repositories to build an intelligent knowledge base.
    *   Embed repository content for efficient retrieval and AI interaction.
*   **Extensible RAG Capabilities:** (Future/Broader Scope)
    *   Foundation for advanced RAG features such as answering questions about the codebase, code completion, and more.

## 3. Installation

To get Otto up and running, follow these steps.

### Prerequisites

*   Python 3.8+
*   Git
*   (Optional) Google Cloud SDK for GCS bucket integration

### Step-by-Step Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/otto-pm/otto.git
    cd otto
    ```

2.  **Create and Activate a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    Otto's services require specific Python packages. You'll need to install them for both the `ingest-service` and `backend`.
    *(Note: A `requirements.txt` file is assumed for dependency management. If not present, you may need to create one based on the imports.)*

    Create a `requirements.txt` in the root of the project with the following (or similar) content:
    ```
    fastapi
    uvicorn[standard]
    pydantic
    python-dotenv
    google-cloud-storage
    requests # For GitHub API interactions
    # Add any other specific dependencies like a particular LLM client library (e.g., openai, google-generativeai)
    ```

    Then install:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory of the project based on the `.env.example` (if provided), or manually create it with the following variables:

    ```env
    # Google Cloud Project ID
    PROJECT_ID="your-gcp-project-id"

    # Google Cloud Storage Buckets for RAG data
    BUCKET_RAW="your-raw-data-bucket-name"
    BUCKET_PROCESSED="your-processed-data-bucket-name"

    # GitHub Personal Access Token (PAT)
    # Required for pushing documentation to GitHub.
    # Must have 'repo' scope.
    GITHUB_TOKEN="ghp_YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"

    # Optional: Directory for local documentation saving
    OUTPUT_DOCS_DIR="./docs"
    ```
    *   **`PROJECT_ID`**: Your Google Cloud project ID where your GCS buckets reside.
    *   **`BUCKET_RAW`**: The name of the Google Cloud Storage bucket where raw ingested repository data will be stored.
    *   **`BUCKET_PROCESSED`**: The name of the Google Cloud Storage bucket where processed (e.g., chunked, embedded) data will be stored.
    *   **`GITHUB_TOKEN`**: A GitHub Personal Access Token with `repo` scope. This is crucial for Otto to be able to create branches and Pull Requests on your behalf when using the `push_to_github` feature.
    *   **`OUTPUT_DOCS_DIR`**: The local directory where generated documentation will be saved if `save_local` is enabled. Defaults to `./docs`.

5.  **Run the Services:**

    Otto typically consists of a backend API and an ingest service.

    *   **Start the Backend API:**
        Navigate to the `backend` directory and run the FastAPI application.
        ```bash
        cd backend
        uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
        ```
        This will start the API server, usually accessible at `http://localhost:8000`.

    *   **Start the Ingest Service (if running independently):**
        The ingest service contains the core RAG logic. It might run as a separate process or be integrated directly into the backend. Based on the file structure, it's likely a module imported by the backend. If it needs to be run as a standalone service, you would typically have an entry point like:
        ```bash
        cd ../ingest-service
        python main.py # (Hypothetical command, depends on actual entry point)
        ```
        For this project, the `RAGServices` are likely instantiated and used by the `backend` service directly.

## 4. Usage

Otto's primary interaction points are its Python API for direct integration and its RESTful API for broader application usage.

### Generating Documentation via Python API

You can directly use the `RAGServices` class within your Python applications.

```python
import os
from ingest_service.src.rag.rag_services import RAGServices
from ingest_service.src.utils.file_manager import DocumentationManager

# Initialize RAGServices (assuming necessary environment/config is set up)
# In a real application, you'd pass necessary clients/configs here.
# For simplicity, we'll assume it can be initialized without explicit args for this example.
rag_service = RAGServices()

# Initialize DocumentationManager to save files locally
doc_manager = DocumentationManager(output_dir="./generated_docs")

# Example 1: Generate API documentation for a specific function
target_function = "RAGServices.generate_documentation"
repo_path = "/path/to/your/local/repo" # Or a GitHub repo URL/name if RAGServices supports cloning
doc_type = "api"

print(f"Generating API documentation for: {target_function} in {repo_path}")
api_docs_result = rag_service.generate_documentation(
    target=target_function,
    repo_path=repo_path,
    doc_type=doc_type,
    stream=False,
    push_to_github=False,
    save_local=True # Save locally
)

print("\nGenerated API Documentation:")
print(api_docs_result.get("content", "No content generated."))
if "file_path" in api_docs_result:
    print(f"Saved to: {api_docs_result['file_path']}")

# Example 2: Generate a README for the entire repository and push to GitHub
target_repo = "otto-pm/otto" # Full GitHub repository name (e.g., "owner/repo")
repo_local_path = "/path/to/your/local/clone/of/otto" # Local path if needed for analysis
doc_type_readme = "readme"

print(f"\nGenerating README for: {target_repo} and pushing to GitHub...")
readme_docs_result = rag_service.generate_documentation(
    target=target_repo,
    repo_path=repo_local_path, # Use local path for analysis, or pass repo_full_name if service handles cloning
    doc_type=doc_type_readme,
    stream=False,
    push_to_github=True, # This will create a branch and PR on GitHub
    save_local=False
)

print("\nGenerated README Documentation (GitHub Integration):")
print(readme_docs_result.get("content", "No content generated."))
if "pr_url" in readme_docs_result:
    print(f"Pull Request created: {readme_docs_result['pr_url']}")
```

### Generating Documentation via REST API

The backend API provides endpoints for generating documentation. Ensure your backend server is running (`uvicorn app.main:app --reload`).

**Authentication:**
For API calls, you'll need to provide a GitHub Personal Access Token (PAT) in the `Authorization` header as a Bearer token. This token is used to authenticate the user and perform GitHub actions (like creating PRs) on their behalf.

```
Authorization: Bearer ghp_YOUR_GITHUB_PERSONAL_ACCESS_TOKEN
```

#### 1. Generate Documentation (Non-Streaming)

**Endpoint:** `POST /docs/generate`
**Description:** Generates documentation and returns the full response once complete. Can optionally push to GitHub.

**Request Body (`GenerateDocsRequest`):**

```json
{
    "repo_full_name": "string",  // e.g., "otto-pm/otto"
    "target": "string",          // What to document (e.g., "RAGServices.generate_documentation", or "ingest-service/src/rag/rag_services.py", or "otto-pm/otto")
    "doc_type": "string",        // Type of documentation: "api", "user_guide", "technical", "readme" (default: "api")
    "push_to_github": "boolean", // Whether to push changes to GitHub (creates branch/PR) (default: false)
    "save_local": "boolean"      // Whether to save the generated documentation locally (default: true)
}
```

**Example cURL Request:**

```bash
curl -X POST "http://localhost:8000/docs/generate" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ghp_YOUR_GITHUB_PERSONAL_ACCESS_TOKEN" \
     -d '{
           "repo_full_name": "otto-pm/otto",
           "target": "ingest-service/src/rag/rag_services.py",
           "doc_type": "technical",
           "push_to_github": true,
           "save_local": false
         }'
```

**Example Response (`GenerateDocsResponse`):**

```json
{
    "content": "## Technical Documentation for rag_services.py\n\nThis file contains the core RAG services...",
    "file_path": null,
    "pr_url": "https://github.com/otto-pm/otto/pull/123",
    "message": "Documentation generated and Pull Request created successfully."
}
```
*Note: `file_path` will be populated if `save_local` is true and `pr_url` if `push_to_github` is true.*

#### 2. Generate Documentation (Streaming)

**Endpoint:** `POST /docs/generate/stream`
**Description:** Generates documentation and streams the response content in real-time. This endpoint does not support `push_to_github` or `save_local` directly, as it's designed for immediate, interactive feedback.

**Request Body (`GenerateDocsRequest`):**

```json
{
    "repo_full_name": "string",  // e.g., "otto-pm/otto"
    "target": "string",          // What to document (e.g., "RAGServices.generate_documentation")
    "doc_type": "string"         // Type of documentation: "api", "user_guide", "technical", "readme" (default: "api")
}
```
*Note: `push_to_github` and `save_local` parameters in the request body will be ignored for this streaming endpoint.*

**Example cURL Request:**

```bash
curl -X POST "http://localhost:8000/docs/generate/stream" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ghp_YOUR_GITHUB_PERSONAL_ACCESS_TOKEN" \
     -d '{
           "repo_full_name": "otto-pm/otto",
           "target": "ingest-service/src/rag/rag_services.py",
           "doc_type": "api"
         }'
```

**Example Streaming Response (Server-Sent Events):**

```
data: {"token": "##"}
data: {"token": " API"}
data: {"token": " Reference"}
data: {"token": " for"}
data: {"token": " `RAGServices`"}
data: {"token": "\n\n"}
data: {"token": "###"}
data: {"token": " `generate_documentation`"}
... (stream continues until complete)
```

## 5. API Reference

### `ingest-service/src/rag/rag_services.py`

#### `class RAGServices`

The core class for AI-powered RAG operations, including documentation generation.

##### `generate_documentation(self, target: str, repo_path: str, doc_type: str = 'api', stream: bool = False, push_to_github: bool = False, save_local: bool = True) -> Dict`

Generate professional documentation based on the specified target.

*   **Args:**
    *   `target` (`str`): What to document (e.g., a function name, file path, or repository name).
    *   `repo_path` (`str`): The local path to the repository or a full GitHub repository name (e.g., "owner/repo").
    *   `doc_type` (`str`, optional): The type of documentation to generate. Valid options: `'api'`, `'user_guide'`, `'technical'`, `'readme'`. Defaults to `'api'`.
    *   `stream` (`bool`, optional): If `True`, the response will be streamed token by token. Defaults to `False`.
    *   `push_to_github` (`bool`, optional): If `True`, the generated documentation will be pushed to a new branch on GitHub, and a Pull Request will be created. Requires `GITHUB_TOKEN`. Defaults to `False`.
    *   `save_local` (`bool`, optional): If `True`, the generated documentation will be saved as a Markdown file locally. Defaults to `True`.
*   **Returns:**
    *   `Dict`: A dictionary containing the generated documentation content, and optionally `file_path` (if `save_local` is `True`) and `pr_url` (if `push_to_github` is `True`).

### `ingest-service/src/utils/file_manager.py`

#### `class DocumentationManager`

Manages the local saving of documentation files.

##### `__init__(self, output_dir: str = "./docs")`

Initialize the documentation manager.

*   **Args:**
    *   `output_dir` (`str`, optional): The directory where documentation files will be saved. Defaults to `./docs`.

##### `save_documentation(self, content: str, name: str, doc_type: str, repo_name: Optional[str] = None) -> str`

Save documentation content to a file within the configured output directory.

*   **Args:**
    *   `content` (`str`): The documentation content to save.
    *   `name` (`str`): The base name for the document file (e.g., "my-function-docs").
    *   `doc_type` (`str`): The type of documentation (e.g., `'api'`, `'user_guide'`, `'technical'`, `'readme'`). This will create a subdirectory for organization.
    *   `repo_name` (`Optional[str]`, optional): An optional repository name to further organize files. Defaults to `None`.
*   **Returns:**
    *   `str`: The absolute path to the saved documentation file.

### Backend API Endpoints (`backend/app/routes/rag.py`)

#### `POST /docs/generate`

**Description:** Generates documentation for a specified target in a repository.
**Request Model:** `GenerateDocsRequest`
**Response Model:** `GenerateDocsResponse` (Pydantic model, details below)

##### `class GenerateDocsRequest(BaseModel)`

Pydantic model for documentation generation requests.

*   `repo_full_name` (`str`): The full name of the GitHub repository (e.g., "owner/repo").
*   `target` (`str`): The specific code element or path to document.
*   `doc_type` (`str`, optional): Type of documentation. Defaults to `"api"`.
*   `push_to_github` (`bool`, optional): Whether to push to GitHub. Defaults to `False`.
*   `save_local` (`bool`, optional): Whether to save locally. Defaults to `True`.

##### `class GenerateDocsResponse(BaseModel)` (Inferred Structure)

Pydantic model for the response from the non-streaming documentation generation.

*   `content` (`str`): The generated documentation content.
*   `file_path` (`Optional[str]`): Path to the locally saved file, if `save_local` was `True`.
*   `pr_url` (`Optional[str]`): URL of the created Pull Request, if `push_to_github` was `True`.
*   `message` (`str`): A status message regarding the operation.

#### `POST /docs/generate/stream`

**Description:** Generates documentation with a real-time streaming response.
**Request Model:** `GenerateDocsRequest` (only `repo_full_name`, `target`, `doc_type` are considered).
**Response:** Server-Sent Events (SSE) stream of text tokens.

## 6. Configuration

Otto relies on environment variables for sensitive information and service configuration. These should be set in a `.env` file in the project root or provided via your deployment environment.

*   **`PROJECT_ID`**: (Required) Your Google Cloud Project ID. Used for accessing Google Cloud Storage buckets.
    *   Example: `PROJECT_ID="my-gcp-project-12345"`
*   **`BUCKET_RAW`**: (Required) The name of the Google Cloud Storage bucket designated for storing raw ingested repository data.
    *   Example: `BUCKET_RAW="otto-raw-repos"`
*   **`BUCKET_PROCESSED`**: (Required) The name of the Google Cloud Storage bucket designated for storing processed (e.g., chunked, embedded) repository data.
    *   Example: `BUCKET_PROCESSED="otto-processed-data"`
*   **`GITHUB_TOKEN`**: (Required for GitHub integration) A GitHub Personal Access Token (PAT) with `repo` scope. This token is used by Otto to authenticate with GitHub for actions like creating branches and Pull Requests.
    *   Example: `GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`
*   **`OUTPUT_DOCS_DIR`**: (Optional) The local directory path where generated documentation files will be saved. If not specified, it defaults to `./docs`.
    *   Example: `OUTPUT_DOCS_DIR="./my_generated_docs"`

## 7. Contributing

We welcome contributions to Otto! Whether it's reporting a bug, suggesting a new feature, or submitting code, your help is appreciated.

### How to Contribute

1.  **Fork the Repository:** Start by forking the `otto-pm/otto` repository to your GitHub account.
2.  **Clone Your Fork:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/otto.git
    cd otto
    ```
3.  **Create a New Branch:**
    Choose a descriptive name for your branch (e.g., `feature/add-new-doc-type`, `bugfix/fix-streaming-issue`).
    ```bash
    git checkout -b feature/your-feature-name
    ```
4.  **Make Your Changes:**
    *   Implement your feature or bug fix.
    *   Ensure your code adheres to the project's coding style (e.g., PEP 8).
    *   Add or update unit tests as appropriate to cover your changes.
    *   Update documentation (like this README) if your changes affect features, installation, or API.
5.  **Run Tests:**
    Before committing, make sure all existing tests pass and your new tests pass.
    *(Assuming a `pytest` setup)*
    ```bash
    pytest
    ```
6.  **Commit Your Changes:**
    Write clear, concise commit messages.
    ```bash
    git add .
    git commit -m "feat: Add new documentation type for X"
    ```
7.  **Push to Your Fork:**
    ```bash
    git push origin feature/your-feature-name
    ```
8.  **Open a Pull Request:**
    Go to the original `otto-pm/otto` repository on GitHub and open a new Pull Request from your branch. Provide a detailed description of your changes, why they are needed, and any relevant context.

### Reporting Bugs

If you find a bug, please open an issue on the [GitHub Issues page](https://github.com/otto-pm/otto/issues). Include:
*   A clear and concise description of the bug.
*   Steps to reproduce the behavior.
*   Expected behavior.
*   Screenshots or error messages if applicable.
*   Your environment details (OS, Python version, etc.).

### Suggesting Enhancements

We'd love to hear your ideas! Open an issue on the [GitHub Issues page](https://github.com/otto-pm/otto/issues) with the label `enhancement`. Describe your suggestion and why you think it would be a valuable addition to Otto.

## 8. License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

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