# 💸 12Bucks – Django Finance & Accounting App

**12Bucks** is a Django-based financial management application built for freelancers, small business owners, and creators. It allows users to track income, expenses, mileage, clients, and invoices — all in one responsive, modern dashboard.

> Developed by [Tom Stout](https://airborne-images.net) for Airborne Images and 12bytes.

![Django](https://img.shields.io/badge/Django-4.x-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)

---

## 🚀 Features

- 📊 **Income & Expense Tracking** by category and subcategory
- 🧾 **Client Management** with invoice generation and email delivery
- 🚘 **Mileage Tracking** with deductible/reimbursable tagging
- 📥 **Receipt Uploads** with image preview
- 📅 **Year-over-Year Keyword-Based Financial Summary**
- 📄 **Financial Statements** and category summaries
- 📧 **Email Integration** for sending invoices
- 📱 **Mobile-Friendly** Bootstrap 5 UI
- 📦 **PDF Export** of invoices and reports (via WeasyPrint)

---

## 📂 Project Structure

```
finance/
├── templates/
│   ├── finance/
│   └── components/
├── static/
├── forms.py
├── models.py
├── views.py
├── urls.py
...
```

---

## 🛠️ Installation

### 📦 Via pip (after PyPI release):
```bash
pip install django-finance-12bucks
```

### 🧪 Manual Setup:
```bash
git clone https://github.com/yourusername/12bucks.git
cd 12bucks
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🧩 Configuration

Set the following in your `.env`:

```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:pass@localhost:5432/yourdb
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=yourpassword
```

---

## 📷 Screenshots

Coming soon...

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to add.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

**Tom Stout**  
✉️ [tom@airborne-images.net](mailto:tom@airborne-images.net)  
🌐 [airborne-images.net](https://www.airborne-images.net)
