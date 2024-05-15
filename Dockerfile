
FROM python:3.11
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app
COPY --chown=user . $HOME/app

COPY ./requirements.txt ~/app/requirements.txt
RUN pip install -r requirements.txt

COPY . .
# Dirty hack to make it work
USER root
# Set an environment variable for the port (optional)
ENV FLASK_RUN_PORT=8000

# Expose the port Flask will run on
EXPOSE 8000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]