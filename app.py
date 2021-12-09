from api import app, db
from api import models

from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.queries import resolve_login, resolve_users, resolve_task, resolve_tasks, test
from api.mutations import resolve_create_tasks, resolve_delete_task, resolve_register, resolve_create_task, resolve_update_due_date, resolve_update_status


query = ObjectType("Query")

query.set_field("login", resolve_login)
query.set_field("users", resolve_users)
query.set_field("task", resolve_task)
query.set_field("tasks", resolve_tasks)


mutation = ObjectType("Mutation")
mutation.set_field("register", resolve_register)
mutation.set_field("createTask", resolve_create_task)
mutation.set_field("createTasks", resolve_create_tasks)
mutation.set_field("updateDueDate", resolve_update_due_date)
mutation.set_field("updateStatus", resolve_update_status)
mutation.set_field("deleteTask", resolve_delete_task)


type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
