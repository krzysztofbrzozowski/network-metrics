# network_metrics
App to measure network statistics, mainly desired for measuring k8s external world connection status


Basic app stage
- App can be run and in Docker (using docker compose) to test it locally


## Repo contains two main Dockerfiles:
### Dockerfile.dev
This one is to be used with docker-compose.yaml - here happening only linkig for config, logs and src
This is to avoid overhead with copying the files everytime the docker is running again

### Dockerfile
This is prod dockerfile - all of the directories are copied to create one package to be used in k8s

## Pushing package to container registry on ghcr.io
```bash
docker login --username <user> --password <PAT> ghcr.io
```
```bash
docker build . -t ghcr.io/krzysztofbrzozowski/network_metrics:0.1.0  -t ghcr.io/krzysztofbrzozowski/network_metrics:latest
```

```bash
docker push ghcr.io/krzysztofbrzozowski/network_metrics:0.1.0
```

## Downloading
```bash

```


TODO:
    - [] Find out why scapy is not working in docker (ping not working)