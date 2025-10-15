# MidNightSanctuary Food Ordering System

## Overview
The **MidNightSanctuary Food Ordering System** is a desktop application built with **Python** and **PyQt6**. It allows customers to browse food categories, add items to a cart, and place orders. The system also logs each order for future reference.

The application supports multiple product types, including **Single-Size Food**, **Multi-Size Food**, and **Beverages**, with quantity, size, and variety selection. Customers can provide their contact number and delivery address at checkout.

---

## Features

### Customer Features
- Browse food categories using **tabs** for easy navigation.
- View product **varieties** and **sizes** dynamically.
- Add items to a **cart** with selected quantity, size, and variety.
- **Checkout** with contact number and delivery address validation.
- Receive **estimated delivery time** and **delivery area**.
- Persistent **order logs** stored in the system database.

### Admin Features (via login)
- Admin login with credentials.
- View logged orders (future enhancement can include editing or reporting).

---

## Technologies Used
- **Python 3.13**
- **PyQt6** – GUI framework
- **SQLite** (via service layer) – for order logs
- Modular code structure with **MVC-like pattern**:
  - `model` – Database models
  - `services` – Data access and business logic
  - `UI` – GUI components

---

## Folder Structure
- System/
  - Core/
    - db.py
  - Features/
    - Admin/
      - UI/
        - home.py
        - order.py
        - cart.py
        - mainadmin.py
      - model.py
      - repository.py
      - services.py
    - Customer/
      - UI/
        - home.py
        - order.py
        - cart.py
        - maincustomer.py
      - model.py
      - repository.py
      - services.py
  - shell/
    - main_window.py
  - main.py
  - cafeteria.db
  - README.md
