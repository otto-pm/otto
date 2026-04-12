# Otto: AI-Powered Project Management

![Otto Logo](https://img.shields.io/badge/Otto-AI%20PM-blueviolet?style=for-the-badge&logo=github)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/otto-pm/otto/main.yml?branch=main&style=for-the-badge)
![License](https://img.shields.io/github/license/otto-pm/otto?style=for-the-badge)
![Primary Language](https://img.shields.io/github/languages/top/otto-pm/otto?style=for-the-badge&color=blue)

## 1. Project Title and Description

**Otto** is an AI-Powered Project Management Solution designed to streamline software development workflows through intelligent code analysis, automated documentation generation, and seamless GitHub integration. It acts as an intelligent assistant, helping teams maintain high-quality documentation, understand complex codebases, and accelerate development cycles.

While the core application and user interface are primarily built with **TypeScript**, the powerful backend and ingestion services leverage **Python** for AI-driven code processing, RAG (Retrieval Augmented Generation), and interaction with external APIs like GitHub.

## 2. Features

Otto offers a robust set of features to enhance your development process:

*   **AI-Powered Documentation Generation:**
    *   Automatically generates professional documentation (API, user guide, technical, README) for specific code targets like functions, classes, or methods.
    *   Utilizes advanced AI models to understand code context and produce comprehensive, human-readable content.
    *   Supports various documentation types, adapting content for different audiences and purposes.
*   **Intelligent Code Analysis & RAG:**
    *   Employs sophisticated code chunking and analysis techniques (e.g., `EnhancedCodeChunker`) to deeply understand code structure, extract class methods, imports, and relationships.
    *   Powers a Retrieval Augmented Generation (RAG) system to fetch relevant code snippets for accurate and context-aware documentation.
*   **Seamless GitHub Integration:**
    *   Connects directly to your GitHub repositories to read code and push generated content.
    *   Automates the process of creating new branches and opening Pull Requests with the generated documentation.
    *   Supports pushing documentation directly to `README.md` or dedicated `docs/` directories.
*   **Local File Management:**
    *   Provides options to save generated documentation and potentially edited code files locally for review or offline access.
    *   Organizes output into structured directories based on documentation type and repository path.
*   **Scalable Backend Architecture:**
    *   Built with FastAPI for a high-performance and scalable API layer.
    *   Integrates with Google Cloud Storage (GCS) for robust and distributed storage of raw and processed code data.
*   **Secure User & Repository Access:**
    *   Ensures secure operations by verifying user authentication, GitHub tokens, and repository access permissions before performing any actions.

## 3. Installation

To get Otto up and running, you'll need to set up both the Python backend/ingest services and potentially the TypeScript frontend (though details for the frontend are not in the provided context, we'll assume a standard setup).

### Prerequisites

*   **Python 3.9+**: For backend and ingest services.
*   **Node.js & npm/yarn**: For the TypeScript frontend (if applicable).
*   **Git**: For cloning repositories.
*   **GitHub Account**: Required for repository integration.
*   **Google Cloud Project**: For storage and potentially other services.

### Backend and Ingest Services (Python)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/otto-pm/otto.git
    cd otto
    ```

2.  **Set up Python environment:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    Navigate to the respective service directories and install their dependencies.

    *   **Ingest Service:**
        ```bash
        cd ingest-service
        pip install -r requirements.txt
        cd ..
        ```
    *   **Backend Service:**
        ```bash
        cd backend
        pip install -r requirements.txt
        cd ..
        ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the `backend` and `ingest-service` directories (or set them directly in your environment).

    ```ini
    # Example .env content for backend and ingest-service
    GITHUB_TOKEN="YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"
    GOOGLE_CLOUD_PROJECT_ID="your-gcp-project-id"
    GCS_BUCKET_PROCESSED="your-gcs-processed-bucket-name"
    GCS_BUCKET_RAW="your-gcs-raw-bucket-name"
    # Add any other necessary environment variables
    ```
    *   **`GITHUB_TOKEN`**: A GitHub Personal Access Token with `repo` scope for accessing private repositories and pushing changes.
    *   **`GOOGLE_CLOUD_PROJECT_ID`**: Your Google Cloud Project ID.
    *   **`GCS_BUCKET_PROCESSED`**: The name of your Google Cloud Storage bucket for processed data.
    *   **`GCS_BUCKET_RAW`**: The name of your Google Cloud Storage bucket for raw data.

5.  **Google Cloud Authentication:**
    Ensure your environment is authenticated with Google Cloud.
    ```bash
    gcloud auth application-default login
    ```
    This will open a browser for you to log in with your Google account.

### Frontend Application (TypeScript - Placeholder)

*(Details for the TypeScript frontend are not available in the provided code chunks. This section is a placeholder for a typical setup.)*

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install # or yarn install
    ```

3.  **Configure Frontend Environment Variables:**
    Create a `.env` file (e.g., `.env.local`) for frontend-specific variables, such as the backend API URL.
    ```ini
    # Example .env.local content for frontend
    VITE_API_BASE_URL="http://localhost:8000/api"
    ```

## 4. Usage

### Running the Services

1.  **Start the Backend Service:**
    From the `otto/backend` directory:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    This will start the FastAPI server, typically accessible at `http://localhost:8000`.

2.  **Start the Ingest Service:**
    The ingest service typically runs as a worker or is triggered by the backend. Depending on the architecture, it might be run as a separate process or integrated. For development, you might run specific scripts or have it implicitly handled by the backend.

3.  **Start the Frontend Application (Placeholder):**
    From the `otto/frontend` directory:
    ```bash
    npm run dev # or yarn dev
    ```
    This will usually start a development server for the frontend.

### Generating Documentation via API

Once the backend service is running, you can use its API to generate documentation.

**Endpoint:** `POST /docs/generate`

**Example Request (using `curl`):**

```bash
curl -X POST "http://localhost:8000/docs/generate" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_AUTH_TOKEN" \
-d '{
  "repo_full_name": "otto-pm/otto",
  "target": "ingest-service/src/rag/rag_services.py::RAGServices::generate_documentation",
  "doc_type": "api",
  "stream": false,
  "push_to_github": true,
  "save_local": true
}'
```

**Explanation of Request Body:**

*   `repo_full_name`: The full name of the GitHub repository (e.g., `owner/repo_name`).
*   `target`: The specific code entity to document. This can be a file path, a class, a function, or a method within a file.
    *   Examples:
        *   `ingest-service/src/rag/rag_services.py` (for a whole file)
        *   `ingest-service/src/rag/rag_services.py::RAGServices` (for a class)
        *   `ingest-service/src/rag/rag_services.py::RAGServices::generate_documentation` (for a method)
*   `doc_type`: The type of documentation to generate.
    *   `api` (default): For API reference documentation.
    *   `user_guide`: For user-focused guides.
    *   `technical`: For in-depth technical explanations.
    *   `readme`: To generate or update a `README.md`.
*   `stream`: If `true`, the API might stream the documentation generation process (implementation dependent).
*   `push_to_github`: If `true`, the generated documentation will be pushed to the specified GitHub repository. This requires a GitHub token with push permissions.
*   `save_local`: If `true`, the generated documentation will also be saved to the local `output` directory of the ingest service.

## 5. API Reference

The primary API endpoint for documentation generation is `POST /docs/generate`.

### `POST /docs/generate`

Generates documentation for a specified code target within a GitHub repository.

*   **Description**: This endpoint triggers the AI-powered documentation generation process. It analyzes the target code, generates documentation based on the specified type, and can optionally push the results to GitHub or save them locally.
*   **Authentication**: Requires an authenticated user (e.g., via JWT or session token) and a valid GitHub Personal Access Token associated with the user, which must have sufficient permissions (`repo` scope) for the target repository.
*   **Request Body (`GenerateDocsRequest`)**:

    | Field            | Type      | Required | Default | Description                                                                                                                            |
    | :--------------- | :-------- | :------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------- |
    | `repo_full_name` | `string`  | Yes      |         | The full name of the GitHub repository (e.g., `otto-pm/otto`).                                                                         |
    | `target`         | `string`  | Yes      |         | The specific code entity to document (e.g., `MyClass.my_method`, `my_function`, `path/to/file.py`).                                    |
    | `doc_type`       | `string`  | No       | `api`   | The type of documentation to generate. Allowed values: `api`, `user_guide`, `technical`, `readme`.                                     |
    | `stream`         | `boolean` | No       | `false` | If `true`, the documentation generation process might stream updates (feature dependent).                                              |
    | `push_to_github` | `boolean` | No       | `false` | If `true`, the generated documentation will be pushed to a new branch and potentially a Pull Request created on GitHub.                |
    | `save_local`     | `boolean` | No       | `true`  | If `true`, the generated documentation will be saved to the local output directory of the ingest service (`./output/documentation/`). |

*   **Response Body (`GenerateDocsResponse`)**:

    | Field            | Type      | Description                                                                                                |
    | :--------------- | :-------- | :--------------------------------------------------------------------------------------------------------- |
    | `documentation`  | `string`  | The generated documentation content in Markdown format.                                                    |
    | `type`           | `string`  | The type of documentation generated (e.g., `api`, `readme`).                                               |
    | `files_referenced` | `integer` | The number of code files referenced during the documentation generation process.                           |
    | `github_pr`      | `string`  | *Optional*. The URL of the created GitHub Pull Request, if `push_to_github` was `true` and a PR was made. |
    | `github_branch`  | `string`  | *Optional*. The name of the new GitHub branch created, if `push_to_github` was `true`.                   |
    | `pushed_by`      | `string`  | *Optional*. The GitHub username of the user who initiated the push, if `push_to_github` was `true`.      |

*   **Error Responses**:
    *   `400 Bad Request`: Invalid request payload or missing required parameters.
    *   `401 Unauthorized`: Missing or invalid authentication token.
    *   `403 Forbidden`: User does not have access to the specified repository or insufficient GitHub token permissions.
    *   `404 Not Found`: The specified `repo_full_name` or `target` could not be found.
    *   `500 Internal Server Error`: An unexpected error occurred on the server.

## 6. Configuration

Otto's behavior can be configured primarily through environment variables and service-specific parameters.

### Environment Variables

These variables are crucial for the Python backend and ingest services. They should be set in your environment or in `.env` files within the respective service directories.

*   **`GITHUB_TOKEN`**:
    *   **Description**: A GitHub Personal Access Token (PAT) used by the `GitHubClient` to interact with the GitHub API.
    *   **Required Scopes**: `repo` (for full control over private repositories and pushing changes), `read:user`, `user:email`.
    *   **Example**: `GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`
*   **`GOOGLE_CLOUD_PROJECT_ID`**:
    *   **Description**: Your Google Cloud Project ID, used for authenticating and interacting with Google Cloud services like GCS.
    *   **Example**: `GOOGLE_CLOUD_PROJECT_ID="my-otto-project-12345"`
*   **`GCS_BUCKET_PROCESSED`**:
    *   **Description**: The name of the Google Cloud Storage bucket where processed code chunks and embeddings are stored.
    *   **Example**: `GCS_BUCKET_PROCESSED="otto-processed-data"`
*   **`GCS_BUCKET_RAW`**:
    *   **Description**: The name of the Google Cloud Storage bucket where raw repository data is temporarily stored during ingestion.
    *   **Example**: `GCS_BUCKET_RAW="otto-raw-repos"`

### Service-Specific Configuration

*   **Local Output Directory (`ingest-service`)**:
    *   The `DocumentationManager` in the ingest service can be initialized with a custom output directory.
    *   **Default**: `./output`
    *   **Configuration**: When instantiating `DocumentationManager`, you can pass `output_dir='/path/to/your/custom/output'`.

## 7. Contributing

We welcome contributions to Otto! Whether it's bug reports, feature requests, or code contributions, your help is valuable.

1.  **Fork the repository:** Start by forking the `otto-pm/otto` repository to your GitHub account.
2.  **Clone your fork:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/otto.git
    cd otto
    ```
3.  **Create a new branch:**
    ```bash
    git checkout -b feature/your-feature-name
    ```
    Choose a descriptive name for your branch (e.g., `bugfix/issue-123`, `feature/add-new-doc-type`).
4.  **Make your changes:**
    *   Ensure your code adheres to the project's coding standards (e.g., Black for Python, ESLint/Prettier for TypeScript).
    *   Write clear, concise commit messages.
    *   Add or update tests for your changes.
5.  **Run tests:**
    Before submitting, ensure all tests pass.
    *   For Python services: `pytest` (from the respective service directory).
    *   For TypeScript frontend: `npm test` or `yarn test`.
6.  **Commit and push your changes:**
    ```bash
    git add .
    git commit -m "feat: Add new documentation type for X"
    git push origin feature/your-feature-name
    ```
7.  **Open a Pull Request:**
    Go to the original `otto-pm/otto` repository on GitHub and open a new Pull Request from your branch. Provide a detailed description of your changes.

## 8. License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---