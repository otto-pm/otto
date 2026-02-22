# Otto: AI Codebase Intelligence & Documentation Pipeline

## 🚀 Project Title and Description

**Otto** is a sophisticated AI-powered project management solution designed to streamline software development workflows through intelligent codebase understanding and automated documentation. This repository specifically details the core **AI Codebase Intelligence & Documentation Pipeline**, a critical component responsible for ingesting, processing, and generating high-quality documentation for software repositories.

Leveraging advanced Retrieval-Augmented Generation (RAG) techniques, Otto can analyze codebases, extract relevant information, and automatically produce various types of documentation—including API references, user guides, technical specifications, and READMEs. With seamless integration for pushing updates directly to GitHub, Otto empowers development teams to maintain up-to-date and comprehensive documentation with minimal manual effort, fostering better collaboration and project clarity within the broader AI-powered project management ecosystem.

## ✨ Features

*   **AI-Powered Documentation Generation**: Automatically generate professional documentation (API, User Guide, Technical, README) for functions, classes, methods, or entire modules.
*   **Intelligent Codebase Ingestion**: Process entire GitHub repositories, including cloning, chunking code into manageable segments, and embedding them for efficient retrieval.
*   **Retrieval-Augmented Generation (RAG)**: Utilizes a RAG pipeline to search relevant code snippets and context, ensuring highly accurate and context-aware documentation.
*   **GitHub Integration**:
    *   Push generated documentation directly to a specified GitHub repository.
    *   Option to create new branches and open Pull Requests for documentation updates.
    *   Handles file path conventions for different documentation types (e.g., `README.md`, `docs/api/my-function.md`).
*   **Local Documentation Saving**: Option to save generated documentation files locally for review or integration into existing documentation systems.
*   **Real-time Streaming**: Generate documentation with real-time, token-by-token Server-Sent Events (SSE) streaming for an interactive user experience.
*   **Scalable Architecture**: Built with FastAPI for high performance and scalability, designed to integrate with cloud storage solutions (e.g., Google Cloud Storage) for managing processed data.
*   **Flexible Configuration**: Customize chunking parameters, target documentation types, and GitHub interaction settings.

## 🛠️ Installation

To set up and run the Otto AI Codebase Intelligence & Documentation Pipeline, follow these steps:

### Prerequisites

*   **Python 3.9+**: Ensure you have a compatible Python version installed.
*   **Git**: Required for cloning repositories.
*   **Poetry (Recommended)**: For dependency management. If not using Poetry, `pip` can be used with `requirements.txt`.
*   **Google Cloud SDK (Optional but Recommended)**: If integrating with Google Cloud Storage for processed data.
*   **GitHub Personal Access Token**: Required for interacting with GitHub repositories (cloning, pushing documentation).

### Steps

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/otto-pm/otto.git
    cd otto
    ```

2.  **Set up Python Environment**:
    If using Poetry:
    ```bash
    poetry install
    poetry shell
    ```
    If using pip:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**:
    Create a `.env` file in the root directory of the `ingest-service` and `backend` directories (or wherever your main application entry points are) and populate it with the necessary environment variables.

    Example `.env` (for `ingest-service` and `backend`):
    ```env
    PROJECT_ID="your-gcp-project-id"
    BUCKET_RAW="your-gcs-raw-bucket-name"
    BUCKET_PROCESSED="your-gcs-processed-bucket-name"
    # Add any other necessary API keys or configurations for LLMs, etc.
    # For GitHub App integration (if used):
    # GITHUB_APP_ID="your-github-app-id"
    # GITHUB_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
    ```
    *   `PROJECT_ID`: Your Google Cloud Project ID.
    *   `BUCKET_RAW`: GCS bucket for raw ingested repository data.
    *   `BUCKET_PROCESSED`: GCS bucket for processed (chunked, embedded) data.

4.  **Run the Services**:
    The Otto solution typically consists of multiple services (e.g., `ingest-service`, `backend`). You'll need to run them.

    For `ingest-service`:
    ```bash
    cd ingest-service
    uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
    ```

    For `backend` (if applicable):
    ```bash
    cd backend
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    *(Adjust ports and host as needed. Ensure all necessary services are running for full functionality.)*

## 🚀 Usage

The Otto AI Codebase Intelligence & Documentation Pipeline is primarily consumed via its RESTful API. Below are common usage patterns.

### 1. Ingest and Process a Repository (Full Pipeline)

Before generating documentation or asking questions, a repository needs to be ingested, chunked, and embedded.

**Endpoint**: `POST /rag/full-pipeline` (or `/pipeline/full` depending on service routing)

**Request Body (`FullPipelineRequest`)**:

```json
{
  "repo_full_name": "owner/repo-name",
  "branch": "main",
  "chunk_size": 150,
  "overlap": 10,
  "force_reembed": false
}
```

**Example `curl` command**:

```bash
curl -X POST "http://localhost:8000/rag/full-pipeline" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
     -d '{
           "repo_full_name": "octocat/Spoon-Knife",
           "branch": "main",
           "chunk_size": 150,
           "overlap": 10,
           "force_reembed": false
         }'
```

### 2. Generate Documentation

Generate documentation for a specific target (e.g., a function, class, or method) within an ingested repository.

**Endpoint**: `POST /docs/generate`

**Request Body (`GenerateDocsRequest`)**:

```json
{
  "repo_full_name": "owner/repo-name",
  "target": "MyClass.myMethod",
  "doc_type": "api",
  "push_to_github": true,
  "create_pr": true,
  "github_token": "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN",
  "save_local": false
}
```

*   `repo_full_name`: The full name of the GitHub repository (e.g., `octocat/Spoon-Knife`).
*   `target`: The specific code element to document (e.g., `MyClass`, `my_function`, `MyModule.MyClass.my_method`).
*   `doc_type`: Type of documentation (`api`, `user_guide`, `technical`, `readme`). This affects the output path on GitHub.
*   `push_to_github`: Boolean, whether to push the generated documentation to GitHub.
*   `create_pr`: Boolean, whether to create a Pull Request on GitHub after pushing.
*   `github_token`: A GitHub Personal Access Token with `repo` scope for pushing changes.
*   `save_local`: Boolean, whether to save the documentation to the local filesystem.

**Example `curl` command**:

```bash
curl -X POST "http://localhost:8000/docs/generate" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
     -d '{
           "repo_full_name": "octocat/Spoon-Knife",
           "target": "README",
           "doc_type": "readme",
           "push_to_github": true,
           "create_pr": true,
           "github_token": "ghp_YOUR_GITHUB_TOKEN",
           "save_local": false
         }'
```

### 3. Generate Documentation with Streaming

For a more interactive experience, documentation can be generated and streamed token-by-token.

**Endpoint**: `POST /docs/generate/stream`

**Request Body (`GenerateDocsRequest`)**: Same as `POST /docs/generate`.

**Example `curl` command**:

```bash
curl -X POST "http://localhost:8001/docs/generate/stream" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
     -d '{
           "repo_full_name": "octocat/Spoon-Knife",
           "target": "MyFunction",
           "doc_type": "api",
           "github_token": "ghp_YOUR_GITHUB_TOKEN"
         }'
```
*(Note: Streaming endpoints might be on a different service, e.g., `ingest-service` on port 8001 as per code context.)*

## 📚 API Reference

The Otto AI Codebase Intelligence & Documentation Pipeline exposes the following key API endpoints:

### Base URL

`http://localhost:8000` (or `http://localhost:8001` for ingest-service endpoints)

### Authentication

All endpoints require authentication, typically via a Bearer token in the `Authorization` header. User-specific GitHub tokens are passed in the request body for GitHub interactions.

### Endpoints

#### 1. `POST /rag/full-pipeline`

*   **Description**: Ingests a GitHub repository, chunks its content, and embeds it for RAG operations. This prepares the repository for documentation generation and querying.
*   **Request Body (`FullPipelineRequest`)**:
    ```json
    {
      "repo_full_name": "string",       // e.g., "octocat/Spoon-Knife"
      "branch": "string | null",        // Optional, default: "main"
      "chunk_size": "integer",          // Optional, default: 150
      "overlap": "integer",             // Optional, default: 10
      "force_reembed": "boolean"        // Optional, default: false. If true, re-embeds even if already processed.
    }
    ```
*   **Response (`FullPipelineResponse`)**:
    ```json
    {
      "status": "string",               // e.g., "success", "failed"
      "message": "string"               // Description of the operation result
    }
    ```

#### 2. `POST /docs/generate`

*   **Description**: Generates comprehensive documentation for a specified target within an ingested repository. Can push directly to GitHub or save locally.
*   **Request Body (`GenerateDocsRequest`)**:
    ```json
    {
      "repo_full_name": "string",           // e.g., "octocat/Spoon-Knife"
      "target": "string",                   // e.g., "MyClass.myMethod", "README"
      "doc_type": "string",                 // "api", "user_guide", "technical", "readme". Default: "api"
      "stream": "boolean",                  // Optional, default: false. Set to true to get a streaming response (use /docs/generate/stream endpoint for this).
      "push_to_github": "boolean",          // Optional, default: false. If true, pushes to GitHub.
      "create_pr": "boolean",               // Optional, default: true. If true and push_to_github is true, creates a PR.
      "github_token": "string",             // Required if push_to_github is true. GitHub Personal Access Token.
      "save_local": "boolean"               // Optional, default: true. If true, saves documentation locally.
    }
    ```
*   **Response (`GenerateDocsResponse`)**:
    ```json
    {
      "documentation": "string",            // The generated documentation content
      "type": "string",                     // The type of documentation generated
      "github_url": "string | null",        // URL to the pushed documentation on GitHub, if applicable
      "local_path": "string | null"         // Local file path, if saved locally
    }
    ```

#### 3. `POST /docs/generate/stream`

*   **Description**: Generates documentation with real-time, token-by-token streaming using Server-Sent Events (SSE).
*   **Request Body (`GenerateDocsRequest`)**: Same as `POST /docs/generate`, but `stream` parameter is implicitly `true`.
*   **Response**: A stream of `text/event-stream` data. Each event will contain a chunk of the generated documentation.
    ```
    data: {"token": "First part of documentation"}
    data: {"token": "Second part of documentation"}
    ...
    data: {"token": "Final part."}
    data: {"event": "end", "github_url": "...", "local_path": "..."}
    ```

## ⚙️ Configuration

The behavior of the Otto AI Codebase Intelligence & Documentation Pipeline can be configured using environment variables and request parameters.

### Environment Variables

These variables should be set in your `.env` file or as system environment variables where the services are deployed.

*   `PROJECT_ID`: (Required) Your Google Cloud Project ID. Used for GCS and other GCP services.
*   `BUCKET_RAW`: (Required) Name of the Google Cloud Storage bucket for storing raw ingested repository data.
*   `BUCKET_PROCESSED`: (Required) Name of the Google Cloud Storage bucket for storing processed (chunked, embedded) repository data.
*   `GITHUB_APP_ID`: (Optional) If using a GitHub App for broader repository access, the App ID.
*   `GITHUB_PRIVATE_KEY`: (Optional) The private key for the GitHub App, used for authentication.
*   `LLM_MODEL_NAME`: (Optional) The specific LLM model to use for generation tasks (e.g., `gemini-pro`, `gpt-4`).
*   `EMBEDDING_MODEL_NAME`: (Optional) The specific embedding model to use for creating vector embeddings.
*   `OUTPUT_DIR`: (Optional) Base directory for saving local output files (default: `./output`).

### Request Parameters

Specific configurations can be controlled via parameters in the API request bodies:

*   **`repo_full_name`**: Specifies the target GitHub repository.
*   **`branch`**: Specifies the branch to clone and process.
*   **`chunk_size`**: Controls the size of text chunks during repository processing.
*   **`overlap`**: Defines the overlap between consecutive text chunks.
*   **`force_reembed`**: Forces reprocessing and re-embedding of a repository, even if it's already cached.
*   **`target`**: Narrows down documentation generation to a specific function, class, or method.
*   **`doc_type`**: Determines the type of documentation to generate (`api`, `user_guide`, `technical`, `readme`).
*   **`push_to_github`**: Enables or disables pushing generated documentation to GitHub.
*   **`create_pr`**: Controls whether a Pull Request is created on GitHub for documentation updates.
*   **`github_token`**: Provides the necessary GitHub Personal Access Token for repository write access.
*   **`save_local`**: Enables or disables saving documentation to the local filesystem.

## 🤝 Contributing

We welcome contributions to the Otto AI Codebase Intelligence & Documentation Pipeline! To contribute, please follow these guidelines:

1.  **Fork the repository**: Start by forking the `otto-pm/otto` repository to your GitHub account.
2.  **Clone your fork**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/otto.git
    cd otto
    ```
3.  **Create a new branch**:
    ```bash
    git checkout -b feature/your-feature-name
    ```
    Or for bug fixes:
    ```bash
    git checkout -b bugfix/issue-description
    ```
4.  **Make your changes**: Implement your features or bug fixes. Ensure your code adheres to the project's coding standards.
5.  **Write tests**: Add or update unit and integration tests to cover your changes.
6.  **Run tests**:
    ```bash
    poetry run pytest
    ```
    Or:
    ```bash
    python -m pytest
    ```
7.  **Commit your changes**:
    ```bash
    git commit -m "feat: Add new feature"
    ```
    (Please use conventional commit messages.)
8.  **Push to your fork**:
    ```bash
    git push origin feature/your-feature-name
    ```
9.  **Create a Pull Request**: Open a Pull Request from your branch to the `main` branch of the original `otto-pm/otto` repository. Provide a clear description of your changes and reference any related issues.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.