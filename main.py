from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


app = FastAPI()

# Pydantic model for To-Do items
class TodoItem(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoItemResponse(TodoItem):
    id: int
    created_at: str

# In-memory storage (list of todo items)
todos = []
next_id = 1

# Helper function to find todo by ID
def find_todo_by_id(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    return None

# Helper function to get index of todo by ID
def find_todo_index(todo_id: int):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            return index
    return -1

#  GET ALL TODOS - See your entire to-do list
@app.get("/todos", response_model=List[TodoItemResponse])
def get_all_todos():
    return todos


#  GET SINGLE TODO - Look at one specific to-do
@app.get("/todos/{todo_id}", response_model=TodoItemResponse)
def get_todo(todo_id: int):
   
    todo = find_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="To-do item not found")
    return todo


#  ADD NEW TODO - Add a new task to your list
@app.post("/todos", response_model=TodoItemResponse)
def create_todo(todo: TodoItem):
   
    global next_id
    
    new_todo = {
        "id": next_id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "created_at": datetime.now().isoformat()
    }
    
    todos.append(new_todo)
    next_id += 1
    
    return new_todo

#  UPDATE TODO - Mark a task as completed or update it
@app.put("/todos/{todo_id}", response_model=TodoItemResponse)
def update_todo(todo_id: int, todo_update: TodoItem):
   
    todo_index = find_todo_index(todo_id)
    if todo_index == -1:
        raise HTTPException(status_code=404, detail="To-do item not found")
    
    todos[todo_index].update({
        "title": todo_update.title,
        "description": todo_update.description,
        "completed": todo_update.completed
    })
    
    return todos[todo_index]

#  DELETE TODO - Remove a task from your list
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    
    todo_index = find_todo_index(todo_id)
    if todo_index == -1:
        raise HTTPException(status_code=404, detail="To-do item not found")
    
    deleted_todo = todos.pop(todo_index)
    
    return {
        "message": "To-do item deleted successfully",
        "deleted_item": deleted_todo}