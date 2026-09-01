# ✈️ VoyageIQ

### Smart Travel Decision Platform

> **Make Better Travel Decisions Before You Book.**

VoyageIQ is a full-stack smart travel decision platform designed to simplify the travel planning process by bringing essential travel information into a single application.

Instead of switching between multiple websites to search for flights, compare hotels, check weather conditions, and estimate trip expenses, VoyageIQ provides these capabilities through one centralized platform.

By integrating multiple travel and weather services, VoyageIQ helps users **compare travel options, evaluate destinations, estimate trip costs, and make better-informed travel decisions**.

The platform was designed around a simple goal:

> **Reduce the friction of travel planning by bringing scattered travel information together in one place.**

VoyageIQ reduces the need to repeatedly jump between different travel websites, addressing one of the major usability problems in traditional travel planning.

---

# 🌍 Why VoyageIQ?

Planning a trip usually requires visiting several different platforms:

```text
Flight Search
     ↓
Hotel Search
     ↓
Weather Forecast
     ↓
Budget Calculation
     ↓
Travel Comparison
     ↓
Final Decision
```

This creates unnecessary context switching and makes it difficult to compare all the information together.

VoyageIQ centralizes these activities:

```text
                 ┌──────────────────────┐
                 │       VoyageIQ       │
                 └──────────┬───────────┘
                            │
       ┌────────────────────┼────────────────────┐
       ↓                    ↓                    ↓
   ✈️ Flights           🏨 Hotels           🌦 Weather
       │                    │                    │
       └────────────────────┼────────────────────┘
                            ↓
                    💰 Budget Estimation
                            ↓
                    📊 Trip Evaluation
                            ↓
                  🧠 Travel Recommendation
```

### 📈 Project Impact

VoyageIQ was designed to reduce the amount of unnecessary switching between different travel websites during the planning process.

**Result: approximately 80% reduction in the need to jump between different tabs/platforms for core travel-planning information.**

This makes the planning workflow more centralized, faster, and easier to compare.

---

# ✨ Key Features

## ✈️ Flight Search

VoyageIQ provides flight-search functionality through integrated travel APIs.

Users can:

* Search domestic and international flights
* Select origin and destination airports
* Search one-way and round-trip flights
* Select travel dates
* Specify passengers
* Select travel class
* View airline information
* View departure and arrival times
* Compare flight duration
* View layover information
* Compare ticket prices

### Airport Autocomplete

The flight search interface includes airport autocomplete functionality to make selecting airports faster and easier.

---

## 🏨 Hotel Search

Users can search and compare hotels for their destination.

Hotel information includes:

* Hotel name
* Hotel images
* Star rating
* Room pricing
* Amenities
* Customer review scores
* Availability information

This allows users to evaluate accommodation options without leaving the VoyageIQ platform.

---

## 🌦 Weather Information

VoyageIQ integrates weather data to help users understand the conditions at their destination before planning their trip.

Users can view:

* Current temperature
* Feels-like temperature
* Humidity
* Wind speed
* Visibility
* Current weather conditions
* Multi-day weather forecasts

Weather information can then be considered while evaluating a destination.

---

## 💰 Travel Budget Estimation

VoyageIQ provides an estimated travel budget based on available travel information.

The system can combine:

```text
Flight Cost
     +
Hotel Cost
     +
Estimated Trip Expenses
     ↓
Overall Trip Budget
```

This gives users a better understanding of the expected cost before making a booking decision.

---

## 📊 Smart Trip Evaluation

VoyageIQ combines multiple travel factors to help users evaluate their trip.

The platform considers information such as:

* Weather conditions
* Travel cost
* Flight options
* Hotel options
* Destination information

The collected information can be used to generate an overall trip evaluation and travel recommendation.

---

## 🎯 Target Trips

Users can create and manage personalized travel plans through the Target Trip feature.

Users can:

* Create target trips
* Save important trip information
* Manage planned destinations
* Track travel plans
* Access saved trips from their dashboard

---

## 👤 Personalized Dashboard

Authenticated users have access to a personalized dashboard where they can manage their travel activities.

The dashboard provides access to:

* Saved searches
* Target Trips
* Search history
* Profile information
* Personalized travel information

---

## 🔐 Authentication & Security

VoyageIQ includes secure user authentication functionality.

Implemented features include:

* User registration
* User login
* Password hashing
* Session management
* Protected routes
* Form validation
* Environment-based secret management

Sensitive application configuration is separated from the source code using environment variables and secure cloud configuration.

---

# 🏗️ System Architecture

VoyageIQ follows a modular full-stack architecture.

```text
                         ┌─────────────────────┐
                         │       Client        │
                         │ Browser / Frontend  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Flask App        │
                         │   Application Layer │
                         └──────────┬──────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
          ┌────────────┐     ┌────────────┐     ┌────────────┐
          │ Blueprints │     │   Forms    │     │   Utils    │
          └──────┬─────┘     └────────────┘     └────────────┘
                 │
                 ▼
          ┌────────────────┐
          │ Service Layer  │
          │ Business Logic │
          └───────┬────────┘
                  │
        ┌─────────┼──────────┐
        │         │          │
        ▼         ▼          ▼
    Flights    Hotels     Weather
      API        API         API
        │         │          │
        └─────────┼──────────┘
                  │
                  ▼
          ┌─────────────────┐
          │ PostgreSQL DB   │
          └─────────────────┘
```

The application separates routing, validation, business logic, database operations, and external API communication to improve maintainability and scalability.

---

# ☁️ Cloud Architecture

VoyageIQ has been deployed using Microsoft Azure services.

The cloud deployment architecture is designed around the following components:

```text
                    Internet
                       │
                       ▼
              ┌─────────────────┐
              │  Azure App      │
              │     Service     │
              └────────┬────────┘
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
      Application Logic     Azure Key Vault
             │             Secrets Management
             │
             ▼
      ┌─────────────────┐
      │ Azure Database  │
      │   PostgreSQL    │
      └─────────────────┘
             │
             ▼
      External Services
   ┌─────────┼──────────┐
   ▼         ▼          ▼
 SERPAPI   SERPAPI   Open-Meteo
 Flights   Hotels     Weather
```

### Azure Services

* **Azure App Service** — Application hosting and deployment
* **Azure Database for PostgreSQL** — Production database
* **Azure Key Vault** — Secure storage and management of application secrets

This cloud-based architecture provides a more production-oriented deployment compared with running the application only in a local development environment.

---

# 🛠️ Technology Stack

## Backend

* Python
* Flask
* Flask Blueprints
* Flask-WTF
* Jinja2

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

## Database

* PostgreSQL
* Azure Database for PostgreSQL

## Cloud & Deployment

* Microsoft Azure
* Azure App Service
* Azure Key Vault
* GitHub

## External APIs

### ✈️ SERPAPI – Google Flights

Used for retrieving flight-search information such as:

* Airlines
* Prices
* Departure/arrival information
* Flight duration
* Layovers

### 🏨 SERPAPI – Google Hotels

Used for hotel-related information including:

* Hotel listings
* Prices
* Ratings
* Amenities
* Reviews
* Images

### 🌦 Open-Meteo

Used for weather information and forecasts.

## Development Tools

* Git
* GitHub
* Visual Studio Code
* pgAdmin 4

---

# 📁 Project Structure

```text
VoyageIQ/
│
├── voyageiq/
│   │
│   ├── auth/
│   │   └── Authentication & authorization
│   │
│   ├── dashboard/
│   │   └── User dashboard
│   │
│   ├── flight/
│   │   └── Flight search functionality
│   │
│   ├── hotel/
│   │   └── Hotel search functionality
│   │
│   ├── weather/
│   │   └── Weather functionality
│   │
│   ├── target_trip/
│   │   └── Target Trip management
│   │
│   ├── profile/
│   │   └── User profile management
│   │
│   ├── models/
│   │   └── Database models
│   │
│   ├── services/
│   │   └── Business logic & API integrations
│   │
│   ├── forms/
│   │   └── Form definitions & validation
│   │
│   ├── templates/
│   │   └── Jinja2 HTML templates
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   └── utils/
│       └── Utility functions
│
├── database/
│   └── Database-related resources
│
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md
└── VoyageIQ Documentation.docx
```

---

# 🔄 Application Workflow

A typical VoyageIQ travel-planning workflow looks like this:

```text
1. User opens VoyageIQ
          ↓
2. Searches origin & destination
          ↓
3. Selects travel dates
          ↓
4. Searches available flights
          ↓
5. Explores hotels
          ↓
6. Checks destination weather
          ↓
7. Estimates overall trip budget
          ↓
8. Evaluates travel options
          ↓
9. Saves the trip as a Target Trip
          ↓
10. Manages the trip from the dashboard
```

The entire workflow is designed to happen within a single platform instead of requiring users to repeatedly switch between different travel websites.

---

# 🔒 Environment Configuration

VoyageIQ uses environment variables for sensitive configuration.

Create a `.env` file based on `.env.example`.

Example configuration:

```env
SECRET_KEY=your_secret_key

DATABASE_URL=your_database_connection_string

SERPAPI_KEY=your_serpapi_key
```

> **Never commit real API keys, passwords, database credentials, or other secrets to GitHub.**

For production deployment, sensitive configuration can be managed through **Azure Key Vault** and Azure application configuration rather than storing secrets directly in the repository.

---

# 🚀 Running VoyageIQ Locally

## 1. Clone the Repository

```bash
git clone <repository-url>
cd VoyageIQ
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

For Windows, create the file manually if required.

Add the required:

* Flask secret key
* Database configuration
* SERPAPI credentials
* Other application configuration

## 5. Configure PostgreSQL

Create a PostgreSQL database and update the database connection string in your environment configuration.

## 6. Start the Application

```bash
python app.py
```

The application will then be available through the local Flask development server.

---

# 🧪 Development & Version Control

VoyageIQ uses Git and GitHub for source-code management and version control.

Development follows a modular approach where individual application features are organized into separate Flask Blueprints and service modules.

This makes it easier to:

* Develop features independently
* Debug individual modules
* Maintain clean code
* Track changes
* Deploy updates
* Extend the application in the future

---

# 📈 Project Highlights

| Area                       | Implementation                   |
| -------------------------- | -------------------------------- |
| Backend                    | Flask / Python                   |
| Frontend                   | HTML, CSS, Bootstrap, JavaScript |
| Database                   | PostgreSQL                       |
| Cloud Database             | Azure Database for PostgreSQL    |
| Hosting                    | Azure App Service                |
| Secrets                    | Azure Key Vault                  |
| Flight Data                | SERPAPI                          |
| Hotel Data                 | SERPAPI                          |
| Weather Data               | Open-Meteo                       |
| Authentication             | Session-based authentication     |
| Architecture               | Modular Flask / Service Layer    |
| Version Control            | Git & GitHub                     |
| Travel Planning Efficiency | ~80% less tab switching          |

---

# 🎯 Project Objectives

VoyageIQ was built to provide practical experience in modern full-stack application development.

The major objectives were:

* Build a real-world full-stack application using Python and Flask.
* Integrate multiple third-party REST APIs.
* Design and manage relational databases using PostgreSQL.
* Implement secure authentication and session management.
* Apply modular architecture using Flask Blueprints.
* Separate business logic through a service layer.
* Build a responsive frontend using Bootstrap and JavaScript.
* Deploy a production-oriented application using Microsoft Azure.
* Manage application secrets securely using Azure Key Vault.
* Work with cloud-hosted PostgreSQL databases.
* Use Git and GitHub for version control and deployment workflows.
* Solve a real-world problem by centralizing fragmented travel information.

---

# 🔮 Future Improvements

VoyageIQ is designed to be extensible, with several potential improvements planned for future versions.

### 🤖 AI-Powered Travel Recommendations

Introduce AI-based recommendations that understand user preferences and suggest suitable:

* Destinations
* Flights
* Hotels
* Travel dates
* Budgets

### 🗺️ Intelligent Itinerary Generation

Automatically generate day-by-day travel itineraries based on:

* Destination
* Trip duration
* Budget
* Weather
* User interests

### 💬 AI Travel Assistant

Add a conversational travel assistant that allows users to ask questions such as:

> "Find me a budget-friendly trip for 4 days with good weather."

### 📊 Advanced Trip Analytics

Provide users with deeper comparisons between:

* Flight prices
* Hotel prices
* Weather conditions
* Overall trip costs

### 🔔 Travel Alerts

Add notifications for:

* Flight price changes
* Weather changes
* Trip dates
* Saved travel plans

---

# 📚 Documentation

Detailed project documentation covering the architecture, implementation, features, and technical decisions is available in:

```text
VoyageIQ Documentation.docx
```

---

# 👨‍💻 Project

**VoyageIQ – Smart Travel Decision Platform**

Built as a full-stack project to explore:

**Python + Flask + PostgreSQL + REST APIs + JavaScript + Azure Cloud**

> **From scattered travel information to one intelligent travel decision platform.**
