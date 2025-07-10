FROM python:3.13-alpine3.22

RUN apk update && apk add gcompat glib nss libxcb libgcc chromium
RUN apk add chromium-chromedriver

RUN adduser -D app
RUN mkdir /app
RUN chown app:app /app
USER app
WORKDIR /app
COPY --chown=app:app . /app

RUN pip install --upgrade -r req.txt

#CMD ["python3", "-m", "fastapi", "run", "app.py", "--port", "80"]
CMD ["python3", "-m", "app"]
