FROM python:3.7.2-alpine3.9

WORKDIR /home/skaborik/wg_forge_backend/task1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]