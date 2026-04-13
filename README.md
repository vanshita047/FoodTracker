FoodTracker - Expense and Price Comparison App

## Problem Statement
While ordering food, users often switch between platforms like Swiggy, Zomato and Eatsure to compare prices, which is time-consuming and inefficient.There is no centralized system to track spendign and compare prices across platforms.


## Solution
FoodTracker is a multi-page web application that allows users to:
-Track food expenses
-Compare prices across platforms
-Manage monthly budgets
-Analyze spending patterns

## Features
-Log and track food orders
-Monthly budget tracking
-Interactive dashboards using Plotly
-Price comparison across platforms
-Spending analytics and insights

## Tech Stack
-Python
-Streamlit
-MySQL
-Pandas
-Plotly

## Project Structure
FoodTracker/
│── app.py
│── db.py
│── theme.py
│── requirements.txt
│── README.md
│── pages/
│ ├── log_order.py
│ ├── price_comparison.py
│ ├── spend_tracker.py
│ ├── budget.py

## How to Run
1. Clone the repository:
```bash
git clone https://github.com/vanshita047/FoodTracker.git
cd FoodTracker
pip install -r requirements.txt
streamlit run app.py

## Future Improvements
-Integrate live price data using APIs
-Add user authentication for multi-user support
-Implement price drop notifications
-Apply machine learning for price prediction

## Key Highlights
-Solves real-world problem of comparing food prices across platforms
-Implements structured data strorage and CRUD operations using MySQL
-Provides data-driven insights through interactive dashboards


## AUTHOR
Vanshita Chandnani