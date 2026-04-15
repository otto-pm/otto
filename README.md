# Otto: AI-Powered Project Management Solution

![Otto Logo Placeholder](https://via.placeholder.com/150/007bff/ffffff?text=Otto+PM)

## 1. Project Title and Description

**Otto** is an advanced, AI-powered project management solution designed to streamline development workflows, enhance team collaboration, and automate tedious tasks. By leveraging cutting-edge artificial intelligence, Otto provides intelligent assistance throughout the software development lifecycle, from code generation and documentation to smart task management and insightful analytics.

Built with a robust backend in Python (FastAPI) and a dynamic frontend in TypeScript (React/Next.js), Otto integrates seamlessly with GitHub, offering a comprehensive platform for modern software teams.

## 2. Features

Otto offers a suite of powerful features to revolutionize your project management experience:

*   **AI-Powered Code Completion**: Get contextually aware code suggestions and completions directly within your repository. Otto intelligently detects the relevant file based on semantic similarity and provides highly accurate code snippets, accelerating development.
    *   *How it works*: Provide a code snippet, and Otto searches the indexed repository for the most similar code, auto-detects the file, and generates a contextually aware completion.
*   **Automated Documentation Generation**: Generate comprehensive documentation for your API endpoints, modules, and READMEs with a single command. Otto can even push these generated documents directly to a new branch and create a Pull Request on GitHub.
    *   Supports various documentation types (e.g., `api`, `module`, `readme`).
*   **Secure GitHub OAuth Authentication**: Seamless and secure user authentication and session management using GitHub's OAuth 2.0. This ensures a streamlined onboarding process and leverages GitHub's robust security features.
    *   Includes CSRF protection during the OAuth flow and secure handling of session tokens via HTTP-only cookies and JSON Web Tokens (JWTs).
*   **Advanced Code Ingestion & Analysis**: An intelligent ingestion service processes your codebase, performing deep analysis including:
    *   Enhanced code chunking for optimal AI model input.
    *   Extraction of Python type hints, decorators, and JavaScript/TypeScript imports for richer context.
    *   Management of documentation and code edits locally before pushing to GitHub.
*   **Comprehensive GitHub Integration**:
    *   Fetch file content directly from GitHub repositories.
    *   Create new branches and push code changes or generated documentation as Pull Requests.
    *   Manage repository access and user metadata.
*   **Intuitive Frontend for Project Management**: A responsive and interactive user interface built with TypeScript, providing tools for:
    *   Issue tracking and management.
    *   Sprint planning and visualization.
    *   Utilities for UI enhancements (e.g., `hexToRgba`, `calculateInsertPosition`, `moveItemWithinArray`).

## 3. Installation

To set up Otto locally, follow these steps. This project consists of multiple services (frontend, backend, ingestion service) and requires Node.js and Python.

### Prerequisites

*   Git
*   Node.js (LTS version recommended)
*   npm or yarn
*   Python 3.9+
*   Poetry (for Python dependency management, recommended) or pip
*   Docker (optional, for containerized deployment)

### Steps

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/otto-pm/otto.git
    cd otto
    ```

2.  **Backend & Ingestion Service Setup (Python):**

    ```bash
    # Navigate to the backend directory
    cd backend
    poetry install # or pip install -r requirements.txt
    
    # Navigate to the ingest-service directory
    cd ../ingest-service
    poetry install # or pip install -r requirements.txt
    ```

3.  **Frontend Setup (TypeScript):**

    ```bash
    cd ../frontend
    npm install # or yarn install
    ```

4.  **Environment Variables:**
    Create `.env` files in the `backend`, `ingest-service`, and `frontend` directories based on provided `.env.example` files (if any, otherwise create them manually).

    **Common Environment Variables:**

    *   `GITHUB_CLIENT_ID`: Your GitHub OAuth Application Client ID.
    *   `GITHUB_CLIENT_SECRET`: Your GitHub OAuth Application Client Secret.
    *   `GITHUB_TOKEN`: A personal access token with `repo` scope for the `ingest-service` to interact with GitHub (e.g., pushing docs).
    *   `JWT_SECRET_KEY`: A strong secret key for signing JWTs.
    *   `FRONTEND_URL`: The URL where your frontend application will be hosted (e.g., `http://localhost:3000`).
    *   `BACKEND_URL`: The URL where your backend API will be hosted (e.g., `http://localhost:8000`).
    *   `INGEST_SERVICE_URL`: The URL for the ingestion service (e.g., `http://localhost:8001`).
    *   `OUTPUT_DIR`: (For `ingest-service`) Directory to save generated files locally (default: `./output`).

    **Example `.env` for `backend`:**
    ```env
    GITHUB_CLIENT_ID=your_github_client_id
    GITHUB_CLIENT_SECRET=your_github_client_secret
    JWT_SECRET_KEY=supersecretjwtkey
    FRONTEND_URL=http://localhost:3000
    ```

    **Example `.env` for `ingest-service`:**
    ```env
    GITHUB_TOKEN=ghp_yourpersonalaccesstoken
    OUTPUT_DIR=./output
    ```

    **Example `.env` for `frontend`:**
    ```env
    NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
    NEXT_PUBLIC_INGEST_SERVICE_URL=http://localhost:8001
    ```

## 4. Usage

### Running the Services

1.  **Start the Backend API:**
    ```bash
    cd backend
    poetry run uvicorn main:app --reload --port 8000
    ```

2.  **Start the Ingestion Service:**
    ```bash
    cd ingest-service
    poetry run uvicorn main:app --reload --port 8001
    ```

3.  **Start the Frontend:**
    ```bash
    cd frontend
    npm run dev # or yarn dev
    ```

Once all services are running, navigate to `http://localhost:3000` (or your configured `FRONTEND_URL`) in your web browser.

### Interacting with the API

You can interact with the backend and ingestion services directly via their API endpoints.

#### Example: AI-Powered Code Completion (Ingestion Service)

```bash
curl -X POST https://ingest-service-484671782718.us-east1.run.app/pipeline/code/complete \
  -H "Content-Type: application/json" \
  -d '{
    "repo_full_name": "owner/repo",
    "code_context": "def calculate_total(items):\n    total = 0\n    for item in items:",
    "language": "python",
    "github_token": "YOUR_GITHUB_TOKEN"
  }'
```

#### Example: Generate Documentation (Ingestion Service)

```bash
curl -X POST https://ingest-service-484671782718.us-east1.run.app/pipeline/docs/generate \
  -H "Content-Type: application/json" \
  -d '{
    "repo_full_name": "owner/repo",
    "target": "src/main.py",
    "doc_type": "module",
    "push_to_github": false,
    "github_token": "YOUR_GITHUB_TOKEN"
  }'
```

## 5. API Reference

Otto exposes several API endpoints across its backend and ingestion services. Detailed API documentation is available within the project repository.

### Authentication System API

The authentication system handles user login, session management, and GitHub OAuth integration.

*   **`GET /login`**: Initiates the GitHub OAuth authentication flow.
*   **`GET /auth/callback`**: Callback endpoint for GitHub OAuth, exchanges authorization code for tokens.
*   **`GET /logout`**: Logs out the current user.
*   **`GET /me`**: Retrieves information about the currently authenticated user.

For comprehensive details on the Authentication API, refer to:
*   `backend/docs/api/otto-pm-otto_authentication-system_*.md`

### Ingestion Service API

The ingestion service provides AI-powered functionalities like code completion and documentation generation.

*   **`POST /pipeline/code/complete`**: Generates AI-powered code completions based on a given context.
*   **`POST /pipeline/docs/generate`**: Generates documentation for specified files or modules.

For more details on the Ingestion Service API, refer to the `Data-Pipeline-Guide.md` and relevant source files in `ingest-service/src/`.

## 6. Configuration

Configuration for Otto is primarily managed through environment variables. Ensure you have set up the `.env` files as described in the [Installation](#4-installation) section.

Key configuration points include:

*   **GitHub OAuth Credentials**: `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`
*   **GitHub Personal Access Token**: `GITHUB_TOKEN` (for `ingest-service` to perform repository actions)
*   **JWT Secret**: `JWT_SECRET_KEY` (for secure session management)
*   **Service URLs**: `FRONTEND_URL`, `BACKEND_URL`, `INGEST_SERVICE_URL`
*   **Local Output Directory**: `OUTPUT_DIR` (for `ingest-service` to store generated files temporarily)

## 7. Contributing

We welcome contributions to Otto! If you're interested in improving the project, please follow these guidelines:

1.  **Fork the repository.**
2.  **Clone your forked repository:**
    ```bash
    git clone https://github.com/your-username/otto.git
    cd otto
    ```
3.  **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/your-feature-name
    ```
4.  **Make your changes.** Ensure your code adheres to the project's coding standards.
5.  **Test your changes.**
6.  **Commit your changes** with a clear and descriptive commit message.
7.  **Push your branch** to your forked repository.
8.  **Open a Pull Request** against the `main` branch of the original `otto-pm/otto` repository.

Please ensure your pull requests are well-documented and include any necessary tests.

## 8. License

This project is licensed under the [MIT License](LICENSE).

---

**Otto: Empowering your project management with AI intelligence.**