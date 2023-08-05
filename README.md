# LunchApp
API for  employees which helps them to
make a decision at the lunch place.

## Features

- Authentication by JWT
- Creating restaurant
- Uploading menu for restaurant
- Creating employee
- Getting current day menu
- Getting results for the current day

## Installing using GitHub:
Install PostgresSQL and create db

1. Clone the repository:

```bash
git clone https://github.com/your-username/LunchApp
```
2. Change to the project's directory:
```bash
cd LunchApp
```
3. Сopy .env_sample file with your examples of env variables to your .env
file

4. Once you're in the desired directory, run the following command to create a virtual environment:
```bash
python -m venv venv
```
5. Activate the virtual environment:

On macOS and Linux:

```bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```

4. Install the dependencies

```bash
pip install -r requirements.txt
```

5. Set up the database:

Run the migrations

```bash
python manage.py migrate
```

Load fixture

```bash
python manage.py loaddata fixture_data.json
```

6. Start the development server

```bash
python manage.py runserver
```

7. Access the website locally at http://localhost:8000.

## Run with Docker

Docker should be installed

```
docker-compose build
docker-compose up
```

## Getting access

 
- get access token via /api/user/token/ by 
```
username = UserTest1
password = user123123
```

or register you own user via /api/users/ and get access token


## Routes

- /user/ - register employee or restaurant
- /user/token - get token
- /user/token/refresh/ - get new refresh token
- /menu/most-voted - most voted restaurant
- /menu/restaurant - all restaurant list if employee or get all owns restaurant if restaurant user
- /menu/all-menu/ - all menu list
- /menu/all-menu/id/vote/ - vote for some menu of restaurant
