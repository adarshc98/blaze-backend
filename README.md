# Stock Market Prediction API

This project provides a Flask API with Swagger documentation to predict stock market trends.

## Features

-   Flask-RESTx for building REST APIs
-   Swagger UI for interactive API documentation
-   Simple API endpoint returning a prediction response

## Installation

### 1. Prerequisites

-   Ensure you have Python 3.7 or later installed on your machine.
-   You'll also need pip to install dependencies.

### 2. Set up a virtual environment (optional but recommended)

Create and activate a virtual environment:

python3 -m venv env
source env/bin/activate # For macOS/Linux

# or

.\env\Scripts\activate # For Windows

3. Install the required dependencies:
   pip3 install -r requirements.txt

4. To Run the app:
   flask run

Navigate to http://127.0.0.1:5000/ in your browser for swagger UI

# conda dependencies for blaze

micromamba env create -f environment.yml
