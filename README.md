# Dashboard Reverse Engineering

This project is a reverse-engineered web analytics dashboard. The goal is to replicate any given dashboard from an image using **Dash**, **Plotly**, and **Flask API** with dynamic data from a **MongoDB** backend. This project is focused on creating a real-time, interactive dashboard in a matter of seconds from a simple image.

## Project Overview

The project involves reverse-engineering an existing dashboard from an image into a fully functional, data-driven system. The dashboard is powered by **MongoDB** for storing data, **Flask API** for backend interaction, and **Dash** for the frontend, using **Plotly** for dynamic visualizations.

The dashboard can include various metrics and charts:
- **Total Sessions**
- **Users**
- **Bounce Rate**
- **Goal Completion**
- **Traffic Sources** (Interactive Pie Chart)
- **Geographical Traffic Distribution** (World Map)
- **Sessions and Goals Over Time** (Line Chart)

## Features

- Interactive components (Pie Chart, Line Chart, World Map).
- Real-time data updates from MongoDB using Flask API.
- Clear and structured layout, leveraging Bootstrap for responsive design.
- Dynamic metrics tracking web analytics with the ability to visualize trends and distribution.
- Placeholder synthetic data insertion, as well as customizability to fit schema for your own data

## Technologies Used

- **Dash**: For building the web interface and managing dynamic interactions.
- **Plotly**: For creating interactive charts and data visualizations.
- **Flask**: Used for creating an API layer to serve data from MongoDB.
- **MongoDB**: The database used to store all analytics data.
- **Bootstrap**: For responsive design, ensuring the dashboard looks good on various devices.

## Installation

To get the project running locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dashboard-reverse-engineering.git
   cd dashboard-reverse-engineering
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
3. Set up and run the MongoDB instance and modify the placeholder client call. (ensure it's running on the default port or adjust accordingly).
4. Setup your OpenAI Credentials
5. run the setup script:
```bash
./setup_env.sh
