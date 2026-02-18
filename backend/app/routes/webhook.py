def verify_webhook_signature
(request: Request, secret: str) -> bool:
    """
    Verifies the signature of an incoming webhook request.

    Args:
        request: The FastAPI Request object containing