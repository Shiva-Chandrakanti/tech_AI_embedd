import pandas as pd
from flask import request
from werkzeug.utils import secure_filename
import os
import PyPDF2
from sentence_transformers import SentenceTransformer
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector

class inser_data_db():
    def __init__(self,config,db_launch):
        self.config=config
        self.db_launch=db_launch
        
    def allowed_file(self,filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'csv'}
    
    def generate_embeddings(self,text):
        try:
            # # Generate embeddings for the input text
            # model = SentenceTransformer('all-MiniLM-L6-v2')
            # embedding = model.encode(text)
            # return embedding
            loader = TextLoader(text,encoding='utf-8')
            # loads the text from the given text
            documents =loader.load()
            textsplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            # splits the given text and based on provided chunk size, maintaning overlap
            texts=textsplitter.split_documents(documents)
            
            embeddings=OpenAIEmbeddings()
            # intilazing the embeddings
            # vector_data=embeddings.embed_dcouments([t.page_content for t in texts])
            db_details=self.config['AML_POSTGRES']
            conn_str=f"postgresql+psycopg2://{db_details['database']}:{db_details['host']}:{db_details['port']}/{db_details['database']}"

            inser_data=PGVector.from_documents(embedding=embeddings,documents=texts,collection_name=self.config['EMBEDIING_data']['table_name'],connection_string=conn_str)
            # passing the embeddings and texts need to be embedded and connection to vector base.
            return {"successfully inserted"}
        except Exception as err:
            print("error while creating embeddings and inserting :",err)
            return "error while creating embeddings and inserting :"+str(err)

    def read_file(self,filepath):
        try:
            """the temperary file is read and converted to text"""
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
        except Exception  as err:
            return "error while reading files "+str(err)

    def upload_file(self):
        """ takes payload file and calls the related functions to upload file into database"""
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
            # self.db_launch.query_execute(q_type = "embed_insert",embedding=embeddings,insert_db=self.config['EMBEDIING_data']['database'],insert_table=self.config['EMBEDIING_data']['table_name'])
            os.remove(filepath)

            return {'message': 'File uploaded successfully'}
        else:
            return {'error': 'Invalid file format'}

        
