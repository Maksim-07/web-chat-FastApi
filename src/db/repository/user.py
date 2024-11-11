from db.models.user import User
from db.repository.base import BaseDatabaseRepository


class UserRepository(BaseDatabaseRepository[User]):
    model = User
