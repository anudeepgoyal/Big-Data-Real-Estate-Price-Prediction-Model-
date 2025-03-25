# Use Bitnami Spark image with version 3.3.2
FROM bitnami/spark:3.3.2

# Switch to root user
USER root

# 1️⃣ Update package lists, install Python3 & pip
RUN apt-get update && apt-get install -y \
    ca-certificates \
    gnupg \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 2️⃣ First install required Python libraries in proper order
RUN pip3 install --no-cache-dir \
    pyspark==3.3.2 \
    streamlit \
    openpyxl \
    numpy==1.23.5 \
    pandas==1.5.3

# 3️⃣ Set the working directory
WORKDIR /app

# 4️⃣ Copy project files
COPY . /app

# 5️⃣ Expose Streamlit port
EXPOSE 8501

# 6️⃣ Run Streamlit app
CMD ["streamlit", "run", "app.py"]
