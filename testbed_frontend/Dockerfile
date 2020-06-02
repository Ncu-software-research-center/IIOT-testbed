FROM node:10.16.0 as builder

WORKDIR /code/website
COPY ./website /code/website

RUN npm config set sass_binary_site https://npm.taobao.org/mirrors/node-sass/
RUN npm install

RUN npm run build
RUN npm cache clean --force \
 && rm -r ./node_modules

FROM python:3.7

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code
COPY --from=builder /code/website /code/website

RUN chmod +x /code/wait-for-it.sh

RUN pip install -r requirements.txt

