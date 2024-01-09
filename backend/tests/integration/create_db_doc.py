from passlib.context import CryptContext
from pymongo.database import Database

from backend.app.schemas.passwords import PasswordList, PasswordStaging
from backend.app.schemas.user import User


# TODO -> Create a class for each collection
class CreateDbDoc:
    def __init__(
        self,
        database: Database,
    ) -> None:
        self._users_collection = database.get_collection("users")
        self._passwords_staging_collection = database.get_collection(
            "users.passwords-staging"
        )
        self._passwords_collection = database.get_collection("users.password")

    def create_user(self, user: User) -> User:
        """Create user in database."""
        user = user.model_dump()
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user["password"] = pwd_context.hash(user["password"])

        user["_id"] = user["id"]
        user.pop("id")
        self._users_collection.insert_one(user)

        doc = self._users_collection.find_one({"_id": user["_id"]})

        user = {k: v for k, v in doc.items() if k != "_id"}
        user["id"] = str(doc["_id"])

        return User(**user)

    def create_password_staging(
        self, password_stg: PasswordStaging
    ) -> PasswordStaging:
        """Create password_stg in database."""
        password_stg = password_stg.model_dump()
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        password_stg["password"] = pwd_context.hash(password_stg["password"])

        password_stg["_id"] = password_stg["id"]
        password_stg.pop("id")
        self._passwords_staging_collection.insert_one(password_stg)

        doc = self._passwords_staging_collection.find_one(
            {"_id": password_stg["_id"]}
        )

        password = {k: v for k, v in doc.items()}
        password["id"] = str(doc["_id"])
        return PasswordStaging(**password)

    # TODO -> Create a function to insert only one element in to list
    def create_password_list(
        self, password_list: PasswordList
    ) -> PasswordList:
        """Create password_list in database."""
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        for password_header in password_list.passwords:
            password_header.password = pwd_context.hash(
                password_header.password
            )

        password_list = password_list.model_dump()

        password_list["_id"] = password_list["id"]
        password_list.pop("id")
        self._passwords_collection.insert_one(password_list)

        doc = self._passwords_collection.find_one(
            {"_id": password_list["_id"]}
        )

        passwords = {k: v for k, v in doc.items()}
        return PasswordList(
            id=passwords["_id"],
            passwords=passwords["passwords"],
        )
