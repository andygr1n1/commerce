# How to install virtual environment to run the project
myenv is by default ignored in .gitignore, so you need to create it yourself.
```
python3 -m venv myenv
source myenv/bin/activate
pip install django
```

<!--  -->
https://docs.djangoproject.com/en/5.1/topics/forms/
# Start
Run python manage.py makemigrations auctions to make migrations for the auctions app.
```
python manage.py makemigrations auctions
```
Run python manage.py migrate to apply migrations to your database.
```
python manage.py migrate
```

# Run
```
python3 manage.py runserver
```