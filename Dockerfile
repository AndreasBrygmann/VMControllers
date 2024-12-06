
FROM python:3.9


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./controllers /code/controllers

EXPOSE 4000


CMD ["vm_controllers", "run", "controllers/main.py", "--port", "4000"]