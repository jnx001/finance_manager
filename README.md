
# 🧾 Personal Finance Manager

A complete **Python-based Personal Finance Management System** built using **Object-Oriented Programming (OOP)**, **file handling**, and **data persistence**.
This project helps users **track expenses**, **categorize spending**, **generate reports**, and **analyze spending patterns** through a simple and user-friendly **Command-Line Interface (CLI)**.

---

## 🚀 Features

### ✅ Core Functionalities

* Add expenses with:
  * Amount
  * Category
  * Date
  * Description
* View all expense records
* Delete or update an expense
* Summary of expenses by category
* Monthly and yearly spending reports
* Total expenditure calculation
* Search expenses by category/date/text

### 🧱 Technical Features

* Fully object-oriented design
* Persistent data storage using JSON/CSV file
* Modular code structure
* Error handling for robust CLI operations
* Clean and intuitive menu-driven interface

---

## 📂 Project Structure
finance_manager.py
backups
data

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/personal-finance-manager.git
cd personal-finance-manager
```

### 2️⃣ Create virtual environment *(optional)*

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the program using:

```bash
python finance_manager.py
```

You will see a menu like:

```
1. Add Expense
2. View Expenses
3. Delete Expense
4. Expense Summary
5. Monthly Report
6. Yearly Report
7. Search Expense
8. Exit
```

Enter the number to perform an action.

---

## 🧠 Concepts Used

This project demonstrates:

* **Object-Oriented Programming**

  * Classes, objects, methods, constructors
* **File Handling**

  * Reading & writing JSON/CSV files
* **Modular Programming**

  * Separate models, utilities, and main program
* **Data Processing**

  * Grouping, filtering, and summarization
* **CLI interaction**

  * User-driven menu system

---

## 📊 Example Output

```
Total Spending This Month: ₹ 12,450
Top Category: Food (₹ 5,300)
Most Active Day: 12 January 2025
```

---

## 🔮 Future Enhancements

* Add income tracking
* Add visual charts using Matplotlib
* Export reports to PDF
* Add authentication
* Convert CLI to Tkinter/Streamlit app

---

## 🤝 Contribution

Contributions are welcome!
Feel free to fork the repo and create a pull request.

---

## 📜 License

This project is licensed under the **MIT License**.
