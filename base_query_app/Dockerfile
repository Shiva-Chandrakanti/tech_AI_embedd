# a simple docker image
FROM python:3.9.6
WORKDIR /open_ai_query_app
COPY config /open_ai_query_app/config/
COPY . /open_ai_query_app
RUN pip3 install -r requirements.txt
EXPOSE 5004
CMD python3 ./query_app.py