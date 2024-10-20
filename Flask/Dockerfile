FROM python:latest
RUN apt update
# RUN pip install -r requirements.txt
RUN pip install Flask
RUN pip install Flask-SQLAlchemy
RUN pip install PyMySQL
RUN pip install python-dotenv
ARG UID=1000
ARG GID=1000
ARG USERNAME=app
ARG GROUPNAME=app

RUN groupadd -g $GID $GROUPNAME && \
    useradd -m -u $UID -g $GID $USERNAME
COPY --chown=$UID:$GID ./ /usr/src/app
WORKDIR /usr/src/app
USER $USERNAME
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000","--debugger", "--reload"]
