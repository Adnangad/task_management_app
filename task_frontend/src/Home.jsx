import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import './Home.css';
import headerImage from '../src/assets/images/header.jpeg';
import { useSpring, animated } from 'react-spring';

function Home() {
    const token = sessionStorage.getItem('token');
    const [tasks, setTasks] = useState([]);
    const [createdTask, setCreate] = useState("");
    const [message, setMessage] = useState("");
    const [errorMessage, setError] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const getTasks = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/getTasks', {
                    method: "GET",
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Token': token
                    }
                });

                if (response.status === 200) {
                    const data = await response.json();
                    setTasks(data.tasks);
                } else if (response.status === 401) {
                    alert('Session expired. Redirecting to login.');
                    navigate('/login');
                } else {
                    setError('Failed to fetch tasks');
                }
            } catch (error) {
                setError('Unable to fetch tasks at this time');
            }
        };
        getTasks();
    }, [token, navigate]);

    const createATask = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://127.0.0.1:8000/createTask', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-Token': token
                },
                body: JSON.stringify({ task: createdTask }),
            });

            const rez = await response.json();
            if (response.status === 200) {
                setMessage(rez.message);
            } else {
                setError(rez.error);
            }
        } catch (error) {
            setError(error);
        }
    };

    const updateTask = async (taskId) => {
        try {
            const response = await fetch('http://127.0.0.1:8000/updateTask', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Token': token
                },
                body: JSON.stringify({ task_id: taskId })
            });

            const rez = await response.json();
            if (response.status === 200) {
                alert('Task updated successfully');
            } else {
                alert(rez.error);
            }
        } catch (error) {
            alert(error);
        }
    };

    const deleteTask = async (taskId) => {
        try {
            const response = await fetch('http://127.0.0.1:8000/deltask', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Token': token
                },
                body: JSON.stringify({ task_id: taskId })
            });

            const rez = await response.json();
            if (response.status === 200) {
                alert('Task deleted successfully');
            } else {
                alert(rez.error);
            }
        } catch (error) {
            alert(error);
        }
    };

    return (
        <>
            <header className="header">
                <h2>Task Management</h2>
                <Link className="account" to="/account">Account</Link>
            </header>

            <div className="container">
                <div className="create-task">
                    <h3>Create a Task</h3>
                    <form className="create-form" onSubmit={createATask}>
                        <input
                            required
                            type="text"
                            name="task"
                            value={createdTask}
                            onChange={(e) => setCreate(e.target.value)}
                        />
                        <button type="submit">Create Task</button>
                    </form>
                    {message && <p className="success-message">{message}</p>}
                    {errorMessage && <p className="error-message">{errorMessage}</p>}
                </div>

                <div className="all-tasks">
                    {tasks.map(task => (
                        <div key={task.id} className={`task ${task.status ? 'completed' : 'incomplete'}`}>
                            <p>{task.task}</p>
                            <p>Status: {task.status ? "Complete" : "Incomplete"}</p>
                            <button onClick={() => updateTask(task.id)}>
                                Mark as {task.status ? "Incomplete" : "Complete"}
                            </button>
                            <button className="delete-btn" onClick={() => deleteTask(task.id)}>
                                Delete
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
}

export default Home;
