# Command-Line Expense Tracker 🐍💰

A robust, feature-rich, command-line interface (CLI) application for personal expense tracking, built with Python and MySQL. 
This project demonstrates a multi-layered application architecture, advanced database concepts, and data analysis capabilities in a non-web environment.

---

## ✨ Key Features

* **Multi-User System:** Secure user registration and login with hashed passwords (`bcrypt`).
* **Role-Based Access:** Distinction between standard `user` and `admin` roles, with admins having special privileges.
* **Full CRUD Functionality:** Complete Create, Read, Update, and Delete operations for:
    * **Accounts:** Manage multiple financial accounts (Cash, Bank, Credit Card).
    * **Categories:** Create custom, nested income and expense categories.
    * **Transactions:** Add, edit, and delete detailed transactions.
    * **Budgets:** Set and update monthly budgets for different expense categories.
* **Advanced Database Integration:** Leverages MySQL features to ensure data integrity and performance:
    * **Stored Procedures:** For atomic transactions like posting a new expense.
    * **Triggers:** To automatically update account balances after any transaction change.
    * **Functions:** For reusable SQL logic.
* **Data Analysis & Visualization:**
    * Generates insightful reports on spending habits using the **pandas** library.
    * Creates and saves visualizations (bar charts, pie charts) using **seaborn** and **matplotlib**.
* **CSV Import/Export:** Easily export your transaction history to a CSV file or import new transactions from a CSV.
* **Robust & Interactive CLI:** A user-friendly, menu-driven interface built with helper functions and input validators.

---

## 🏗️ Project Architecture

This application is built using a multi-layered architecture, which separates concerns and makes the codebase modular, scalable, and easy to test.

```
+---------------------------------+
|   Command-Line Interface (CLI)  |  <-- (main.py) - User Interaction
+---------------------------------+
                |
+---------------------------------+
|         Service Layer           |  <-- (services/) - Business Logic
+---------------------------------+
                |
+---------------------------------+
|        Repository Layer         |  <-- (repos/) - Data Access Logic
+---------------------------------+
                |
+---------------------------------+
|          Model Layer            |  <-- (models/) - Data Structures
+---------------------------------+
                |
+---------------------------------+
|       MySQL Database            |  <-- Stored Procs, Triggers, Functions
+---------------------------------+
```

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Database:** MySQL
* **Core Libraries:**
    * `mysql-connector-python`: For connecting to and interacting with the MySQL database.
    * `bcrypt`: For modern, secure password hashing.
    * `python-dotenv`: For managing environment variables (like database credentials).
* **Data Science & Visualization:**
    * `pandas`: For data manipulation and analysis.
    * `seaborn` & `matplotlib`: For creating and saving plots.
* **CLI & Utilities:**
    * `tabulate`: For printing clean, formatted tables in the console.

---

## 🚀 How to Run the Project

Follow these steps to get the application running on your local machine.

### Prerequisites

* Python 3.10 or newer
* A running MySQL Server instance
* Git for cloning the repository

### Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/Shailya777/Expense-Tracker.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Set Up a Virtual Environment**
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate it
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the Database**
    * Create a `.env` file in the root directory by copying the example file:
        ```bash
        cp .env.example .env
        ```
    * Open the `.env` file and fill in your MySQL credentials (`DB_USER`, `DB_PASSWORD`, etc.).

    * Log in to your MySQL client and run the provided SQL scripts **in the following order** to set up the database, tables, and sample data:
        1.  `sql/schema.sql`
        2.  `sql/procs.sql`
        3.  `sql/functions.sql`
        4.  `sql/triggers.sql`
        5.  `sql/final_seed.sql`

5.  **Run the Application**
    You're all set! Start the application with this command:
    ```bash
    python expense_tracker/main.py
    ```
    The CLI menu will appear, and you can start by registering a new user.


---

## 🧠 What I Learned

This project was a fantastic learning experience that went beyond basic scripting. Here are some of the key concepts I mastered:

* **Advanced SQL:** I learned that a database is more than just a data store. By implementing **Stored Procedures**, **Triggers**, and **Functions**, I was able to enforce complex business rules and data integrity directly at the database level, making the application more robust and secure.

* **Multi-Layered Architecture:** I gained a deep appreciation for the **Service** and **Repository** patterns. Separating the application into distinct layers (UI, business logic, data access) made the code incredibly organized, easy to debug, and highly testable.

* **Object-Oriented Programming (OOP) in Python:**
    * I used **Abstract Base Classes (`abc`)** to define common interfaces for models like `Account` and `Transaction`, enforcing a consistent structure through inheritance.
    * The **`dataclasses`** module was a game-changer for creating clean, boilerplate-free model classes, making the code that represents data both readable and concise.

* **Modern Python Features:**
    * I extensively used the **`typing`** module for type hinting. This dramatically improved code clarity and allowed me to catch potential bugs early without even running the code.
    * I learned about secure authentication practices, using the **`bcrypt`** library to hash and verify passwords, ensuring user credentials are never stored in a readable format.

* **Data Analysis Workflow:** I implemented a complete data analysis pipeline: fetching raw data from the SQL database, loading it into a **pandas** DataFrame for powerful aggregation and manipulation, and finally, using **seaborn** to create meaningful visualizations that tell a story about user spending.

---

### Created by: Shailya Gandhi (https://www.linkedin.com/in/shailya-gandhi-b395a953/)
