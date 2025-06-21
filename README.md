# Invoice API

A lightweight and scalable Invoice Management API built with **FastAPI**. This API is designed for managing user accounts, authentication, and issuing invoices with support for future extensions like payment integration, PDF export, and more.


## 🚀 Features

- User registration and login
- JWT-based authentication
- Role-based access control (e.g., admin, staff)
- CRUD operations for invoices
- Association between users and invoices
- RESTful and clean endpoint design
- Pydantic-based request validation
- Modular, production-ready project structure


## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/invoice-api.git
cd invoice-api
```
2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**
   - On Windows:
   ```bash
   venv\Scripts\activate
   ```
   - On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Set up environment variables**
   - Create a `.env` file in the root directory and add your configuration:
   ```plaintext
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///./test.db  # or your database URL
   ```

6. **Run the application**

```bash
uvicorn app.main:app --reload
```

## 📖 API Documentation
Visit the interactive API documentation at [http://localhost:8000/docs](http://localhost:8000/docs) after running the application.

 