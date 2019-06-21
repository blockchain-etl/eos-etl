# Uploading to Docker Hub

```bash
> docker build -t eos-etl:1.0-streaming -f Dockerfile_with_streaming .
> docker tag eos-etl:1.0-streaming blockchainetl/eos-etl:1.0-streaming
> docker push blockchainetl/eos-etl:1.0-streaming

> docker tag eos-etl:1.0-streaming blockchainetl/eos-etl:latest-streaming
> docker push blockchainetl/eos-etl:latest-streaming
```