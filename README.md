# Otto: AI-Powered Project Management Solution

![Otto Logo](https://via.placeholder.com/150/007bff/ffffff?text=Otto) <!-- Placeholder for a project logo -->

Otto is an innovative, AI-powered project management solution designed to streamline development workflows, enhance collaboration, and automate tedious tasks. By leveraging artificial intelligence, Otto assists teams in generating documentation, completing code, and managing project tasks more efficiently, all while integrating seamlessly with your existing GitHub repositories.

## 1. Project Title and Description

**Otto: AI-Powered Project Management Solution**

Otto is a cutting-edge project management platform that integrates artificial intelligence to revolutionize how development teams plan, execute, and document their work. Built with a robust backend (Python/FastAPI) and a dynamic frontend (TypeScript/React), Otto connects directly to your GitHub repositories, providing intelligent assistance for various development tasks. From automated documentation generation and smart code completion to secure user authentication via GitHub OAuth, Otto aims to be the central hub for your AI-enhanced development lifecycle.

## 2. Features

Otto offers a comprehensive suite of features designed to boost productivity and improve code quality:

*   **AI-Powered Documentation Generation**: Automatically generates comprehensive documentation for your codebase, including API references, module descriptions, and READMEs.
    *   Supports various documentation types (`api`, `module`, `readme`).
    *   Can push generated documentation directly to GitHub as a new branch and Pull Request.
*   **Intelligent Code Completion**: Provides contextually aware code suggestions and completions based on your repository's existing codebase.
    *   Uses semantic similarity search to detect the most relevant file for a given code snippet.
*   **Secure GitHub OAuth Integration**: Seamless and secure user authentication and authorization through GitHub.
    *   Leverages GitHub's OAuth 2.0 for streamlined login and access.
    *   Manages user sessions securely using JSON Web Tokens (JWTs) and HTTP-only cookies.
    *   Includes CSRF protection during the OAuth flow.
*   **Repository Ingestion and Analysis**: Processes and indexes your GitHub repositories to enable AI features.
    *   Advanced code chunking (`EnhancedCodeChunker`) to intelligently break down code for AI processing.
    *   Extracts valuable metadata like type hints, decorators, and imports from code.
*   **Local File Management**: Manages and saves generated documentation and code edits locally before pushing to GitHub.
*   **GitHub Integration for Code Changes**: Programmatically interacts with GitHub to:
    *   Fetch file content from repositories.
    *   Create new branches and push code changes or documentation updates.
    *   Open Pull Requests for review.
*   **Frontend UI**: An intuitive web interface built with TypeScript and React for managing projects, viewing AI suggestions, and interacting with the system.
    *   Helper utilities for UI elements (e.g., `hexToRgba`, `calculateInsertPosition`, array manipulation).

## 3. Installation

To set up Otto locally, you'll need to have several prerequisites installed.

### Prerequisites

*   **Git**: For cloning the repository.
*   **Node.js & npm/yarn**: For the frontend application.
*   **Python 3.9+ & pip**: For the backend and ingest services.
*   **Docker & Docker Compose** (Recommended): For easily running services and databases.
*   **GitHub Account**: Required for authentication and repository integration.
*   **GitHub OAuth Application**: You'll need to register a new OAuth application on GitHub to get `CLIENT_ID` and `CLIENT_SECRET`.

### Steps

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/otto-pm/otto.git
    cd otto
    ```

2.  **Set up Environment Variables**:
    Create `.env` files in the `backend/`, `ingest-service/`, and `frontend/` directories based on provided examples (or create them manually).

    **`backend/.env`**:
    ```env
    GITHUB_CLIENT_ID=your_github_oauth_client_id
    GITHUB_CLIENT_SECRET=your_github_oauth_client_secret
    JWT_SECRET_KEY=a_very_secret_key_for_jwt_signing
    DATABASE_URL=postgresql://user:password@db:5432/otto_db # Adjust if not using Docker
    FRONTEND_URL=http://localhost:3000
    # Add any other backend specific environment variables
    ```

    **`ingest-service/.env`**:
    ```env
    GITHUB_TOKEN=your_personal_github_token # With repo scope for pushing changes
    OPENAI_API_KEY=your_openai_api_key
    # Add any other ingest-service specific environment variables
    ```

    **`frontend/.env.local`**:
    ```env
    NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
    # Add any other frontend specific environment variables
    ```

3.  **Database Setup (PostgreSQL)**:
    If using Docker Compose, the database will be set up automatically. Otherwise, you'll need to install and configure PostgreSQL manually and update `DATABASE_URL` accordingly.

4.  **Install Backend Dependencies**:
    ```bash
    cd backend
    pip install -r requirements.txt
    # Apply database migrations (if applicable, e.g., using Alembic)
    # alembic upgrade head
    cd ..
    ```

5.  **Install Ingest Service Dependencies**:
    ```bash
    cd ingest-service
    pip install -r requirements.txt
    cd ..
    ```

6.  **Install Frontend Dependencies**:
    ```bash
    cd frontend
    npm install # or yarn install
    cd ..
    ```

7.  **Run Services (using Docker Compose - Recommended)**:
    ```bash
    docker-compose up --build
    ```
    This will build and start all services (backend, ingest-service, frontend, database, etc.).

8.  **Run Services (Manually)**:
    *   **Backend**:
        ```bash
        cd backend
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        ```
    *   **Ingest Service**:
        ```bash
        cd ingest-service
        python main.py # Or run with a WSGI server like Gunicorn if it's an API
        ```
        *(Note: The `ingest-service` might be a long-running process or a serverless function, depending on its design. Adjust command as necessary.)*
    *   **Frontend**:
        ```bash
        cd frontend
        npm run dev # or yarn dev
        ```

## 4. Usage

Once all services are running, you can access Otto through your web browser.

1.  **Access the Frontend**: Open your browser and navigate to `http://localhost:3000` (or the `FRONTEND_URL` you configured).
2.  **Login with GitHub**: Use the "Login with GitHub" button to authenticate. You will be redirected to GitHub, asked to authorize the Otto application, and then redirected back to the Otto dashboard.
3.  **Connect Repositories**: Once logged in, you can connect your GitHub repositories to Otto. This will trigger the ingestion process, allowing Otto's AI to analyze your codebase.
4.  **Utilize AI Features**:
    *   **Generate Documentation**: Navigate to a project or file, and use the "Generate Documentation" feature. Otto will create relevant documentation based on the code.
    *   **Code Completion**: While working on code, you can use the code completion API (or integrated UI elements) to get AI-powered suggestions.
    *   **Project Management**: Use the dashboard to manage tasks, track progress, and collaborate with your team.

### Example: AI-Powered Code Completion (API)

You can interact with the AI features directly via the API. For instance, to get code completion:

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

This will return a contextually aware completion for the provided code snippet, automatically detecting the relevant file in your indexed repository.

## 5. API Reference

Otto exposes several APIs for its various services. Detailed API documentation is available for key components.

### Authentication System API

The Authentication System API handles user login, session management, and authorization.

*   **Overview**: Provides secure user authentication via GitHub OAuth 2.0, issues JWTs for session management, and handles CSRF protection.
*   **Endpoints**:
    *   `GET /login`: Initiates GitHub OAuth flow.
    *   `GET /auth/callback`: Handles GitHub OAuth callback, exchanges code for token, and sets JWT.
    *   `GET /logout`: Clears user session.
    *   `GET /user/me`: Retrieves current authenticated user details.
*   **Security**: Uses HTTP-only cookies for JWTs, CSRF state tokens.

### Ingestion Service API

The Ingestion Service API is responsible for processing repositories, generating documentation, and providing AI-powered code assistance.

*   **Overview**: Manages the pipeline for ingesting repository data, chunking code, and interacting with AI models for various tasks.
*   **Endpoints (Examples)**:
    *   `POST /pipeline/repo/ingest`: Triggers the ingestion process for a given GitHub repository.
    *   `POST /pipeline/doc/generate`: Generates documentation for a specified file or module.
        *   **Parameters**: `repo_full_name`, `target` (file path), `doc_type` (`"api"`, `"module"`, `"readme"`), `push_to_github` (boolean).
    *   `POST /pipeline/code/complete`: Provides AI-powered code completion.
        *   **Parameters**: `repo_full_name`, `code_context`, `language`, `github_token`.
*   **Utilities**: Utilizes `DocumentationManager` for local file saving and `GitHubClient` for GitHub interactions (fetching content, creating branches/PRs).

For comprehensive API details, refer to the dedicated API documentation files within the `backend/docs/api/` directory (e.g., `otto-pm-otto_authentication-system_*.md`).

## 6. Configuration

Otto's behavior can be configured using environment variables. Below are some of the critical configuration parameters:

*   **`GITHUB_CLIENT_ID`**: Your GitHub OAuth application's Client ID. (Backend)
*   **`GITHUB_CLIENT_SECRET`**: Your GitHub OAuth application's Client Secret. (Backend)
*   **`JWT_SECRET_KEY`**: A strong, random secret key used for signing JWTs. (Backend)
*   **`DATABASE_URL`**: Connection string for the PostgreSQL database. (Backend)
*   **`FRONTEND_URL`**: The URL where the frontend application is hosted (e.g., `http://localhost:3000`). Used for CORS and redirects. (Backend)
*   **`GITHUB_TOKEN`**: A GitHub Personal Access Token with `repo` scope, used by the ingest service to read/write to repositories. (Ingest Service)
*   **`OPENAI_API_KEY`**: Your API key for OpenAI or other LLM providers. (Ingest Service)
*   **`OUTPUT_DIR`**: Base directory for saving generated files locally by the `DocumentationManager`. Defaults to `./output`. (Ingest Service)
*   **`NEXT_PUBLIC_BACKEND_URL`**: The URL of the backend API, accessible from the frontend. (Frontend)

It is highly recommended to use a `.env` file for each service to manage these variables. Never commit sensitive information like API keys or secrets directly into your repository.

## 7. Contributing

We welcome contributions to Otto! If you're interested in improving the project, please follow these guidelines:

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
4.  **Make your changes**: Implement your feature or fix. Ensure your code adheres to the project's coding standards.
5.  **Write tests**: Add appropriate unit and integration tests for your changes.
6.  **Update documentation**: If your changes affect any public APIs or features, update the relevant documentation.
7.  **Commit your changes**: Write clear and concise commit messages.
    ```bash
    git commit -m "feat: Add new feature for X"
    ```
8.  **Push to your fork**:
    ```bash
    git push origin feature/your-feature-name
    ```
9.  **Create a Pull Request**: Open a pull request from your branch to the `main` branch of the original `otto-pm/otto` repository. Describe your changes thoroughly and reference any related issues.

### Code Style

*   **Python**: Follow PEP 8 guidelines. Use a linter like `flake8` or `black`.
*   **TypeScript/React**: Adhere to Airbnb's style guide or similar. Use `ESLint` and `Prettier`.

## 8. License

This project is licensed under the [MIT License](LICENSE).

---

**Otto: AI-Powered Project Management Solution** - Empowering developers with intelligent tools.