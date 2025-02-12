import pandas as pd
from flask import request
from werkzeug.utils import secure_filename
import os
import PyPDF2
from sentence_transformers import SentenceTransformer

class inser_data_db():
    def __init__(self,config,db_launch):
        self.config=config
        self.db_launch=db_launch
        
    def allowed_file(self,filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'csv'}
    
    def generate_embeddings(self,text):
        # Generate embeddings for the input text
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embedding = model.encode(text)
        return embedding

    def read_file(self,filepath):
        extension = filepath.rsplit('.', 1)[1].lower()

        if extension == 'txt':
            with open(filepath, 'r') as file:
                return file.read()

        elif extension == 'pdf':
            with open(filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text()
                return text

        elif extension == 'csv':
            df = pd.read_csv(filepath)
            return df.to_string()

    def upload_file(self):
        if 'file' not in request.files:
            return {'error': 'No file part'}
        
        file = request.files['file']
        if file.filename == '':
            return {'error': 'No selected file'}
        
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(self.config['file_path']['file_path'], filename)
            file.save(filepath)

            # Process file depending on its type
            content = self.read_file(filepath)

            # Generate embeddings (for example using OpenAI's API)
            embeddings = self.generate_embeddings(content)

            # Insert into PostgreSQL (example function call)
            self.db_launch.query_execute(q_type = "embed_insert",embedding=embeddings,insert_db=self.config['EMBEDIING_data']['database'],insert_table=['EMBEDIING_data']['table_name'])
            os.remove(filepath)

            return {'message': 'File uploaded successfully'}
        else:
            return {'error': 'Invalid file format'}

        
