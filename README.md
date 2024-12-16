# Backend for blazeSql Filtering

This project provides a Flask API with Swagger documentation for blaze filtering

## Features

-   Flask-RESTx for building REST APIs
-   Swagger UI for interactive API documentation
-   Simple API endpoint returning a prediction response

## Installation

micromamba create -n blazingsql_env python=3.8
micromamba activate blazingsql_env
micromamba install -c blazingsql -c rapidsai -c nvidia -c conda-forge -c defaults blazingsql python=3.8 cudatoolkit=11.4
micromamba install --file req.txt

## to run
micromamba activate blazingsql_env
flask run --port=8889