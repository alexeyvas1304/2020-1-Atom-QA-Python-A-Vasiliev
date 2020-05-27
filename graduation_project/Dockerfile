FROM python:3.8

ADD /requirements.txt requirements.txt

RUN pip3.8 install -r requirements.txt

ADD /mock.py mock.py

EXPOSE 5000

CMD ["python3.8", "mock.py"]