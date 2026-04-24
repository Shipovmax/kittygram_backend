# Kittygram Backend

Django REST Framework backend for the Kittygram cat photo sharing platform.

> **Frontend:** [kittygram-frontend](https://github.com/Shipovmax/kittygram_frontend)  
> **Full-stack deployment (Docker + CI/CD):** [kittygram_final](https://github.com/Shipovmax/kittygram_final)

---

## Features

- **Cat CRUD** — create, read, update, delete cats with name, color (hex → CSS name validation), birth year, photo
- **Achievements** — M2M relation via `AchievementCat` through-table; get-or-create on write
- **Age calculation** — computed `age` field via `SerializerMethodField`
- **Base64 image upload** — `Base64ImageField` decodes data URIs from the React frontend
- **Hex color validation** — `Hex2NameColor` custom field; rejects hex values without a CSS color name
- **Auth** — token-based via Djoser (`/api/token/login/`, `/api/token/logout/`)
- **User management** — registration and profile via Djoser (`/api/users/`)
- **Pagination** — `PageNumberPagination` on cats; disabled on achievements
- **OpenAPI schema** — `schema.yaml` included

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python |
| Framework | Django 5.1, DRF 3.15 |
| Auth | Djoser 2.3 (Token) |
| Image processing | Pillow 11.0 |
| Color validation | webcolors 1.11 |
| Database | SQLite3 (dev) / PostgreSQL (prod) |

---

## Quick Start

```bash
git clone https://github.com/Shipovmax/kittygram_backend
cd kittygram_backend

python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API at `http://127.0.0.1:8000/api/`

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET/POST` | `/api/cats/` | List cats (paginated) / create | Read: No, Write: Yes |
| `GET/PUT/PATCH/DELETE` | `/api/cats/{id}/` | Cat detail | Owner only for write |
| `GET/POST` | `/api/achievements/` | List / create achievements | Yes |
| `POST` | `/api/token/login/` | Obtain token | — |
| `POST` | `/api/token/logout/` | Revoke token | Yes |
| `POST` | `/api/users/` | Register user | — |

---

## Models

```
Cat
├── name          CharField(16)
├── color         CharField(16)  # stored as CSS color name
├── birth_year    IntegerField
├── owner         FK → User
├── image         ImageField (upload_to='cats/images/')
└── achievements  M2M → Achievement (through AchievementCat)

Achievement
└── name  CharField(64)
```

---

## Author

- GitHub: [Shipovmax](https://github.com/Shipovmax)
- Email: shipov.max@icloud.com
