# Otto: An AI Powered Project Management Solution

## Project Title and Description

**Otto** is an advanced AI-powered project management solution designed to streamline development workflows, enhance code understanding, and automate documentation generation. Leveraging cutting-edge AI and RAG (Retrieval Augmented Generation) techniques, Otto provides intelligent insights into your codebase, making project management more efficient and development cycles faster.

Built with a robust Python backend for AI services and a TypeScript-based frontend (inferred), Otto offers a comprehensive suite of tools for modern software teams. It aims to reduce manual effort in documentation, improve code discoverability, and foster better collaboration.

## Features

Otto provides a powerful set of features to assist developers and project managers throughout the software development lifecycle:

*   **AI-Powered Documentation Generation:**
    *   **Automated Content Creation:** Generate professional and contextually accurate documentation for functions, classes, methods, and entire codebases.
    *   **Versatile Documentation Types:** Supports various documentation formats including API references, user guides, technical specifications, and READMEs.
    *   **Deep Code Understanding:** Utilizes advanced code analysis and Retrieval Augmented Generation (RAG) to understand code structure, relationships, and intent, ensuring highly relevant and precise documentation.
    *   **Configurable Output:** Choose to save generated documentation locally or push it directly to your GitHub repository.
*   **Seamless GitHub Integration:**
    *   **Repository Access & Management:** Authenticate and interact with private and public GitHub repositories.
    *   **Automated Git Operations:** Push generated documentation to specific branches and automatically create Pull Requests for review, streamlining integration into your existing CI/CD workflows.
    *   **Permission Management:** Verifies user repository access and permissions before performing write operations.
*   **Intelligent Codebase Ingestion & Search:**
    *   **Repository Processing:** Efficiently ingests and processes your repository's code, preparing it for AI analysis and RAG queries.
    *   **Enhanced Code Chunking:** Employs sophisticated chunking strategies (e.g., extracting class methods, imports, file context) to break down code into granular, meaningful segments, optimizing retrieval for AI models.
    *   **Semantic Search:** Enables intelligent search capabilities over the ingested codebase to find relevant code snippets for documentation or other AI tasks.
*   **Local File Management:**
    *   **Structured Output:** Manages and stores all generated output files (documentation, edited code) in a well-organized local directory structure.
    *   **Timestamped Versions:** Automatically adds timestamps to saved files for versioning and easy tracking.
*   **Scalable Backend Architecture:**
    *   **FastAPI Framework:** Built on FastAPI for a high-performance, asynchronous, and robust API backend.
    *   **Modular Design:** Services are logically separated (e.g., RAG services, GitHub client, file manager) for maintainability and scalability.

## Installation

To set up and run Otto locally, follow these instructions. This project primarily consists of a Python backend and AI services, with an inferred TypeScript frontend.

### Prerequisites

*   **Python 3.9+**: For the backend and AI services.
*   **Node.js (LTS recommended) & npm/yarn**: For the inferred TypeScript frontend.
*   **Git**: For cloning the repository and version control.
*   **GitHub Personal Access Token (PAT)**: Required for GitHub integration, with `repo` scope for full functionality (reading and writing to repositories).

### Backend (Python) Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/otto-pm/otto.git
    cd otto
    ```

2.  **Create and activate a virtual environment:**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install Python dependencies:**
    Navigate to the `backend/` or `ingest-service/` directory and install the required packages.
    ```bash
    # Assuming a single requirements.txt for all Python services
    pip install -r requirements.txt
    ```
    *(If `requirements.txt` is not provided, common dependencies include `fastapi`, `uvicorn`, `pydantic`, `python-github`, `google-cloud-storage`, `pathlib`, `typing`, `re`, `time`, `os`, `datetime`.)*

4.  **Configure Environment Variables:**
    Create a `.env` file in the root of your project (or in `backend/` and `ingest-service/` directories if they have separate configurations) and populate it with necessary environment variables.

    ```env
    # .env example
    GITHUB_TOKEN="YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"
    # Optional: Google Cloud Project ID if using GCP services (e.g., Storage)
    # GOOGLE_CLOUD_PROJECT_ID="your-gcp-project-id"
    # Optional: Bucket names for raw and processed data if using cloud storage
    # BUCKET_PROCESSED="your-processed-data-bucket"
    # BUCKET_RAW="your-raw-data-bucket"
    # Optional: Output directory for local file management (default is ./output)
    # OUTPUT_DIR="./local_output_files"
    ```
    Ensure your GitHub PAT has the necessary scopes (e.g., `repo`) to read repository content and push changes/create PRs.

### Frontend (TypeScript) Setup (Inferred)

*(This section is based on the inferred primary language being TypeScript and common project structures. Adjust paths as necessary.)*

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend # Or the actual path to your frontend application
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install # or yarn install
    ```

3.  **Configure Frontend Environment Variables:**
    Create a `.env.local` file in your frontend directory for frontend-specific configurations, such as the backend API URL.
    ```env
    # .env.local example
    REACT_APP_API_URL="http://localhost:8000" # Or the URL where your backend is running
    ```

## Usage

### Running the Application

1.  **Start the Backend:**
    Navigate to the `backend/` directory and run the FastAPI application using Uvicorn.
    ```bash
    cd backend
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    *(Note: `app.main:app` is an assumption for the main FastAPI application entry point. Adjust if your entry file is different, e.g., `app.routes.rag:router` if running only a specific router.)*
    The backend API will be accessible at `http://localhost:8000`.

2.  **Start the Frontend (Inferred):**
    Navigate to the `frontend/` directory and start the development server.
    ```bash
    cd frontend
    npm start # or yarn start
    ```
    The frontend application should now be accessible in your web browser, typically at `http://localhost:3000`.

### Generating Documentation via API

The core AI-powered documentation generation feature is exposed through a REST API endpoint. Below is an example of how to trigger it using `curl`.

**Example: Generate API Documentation for a Specific Function and Push to GitHub**

```bash
curl -X POST "http://localhost:8000/docs/generate" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_USER_AUTH_TOKEN" \
-d '{
    "repo_full_name": "otto-pm/otto",
    "target": "generate_documentation",
    "doc_type": "api",
    "stream": false,
    "push_to_github": true,
    "save_local": true
}'
```
*   Replace `YOUR_USER_AUTH_TOKEN` with a valid authentication token obtained after a user logs in (e.g., JWT token). This token is used to identify the user and verify their GitHub repository access.
*   The `repo_full_name` should be the full name of the GitHub repository (e.g., `owner/repo-name`).
*   The `target` specifies the code entity to document (e.g., a function name, class name, or potentially a file path).
*   The `doc_type` can be `api`, `user_guide`, `technical`, or `readme`.

Upon successful execution, the API will return the generated documentation, and if `push_to_github` is `true`, it will attempt to push the documentation to a new branch and create a Pull Request on the specified repository.

## API Reference

Otto's backend exposes a RESTful API for its core functionalities. The primary endpoint for AI-powered documentation generation is detailed below.

### Generate Documentation

Generates AI-powered documentation for a specified code target within a GitHub repository.

*   **Endpoint:** `POST /docs/generate`
*   **Description:** Initiates the AI-powered documentation generation process for a given code entity (e.g., function, class, file). The generated content can be returned directly, saved locally, and/or pushed to GitHub.
*   **Authentication:** Requires a valid authentication token (e.g., Bearer Token) for a user who has appropriate read and write permissions to the target GitHub repository.

#### Request Body (`GenerateDocsRequest`)

| Field            | Type      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         