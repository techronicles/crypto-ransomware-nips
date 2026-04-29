# AI-Driven NIPS for Crypto-Ransomware Attacks

A full-stack final year project for detecting and preventing crypto-ransomware traffic using a Vue dashboard, FastAPI backend, PostgreSQL database, and AI-based prediction workflow.

---

## Tech Stack

### Frontend
- Vue 3
- Vite
- Tailwind CSS
- Axios
- Vue Router

### Backend
- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL

### Database
- PostgreSQL
- pgAdmin

---

## Project Structure

```text
crypto-ransomware-nips/
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── seed.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── .env
│
├── docker-compose.yml
├── README.md
└── .gitignore


Baaada ya ku-clone [git clone https://github.com/techronicles/crypto-ransomware-nips.git
cd crypto-ransomware-nips]

Nenda 'cd backend'

kisha  create virtual environment 'python -m venv venv'

kisha activate '.\venv\Scripts\Activate.ps1'

install dependencies kama huna 'pip install -r requirements.txt'


DATABASE 

Kwenye pgAdmin tengeneza db 'crypo_nips'

tengeneza file backend.env    kisha weka DATABASE_URL=postgresql://postgres:hapa_weka_password_ya_db@localhost:5432/crypo_nips


ndani ya backend folder run this comand 'alembic upgrade head'

kisha populate db yako kwa kurun hili file seed.py command ni 'python seed.py'