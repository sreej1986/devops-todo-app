// frontend/script.js
const BACKEND_URL = 'http://54.211.122.75'; // Will be replaced by deployed URL

document.addEventListener('DOMContentLoaded', fetchTodos);

async function fetchTodos() {
    try {
        const response = await fetch(`${BACKEND_URL}/todos`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const todos = await response.json();
        renderTodos(todos);
    } catch (error) {
        console.error('Error fetching todos:', error);
        document.getElementById('todoList').innerHTML = '<li>Error loading todos. Please check backend.</li>';
    }
}

async function addTodo() {
    const input = document.getElementById('todoInput');
    const task = input.value.trim();
    if (task === '') return;

    try {
        const response = await fetch(`${BACKEND_URL}/todos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task: task })
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        input.value = '';
        fetchTodos(); // Refresh list
    } catch (error) {
        console.error('Error adding todo:', error);
        alert('Could not add To-Do. See console for details.');
    }
}

async function toggleComplete(id, currentStatus) {
    try {
        const response = await fetch(`${BACKEND_URL}/todos/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ completed: !currentStatus })
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        fetchTodos(); // Refresh list
    } catch (error) {
        console.error('Error toggling complete:', error);
        alert('Could not update To-Do. See console for details.');
    }
}

async function deleteTodo(id) {
    if (!confirm('Are you sure you want to delete this To-Do?')) return; // Minimal alert, replace with modal for production

    try {
        const response = await fetch(`${BACKEND_URL}/todos/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        fetchTodos(); // Refresh list
    } catch (error) {
        console.error('Error deleting todo:', error);
        alert('Could not delete To-Do. See console for details.');
    }
}

function renderTodos(todos) {
    const todoList = document.getElementById('todoList');
    todoList.innerHTML = '';
    if (todos.length === 0) {
        todoList.innerHTML = '<li>No To-Dos yet! Add one above.</li>';
        return;
    }
    todos.forEach(todo => {
        const li = document.createElement('li');
        li.className = todo.completed ? 'completed' : '';
        li.innerHTML = `
            <span>${todo.task}</span>
            <div class="actions">
                <button class="complete-btn" onclick="toggleComplete('${todo.id}', ${todo.completed})">✔</button>
                <button class="delete-btn" onclick="deleteTodo('${todo.id}')">✖</button>
            </div>
        `;
        todoList.appendChild(li);
    });
}
