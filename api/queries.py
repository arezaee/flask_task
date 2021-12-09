from flask_graphql_auth.util import get_jwt_identity
from .models import MyUser, Task
from ariadne import convert_kwargs_to_snake_case
from flask_graphql_auth import create_access_token, query_header_jwt_required


@convert_kwargs_to_snake_case
def resolve_users(obj, info):
    try:
        users = [user.to_dict() for user in MyUser.query.all()]
        payload = {
            "success": True,
            "users": users
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def resolve_login(obj, info, username, password):
    try:
        user = MyUser.query.filter((MyUser.username == username) & (
            MyUser.password == password)).first()
        payload = {
            "success": True,
            "user": user.to_dict(),
            "token": create_access_token({"id": user.id, "username": username})
        }

    except Exception:
        payload = {
            "success": False,
            "errors": [f"Wrong Username or Password"]
        }

    return payload


@query_header_jwt_required
@convert_kwargs_to_snake_case
def resolve_tasks(obj, info, status=None, due_date=None):
    try:
        user_id = get_jwt_identity()['id']

        tasks_obj = Task.query.filter(Task.user_id == user_id)
        if status != None:
            tasks_obj = tasks_obj.filter(Task.status == status)
        if due_date != None:
            tasks_obj = tasks_obj.filter(Task.due_date == due_date)

        tasks_obj = tasks_obj.all()
        tasks = [task.to_dict() for task in tasks_obj]
        payload = {
            "success": True,
            "tasks": tasks
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@query_header_jwt_required
@convert_kwargs_to_snake_case
def resolve_task(obj, info, id):
    try:
        user_id = get_jwt_identity()['id']

        task = Task.query.filter((Task.id == id) & (
            Task.user_id == user_id)).first()

        payload = {
            "success": True,
            "task": task.to_dict()
        }

    except AttributeError:  # task not found
        payload = {
            "success": False,
            "errors": [f"Task item matching id {id} not found"]
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload


def test(obj, info, id):
    return {
        "success": False,
        "errors": ["AAA"]
    }
