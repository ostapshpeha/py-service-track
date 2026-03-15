# Gemini Context: Service Track (Auto Repair CRM)

This `GEMINI.md` provides context and guidelines for working on the Service Track project, a Django-based CRM for auto repair shops.

## Project Overview

Service Track is a CRM system designed for auto service employees to manage clients, vehicles, orders, and mechanic notes. It features a role-based system (Manager, Mechanic) and uses the AdminLTE 3 template for the frontend.

## Tech Stack

*   **Backend:** Python 3, Django 6.0
*   **Database:** SQLite (Development), PostgreSQL (Production capability implied)
*   **Frontend:** Django Templates, AdminLTE 3 (Bootstrap 4), `django-crispy-forms`
*   **Asset Management:** `whitenoise` (Static), `cloudinary` (Media)
*   **Key Libraries:**
    *   `django-filter`: For search and filtering.
    *   `django-select2`: For enhanced select widgets.
    *   `django-simple-history`: for tracking model changes.
    *   `django-debug-toolbar`: For debugging.

## Key Directories & Structure

*   **`config/`**: Main project configuration.
    *   `settings/`: Split settings (`base.py`, `dev.py`, `prod.py`).
    *   `urls.py`: Main URL routing.
*   **`accounts/`**: Authentication and User Management.
    *   `models.py`: Defines `CustomUser` with roles (Mechanic, Manager).
*   **`crm/`**: Core CRM functionality.
    *   Manages `Client` and `Vehicle` models.
*   **`orders/`**: Order processing.
    *   Manages `Order` and `Invoice` models.
*   **`notes/`**: internal communication.
    *   Allows mechanics to attach notes and images to tasks.
*   **`templates/`**: HTML templates using AdminLTE structure.
*   **`static/`**: Static assets (CSS, JS, Images).

## Setup & Development

### Installation

1.  **Clone & Environment:**
    ```bash
    git clone <repo_url>
    cd py-service-track
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

2.  **Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Variables:**
    Create a `.env` file in the project root:
    ```env
    DEBUG=True
    SECRET_KEY=your-secret-key
    # CLOUDINARY_CLOUD_NAME=...
    # CLOUDINARY_API_KEY=...
    # CLOUDINARY_API_SECRET=...
    ```

4.  **Database & Admin:**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

5.  **Run Server:**
    ```bash
    python manage.py runserver
    ```

### Testing & Linting

*   **Linting:** `flake8` is configured.
    ```bash
    flake8
    ```
    *   Max line length: 79 characters.
    *   Excludes migrations, venv, git, pycache.

*   **Testing:** `pytest` is included in requirements.

## Deployment

*   **Build Script:** `build.sh` handles dependency installation, static collection, and migrations.
*   **Static Files:** Served via `WhiteNoise`.
*   **Media Files:** Stored in Cloudinary.

## Conventions

*   **User Model:** Always refer to `accounts.CustomUser` (or `get_user_model()`), never `auth.User`.
*   **Templates:** Follow AdminLTE structure. Use `base.html` for inheritance.
*   **Forms:** Use `crispy_forms` with Bootstrap 4 pack.
