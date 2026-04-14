# FROST - Men's Wear E-commerce Website <img width="100" height="100" alt="logo" src="https://github.com/user-attachments/assets/46778370-700c-4831-ab27-09d399c81aae" />


## Live Website (Production)

🔗 https://frost-996m.onrender.com/

---

##  Overview

FROST is a full-stack, production-ready and fully deployed e-commerce web application built using Django. The platform is live and allows users to browse products, manage carts, place orders, and track purchase history.

It replicates real-world e-commerce systems with complete user and admin workflows, including authentication, session management, product handling, and order processing.

---

##  Features

### User Authentication

* Email-based registration & login
* Secure user accounts
* Session-based cart persistence

---

### Product & Store

* Browse men's wear products
* Individual product detail pages
* Product variations (size, color)
* Category-based product organization
* Search functionality
* Pagination for product listings

---

### Product Detail Experience

* View detailed product information
* Select size and color variations
* Add products directly to cart

---

### Cart System

* Add/remove products
* Increase/decrease quantity
* Dynamic price calculation
* Tax & grand total computation

---

###  Advanced Cart Logic

* Anonymous users can add items to cart
* On login, session cart is merged with user account
* Cart persists across sessions using cookies

---

###  Checkout & Orders

* Login required before checkout
* Orders stored per user
* Order history & status tracking

---

###  Reviews System

* Only verified buyers can review products

---

###  Admin Capabilities

* Custom admin panel for product management
* Add, edit, and delete products
* Manage categories dynamically
* Control product variations (size, color)
* Manage orders and users

---

## 🛠️ Tech Stack

* **Backend:** Django
* **Frontend:** HTML, CSS, JavaScript
* **Database:** PostgreSQL
* **Media Storage:** Cloudinary
* **Deployment:** Render

---

## Screenshots
1. HomePage
<img width="1920" height="1080" alt="Screenshot (3593)" src="https://github.com/user-attachments/assets/98846af3-419e-4613-8fcf-8d7c19623a21" />
2. Home page woth Products
<img width="1920" height="1080" alt="Screenshot (3596)" src="https://github.com/user-attachments/assets/7f7bb973-1dd7-4266-b87e-bf9cb764c155" />
3. STore Page with category search & pagination
<img width="1920" height="1080" alt="Screenshot (3597)" src="https://github.com/user-attachments/assets/bcf36628-91aa-46b4-9a77-86da990548c5" />
4. Login/Register Page
<img width="1920" height="1080" alt="Screenshot (3598)" src="https://github.com/user-attachments/assets/678dffe0-3b8a-43da-aa32-8455e0dbda35" />
5. Cart with checkout option & increase and decrease in quantity and price changes accordingly
<img width="1920" height="1080" alt="Screenshot (3599)" src="https://github.com/user-attachments/assets/45614cbf-6a49-4191-99c8-6f034f17ad22" />
6. Product Description Page
<img width="1920" height="1080" alt="Screenshot (3600)" src="https://github.com/user-attachments/assets/c863de21-121f-4c98-a6cc-e42c8bedda6d" />
7. Mobile View of the website
   ![IMG_20260415_014211 jpg](https://github.com/user-attachments/assets/2ffb68f5-dd55-48d2-b659-f7217bb1cce7)



---

##  Installation

```bash
git clone https://github.com/priyanshusongara/frost.git
cd frost
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Core Concepts Implemented

* Django MVT Architecture
* Custom User Model (Email Authentication)
* Session & Cookie Handling
* Cart Logic (Anonymous → Logged-in user merge)
* Order Management System
* Product Variations (Size, Color)
* Category Management System
* Review & Rating System
* Pagination & Search

---

## Key Highlights

* Real-world e-commerce workflow implementation
* Seamless cart experience across sessions
* Secure checkout with authentication
* Dynamic pricing logic with tax calculation
* Scalable product & category management system
* Clean and responsive UI (mobile + desktop)

---

## What I Learned

* Built a complete e-commerce platform from scratch
* Implemented complex cart and session logic
* Designed scalable backend architecture
* Handled real-world deployment challenges (media, static files)
* Improved debugging and full-stack development skills

---

## Author & Developer :  **Priyanshu Songara**
﻿
