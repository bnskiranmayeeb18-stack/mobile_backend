# Clone
git clone https://github.com/bnskiranmayeeb18-stack/mobile_backend.git
cd mobile_backend

# Venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# DB
python manage.py migrate

# Run 26 Tests - PROOF
python manage.py test rides --verbosity=1
# Result: Ran 26 tests - OK

# Server
python manage.py runserver
# http://127.0.0.1:8000/api/docs/
# http://127.0.0.1:8000/admin/