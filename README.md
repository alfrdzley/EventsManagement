# Technical Test
***

## Installation
1. Clone the repository
```bash
git clone https://github.com/alfrdzley/EventsManagement.git
```
2. Change the directory
```bash
cd EventsManagement
````
3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Migrate the database
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the server
```bash
python manage.py runserver
```

6. Open the browser and go to `http://127.0.0.1:8000/events/`

7. Use HTTP <method> to test the API
```bash
http GET http://127.0.0.1:8000/events/ # Get all events
http GET http://127.0.0.1:8000/events/statistics/ # Get statistics

```


***
Created With ❤️ by **SYERA-ALFARIDZI**