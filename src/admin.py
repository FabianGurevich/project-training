from src.models.user import Users
from sqladmin import ModelView


class UserAdmin(ModelView, model=Users):
    column_list = [
        Users.email,
        Users.id,
    ]
    column_searchable_list = [Users.id, Users.email]
