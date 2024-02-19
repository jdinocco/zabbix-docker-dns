FROM python:3.8-slim

# Instala dnsutils y utilidades para configurar la zona horaria
RUN apt-get update && apt-get install -y dnsutils tzdata

# Configura la zona horaria
ENV TZ=America/Buenos_Aires
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Establece el directorio de trabajo en /app
WORKDIR /app

# Actualiza pip e instala jc
RUN pip install --upgrade pip && pip install jc

# Instala las dependencias de Python especificadas en requirements.txt
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copia el resto de tu aplicación al directorio de trabajo /app
COPY . /app

# Indica el comando para ejecutar tu aplicación
CMD ["python", "app.py"]

