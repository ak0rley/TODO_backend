# Intern Project: Todo API

Welcome to your first real project. By the time you finish this, you will have built something that works exactly like the apps you use every day — a frontend you can see and click, talking to a backend you built from scratch, saving data to a real database. That is not a small thing.

Take your time with each section. If something doesn't make sense, re-read it before asking for help. The skill of figuring things out from reading is just as important as the code itself.

---

## What Are We Building?

A Todo app. You've probably seen hundreds of them. But this time, you're not just using one — you're building one. And you're building it properly, in three separate pieces that talk to each other.

Here's the big picture:

- A **React frontend** — the part users see and click on in their browser
- A **Django API** — the engine in the middle that handles all the logic
- A **PostgreSQL database** — where all the data actually lives

Think of it like a restaurant. The React frontend is the dining room — it's what the customer sees. The Django API is the kitchen — it does all the work. The database is the pantry — it stores everything.

---

## Part 1: Understanding the Stack

### What is Django?

Django is a Python web framework. A framework is a set of tools that someone else already built, so you don't have to start from zero. Django handles a lot of the boring stuff — connecting to the database, routing URLs, managing users — so you can focus on your specific app.

### What is Django REST Framework (DRF)?

By default, Django is built to serve HTML pages (websites). But we don't want HTML — we want our backend to speak **JSON**, so that our React frontend can talk to it. Django REST Framework is a plugin for Django that makes it easy to build APIs that speak JSON. An API (Application Programming Interface) is basically a set of rules for how two programs can talk to each other.

### What is React?

React is a JavaScript library for building user interfaces. Instead of writing raw HTML that never changes, React lets you build components — reusable pieces of UI that update automatically when data changes. When you add a task and the list updates without refreshing the page, that's React doing its job.

### What is PostgreSQL?

PostgreSQL (often called Postgres) is a database. It stores your data in tables — like spreadsheets — and you can query it to find, create, update, or delete records. Django talks to Postgres through something called an ORM (Object-Relational Mapper), which means you write Python code and Django translates it into database language (SQL) for you.

---

## Part 2: The Data Model

Every app needs to think about its data first. What information are we storing?

For this app, we have two things: **Users** and **Tasks**.

### Users
We're using Django's built-in User model. You don't need to create this — it already exists. It has fields like username, email, and password built in.

### Tasks
You will create this model yourself. A task has:

- **title** — what the task is (e.g. "Buy groceries")
- **completed** — whether it's done or not (true or false)
- **created_at** — when it was created (Django fills this in automatically)
- **user** — which user this task belongs to (this is the important one — every task must be linked to a user)

That link between a task and a user is called a **foreign key**. It's how the database knows "this task belongs to this user, not to someone else."

---

## Part 3: The API Endpoints

An endpoint is a URL that your frontend sends requests to. Think of each endpoint as a door into your backend, and different HTTP methods (GET, POST, PATCH, DELETE) as different ways of knocking.

Here are all the endpoints you'll build:

### Authentication

| Method | URL | What it does |
|--------|-----|--------------|
| POST | /api/auth/register/ | Create a new account |
| POST | /api/auth/login/ | Log in and receive a token |

### Tasks

| Method | URL | What it does |
|--------|-----|--------------|
| GET | /api/tasks/ | Get all your tasks |
| POST | /api/tasks/ | Create a new task |
| PATCH | /api/tasks/{id}/ | Edit a task (change title or mark complete) |
| DELETE | /api/tasks/{id}/ | Delete a task |

### What is a Token?

When you log in, the server gives you a **token** — a long string of random characters, like a digital ID card. Every time your frontend makes a request after that, it includes this token in the request header. The server checks it and says "okay, I know who this is" and responds with only that user's data.

This is why storing the token correctly matters. Your React app will save it in localStorage and attach it to every API request.

---

## Part 4: The Frontend

Your React app will have three main components:

### TaskList
This component loads when the page opens. It calls the API to get all the user's tasks and displays them as a list. It re-renders automatically when tasks are added or deleted.

### TaskForm
A simple text input and a submit button. When the user types a task name and clicks submit, it sends a POST request to the API to create the task. After it succeeds, the task list should update.

### TaskItem
A single row in the list. It shows the task title, a checkbox to mark it complete, and a delete button. Clicking the checkbox sends a PATCH request. Clicking delete sends a DELETE request.

---

## Part 5: What You Need to Deliver

By the end of this project, you must have all of the following working:

1. A Django project with the Task model created and migrations applied
2. A DRF serializer and viewset that returns only the logged-in user's tasks (not everyone's tasks — this is important)
3. Register and login working and testable via Postman or Thunder Client before you write any React
4. A React app that stores the token after login and attaches it to every request
5. All four task operations working end to end: create, read, update, delete

---

## Part 6: Things That Will Trip You Up

Read this section carefully. These are the most common mistakes:

### CORS Error
When your React app (running on port 3000) tries to talk to your Django server (running on port 8000), the browser will block it by default. This is a security rule called CORS. You need to install a Django package called `django-cors-headers` and configure it. If you see an error in the browser console about "blocked by CORS policy", this is why.

### Returning All Tasks Instead of Just Yours
When you write your task list endpoint, the wrong version looks like this: return all tasks in the database. The right version is: return only tasks where the user is the currently logged-in user. This is not just a logic mistake — it's a security bug. Another user would be able to see your tasks.

### PATCH Requires partial=True
When you want to update just one field (like marking a task complete without changing the title), you use a PATCH request. DRF requires you to pass `partial=True` to the serializer for this to work. If you forget it, updating will fail.

### Token in localStorage
Your React app will store the auth token using `localStorage.setItem('token', ...)` after login, and retrieve it with `localStorage.getItem('token')` when making requests. This is fine for a learning project. In production apps, there are more secure ways to handle this — you'll learn those later.

---

## Part 7: How to Think About This Project

Here is the most important advice: **test each layer before moving to the next one**.

1. Get your Django models working first. Check the Django admin panel to confirm your Task model shows up.
2. Get your API endpoints working in Postman before touching React. If you can't make a task via Postman, React can't do it either.
3. Only once the API works perfectly, start building the React frontend.

If you skip these steps and try to build everything at once, you won't know which layer your bug is in. Debugging becomes 10x harder.

---

## Summary

You are building a todo app with three layers:

- **React** — what users see
- **Django + DRF** — the logic layer that handles requests
- **PostgreSQL** — where the data lives

Every task is linked to a user. Every API request from the frontend includes a token so the backend knows who is asking. The backend only returns data that belongs to that user.

When this is done, you will have traced a real request from a button click in your browser all the way to a database row and back. That is the foundation of every web application ever built.

Good luck.
