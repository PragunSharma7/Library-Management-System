# Library Management System

A command-line Library Management System built with Python and MySQL.

Designed for small libraries, this application provides all the core functionality needed to manage books, customers, borrowing, returns, sales, fines, and reporting from a single interface.

The project was developed with maintainability and readability in mind. The user interface(UI) and database operations are clearly separated, making the codebase easy to understand, extend, and modify. Even users with limited programming experience should be able to follow the program flow and understand how the system works.

## Design Decisions

### No Graphical User Interface (GUI)

This project uses a command-line interface by design. The goal was to keep the application lightweight, portable, and easy to understand while demonstrating the underlying architecture of a management system. The separation between the user interface, business logic, and database layer also makes it straightforward to build a GUI or web interface on top of the existing codebase in the future.

### No Payment Gateway Integration

Payment processing is intentionally not included. Payment gateways vary significantly between organizations, regions, and payment providers, and are often integrated according to specific business requirements. The system is designed so that a payment solution can be added separately if needed.

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
Creates  the database, tables and provides sample data.
Go to the project file directory in command prompt and use the following command

```bash
mysql -u root -p < sqldata.sql
```

### 2. Configure Environment variables 

Add your password and configure the other variables to your liking in the '.env' file

### 3. Run the Application 

Go to the project file directory in command prompt and use the following command

```bash
python "Liberary Management System.py"
```