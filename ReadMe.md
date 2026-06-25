# Library Management System

A command-line Library Management System built with Python and data is stored in MySQL

## Requirments

* Python 3.10+
* MySQL Server
* Python packages: mysql-connecctor-python, python-dotenv, InquirerPy

```bash
pip install mysql-connector-python python-dotenv InquirerPy
```

## Setup

### 1. Create the Database

You have two options:

#### Option A: Structure Only

Creates the database and table without any data.
Go to the project file directory in command prompt and use the following command

```bash 
mysql -u root -p < structure.sql
```

#### Option B: Structure + Data
Creates  the database, tables and provides sample data
Go to the project file directory in command prompt and use the following command

```bash
mysql -u root -p < sqldata.py
```

### 2. Configure Environment variables 

Add your password and configure the other variables to your liking in the '.env' file

### 3. Run the Application 

Go to the project file directory in command prompt and use the following command

```bash
python "Liberary Management System.py"
```