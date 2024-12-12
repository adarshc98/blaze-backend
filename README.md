# Backend for blazeSql Filtering

This project provides a Flask API with Swagger documentation for blaze filtering

## Features

-   Flask-RESTx for building REST APIs
-   Swagger UI for interactive API documentation
-   Simple API endpoint returning a prediction response

## Installation
micromamba create -n blazingsql_env python=3.8 cudatoolkit=11.4 cudf=21.08 dask-cudf=21.08 blazingsql=21.8.2 -c rapidsai -c nvidia -c conda-forge
micromamba activate blazingsql_env
micromamba install --file req.txt

flask run --port=8889