# Deploy Wazuh Docker in single node configuration

This deployment is defined in the `Dockerfile` file with one Wazuh manager containers, one Wazuh indexer containers, and one Wazuh dashboard container. Additionally the ns3 Simulation container is deployed from here as well.

It can be deployed by following this step: 

1) Start the environment with docker compose:

- In the foregroud:
```
$ docker compose up
```
- In the background:
```
$ docker compose up -d
```

The environment takes about 1 minute to get up (depending on your Docker host) for the first time since Wazuh Indexer must be started for the first time and the indexes and index patterns must be generated.

To access a running container run:

```
$ docker exec -it <CONTAINER_NAME> /bin/bash
```

To stop the deployment just run:
``` 
$ docker compose down
```


