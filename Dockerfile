FROM python:3

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt
RUN python3 -m pip install -U discord.py

ENV NAME World

CMD ["python3", "main.py"]