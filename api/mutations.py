from datetime import datetime

from ariadne import convert_kwargs_to_snake_case

from api import db
from api.models import MyUser, Task

from flask_graphql_auth import create_access_token, mutation_header_jwt_required, get_jwt_identity


@convert_kwargs_to_snake_case
def resolve_register(obj, info, name, username, password):
    try:
        user = MyUser(
            name=name, username=username, password=password
        )
        db.session.add(user)
        db.session.commit()
        payload = {
            "success": True,
            "user": user.to_dict(),
            "token": create_access_token(username)
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }

    return payload


@mutation_header_jwt_required
@convert_kwargs_to_snake_case
def resolve_create_task(obj, info, task):
    try:
        user_id = get_jwt_identity()['id']

        due_date = datetime.strptime(task['due_date'], '%d-%m-%Y').date()
        new_task = Task(
            user_id=user_id, title=task['title'], description=task['description'], due_date=due_date
        )

        db.session.add(new_task)
        db.session.commit()
        payload = {
            "success": True,
            "task": new_task.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }

    return payload


@mutation_header_jwt_required
@convert_kwargs_to_snake_case
def resolve_create_tasks(obj, info, tasks):
    try:
        user_id = get_jwt_identity()['id']

        new_tasks = []
        tasks_dic = []
        for task in tasks:
            due_date = datetime.strptime(task['due_date'], '%d-%m-%Y').date()
            new_task = Task(
                user_id=user_id, title=task['title'], description=task['description'], due_date=due_date
            )

            new_tasks.append(new_task)

        db.session.add_all(new_tasks)
        db.session.commit()

        tasks_dic = [new_task.to_dict() for new_task in new_tasks]

        payload = {
            "success": True,
            "tasks": tasks_dic,
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }

    return payload


@mutation_header_jwt_required
@convert_kwargs_to_snake_case
def resolve_update_due_date(obj, info, id, new_date):
    try:
        user_id = get_jwt_identity()['id']

        task = Task.query.filter((Task.id == id) & (
            Task.user_id == user_id)).first()

        if task:
            task.due_date = datetime.strptime(new_date, '%d-%m-%Y').date()
        db.session.add(task)
        db.session.commit()
        payload = {
            "success": True,
            "task": task.to_dict()
        }

    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": ["Incorrect date format provided. Date should be in "
                       "the format dd-mm-yyyy"]
        }
    except AttributeError:  # task not found
        payload = {
            "success": False,
            "errors": [f"Task matching id {id} not found"]
        }
    return payload


@mutation_header_jwt_required
@convert_kwargs_to_snake_case
def resolve_update_status(obj, info, id, new_status):
    try:
        user_id = get_jwt_identity()['id']

        task = Task.query.filter((Task.id == id) & (
            Task.user_id == user_id)).first()

        if task:
            task.status = new_status
        db.session.add(task)
        db.session.commit()
        payload = {
            "success": True,
            "task": task.to_dict()
        }

    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": ["Incorrect date format provided. Date should be in "
                       "the format dd-mm-yyyy"]
        }
    except AttributeError:  # task not found
        payload = {
            "success": False,
            "errors": [f"Task matching id {id} not found"]
        }
    return payload


@mutation_header_jwt_required
@convert_kwargs_to_snake_case
def resolve_delete_task(obj, info, id):
    try:
        user_id = get_jwt_identity()['id']

        task = Task.query.filter((Task.id == id) & (
            Task.user_id == user_id)).first()
        db.session.delete(task)
        db.session.commit()
        payload = {"success": True}

    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"Task matching id {id} not found"]
        }

    return payload
