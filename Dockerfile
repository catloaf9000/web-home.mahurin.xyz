FROM python:3.9.19-alpine3.20
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]