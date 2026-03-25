# Digital Lost & Found (Flask + REST + SQLite/MySQL)

This project is a Digital Lost & Found website:
- User registration/login (JWT)
- Report lost/found items (with image upload)
- Public listing + search/filter by keyword/category/status
- Contact fields (email/phone)
- Admin panel to list/delete posts
- Optional status updates (claimed/unclaimed) and user dashboard

## Tech Stack
- Backend: Python + Flask
- ORM/DB: SQLAlchemy (SQLite by default; MySQL supported via `DATABASE_URL`)
- Auth: JWT (`Flask-JWT-Extended`)
- Frontend: HTML/CSS + minimal JavaScript calling REST APIs

## Folder Structure (high level)
- `backend/app.py`: Flask app entrypoint
- `backend/models/`: SQLAlchemy models
- `backend/routes/`: REST endpoints (auth/items/status/admin/dashboard)
- `backend/templates/`: HTML pages
- `backend/static/`: CSS/JS
- `backend/uploads/`: uploaded images

## Setup & Run (Local - SQLite)
1. Install dependencies:
   - `pip install -r requirements.txt`
2. Configure environment:
   - Copy `.env.example` to `.env` (or set the environment variables directly).
3. Run the server:
   - `python backend/app.py`
4. Open:
   - `http://localhost:5000`

## Important Environment Variables
- `SECRET_KEY`: Flask secret (CSRF/session signing; also used by JWT config)
- `JWT_SECRET_KEY`: JWT signing secret
- `DATABASE_URL`: DB connection string
  - Default (SQLite): stored at `backend/lost_found.db`
  - Example for MySQL: `mysql+pymysql://user:password@localhost:3306/lost_found`
- `UPLOAD_FOLDER`: image upload directory (default: `backend/uploads`)
- `MAX_CONTENT_LENGTH_MB`: max upload size (default: 5)

### Dev-only Admin Bootstrap
To create the first admin user without manual DB edits:
- Set `BOOTSTRAP_ADMIN_EMAIL` to an email
- When that email registers, the account gets `is_admin=True`

## REST API Endpoints

### Authentication
- `POST /api/auth/register` (JSON): `username,email,password`
- `POST /api/auth/login` (JSON): `email,password` (or `username,password`)
- `GET /api/auth/me`

### Public Listing / Search
- `GET /api/lost-items?keyword=&category=&status=`
- `GET /api/found-items?keyword=&category=&status=`
- `GET /api/lost-items/<id>`
- `GET /api/found-items/<id>`

### Protected Create (with image upload)
- `POST /api/lost-items` (multipart/form-data, JWT required)
- `POST /api/found-items` (multipart/form-data, JWT required)

### Status Update (claimed/unclaimed)
- `POST /api/lost-items/<id>/status` (JWT required)
- `POST /api/found-items/<id>/status` (JWT required)

Body: `{ "status": "claimed" | "unclaimed" }`

Permission rule (current implementation):
- Admins can update any item
- Otherwise, only the reporter who created the item can update it

### User Dashboard
- `GET /api/me/dashboard` (JWT required)

### Admin Panel
- `GET /api/admin/lost-items` (admin only)
- `GET /api/admin/found-items` (admin only)
- `DELETE /api/admin/lost-items/<id>` (admin only)
- `DELETE /api/admin/found-items/<id>` (admin only)

## Notes / Next Improvements
- For production: use migrations (e.g., Flask-Migrate) instead of `db.create_all()`.
- Add CSRF protection if you later switch to cookie-based sessions.
- Add pagination for lists if the dataset grows.

