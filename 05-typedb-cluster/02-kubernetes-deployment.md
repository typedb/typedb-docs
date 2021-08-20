---
pageTitle: Deploy TypeDB Cluster on Kubernetes
keywords: typedb, cluster, kubernetes, cloud, deployment
longTailKeywords: typedb on kubernetes
summary: Deploy TypeDB Cluster on Kubernetes
toc: false
---

## Deploying TypeDB Cluster onto Kubernetes

This guide describes how to deploy a 3-node TypeDB Cluster onto Kubernetes using [Helm](https://helm.sh/) package manager.


### Initial Setup

Regardless of the TypeDB Cluster configuration, these steps need to be performed once before the setup.

As a first step, create a secret to access TypeDB Cluster image on Docker Hub:

```
kubectl create secret docker-registry private-docker-hub --docker-server=https://index.docker.io/v2/ \
--docker-username=USERNAME --docker-password='PASSWORD' --docker-email=EMAIL
```

Next, configure Helm repo:

```
helm repo add vaticle https://repo.vaticle.com/repository/helm/
```

Additionally, if you choose to enable encrypted connections, you would need to install [`mkcert`](https://github.com/FiloSottile/mkcert/releases) and
also obtain a TypeDB Cluster distribution from [GitHub Releases](https://github.com/vaticle/typedb-cluster/releases).


### Deployment

Depending on the deployment method you choose, next steps to perform the deployment are as follows:

 #### Non-exposed Cluster

**Use this mode if your application is located within the same Kubernetes network as the cluster.**

Encryption can be enabled for this mode. Generated certificates need to be valid for `*.<helm-release-name>`,
so for deployment named `typedb-cluster`, certificate needs to be valid for `*.typedb-cluster` hostnames.
To generate them, execute these commands:

```
$ mkcert -cert-file rpc-certificate.pem -key-file rpc-private-key.pem "*.typedb-cluster"
$ # unpack distribution of TypeDB Cluster into `dist` folder
$ ./dist/typedb-cluster-all-<platform>-<version>/tool/create-encryption-mq-key.sh
$ kubectl create secret generic typedb-cluster \
  --from-file rpc-private-key.pem \
  --from-file rpc-certificate.pem \
  --from-file rpc-root-ca.pem="$(mkcert -CAROOT)/rootCA.pem" \
  --from-file mq-secret-key \
  --from-file mq-public-key
```

Note: Kubernetes secret need to be named the same as a deployment would be (`typedb-cluster`) and contain exactly
these keys (`rpc-private-key.pem`, `rpc-certificate.pem`, `rpc-root-ca.pem`, `mq-secret-key`, `mq-public-key`)

Deploying TypeDB Cluster in non-exposed mode means it would only be accessible from within the same Kubernetes cluster.
To do it, execute the command:

```
helm install typedb-cluster vaticle/typedb-cluster \
--set "cpu=7,replicas=3,singlePodPerNode=true,storage.persistent=true,storage.size=100Gi,exposed=false"
```

To enable encryption, append `encrypted` option to the argument:

```
helm install typedb-cluster vaticle/typedb-cluster \
--set "cpu=7,replicas=3,singlePodPerNode=true,storage.persistent=true,storage.size=100Gi,exposed=false,encrypted=true"
```

This command deploys a 3-node Cluster using 100Gi volumes for persistence. It would be accessible via `typedb-cluster-{0..2}.typedb-cluster`
hostname within the Kubernetes network.

#### Exposed Cluster - Cloud

*Use this mode if you need to access the Cluster from outside of Kubernetes such as with Workbase or Console from your local machine.*

**Enabling encryption (optional)**

In order to enable encryption, there are two certificate that needs to be configured: external certificate (TLS) and internal certificate (Curve).

Let's start by configuring the external certificate.

The TLS certificate is typically obtained from trusted third-party providers. Alternatively it is also possible to generate the certificate manually for development purpose using `mkcert`:

```
$ mkcert -cert-file rpc-certificate.pem -key-file rpc-private-key.pem "*.typedb-cluster.example.com" "*.typedb-cluster"
```

Please note that TLS certificate must be bound to a domain name, and not IP addresses. This means that your server instances must each be accessible via domain names and not IP addresses.

Also, the certificate need to be valid for `*.<helm-release-name>.<domain-name>` and `*.<helm-release-name>`, so for deployment named `typedb-cluster` and domain `example.com`, certificate needs to be valid for `*.typedb-cluster.example.com` and `*.typedb-cluster` hostnames.

Once done, proceed to configure the internal certificate:

```
$ # unpack distribution of TypeDB Cluster into `dist` folder
$ ./dist/typedb-cluster-all-<platform>-<version>/tool/create-encryption-mq-key.sh
```

**Deployment**

Once done, you can proceed to initiate the deployment:

```
$ kubectl create secret generic typedb-cluster \
  --from-file rpc-private-key.pem \
  --from-file rpc-certificate.pem \
  --from-file rpc-root-ca.pem="$(mkcert -CAROOT)/rootCA.pem" \
  --from-file mq-secret-key \
  --from-file mq-public-key
```

Note: Kubernetes secret need to be named the same as a deployment would be (`typedb-cluster`) and contain exactly these keys (`rpc-private-key.pem`, `rpc-certificate.pem`, `rpc-root-ca.pem`, `mq-secret-key`, `mq-public-key`)


If an application does not use Kubernetes, TypeDB Cluster needs to be exposed on public IPs or public domains (**required** for encryption).
This is handled by cloud provider of Kubernetes  which would allocate and assign a public IP address to the services we're deploying. Each TypeDB Cluster pod will get an associated `LoadBalancer`,
so for a 3-node TypeDB Cluster, 3 public IPs would be allocated. To do it, execute the command:

```
helm install typedb-cluster vaticle/typedb-cluster \
--set "cpu=7,replicas=3,singlePodPerNode=true,storage.persistent=true,storage.size=100Gi,exposed=true"
```

To enable encryption, append `encrypted` and `domain` options to the argument:

```
helm install typedb-cluster vaticle/typedb-cluster \
--set "cpu=7,replicas=3,singlePodPerNode=true,storage.persistent=true,storage.size=100Gi,exposed=false,encrypted=true,domain=example.com"
```

After deployment, you need to configure your DNS such that for every cluster node there is an A record pointing to its public IP:

`typedb-cluster-0.typedb-cluster.example.com` => `external ip of typedb-cluster-0 service`
`typedb-cluster-1.typedb-cluster.example.com` => `external ip of typedb-cluster-1 service`
`typedb-cluster-2.typedb-cluster.example.com` => `external ip of typedb-cluster-2 service`

This command deploys a 3-node Cluster using 100Gi volumes for persistence.

Unencrypted cluster nodes would be accessible via public IPs assigned to the services which can obtained via executing this command:

```
kubectl get svc -l external-ip-for=typedb-cluster \
-o='custom-columns=NAME:.metadata.name,IP:.status.loadBalancer.ingress[0].ip'
```

Encrypted cluster nodes would be accessible via `typedb-cluster-{0..2}.typedb-cluster.example.com` hostnames.

#### Exposed Cluster - Minikube

*Use this mode for setting up a development cluster in your local machine.*

**Enabling encryption (optional)**

Encryption *cannot* be enabled in this configuration.

**Deployment**

Please make sure to have [Minikube](https://minikube.sigs.k8s.io/) installed and running.

Once done, we can perform the deployment:

```
helm install vaticle/typedb-cluster --generate-name \
--set "cpu=2,replicas=3,singlePodPerNode=false,storage.persistent=true,storage.size=10Gi,exposed=true"
```

Then, enable tunneling from another terminal:

```
minikube tunnel
```

This deployment mode is primarily inteded for development purpose. Certain adjustments will be made compared to other deployment modes:

* Minikube only has a single node, so `singlePodPerNode` needs to be set to `false`
* Minikube's node only has as much CPUs as the local machine: `kubectl get node/minikube -o=jsonpath='{.status.allocatable.cpu}'`.
  Therefore, for deploying a 3-node TypeDB Cluster to a node with 8 vCPUs, `cpu` can be set to `2` at maximum.
* Storage size probably needs to be tweaked from default value of `100Gi` (or fully disabled persistent)
  as total storage required is `storage.size` multiplied by `replicas`. In our example, total storage requirement is 30Gi.


### Configuration Reference

Configurable settings for Helm package include:

| Key | Default value | Description
| :----------------: | :------:| :---------------------------------------------------------------------------------------: |
| `replicas`          | `3`     | Number of TypeDB Cluster nodes to run                                                     |
| `cpu`               | `7`     | How many CPUs should be allocated for each TypeDB Cluster node                            |
| `storage.size`      | `100Gi` | How much disk space should be allocated for each TypeDB Cluster node                      |
| `storage.persistent`| `true`  | Whether TypeDB Cluster should use a persistent volume to store data                       |
| `singlePodPerNode`  | `true`  | Whether TypeDB Cluster pods should be scheduled to different Kubernetes nodes             |
| `exposed`           | `false` | Whether TypeDB Cluster supports connections via public IP (outside of Kubernetes network) |


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

#### One or more pods of TypeDB Cluster are stuck in `Pending` state
This might mean pods requested more resources than available. To check if that's the case, run
`kubectl describe pod/typedb-cluster-0` on a stuck pod (e.g. `typedb-cluster-0`). Error message similar to 
`0/1 nodes are available: 1 Insufficient cpu.` or `0/1 nodes are available: 1 pod has unbound immediate PersistentVolumeClaims.`
indicates that `cpu` or `storage.size` values need to be decreased.


#### One or more pods of TypeDB Cluster are stuck in `CrashLoopBackOff` state
This might indicate any misconfiguration of TypeDB Cluster. Please obtain the logs by executing
`kubectl logs pod/typedb-cluster-0` and share them with TypeDB Cluster developers.


### Current Limitations

Deployment has several limitations which shall be resolved in the future:

* TypeDB Cluster doesn't support dynamic reconfiguration of node count without restarting all of the nodes.
