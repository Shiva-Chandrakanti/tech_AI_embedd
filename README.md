# tech_AI_embedd

The api_service contains aplication enabler, which enables flask app, the api.py has functions corresponding to get payload from request, to return the json response

The config folder contains an YAML file where the user can configure api key, upload file temporary store path, the database connection details.

The db_service is used for databse connection, here it uses configured database details and connects to database and executes different queries.

The modules folder contains, main modules
- insert_data -> which reads the file from temporary store and convertes to embeddings and insert into provided database.
- gpt_connect -> takes the query from user, converts to embeddings query the database using similarity index, then data is passed to gpt for furthur details.

utilities folder mainly has config reader, which is used for reading elements from config file.

The object for db_service_launcher created in query_app, acts as connector for database.
The object is passed to functions that are called through api execution, for furthur connect to database.

query_app

intilizes app
initilizes db_service 
initlizes app_launcher

takes api request, calls corresponding functions.