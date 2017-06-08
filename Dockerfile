FROM python:3-alpine
MAINTAINER Baard Johansen "baard.johansen@sesam.io"
RUN apk update && \
    apk upgrade && \
    apk add p7zip gcc musl-dev
COPY ./service /service
WORKDIR /service
RUN pip install -r requirements.txt
EXPOSE 5000/tcp
ENTRYPOINT ["python"]
CMD ["datasource-service.py"]
