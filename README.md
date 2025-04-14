# Fingerprint-Based ATM Authentication System

This project implements a secure ATM authentication system using **fingerprint recognition** and **PIN-based login**. It aims to modernize ATM access by combining biometrics with a simple and secure PIN system—eliminating the need for cards or mobile-based OTPs.

---

## 🔐 Features

- **User Registration**  
  Capture and store user fingerprint data along with account information.

- **Secure Login**  
  Authenticate users via fingerprint recognition and a personal identification number (PIN).

- **ATM Transactions**  
  - Check balance  
  - Deposit/Withdraw funds  
  - View recent transaction history (Mini Statement)

---

## 🛠️ Technologies Used

- **Python**
- **Fingerprint Recognition** (via SOCOFing Dataset)
- **MongoDB** – NoSQL database for storing user and transaction data

---

## 📁 Dataset

Uses the dataset of FingerPrints

---

## 📦 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/EtikalaAkhila/Fingerprint-Based-ATM-aunthentication.git
cd Fingerprint-Based-ATM-aunthentication
```

2. **Install Dependencies**

```bash
pip install pymongo
pip install inputimeout
```

3. **MongoDB Setup**

- Install MongoDB locally or use a cloud service like **MongoDB Atlas**.
- Create a database, e.g., `ATMAuthDB`
- Create collections:
  - `users` – stores user account and fingerprint data
  - `transactions` – stores transaction history

Example MongoDB document structure:

```json
// users collection
{
  "_id": ObjectId,
  "first_name": "John",
  "last_name": "Doe",
  "pin": "1234",
  "fingerprint_id": "001", 
  "balance": 5000
}

// transactions collection
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "type": "deposit",
  "amount": 1000,
  "timestamp": "2025-04-14T10:00:00Z"
}
```

---

## 🔑 How It Works

1. The user scans their fingerprint.
2. The system matches it against stored records in the database.
3. If a match is found, the user enters their PIN.
4. Upon PIN verification, they can access account features like deposits, withdrawals, and viewing balance.

---

## ✅ To-Do / Future Enhancements

- Integrate real-time fingerprint scanning hardware.
- Add facial recognition as a backup authentication method.
- Encrypt sensitive data like PINs.
