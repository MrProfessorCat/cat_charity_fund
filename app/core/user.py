from typing import Union

from fastapi import Depends
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


# Асинхронный генератор для обеспечения доступа к БД через SQLAlchemy
# Нужен в качестве зависимости для объекта класса UserManager
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


# Транспорт - способ передачи токена аутнтификации
# BearerTransport - передача токена через заголовок HTTP-запроса Authorization
# tokenUrl - URL для получения токена
bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


# Стратегия - способ генерации и хранения токена
# JWT Strategy - аутентификационный токен содержится непосредственно в передаваемом JWT.
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


# Объект бэкенда аутентификации с выбранными параметрами.
auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


# объект класса FastAPIUsers — объект,
# связывающий объект класса UserManager и бэкенд аутентификации.
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

# Методы для использования в DL (Dependency Injection)
# для получения текущего пользователя и суперюзера
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
