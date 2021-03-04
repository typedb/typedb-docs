---
pageTitle: Deploy Grakn Cluster on Kubernetes
keywords: grakn, cluster, kubernetes, cloud, deployment
longTailKeywords: grakn on kubernetes
summary: Deploy Grakn Cluster on Kubernetes
toc: false
---

## Deploying Grakn Cluster onto Kubernetes

This guide describes how to deploy a 3-node Grakn Cluster onto Kubernetes.
It assumes we'd want to run them on separate Kubernetes nodes (for increased fault-tolerancy)
and that the cluster has these nodes available with sufficient resources (8 CPUs).
Additionally, it assumes Kubernetes provides persistent volumes.

1. Create a secret to access Grakn Cluster image on Docker Hub:

```
kubectl create secret docker-registry private-docker-hub --docker-server=https://index.docker.io/v2/ \
--docker-username=USERNAME --docker-password='PASSWORD' --docker-email=EMAIL
```

2. Create a sample config (`grakn-cluster.yml`):

```
---
apiVersion: v1
kind: Service
metadata:
  name: grakn-cluster
  labels:
    app: grakn-cluster
spec:
  ports:
    - port: 1729
      targetPort: 1729
      name: grakn-cluster
  type: ClusterIP
  selector:
    app: grakn-cluster
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: grakn-cluster
spec:
  serviceName: "grakn-cluster"
  replicas: 3
  selector:
    matchLabels:
      app: grakn-cluster
  template:
    metadata:
      labels:
        app: grakn-cluster
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: "app"
                    operator: In
                    values:
                      - grakn-cluster
              topologyKey: "kubernetes.io/hostname"
      imagePullSecrets:
        - name: private-docker-hub
      containers:
        - name: grakn-cluster
          image: graknlabs/grakn-cluster:k8s-1
          resources:
            requests:
              cpu: "7"
          command:
            - /bin/bash
            - -c
            - '/opt/util/wait-for-host.sh grakn-cluster-0.grakn-cluster && /opt/util/wait-for-host.sh grakn-cluster-1.grakn-cluster && /opt/util/wait-for-host.sh grakn-cluster-2.grakn-cluster && /opt/grakn-cluster-all-linux/grakn server --data=/mnt/data/ --replication=/mnt/replication/ --address $(hostname).grakn-cluster:1729:1730 --peer grakn-cluster-0.grakn-cluster:1729:1730 --peer grakn-cluster-1.grakn-cluster:1729:1730 --peer grakn-cluster-2.grakn-cluster:1729:1730'
	  ports:
            - containerPort: 1729
              name: client-port
            - containerPort: 1730
              name: server-port
          volumeMounts:
            - name: grakn-data
              mountPath: /mnt/
  volumeClaimTemplates:
    - metadata:
        name: grakn-data
      spec:
        accessModes: [ "ReadWriteOnce" ]
        resources:
          requests:
            storage: 100Gi
---
```

3. Deploy the config:

```
kubectl apply -f grakn-cluster.yml
```

## Current limitations

Deployment has several limitations which shall be resolved in future:

* Deployment doesn't support exposing nodes publicly (with `LoadBalancer` instead of `ClusterIP`) and only
supports connection from within the cluster (client should be able to connect to all `grakn-cluster-{0..2}.grakn-cluster`)
* Grakn Cluster doesn't support dynamic reconfiguration of node count without restarting all of the nodes
* Node count is hardcoded in the startup command of the container
