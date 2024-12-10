from fastapi import Depends

from db.repository.user import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo
