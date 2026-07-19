"""A simple Flask application to manage a todo list using in-memory storage."""
from flask import Flask, request

database = {}
app = Flask(__name__)

@app.route("/")
def index():
    """Landing endpoint."""
    return "Welcome!"

@app.route('/tasks', methods=['POST'])
def post_todo_details():
    """Handles POST request to create a new todo item."""
    try:
        data = request.get_json()
        task_name = data["name"]
        status = data["status"]
        database[task_name] = status
        return 'Success', 200
    except (KeyError, TypeError, ValueError) as e:
        app.logger.error("Error during saving object: %s", e)
        return 'Failed', 400

@app.route('/tasks', methods=['PUT'])
def put_todo_details():
    """Handles PUT request to update a todo item."""
    try:
        data = request.get_json()
        task_name = data["name"]
        status = data["status"]
        database[task_name] = status
        return 'Success', 200
    except (KeyError, TypeError, ValueError) as e:
        app.logger.error("Error during updating object: %s", e)
        return 'Failed', 400

@app.route('/tasks', methods=['GET'])
def get_todo_details():
    """
    Handles GET request to:
    - Return all task names with statuses if no query param is provided.
    - Return specific task status if 'name' query param is present.
    """
    task_name = request.args.get("name")

    if task_name:
        status = database.get(task_name)
        if status is None:
            return 'Record Not Found', 404
        return f'Record Found {task_name} status is {status}', 200
    else:
        if not database:
            return 'No tasks found', 200
        # Format the response for all tasks as plain text
        response_lines = [f"{name} - {status}" for name, status in database.items()]
        return "\n".join(response_lines), 200


@app.route('/tasks/<task_name>', methods=['DELETE'])
def delete_todo_details(task_name):
    """Handles DELETE request to remove a todo item by name."""
    try:
        database.pop(task_name)
        return 'Record deleted successfully', 200
    except KeyError:
        return 'Record Not Found', 404
    except (RuntimeError, ValueError) as e:
        app.logger.error("Unexpected error: %s", e)
        return 'Unexpected error occurred', 500
    
if __name__ == '__main__':
    app.run(debug=True)

