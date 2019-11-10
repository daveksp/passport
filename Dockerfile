FROM python:2.7

RUN mkdir -p /opt/app/

ARG BUILD_AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY_ID=$BUILD_AWS_ACCESS_KEY_ID

ARG BUILD_AWS_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=$BUILD_AWS_ACCESS_KEY


WORKDIR /opt/app
COPY . /opt/app/
RUN ls /opt/app
RUN pip install -r resources/requirements.txt

EXPOSE 80

ENV C_FORCE_ROOT true

CMD ["python", "manage.py", "runserver", "-p", "80", "--host", "0.0.0.0"]
#CMD python manage.py runserver -p 80 -t 0.0.0.0
