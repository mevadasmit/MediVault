# **Medivault - Inventory Management System**

Medivault is a **comprehensive inventory management system** designed to streamline the **tracking, approval, and return processes** for medical inventory. 
It facilitates smooth operations for **nurses, inventory managers, and administrators** by providing a structured workflow for managing stock.

---

## 🚀 **Features**

- **User Authentication** – Secure login, registration, and password management
- **Role-Based Access Control** – Separate dashboards for **Nurses, Inventory Managers, and Admins**
- **Inventory Requests** – Nurses can request medical items, and managers can approve/reject requests
- **Returns Management** – Track returnable inventory with automated stock updates
- **Cart System** – Add requested items to a cart before submission
- **Email Notifications** – Auto-send credentials upon user registration
- **Reusable & Disposable Items** – Separate logic for stock deduction and returns
- **Admin Panel** – Manage users, inventory, and approvals seamlessly  

---

## 🛠️ **Tech Stack**

- **Backend:** Django, Django REST Framework (DRF)
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, Bootstrap (Jinja templating)
- **Authentication:** Django Authentication System
- **Messaging:** Django Email Backend

---

## 📌 **Setup Instructions**

### **1️⃣ Clone the repository**
```bash
 git clone (https://github.com/mevadasmit/MediVault.git)
 cd medivault
```

### **2️⃣ Create a virtual environment and install dependencies**
```bash
 python -m venv venv
 source venv/bin/activate
 On Windows use: venv\Scripts\activate
 pip install -r requirements.txt
```

### **3️⃣ Set up environment variables**
Create a `.env` file and configure the required settings:
```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://your-db-user:your-db-pass@localhost:5432/your-db-name
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

### **4️⃣ Apply Migrations**
```bash
 python manage.py makemigrations
 python manage.py migrate
```

### **5️⃣ Create a Superuser**
```bash
 python manage.py createsuperuser
```

### **6️⃣ Run the Development Server**
```bash
 python manage.py runserver
```

---

## 📜 **API Endpoints (if applicable)**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/login/` | User login |
| GET | `/api/inventory/` | Retrieve inventory list |
| POST | `/api/inventory/request/` | Request inventory item |
| PUT | `/api/inventory/return/{item_id}/` | Return inventory item |

---

## 🏗️ **Project Structure**
```bash
medivault/
│-- users/             # User authentication & roles
│-- inventory_manager/ # Inventory & requests management
│-- templates/         # HTML templates
│-- static/            # CSS, JS, images
│-- main_admin/        # Admin panel features
│-- base/              # Utility functions and settings
│-- manage.py          # Django project entry point
│-- requirements.txt   # Project dependencies
```

## 📝 **License**
This project is licensed under the **MIT License** – feel free to use and modify it! 🎉

Author 
Mevada Smit
