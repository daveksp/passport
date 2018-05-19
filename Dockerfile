FROM python:2.7

RUN mkdir -p /opt/app/

WORKDIR /opt/app
COPY ../passport/ /opt/app/
RUN ls /opt/app
RUN pip install -r resources/requirements.txt

EXPOSE 8089

ENV C_FORCE_ROOT true

CMD ["python", "manage.py", "runserver", "-p", "8089"]
