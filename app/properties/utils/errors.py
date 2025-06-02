from fastapi import HTTPException, status

OWNER_DOES_NOT_EXIST = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Owner doesn't exist",
)

