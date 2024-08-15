FROM python:3.9.9
WORKDIR /app
COPY . .
EXPOSE 8501
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "Application.py"]