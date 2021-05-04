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

### Steps

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
    helm install graknlabs/grakn-cluster --generate-name --set "cpu=7,replicas=3,singlePodPerNode=true,storage.persistent=true"
    ```

<div class="note">
[Note]
When running on <a href="https://minikube.sigs.k8s.io/">Minikube</a>, certain adjustments need to be made:

* Minikube only has a single node, so `singlePodPerNode` needs to be set to `false`
* Minikube's node only has as much CPUs as the local machine: `kubectl get node/minikube -o=jsonpath='{.status.allocatable.cpu}'`.
Therefore, for deploying a 3-node Grakn Cluster to a node with 8 vCPUs, `cpu` can be set to `2` at maximum.
* Storage size probably needs to be tweaked from default value of `100Gi` (or fully disabled persistent) as total storage required is `storage.size` multiplied by `replicas`
* It's possible to expose Grakn Cluster to connect to it from outside the Grakn Cluster, but for the IP to be assigned,
you need to run `minikube tunnel` in a separate terminal.

The final command for Minikube would look something like:
```
helm install graknlabs/grakn-cluster --generate-name --set "cpu=2,replicas=3,exposed=true,storage.size=10Gi,singlePodPerNode=false"
```
</div>

### Configuration

Configurable settings for Helm package include:

| Key | Default value | Description
| :----------------: | :------:| :---------------------------------------------------------------------------------------: |
| `replicas`          | `3`     | Number of Grakn Cluster nodes to run                                                     |
| `cpu`               | `7`     | How many CPUs should be allocated for each Grakn Cluster node                            |
| `storage.size`      | `100Gi` | How much disk space should be allocated for each Grakn Cluster node                      |
| `storage.persistent`| `true`  | Whether Grakn Cluster should use a persistent volume to store data                       |
| `singlePodPerNode`  | `true`  | Whether Grakn Cluster pods should be scheduled to different Kubernetes nodes             |
| `exposed`           | `false` | Whether Grakn Cluster supports connections via public IP (outside of Kubernetes network) |


## Current limitations

Deployment has several limitations which shall be resolved in the future:

* Grakn Cluster doesn't support dynamic reconfiguration of node count without restarting all of the nodes.
