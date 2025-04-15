import os

from sqladmin import Admin, ModelView
from admin.auth import AdminAuth
from db.models_orm import Cheese, Category, Blog
from dotenv import load_dotenv

load_dotenv()


class CheeseAdmin(ModelView, model=Cheese):
    column_list = [Cheese.id, Cheese.name, Cheese.country, Cheese.fat_content, Cheese.is_pasteurized]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name, Category.description]
    name = "Categorie"
    form_columns = [Category.name, Category.description, Category.image_url]


class BlogAdmin(ModelView, model=Blog):
    column_list = [Blog.id, Blog.name, Blog.short_description]


def register_admin(app, engine):
    authentication_backend = AdminAuth(secret_key=os.getenv("SECRET_KEY"))
    admin = Admin(app, engine, authentication_backend=authentication_backend, base_url="/admin")
    admin.add_view(CheeseAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(BlogAdmin)
