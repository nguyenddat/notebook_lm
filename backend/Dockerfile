FROM python:3.12.6

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Tạo thư mục làm việc
RUN mkdir /backend
WORKDIR /backend

# Copy toàn bộ source code vào container
COPY . /backend/

# Cài đặt thư viện Python
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install python-multipart \
    && pip install uvicorn[standard]

EXPOSE 9000
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-9000}`"]