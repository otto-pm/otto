def verify_webhook_signature(request: Request, secret: str) -> bool:
```python
    signature_header = request.headers.get("X-Signature")
    if not signature_header:
        return False

    # Assuming signature format is "sha25