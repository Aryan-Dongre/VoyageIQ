# VoyagIQ
An smart travel planning platform 

# ✈️ VoyageIQ – Smart Travel Decision Platform
> **Make Better Travel Decisions Before You Book.**

VoyageIQ is an intelligent travel decision platform designed to help travelers make informed decisions before booking a trip. Instead of functioning as a booking website, VoyageIQ brings together essential travel information such as flights, hotels, weather forecasts, and estimated travel expenses into a single platform.

The application enables users to compare multiple travel options, analyze weather conditions, estimate trip costs, and receive travel recommendations, making travel planning faster, smarter, and more convenient.

---

# 📖 Project Overview

Planning a trip often requires users to visit multiple websites to compare flights, search for hotels, check weather forecasts, and estimate travel expenses. This process is time-consuming, inefficient, and often leads to poor travel decisions due to scattered information.

VoyageIQ addresses this challenge by integrating multiple travel services into one centralized platform. Users can search destinations, compare flight options, explore hotels, view real-time weather forecasts, calculate travel budgets, and manage their travel plans through a personalized dashboard.

The application follows a modular Flask architecture, making it scalable, maintainable, and easy to extend with future features such as AI-based travel recommendations and itinerary planning.

---

# 🎯 Purpose of Building VoyageIQ

VoyageIQ was developed as a comprehensive full-stack web application to solve a real-world travel planning problem while demonstrating modern software engineering practices.

The project was built with the following objectives:

- Develop a scalable web application using the Flask framework.
- Gain practical experience in integrating third-party REST APIs.
- Design and manage relational databases using PostgreSQL.
- Implement secure user authentication and session management.
- Apply modular software architecture using Flask Blueprints.
- Build a responsive and user-friendly interface using Bootstrap.
- Practice service-layer architecture for better code organization.
- Learn version control and collaborative development using Git and GitHub.
- Create an industry-ready portfolio project showcasing backend development skills.

---

# ✨ Features

## 🌍 Travel Search

- Search domestic and international destinations.
- Support for one-way and round-trip travel.
- Passenger and travel class selection.
- Simple and intuitive search interface.

---

## ✈️ Flight Search

- Real-time flight information.
- Airline details.
- Flight duration.
- Departure and arrival timings.
- Layover information.
- Ticket pricing.

---

## 🏨 Hotel Search

- Hotel availability.
- Star ratings.
- Room pricing.
- Amenities.
- Customer review scores.
- Hotel images.

---

## 🌦 Weather Information

- Current weather conditions.
- Temperature.
- Feels-like temperature.
- Humidity.
- Wind speed.
- Visibility.
- Multi-day weather forecast.

---

## 💰 Budget Estimation

- Flight cost estimation.
- Hotel cost estimation.
- Overall trip budget calculation.

---

## 📊 Smart Trip Recommendation

- Weather analysis.
- Budget evaluation.
- Trip score generation.
- Intelligent travel recommendations.

---

## 👤 User Dashboard

Authenticated users can:

- Manage profile information.
- Save travel searches.
- Create and manage Target Trips.
- View previous search history.
- Access personalized travel information.

---

## 🔐 Authentication

- User Registration
- Secure Login
- Password Hashing
- Session Management

---

# 🛠️ Technology Stack

### Backend

- Python
- Flask
- Flask Blueprints
- Flask-WTF
- Jinja2

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Database

- PostgreSQL

### External APIs

- SERPAPI – Google Flights
- SERPAPI – Google Hotels
- Open-Meteo Weather API

### Development Tools

- Git
- GitHub
- Visual Studio Code
- pgAdmin 4



# 🏗️ Project Architecture

VoyageIQ follows a modular architecture to improve maintainability, scalability, and code organization.

                    Client
                       │
                       ▼
             Flask Routes (Blueprints)
                       │
                       ▼
              Forms & Validation
                       │
                       ▼
             Service Layer (Business Logic)
                       │
                       ▼
            Database Models (PostgreSQL)
                       │
                       ▼
                 PostgreSQL Database


# 📁 Project Structure
```text

VoyageIQ/
│
├── voyageiq/
│   ├── auth/
│   ├── dashboard/
│   ├── flight/
│   ├── hotel/
│   ├── weather/
│   ├── target_trip/
│   ├── profile/
│   ├── models/
│   ├── services/
│   ├── forms/
│   ├── templates/
│   ├── static/
│   └── utils/
│
├── database/
│
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md
└── VoyageIQ Documentation.docx
```
