# API Documentation: Webhook System

## 1. Overview and Purpose

The Webhook System provides a robust mechanism for receiving and processing external events, primarily from GitHub. It acts as an integration point, allowing the Otto AI Project Management Solution to react to changes and activities in connected repositories, such as code pushes, pull requests, and GitHub App installations.

The primary goal of this system is to:
*   **Integrate with External Services**: Seamlessly connect with platforms like GitHub to receive real-time event notifications.
*   **Automate Workflows**: Trigger internal processes, such as RAG (Retrieval Augmented Generation) pipeline ingestion for code changes, documentation generation, or repository synchronization.
*   **Maintain Data Freshness**: Ensure the system's understanding of connected repositories is always up-to-date by reacting to code modifications.
*   **Securely Handle Events**: Verify the authenticity and integrity of incoming webhooks using shared secrets to prevent unauthorized access or tampering.

This documentation details the public API endpoint for receiving webhooks and the internal function responsible for their processing.

---

## 2. API Endpoints

### `POST /webhooks/github`

This endpoint is the entry point for all GitHub webhook events. It receives event payloads and headers, verifies their authenticity, and dispatches them for internal processing.

*   **Description**:
    Receives and processes incoming GitHub webhook events. This endpoint is designed to be called by GitHub whenever a configured event (e.g., `push`, `pull_request`, `installation`) occurs in a repository where the Otto GitHub App is installed. It performs signature verification, parses the event type, and triggers appropriate internal workflows.

*   **Signature**:
    ```python
    async def handle_github_webhook(payload: Dict, headers: Dict) -> Dict:
        # Internal processing logic
    ```
    *(Note: This is a conceptual signature for the public endpoint. The actual implementation will involve FastAPI dependencies for payload and header parsing.)*

*   **Parameters**:

    *   `payload`
        *   **Type**: `Dict` (JSON object)
        *   **Description**: The body of the HTTP POST request, containing the event-specific data from GitHub. The structure of this payload varies significantly based on the `X-GitHub-Event` header.
        *   **Required**: Yes

    *   `headers`
        *   **Type**: `Dict`
        *   **Description**: A dictionary of HTTP headers sent with the webhook request. Key headers for processing include:
            *   `X-GitHub-Event`: Specifies the type of event (e.g., `push`, `pull_request`, `installation`).
            *   `X-Hub-Signature-256`: The HMAC hex digest of the request body, used for verifying the webhook's authenticity.
            *   `Content-Type`: Typically `application/json`.
        *   **Required**: Yes

*   **Return Values**:

    *   **Type**: `Dict` (JSON object)
    *   **Description**: A dictionary indicating the status of the webhook processing. The system aims to return a `200 OK` HTTP status promptly, with the internal processing status reflected in the JSON body. Asynchronous processing may be initiated for complex tasks.
    *   **Example Successful Response**:
        ```json
        {
            "status": "success",
            "message": "Push event processed."
        }
        ```
    *   **Example Unsupported Event Response**:
        ```json
        {
            "status": "success",
            "message": "Unknown GitHub event type: [event_type_name]. Event received but not specifically handled."
        }
        ```
    *   **HTTP Status Codes**:
        *   `200 OK`: Indicates that the webhook was successfully received and acknowledged, and initial processing (including event type identification) has begun. This is the standard response for both successfully handled and unhandled (but recognized) GitHub events.
        *   `400 Bad Request`: If essential headers are missing or malformed, or the payload cannot be parsed.
        *   `401 Unauthorized`: If the `X-Hub-Signature-256` header fails verification, indicating a potentially malicious or unauthorized request.

*   **Error Handling**:

    The webhook endpoint implements several layers of error handling:

    1.  **Webhook Signature Verification**:
        *   **Mechanism**: The system verifies the `X-Hub-Signature-256` header against a computed signature using a shared secret. This ensures the request genuinely originated from GitHub and has not been tampered with.
        *   **Behavior**: If verification fails, the request is rejected with a `401 Unauthorized` HTTP status code, and no further processing occurs.
        *   **Exception**: `HTTPException` (FastAPI) or similar internal security exception.

    2.  **Missing/Invalid Headers**:
        *   **Mechanism**: Checks for the presence and validity of critical headers like `X-GitHub-Event`.
        *   **Behavior**: If required headers are missing or malformed, a `400 Bad Request` HTTP status code is returned.
        *   **Exception**: `HTTPException` (FastAPI) or similar validation error.

    3.  **Unsupported Event Types**:
        *   **Mechanism**: The `X-GitHub-Event` header is parsed to identify the event type. While the system handles `push` and `pull_request` events explicitly, other GitHub events might be received.
        *   **Behavior**: For unsupported event types, the system acknowledges receipt with a `200 OK` status and a JSON response indicating that the event was received but not specifically processed (e.g., `{"status": "success", "message": "Unknown GitHub event type: [event_type_name]"}`). This prevents GitHub from marking the webhook as failed.

    4.  **Internal Processing Errors**:
        *   **Mechanism**: Errors occurring during the asynchronous processing of a valid event (e.g., failure to trigger the RAG pipeline, issues with GitHub API calls for creating branches/PRs).
        *   **Behavior**: Since the webhook endpoint returns `200 OK` promptly (often before asynchronous processing completes), these errors typically do not result in an immediate HTTP error response to GitHub. Instead, they are logged internally, and appropriate alerts or retry mechanisms are triggered within the system. The initial `200 OK` response signifies successful *reception* and *dispatch*, not necessarily the *completion* of all subsequent tasks.

*   **Usage Example**:

    To simulate a GitHub `push` event, you would send a `POST` request to `/webhooks/github` with a JSON payload and specific headers.
    *(Note: Replace `YOUR_WEBHOOK_SECRET` with the actual secret configured for your GitHub App webhook.)*

    ```bash
    curl -X POST "https://api.otto-pm.com/webhooks/github" \
         -H "Content-Type: application/json" \
         -H "X-GitHub-Event: push" \
         -H "X-GitHub-Delivery: a1b2c3d4-e5f6-7890-1234-567890abcdef" \
         -H "X-Hub-Signature-256: sha256=YOUR_WEBHOOK_SECRET_SIGNATURE" \
         -d '{
               "ref": "refs/heads/main",
               "before": "a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4",
               "after": "b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5",
               "repository": {
                 "id": 123456789,
                 "node_id": "MDEwOlJlcG9zaXRvcnkxMjM0NTY3ODk=",
                 "name": "example-repo",
                 "full_name": "octocat/example-repo",
                 "private": false,
                 "owner": {
                   "login": "octocat",
                   "id": 1,
                   "type": "User"
                 },
                 "html_url": "https://github.com/octocat/example-repo",
                 "description": "An example repository",
                 "fork": false,
                 "url": "https://api.github.com/repos/octocat/example-repo"
               },
               "pusher": {
                 "name": "octocat",
                 "email": "octocat@github.com"
               },
               "sender": {
                 "login": "octocat",
                 "id": 1,
                 "type": "User"
               },
               "created": false,
               "deleted": false,
               "forced": false,
               "base_ref": null,
               "compare": "https://github.com/octocat/example-repo/compare/a1b2c3d4...b2c3d4e5",
               "commits": [
                 {
                   "id": "b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5",
                   "tree_id": "c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f6",
                   "distinct": true,
                   "message": "Update README.md",
                   "timestamp": "2023-10-27T10:00:00Z",
                   "url": "https://github.com/octocat/example-repo/commit/b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5",
                   "author": {
                     "name": "Octocat",
                     "email": "octocat@github.com",
                     "username": "octocat"
                   },
                   "committer": {
                     "name": "Octocat",
                     "email": "octocat@github.com",
                     "username": "octocat"
                   },
                   "added": [],
                   "removed": [],
                   "modified": ["README.md"]
                 }
               ],
               "head_commit": {
                 "id": "b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5",
                 "tree_id": "c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f6",
                 "distinct": true,
                 "message": "Update README.md",
                 "timestamp": "2023-10-27T10:00:00Z",
                 "url": "https://github.com/octocat/example-repo/commit/b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5",
                 "author": {
                   "name": "Octocat",
                   "email": "octocat@github.com",
                   "username": "octocat"
                 },
                 "committer": {
                   "name": "Octocat",
                   "email": "octocat@github.com",
                   "username": "octocat"
                 },
                 "added": [],
                 "removed": [],
                 "modified": ["README.md"]
               }
             }'
    ```

---

## 3. Internal Functions (Used by API Endpoints)

### `process_webhook`

This is an internal method, likely part of a `WebhookService` or similar class, responsible for the core logic of parsing and reacting to specific GitHub event types.

*   **Description**:
    Processes the raw webhook payload and headers, identifies the GitHub event type, and dispatches the event to the appropriate handler. It currently supports `push` and `pull_request` events and provides a fallback for other event types. This function is typically called by the public `POST /webhooks/github` endpoint after initial validation and signature verification.

*   **Signature**:
    ```python
    def process_webhook(self, payload: Dict, headers: Dict) -> Dict:
    ```

*   **Parameters**:

    *   `self`
        *   **Type**: Instance of the containing class (e.g., `WebhookService`).
        *   **Description**: The instance of the class on which this method is called.
        *   **Required**: Yes (implicit for instance methods)

    *   `payload`
        *   **Type**: `Dict`
        *   **Description**: The webhook payload received from GitHub, deserialized into a Python dictionary.
        *   **Required**: Yes

    *   `headers`
        *   **Type**: `Dict`
        *   **Description**: A dictionary of HTTP headers from the webhook request. Used primarily to extract the `X-GitHub-Event` type.
        *   **Required**: Yes

*   **Return Values**:

    *   **Type**: `Dict`
    *   **Description**: A dictionary indicating the outcome of the internal processing. This dictionary is typically serialized and returned as the JSON response to the webhook sender.
    *   **Example `push` event processed**:
        ```json
        {"status": "success", "message": "Push event processed."}
        ```
    *   **Example `pull_request` event processed**:
        ```json
        {"status": "success", "message": "Pull Request event processed."}
        ```
    *   **Example unknown event type**:
        ```json
        {"status": "success", "message": "Unknown GitHub event type: [event_type_name]"}
        ```

*   **Error Handling**:

    The `process_webhook` function itself is designed to handle different event types gracefully.

    1.  **Missing `X-GitHub-Event` Header**:
        *   **Mechanism**: If the `X-GitHub-Event` header is not present, the `headers.get('X-GitHub-Event')` call will return `None`, leading to the `elif event_type:` block being skipped.
        *   **Behavior**: The current implementation does not explicitly raise an error for a missing `X-GitHub-Event` within this function. It would likely be caught at a higher level (e.g., by the FastAPI endpoint handler) as a `400 Bad Request`. If it somehow reached this function without `event_type`, it would fall through without returning a specific status. A more robust implementation might explicitly check for its presence here.

    2.  **Unsupported Event Type**:
        *   **Mechanism**: If `X-GitHub-Event` is present but does not match `push` or `pull_request`.
        *   **Behavior**: The function logs the unknown event type and returns a success status with a message indicating that the event was received but not specifically handled. This ensures the webhook sender receives a `200 OK` and doesn't mark the webhook as failed.
        *   **Example**: `print(f"Unknown GitHub event type: {event_type}")` followed by `return {"status": "success", "message": "s..."}` (truncated in chunk, but implies a message like "Unknown event type received").

    3.  **Internal Processing Failures (within event handlers)**:
        *   **Mechanism**: The provided code snippets for `push` and `pull_request` events are placeholders (`# Process push event`). In a full implementation, these blocks would contain calls to other services (e.g., RAG pipeline).
        *   **Behavior**: If these internal service calls fail, the `process_webhook` function, as currently shown, would still return `{"status": "success", "message": "..."}`. A more robust system would wrap these internal calls in `try-except` blocks and return a `{"status": "failed", "message": "..."}` or raise specific exceptions that could be caught by the API endpoint to potentially return a `500 Internal Server Error` if the failure is critical and immediate. Given the `checklist.md`'s "Return 200 OK promptly (process async if needed)", it's implied that such failures would be handled asynchronously and not block the webhook response.

---

## 4. Common Use Cases

The webhook system is fundamental for integrating Otto with GitHub and enabling automated, event-driven workflows:

1.  **Automated Code Ingestion and RAG Pipeline Triggering**:
    *   **Scenario**: A developer pushes new code or updates existing code to a connected GitHub repository.
    *   **Webhook Event**: `push` event.
    *   **System Action**: The webhook system receives the `push` event, identifies the repository and workspace, and triggers the RAG (Retrieval Augmented Generation) pipeline. This pipeline then ingests the new or changed code, updates the knowledge base, and ensures the AI can answer questions based on the latest codebase. This is crucial for maintaining an up-to-date understanding of the project.

2.  **Pull Request Analysis and Feedback**:
    *   **Scenario**: A developer opens or updates a pull request in a connected GitHub repository.
    *   **Webhook Event**: `pull_request` event.
    *   **System Action**: The webhook system receives the `pull_request` event. It can then initiate automated code reviews, generate summaries of changes, identify potential issues, or provide AI-powered suggestions directly within the pull request comments.

3.  **GitHub App Installation and Configuration**:
    *   **Scenario**: A user installs the Otto GitHub App on a new repository or organization, or uninstalls it.
    *   **Webhook Event**: `installation` or `installation_repositories` events.
    *   **System Action**: The webhook system processes these events to record the installation ID, verify required permissions, and link the GitHub installation to the corresponding workspace within Otto. This ensures that Otto has the necessary access to the repository and can manage its lifecycle within the platform.

4.  **Repository Synchronization and Metadata Updates**:
    *   **Scenario**: Changes occur to repository metadata (e.g., description, default branch, rename) or branch protection rules.
    *   **Webhook Event**: Various events like `repository`, `branch_protection_rule`.
    *   **System Action**: While not explicitly handled in the provided `process_webhook` snippet, the system can be extended to listen for these events to keep Otto's internal representation of the repository synchronized with GitHub, ensuring accurate project context.

5.  **CI/CD Integration and Workflow Orchestration**:
    *   **Scenario**: Beyond code ingestion, webhooks can be used to trigger broader CI/CD workflows, such as running tests, deploying applications, or updating project boards based on specific GitHub events.
    *   **Webhook Event**: `push`, `pull_request`, `status`, `check_run`, etc.
    *   **System Action**: The webhook system can act as a central orchestrator, receiving events and forwarding them to various downstream services or triggering internal automation scripts to manage the entire development lifecycle.