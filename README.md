## 🚀 Elixir Tech Assessment - Charlie Maunder

This README will guide you through the startup process for both the backend and frontend components of the application. Let's get started! 🎉

---

## 📌 Requirements

### Backend Requirements

- Python (>=3.8)
- Pipenv (for dependency management)

### Frontend Requirements

- Node.js (>=16.0.0)
- npm (>=8.0.0)

---

## 🛠️ Setup Instructions

### Backend Setup

1. Open a terminal and navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install the required Python dependencies using `pipenv` (see: https://pipenv.pypa.io/en/latest/installation.html):
   ```bash
   pipenv install
   ```
3. Activate the virtual environment:
   ```bash
   pipenv shell
   ```
4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Running Backend Tests

To run the backend tests using `pytest`, use the following command:

```bash
pytest
```

If `pytest` is not installed, you can add it to your environment:

```bash
pipenv install pytest
```

### Frontend Setup

1. Open a new terminal and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install the required Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the frontend development server:
   ```bash
   npm run dev
   ```

---

## 🎯 You're All Set!

Now you can access the UI running at `http://localhost:5173`

Happy wordle-ing! 💻✨

---

## 🔮 Future Work

- Implement a **daily global word refresh** feature.
- Clean up inline TODOs related to **performance improvements** and **code DRY-ness**.
- Add **unit tests for the frontend** to improve reliability.
- Increase **unit test coverage for the backend**.
- Allowed words should be in the database
- Animations
- Dockerize
- Show word on failure
- Keyboard support
