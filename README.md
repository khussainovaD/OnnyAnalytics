# Analytics Project for "OnnyAnalytics"

Welcome to the project repository for an e-commerce data analysis based on the public Olist dataset.

## 📝 Project Description

**"BrazAnalytics"** is a fictional analytics company that helps businesses make data-driven decisions.

In this project, we are conducting a comprehensive analysis of data from the Brazilian marketplace, Olist. The goal is to identify key performance metrics, understand customer behavior, evaluate logistics processes, and find growth opportunities for the business.

## 🏛️ Database Architecture

To meet the requirements of a relational database and to facilitate analysis, the original flat dataset was normalized. The schema below describes the tables and the relationships between them.

![ER Diagram](screenshots/er_diagram.png)
*<p align="center">A screenshot of my ER Diagram </p>*

## 🛠️ Tools and Technologies

* **Database:** PostgreSQL
* **Programming Language:** Python 3.11
* **Key Python Libraries:**
    * `pandas` - for data processing during import.
    * `psycopg2-binary` (for PostgreSQL) - for connecting to the database.
    * `sqlalchemy` - for easier interaction with the DB.
* **Version Control:** Git & GitHub

***
## 📈 Data Analysis: SQL Queries and Results

This section presents the results of executing SQL queries against the database, from basic exploration to complex analytical questions.

##### Basic Queries
These are examples of basic queries used for the initial exploration of the data.

1. (SELECT, LIMIT)
![Basic Query Result 1](screenshots/basic_query_01.png)
<p align="center">View the first 10 rows of the orders table</p>

2. (GROUP BY, COUNT)
![Basic Query Result 1](screenshots/basic_query_01.png)
<p align="center">Group and count: number of orders per status</p>

3. (JOIN)
![Basic Query Result 1](screenshots/basic_query_01.png)
<p align="center">Join tables: show client city for each order</p>

