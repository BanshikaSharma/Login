# Login and Signup Project

This is a simple web application built using **Flask** for handling **login** and **signup** functionality. It integrates with **PostgreSQL** for user data storage and uses **Tailwind CSS** for responsive and beautiful UI.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Database Setup](#database-setup)
- [License](#license)

## Features

- **User Registration (Signup):** Users can create an account with their name, email, password, and profile picture.
- **User Authentication (Login):** Users can log in with their email and password.
- **Password Validation:** Ensures strong passwords during signup.
- **Profile Picture Upload:** During signup, users can upload a profile picture.
- **Responsive Design:** Built using **Tailwind CSS**, making the application responsive on all screen sizes.

## Technologies Used

- **Flask:** Web framework to handle server-side logic.
- **PostgreSQL:** A relational database for storing user data securely.
- **Tailwind CSS:** A utility-first CSS framework used for the frontend.
- **Flask-SQLAlchemy:** ORM used for database operations.
- **Flask-WTF:** For form handling and CSRF protection.
- **Flask-Login:** To manage user sessions and authentication.
- **psycopg2:** PostgreSQL adapter for Python.

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/login-signup-app.git
cd login-signup-app
2. Create and Activate a Virtual Environment
Create and activate a virtual environment to keep dependencies isolated:

For Windows:

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate
For macOS/Linux:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Install the necessary dependencies using pip:

bash
Copy
Edit
pip install -r requirements.txt
4. Set Up PostgreSQL
Make sure PostgreSQL is installed and running. You need to create a database for your application.

Create a Database in PostgreSQL:

sql
Copy
Edit
CREATE DATABASE gum_chat;
Set Up Database Configuration:

Open config.py and update the database URI with your PostgreSQL credentials:

python
Copy
Edit
SQLALCHEMY_DATABASE_URI = 'postgresql://<username>:<password>@localhost/gum_chat'
Replace <username> and <password> with your PostgreSQL credentials.

5. Initialize the Database
Run the following commands to create your database tables:

bash
Copy
Edit
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
6. Create a Superuser (Optional)
To create a superuser (admin), you can run a script or use the Flask shell to create a user directly in the database.

Example Flask shell command:

bash
Copy
Edit
flask shell
Then create a user inside the shell:

python
Copy
Edit
from app import db
from models import User
user = User(email='admin@example.com', password='adminpassword', name='Admin')
db.session.add(user)
db.session.commit()
Running the Application
To run the application locally:

bash
Copy
Edit
flask run
By default, it will be hosted at http://127.0.0.1:5000/.

1. Signup Page
Visit the Signup page where users can enter their name, email, password, and upload a profile picture. Once the user submits the form, they will be stored in the database.

2. Login Page
Once a user is signed up, they can log in using their email and password. If the credentials are valid, they will be redirected to the homepage or dashboard.

3. Password Reset (Optional)
You can also implement password reset functionality if required.

Database Setup
If you encounter issues like collation mismatch in PostgreSQL, you can run the following command:

sql
Copy
Edit
ALTER DATABASE gum_chat REFRESH COLLATION VERSION;
If the issue persists, make sure PostgreSQL is up-to-date, or rebuild the template1 database by running:

sql
Copy
Edit
REINDEX SYSTEM template1;
This can resolve collation version mismatches.

License
This project is licensed under the MIT License. See the LICENSE file for more information.

Enjoy using the login/signup system built with Flask and PostgreSQL!

Project Workflow
If you plan to contribute to this project, follow the steps below:

Fork the repository on GitHub.

Clone your forked repository locally.

Create a new branch for the feature or bugfix you're working on.

Make your changes locally.

Commit your changes with clear commit messages.

Push your changes to your forked repository.

Open a pull request to merge your changes into the main repository.

Feel free to open an issue if you need help or encounter any problems while setting up the project.

markdown
Copy
Edit

### Key Sections in the README:

- **Features:** Highlights the key functionality like signup, login, password validation, and profile picture upload.
- **Technologies Used:** Lists all the technologies that power the app.
- **Setup Instructions:** Step-by-step guide to clone, create a virtual environment, install dependencies, set up PostgreSQL, and initialize the database.
- **Running the Application:** Instructions on how to run the Flask app locally, sign up, and log in.
- **Database Setup:** Explains how to handle potential issues like collation mismatch with PostgreSQL.
- **License:** Mentions the license under which the project is distributed.

### Notes:

- **Replace** placeholder text (`yourusername`, `gum_chat`) as per your actual details and project settings.
- **Database URI** in the `config.py` file should be updated with your actual PostgreSQL credentials.

This `README.md` file is more focused on the login/signup functionality, ensuring that users or developers can easily set up, run, an

### Loom video Link : https://www.loom.com/share/49ea74883efd435c97ab3ea9f23e9cc1?sid=ae469fb8-7daa-4bf2-8059-ac4472764ed8
