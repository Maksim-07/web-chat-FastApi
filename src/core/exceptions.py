from fastapi import HTTPException, status

user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)

id_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User ID not found",
)

login_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User login not found",
)

token_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Token not found",
)

user_already_exists_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The user already exists",
)

incorrect_password_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid password",
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)

invalid_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token",
)
