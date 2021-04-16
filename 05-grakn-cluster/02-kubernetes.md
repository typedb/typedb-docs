---
pageTitle: Deploy Grakn Cluster on Kubernetes
keywords: grakn, cluster, kubernetes, cloud, deployment
longTailKeywords: grakn on kubernetes
summary: Deploy Grakn Cluster on Kubernetes
toc: false
---

## Deploying Grakn Cluster onto Kubernetes

This guide describes how to deploy a 3-node Grakn Cluster onto Kubernetes using [Helm](https://helm.sh/) package manager.

It assumes we'd want to run them on separate Kubernetes nodes (for increased fault-tolerancy)
and that the cluster has these nodes available with sufficient resources (8 CPUs).
Additionally, it assumes Kubernetes provides persistent volumes.

1. Create a secret to access Grakn Cluster image on Docker Hub:

```
kubectl create secret docker-registry private-docker-hub --docker-server=https://index.docker.io/v2/ \
--docker-username=USERNAME --docker-password='PASSWORD' --docker-email=EMAIL
```

2. Configure Helm repo:

```
helm repo add graknlabs https://repo.grakn.ai/repository/helm/
```


3. Install Grakn Cluster with Helm:
```
helm install graknlabs/grakn-cluster --generate-name --set "cpu=7,replicas=3,singlePodPerNode=true,usePersistentDisk=true"
```

Configurable settings for Helm package include:

| Key | Default value | Description
| :----------------: | :------:| :--------------------------------------------------------------------------: |
| `replicas`         | `3`     | Number of Grakn Cluster nodes to run                                         |
| `cpu`              | `7`     | How many CPUs should be allocated for each Grakn Cluster node                |
| `storageSize`      | `100Gi` | How much disk space should be allocated for each Grakn Cluster node          |
| `singlePodPerNode` | `true`  | Whether Grakn Cluster pods should be scheduled to different Kubernetes nodes |
| `usePersistentDisk`| `true`  | Whether Grakn Cluster should use a persistent volume to store data           |


## Current limitations

Deployment has several limitations which shall be resolved in future:

* Deployment doesn't support exposing nodes publicly (with `LoadBalancer` instead of `ClusterIP`) and only
supports connection from within the cluster (client should be able to connect to all `grakn-cluster-{0..2}.grakn-cluster`)
* Grakn Cluster doesn't support dynamic reconfiguration of node count without restarting all of the nodes
* Node count is hardcoded in the startup command of the container
