FROM python:3.8

ADD agente.py .

RUN pip install prometheus-client 

CMD [ "python", "./agent.py" ]