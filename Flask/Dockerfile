FROM python:latest
RUN apt update
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

ARG UID=1000
ARG GID=1000
ARG USERNAME=app
ARG GROUPNAME=app

RUN groupadd -g $GID $GROUPNAME && \
    useradd -m -u $UID -g $GID $USERNAME
COPY --chown=$UID:$GID ./ /usr/src/app
WORKDIR /usr/src/app
USER $USERNAME
# RUN pip install -r /requirements.txt
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
