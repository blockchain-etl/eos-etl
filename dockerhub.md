# Uploading to Docker Hub

```bash
> EOSETL_STREAMING_VERSION=1.0.0-streaming
> docker build -t eos-etl:${EOSETL_STREAMING_VERSION} -f Dockerfile_with_streaming .
> docker tag eos-etl:${EOSETL_STREAMING_VERSION} blockchainetl/eos-etl:${EOSETL_STREAMING_VERSION}
> docker push blockchainetl/eos-etl:${EOSETL_STREAMING_VERSION}
```