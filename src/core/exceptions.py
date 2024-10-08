from fastapi import HTTPException, status

item_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Item not found",
)

user_already_exists_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
)

incorrect_login_of_password_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Неверный логин или пароль"
)
