# Trees Everywhere App

Welcome to Trees Everywhere App! This application allows users to plant and manage trees in their accounts.

## Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

Make sure you have Python and pip installed on your system.

### Cloning the Repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/KleberASGC/treeseverywhere.git
```

### Setting Up a Virtual Environment (Optional but Recommended)

Creating a virtual environment helps in isolating project dependencies and keeps them separate from other projects.

#### Creating a Virtual Environment

Navigate to the project directory and create a virtual environment using the following command:

```bash
python -m venv env
```

Replace myenv with the name you prefer for your virtual environment.

Activating the Virtual Environment
Activate the virtual environment using the appropriate command for your operating system:

On Windows:

```bash
myenv\Scripts\activate
```

On macOS and Linux:

```bash
source myenv/bin/activate
```

### Installing Dependencies

Navigate to the project directory and install the required dependencies using pip:

```bash
cd trees_everywhere
pip install -r requirements.txt
```

### Setting Up the Database

Update the database credentials in the settings.py file located in the trees_everywhere_app directory. Replace the default database settings with your own database credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Running Migrations

Apply the database migrations to create the necessary tables in the database:

```bash
python manage.py migrate
```

### Starting the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

You can now access the application at http://localhost:8000/.

### Contact

If you have any questions or need further assistance, feel free to get in touch.
