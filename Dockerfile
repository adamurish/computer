FROM python:3
EXPOSE 2667
WORKDIR /home_auto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "paapas:create_app()"]
