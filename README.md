# 🏦 WalletScope: Personal Finance Tracker

## Overview
WalletScope is a comprehensive personal finance management application that helps users track expenses, set budgets, and visualize spending patterns through an intuitive dashboard.

![WalletScope](https://i.ibb.co/hJG6hgn9/Wallet-Scope.png)

## ✨ Features

- **Expense Tracking**: Log and categorize your daily expenses
- **Budget Management**: Set monthly budgets for different spending categories
- **Interactive Dashboard**: Visualize your spending patterns and financial health
- **User Authentication**: Secure account system for personal data protection
- **Responsive Design**: Access your finances on any device

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Visualization**: Chart.js

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Setup Steps

1. Clone the repository
```bash
git clone https://github.com/yourusername/walletscope.git
cd walletscope
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize the database
```bash
flask --app app init-db
```

5. Run the application
```bash
python run.py
```

6. Access the application
Open your browser and navigate to `http://localhost:5000`

## 📱 Usage

### User Registration & Login
- Create a new account using your email address
- Log in with your credentials to access your personal dashboard

### Adding Expenses
1. Navigate to the Expenses page
2. Fill in the expense details (amount, category, date, description)
3. Submit to save your expense

### Setting Budgets
1. Go to the Budget page
2. Create monthly budgets for different spending categories
3. Track your spending against your budget limits

### Dashboard
- View spending trends over time
- Analyze expense distribution by category
- Check budget compliance with visual indicators

## 🔒 Security

- User passwords are securely hashed
- Data is stored locally in an SQLite database
- Session management ensures secure user authentication

## 📊 Future Enhancements

- Export financial reports as PDF or CSV
- Recurring expense tracking
- Financial goal setting and tracking
- Mobile application support
- Multi-currency support
- Integration with bank accounts (read-only)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

Your Name - [@yourusername](https://twitter.com/yourusername)

Project Link: [https://github.com/yourusername/walletscope](https://github.com/yourusername/walletscope)

---

**Disclaimer**: This application is for personal financial management only. Always consult with a financial advisor for professional financial advice.