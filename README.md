# Backend Setup

## Clone Repo:

    mkdir shutr_venv
    git clone https://github.com/SHUTR-TEAM/shutr-backend.git

## Create Venv

    python -m venv venv

## Activate Venv

### Mac and Linux:

    source venv/bin/activate

### Windows:

    venv\Scripts\activate

## Install dependencies:

    cd shutr/backend
    pip install -r requirements.txt

## Set up your .env file:

    MONGO_USERNAME=your_username
    MONGO_PASSWORD=your_password
    MONGO_CLUSTER=your_cluster.mongodb.net
    MONGO_DB_NAME=your_database_name

## Run Server

    python manage.py runserver
    daphne shutr_backend.asgi:application
