# TaskAPI

A robust, scalable Task Management and Authentication API built with Django and Django REST Framework. TaskAPI allows users to manage personal tasks, subtasks, comments, attachments, and more—secured with JWT authentication and enhanced with admin capabilities.

---

## 🚀 Features

### 🔐 User Authentication

* **Registration** with email/password
* **Email Verification** with resend capability
* **JWT Login** (access & refresh tokens)
* **Logout** with token blacklisting
* **Forgot Password** flow
* **Reset Password** via secure tokenized link
* **Password Change Confirmation** email

### 📋 Task Management

* **CRUD operations** for tasks
* **Soft Delete** and **Trash Restore**
* **Mark as Completed**
* **Task Priorities** (Low/Medium/High)
* **Search & Filtering** (by status, priority, due date, tags)
* **Pagination** for large task sets
* **Categories/Tags**
* **Attachments** support
* **Comments** on tasks
* **Subtasks**

### 🛡️ Security & Admin

* **JWT authentication** using Simple JWT
* **Rate limiting** for login brute-force protection
* **Django Admin Panel** for users and tasks

---

## 📦 Installation

```bash
# Clone the repo
$ git clone https://github.com/Only1JohnN/TaskAPI.git
$ cd TaskAPI

# Create virtual environment
$ python -m venv venv
$ source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
$ pip install -r requirements.txt

# Apply migrations
$ python manage.py migrate

# Create a superuser (for admin access)
$ python manage.py createsuperuser

# Run the server
$ python manage.py runserver
```

---

## 🔌 API Endpoints Overview

### 🔐 Authentication

| Endpoint                               | Method | Description                      |
| -------------------------------------- | ------ | -------------------------------- |
| `/api/auth/register/`                  | POST   | Register new user                |
| `/api/auth/login/`                     | POST   | Obtain JWT access/refresh tokens |
| `/api/auth/refresh/`                   | POST   | Refresh JWT access token         |
| `/api/auth/logout/`                    | POST   | Logout user (token blacklist)    |
| `/api/auth/verify-email/`              | GET    | Verify email with token          |
| `/api/auth/resend-verification-email/` | POST   | Resend email verification        |
| `/api/auth/forgot-password/`           | POST   | Request password reset link      |
| `/api/auth/reset-password/`            | POST   | Reset password with token        |
| `/api/auth/change-password/`           | POST   | Authenticated password change    |

### 📋 Tasks

| Endpoint                                  | Method               | Description                                   |
| ----------------------------------------- | -------------------- | --------------------------------------------- |
| `/api/tasks/`                             | GET/POST             | List or create tasks                          |
| `/api/tasks/<id>/`                        | GET/PUT/PATCH/DELETE | Retrieve, update, soft-delete a task          |
| `/api/tasks/<id>/complete/`               | POST                 | Mark task as complete/incomplete              |
| `/api/tasks/<id>/restore/`                | POST                 | Restore a soft-deleted task                   |
| `/api/tasks/?search=`                     | GET                  | Search tasks by title/description             |
| `/api/tasks/?priority=&status=&due_date=` | GET                  | Filter tasks by priority, status, or due date |

### 🧩 Subtasks

| Endpoint                    | Method   | Description                        |
| --------------------------- | -------- | ---------------------------------- |
| `/api/tasks/<id>/subtasks/` | GET/POST | List or create subtasks for a task |

### 📝 Comments

| Endpoint                         | Method   | Description                    |
| -------------------------------- | -------- | ------------------------------ |
| `/api/tasks/<task_id>/comments/` | GET/POST | List or add comments to a task |

### 📎 Attachments

| Endpoint                            | Method   | Description                     |
| ----------------------------------- | -------- | ------------------------------- |
| `/api/tasks/<task_id>/attachments/` | GET/POST | Upload or view task attachments |

### 📂 Categories

| Endpoint                      | Method   | Description                 |
| ----------------------------- | -------- | --------------------------- |
| `/api/categories/`            | GET/POST | List or create categories   |
| `/api/categories/<id>/tasks/` | GET      | List tasks under a category |

### 🗑️ Trash

| Endpoint            | Method | Description             |
| ------------------- | ------ | ----------------------- |
| `/api/tasks/trash/` | GET    | Retrieve tasks in trash |

---

## 🧩 Action Endpoints

Here are some additional actions supported by the API for tasks, comments, categories, and attachments:

### Task Actions:

* **Mark Complete**: `/api/tasks/<id>/complete/` - Mark a task as completed or incomplete.
* **Restore Task**: `/api/tasks/<id>/restore/` - Restore a soft-deleted task.

### Subtask Actions:

* **List Subtasks**: `/api/tasks/<id>/subtasks/` (GET) - Get all subtasks for a task.
* **Create Subtask**: `/api/tasks/<id>/subtasks/` (POST) - Create a new subtask for a task.

### Comments Actions:

* **List Comments**: `/api/tasks/<task_id>/comments/` (GET) - Get all comments for a task.
* **Add Comment**: `/api/tasks/<task_id>/comments/` (POST) - Add a comment to a task.

### Attachment Actions:

* **List Attachments**: `/api/tasks/<task_id>/attachments/` (GET) - Get all attachments for a task.
* **Upload Attachment**: `/api/tasks/<task_id>/attachments/` (POST) - Upload an attachment to a task.

---

# 🗺️ Roadmap
## Basic Features (MVP - Minimum Viable Product)
* [x] User Authentication (JWT, session, etc.)
* [x] Create Task (title, description, due date, etc.)
* [x] List Tasks (all tasks for a user)
* [x] Retrieve Single Task (by ID)
* [x] Update Task (edit title, description, status, due date)
* [x] Delete Task (soft delete or hard delete)
* [x] Task Status (e.g., Pending, In Progress, Completed)

## Intermediate Features
* [x] Pagination (for listing many tasks)
* [x] Task Priorities (Low, Medium, High)
* [x] Search and Filter Tasks (by status, due date, priority)
* [x] Soft Delete and Restore (trash bin)
* [x] Categories or Tags (group tasks)
* [x] Attachments (upload files to tasks, like PDFs, images)
* [x] Task Comments (users can add notes/comments to tasks)
* [x] Rate Limiting (protect the API)
* [ ] Due Date Reminders (optional field, notification system if advanced)

## Advanced Features
* [x] Subtasks (tasks can have nested subtasks)
* [ ] Recurring Tasks (daily, weekly, monthly repetition)
* [ ] Collaborators (share tasks with other users)
* [ ] Task Activity Logs (see who updated/completed what and when)
* [ ] Notification System (email or in-app notifications on due dates or updates)
* [ ] Task Templates (save task setups and reuse)

---

## 🧑‍💻 Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss.

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 📫 Contact

Created by [@Only1JohnN](https://github.com/Only1JohnN) – feel free to reach out with questions or suggestions!
