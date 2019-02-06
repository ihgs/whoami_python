FROM node:8 AS build

RUN mkdir /work
WORKDIR /work

COPY ./front /work
RUN npm install
RUN npm run build
# This results in a single layer image
FROM python:3.7

RUN mkdir /work
WORKDIR /work
RUN pip install pipenv
COPY server/Pipfile /work
COPY server/Pipfile.lock /work
RUN pipenv install
COPY ./server /work

COPY --from=build /work/dist /work/static
ENV PORT 80
EXPOSE 80
CMD ["pipenv", "run", "serve"]