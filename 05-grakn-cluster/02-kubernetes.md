---
pageTitle: Deploy Grakn Cluster on Kubernetes
keywords: grakn, cluster, kubernetes, cloud, deployment
longTailKeywords: grakn on kubernetes
summary: Deploy Grakn Cluster on Kubernetes
toc: false
---

## Deploying Grakn Cluster onto Kubernetes

This guide describes how to deploy a 3-node Grakn Cluster onto Kubernetes using [Helm](https://helm.sh/) package manager.


### Initial Setup

Regardless of the Grakn Cluster configuration, these steps need to be performed once before the setup.

As a first step, create a secret to access Grakn Cluster image on Docker Hub:

```
kubectl create secret docker-registry private-docker-hub --docker-server=https://index.docker.io/v2/ \
--docker-username=USERNAME --docker-password='PASSWORD' --docker-email=EMAIL
```

Next, configure Helm repo:

```
helm repo add graknlabs https://repo.grakn.ai/repository/helm/
```

### Deployment

Depending on the deployment method you choose, next steps to perform the deployment are as follows:

<div class="tabs light">

[tab:Non-exposed Cluster]

**Use this mode if your an application resides within the same Kubernetes network.**

Deploying Grakn Cluster in non-exposed mode means it would only be accessible from within the same Kubernetes cluster. To do it, execute the command:

```
helm install graknlabs/grakn-cluster --generate-name \
--set "cpu=7,replicas=3,singlePodPerNode=true,storage.persistent=true,storage.size=100Gi,exposed=false"
```

This command deploys a 3-node Cluster using 100Gi volumes for persistence. It would be accessible via `grakn-cluster-{0..2}.grakn-cluster`
hostname within the Kubernetes network.
[tab:end]

[tab:Exposed Cluster - Cloud]

**Use this mode if you need to access the Cluster from outside of Kubernetes. For example, if you need to connect using Workbase or Console from your local machine.**

If an application does not use Kubernetes, Grakn Cluster needs to be exposed on public IPs. This is handled by cloud provider of Kubernetes
which would allocate and assign a public IP address to the services we're deploying. Each Grakn Cluster pod will get an associated `LoadBalancer`,
so for a 3-node Grakn Cluster, 3 public IPs would be allocated. To do it, execute the command:

```
helm install graknlabs/grakn-cluster --generate-name \
--set "cpu=7,replicas=3,singlePodPerNode=true,storage.persistent=true,storage.size=100Gi,exposed=true"
```

This command deploys a 3-node Cluster using 100Gi volumes for persistence.
It would be accessible via public IPs assigned to the services which can obtained via executing this command:

```
kubectl get svc -l external-ip-for=grakn-cluster \
-o='custom-columns=NAME:.metadata.name,IP:.status.loadBalancer.ingress[0].ip'
```
[tab:end]

[tab:Exposed Cluster - Minikube]

**Use this mode for local development with Grakn Cluster.**

Having installed and started [Minikube](https://minikube.sigs.k8s.io/), this is the command to deploy Grakn Cluster:

```
helm install graknlabs/grakn-cluster --generate-name \
--set "cpu=2,replicas=3,singlePodPerNode=false,storage.persistent=true,storage.size=10Gi,exposed=true"
```

and in another terminal (this is a foreground process that needs to continue running):

```
minikube tunnel
```

Certain adjustments are made to the usual cloud deployment:

* Minikube only has a single node, so `singlePodPerNode` needs to be set to `false`
* Minikube's node only has as much CPUs as the local machine: `kubectl get node/minikube -o=jsonpath='{.status.allocatable.cpu}'`.
  Therefore, for deploying a 3-node Grakn Cluster to a node with 8 vCPUs, `cpu` can be set to `2` at maximum.
* Storage size probably needs to be tweaked from default value of `100Gi` (or fully disabled persistent)
  as total storage required is `storage.size` multiplied by `replicas`. In our example, total storage requirement is 30Gi.

[tab:end]
</div>

### Configuration Reference

Configurable settings for Helm package include:

| Key | Default value | Description
| :----------------: | :------:| :---------------------------------------------------------------------------------------: |
| `replicas`          | `3`     | Number of Grakn Cluster nodes to run                                                     |
| `cpu`               | `7`     | How many CPUs should be allocated for each Grakn Cluster node                            |
| `storage.size`      | `100Gi` | How much disk space should be allocated for each Grakn Cluster node                      |
| `storage.persistent`| `true`  | Whether Grakn Cluster should use a persistent volume to store data                       |
| `singlePodPerNode`  | `true`  | Whether Grakn Cluster pods should be scheduled to different Kubernetes nodes             |
| `exposed`           | `false` | Whether Grakn Cluster supports connections via public IP (outside of Kubernetes network) |


### Troubleshooting

These are the common error scenarios and how to troubleshoot them:

#### All pods are stuck in `ErrImagePull` or `ImagePullBackOff` state:
This means the secret to pull the image from Docker Hub has not been created. 
Make sure you've followed [Initial Setup](#initial-setup) instructions and verify that the pull secret is present by
executing `kubectl get secret/private-docker-hub`. Correct state looks like this:

```
$ kubectl get secret/private-docker-hub
NAME                 TYPE                             DATA   AGE
private-docker-hub   kubernetes.io/dockerconfigjson   1      11d
```

#### One or more pods of Grakn Cluster are stuck in `Pending` state
This might mean pods requested more resources than available. To check if that's the case, run
`kubectl describe pod/grakn-cluster-0` on a stuck pod (e.g. `grakn-cluster-0`). Error message similar to 
`0/1 nodes are available: 1 Insufficient cpu.` or `0/1 nodes are available: 1 pod has unbound immediate PersistentVolumeClaims.`
indicates that `cpu` or `storage.size` values need to be decreased.


#### One or more pods of Grakn Cluster are stuck in `CrashLoopBackOff` state
This might indicate any misconfiguration of Grakn Cluster. Please obtain the logs by executing
`kubectl logs pod/grakn-cluster-0` and share them with Grakn Cluster developers.


### Current Limitations

Deployment has several limitations which shall be resolved in the future:

* Grakn Cluster doesn't support dynamic reconfiguration of node count without restarting all of the nodes.
