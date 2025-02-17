# tech_AI_embedd

Flow
Run the query_app, which enables application, provides RESTAPI service to insert and query data.


Overview

This project provides a REST API service that interacts with a database, allowing users to upload files, perform data insertions, and query data using machine learning embeddings. The service leverages a configurable environment and includes functionality to interact with GPT for further data analysis.

Project Structure
    1. api_service
        Application Enabler: This component enables the  application and handles incoming requests. It routes requests to the appropriate functions and returns JSON responses.
        api.py: Contains functions to handle payloads from requests and return the appropriate JSON response.


    2. config
        YAML Configuration File: This file allows users to configure essential settings, including:
        API key authentication
        File upload temporary storage path
        Database connection details


    3. db_service
        Database Connection: This module is responsible for connecting to the database using the details specified in the configuration file. It handles the execution of various database queries and operations.


    4. modules
        insert_data: This module reads uploaded files from the temporary storage, converts the data into embeddings, and inserts the processed data into the provided database.
        gpt_connect: This module accepts user queries, converts them into embeddings, uses similarity indexing to query the database, and sends the retrieved data to GPT for further processing.


    5. utilities
        Config Reader: This utility reads values from the YAML configuration file, making it easier to retrieve configuration settings like the database connection details and file paths.


    6. query_app
        App Initialization: This module initializes the Flask app, sets up the database service, and prepares the application launcher for handling incoming API requests.
        API Request Handling: It processes incoming requests, invokes the appropriate functions, and manages the connection to the database via the db_service_launcher object.


Key Features
    File Upload: Users can upload files, which are stored temporarily and processed for database insertion.
    
    Embedding-based Search: Uses machine learning embeddings to perform similarity searches against the database.
    
    GPT Integration: Once relevant data is retrieved from the database, it is passed to GPT for further analysis or refinement.
    
    Database Connectivity: The application uses a configured database connection to perform data operations such as insertion and querying.


How it Works
    API Request: A user sends an API request, which is routed to the corresponding function in api.py.
    
    Database Connection: Through the db_service_launcher object, the application establishes a connection to the database.
    Data Processing: Depending on the request, the data may be inserted into the database (via insert_data) or queried using embeddings (via gpt_connect).

Response: The Flask app responds to the user with the requested information or an acknowledgment of the data insertion.
Setup and Configuration

Configuration File: Make sure to configure the config.yaml file with the necessary API keys, file paths, and database connection information.

Database Connection: Ensure that the database details are correct in the YAML configuration to allow proper connection and query execution.


Usage
    POST Request for Inserting Data: Upload a file via the API, which will be processed and inserted into the database.

    GET Request for Querying Data: Submit a query to the API, which will be processed using machine learning embeddings and return relevant database results.



