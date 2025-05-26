from fastapi import HTTPException, status

INVALID_TEMPLATE_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid template",
)

