---
sidebarTitle: Google Cloud
pageTitle: Google Cloud Deployment
summary:
permalink: /docs/cloud-deployment/google-cloud
---

### Deploying Grakn on Google Cloud

As illustrated below, deploying [Grakn KGMS on Google Cloud](https://console.cloud.google.com/marketplace/details/grakn-public/grakn-kgms-premium) is a straight-forward process.

<div class="slideshow">

[slide:start]

[header:start]Visit KGMS on Google Cloud[header:end]

[body:start]![Visit KGMS on Google Cloud](/docs/images/cloud-deployment/gc_listing_a.png)[body:end]

[footer:start]
Visit the [KGMS listing on GCP Marketplace](https://console.cloud.google.com/marketplace/details/grakn-public/grakn-kgms-premium)
[footer:end]

[slide:end]
<!-- -->
[slide:start]

[header:start]Launch[header:end]

[body:start]![Launch](/docs/images/cloud-deployment/gc_listing_b.png)[body:end]

[footer:start]Click on **LAUNCH ON COMPUTE ENGINE**[footer:end]

[slide:end]
<!-- -->
[slide:start]

[header:start]Configure[header:end]

[body:start]![Configure](/docs/images/cloud-deployment/gc_new_deployment_a.png)[body:end]

[footer:start]Adjust the settings based on your requirements. You may also refer to the [best practices](#best-practices) for deploying Grakn KGMS on Google Cloud.[footer:end]

[slide:end]
<!-- -->
[slide:start]

[header:start]Configure Firewall Settings[header:end]

[body:start]![Configure Firewall Settings](/docs/images/cloud-deployment/gc_new_deployment_b.png)[body:end]

[footer:start]
In order to connect to the Grakn Server from outside the cluster, you need to _Allow TCP port 48555 traffic_.
[footer:end]

[slide:end]
<!-- -->
[slide:start]

[header:start]Configure Firewall Settings[header:end]

[body:start]![Configure Firewall Settings](/docs/images/cloud-deployment/gc_new_deployment_c.png)[body:end]

[footer:start]You can then click on _More_ to restrict access to certain IP addresses.[footer:end]

[slide:end]
<!-- -->
[slide:start]

[header:start]Deploy[header:end]

[body:start]![Deploy](/docs/images/cloud-deployment/gc_new_deployment_d.png)[body:end]

[footer:start]When satisfied with the configuration, click on **Deploy**.[footer:end]

[slide:end]
<!-- -->
[slide:start]

[header:start]Finishing Deployment[header:end]

[body:start]![Finishing Deployment](/docs/images/cloud-deployment/gc_finishing_deployment.png)[body:end]

[footer:start]That is all! Your cluster deployment is now pending.[footer:end]

[slide:end]
<!-- -->
[slide:start]

[header:start]Default Password[header:end]

[body:start]![Default Password](/docs/images/cloud-deployment/gc_default_password.png)[body:end]

[footer:start]Take note of the default password, as we will need this to for the initial authentication.[footer:end]

[slide:end]
</div>

### Running Grakn
Once the deployment is complete, a Grakn Cluster starts automatically. There is no need for starting Grakn Servers manually.

<div class="galert">
[Important]
Once deployed, it will take some time for the cluster to fully bootup and synchronise. Allow approximately **two minutes per cluster node**. To check the status of the cluster bootup, you can perform a [cluster health check](#cluster-health-check).
</div>

### Default Credentials
As part of the deployment, Google Cloud produces the default credentials with username being `grakn` and the password as displayed on the post-deployment screen. We will need these credentials to access the Graql and Grakn consoles.

![Default Credentials](/docs/images/cloud-deployment/gc_default_password.png)

We strongly encourage changing the default password. To do this, we need to first [access Grakn Console](#accessing-grakn-console) and then [update the user](/docs/management/users#update-a-user) `grakn` giving it a new secured password.

### Logging into a node
For a more direct interaction with the database, we need to log into a node. To do so, we need to start an `ssh` session as illustrated below.

<div class="slideshow">

[slide:start]

[header:start]SSH Options[header:end]

[body:start]![SSH Options](/docs/images/cloud-deployment/gc_ssh_options.png)[body:end]

[footer:start]
Click on the dropdown caret. Choose an option. For the purpose of this demonstration, we will use (the first option) an in-browser terminal for the SSH session.
[footer:end]

[slide:end]
<!-- -->
[slide:start]

[header:start]Connecting[header:end]

[body:start]![Connecting](/docs/images/cloud-deployment/gc_ssh_connecting.png)[body:end]

[footer:start]
Wait while a secured connection is being made.
[footer:end]

[slide:end]
<!-- -->
[slide:start]

[header:start]we are in![header:end]

[body:start]![we are in!](/docs/images/cloud-deployment/gc_ssh_connected.png)[body:end]

[footer:start]
We are now inside the node and can directly interact with the database.
[footer:end]

[slide:end]
<!-- -->
</div>

### Cluster Health Check
While [logged into a node](#logging-into-a-node), run `grakn cluster status`. This outputs the list of all nodes, as shown below, with the first column indicating the Status (**U**p/**D**own) and State (**N**ormal/**L**eaving/**J**oining/**M**oving).

![Cluster Health Check](/docs/images/cloud-deployment/gc_cluster_health_check.png)

### Accessing Grakn Console
While [logged into a node](#logging-into-a-node), run `grakn console start`. This requires us to enter our credentials. If this is our first login, we need to enter the [default credentials](#default-credentials). Once authenticated, we are in the Grakn Console where, for instance, we may manage [authentication](/docs/management/users).

### Accessing Graql Console
While [logged into a node](#logging-into-a-node), we can enter the [Graql Console](/docs/running-grakn/console) where we can interact with and perform [queries](/docs/query/overview) on our [keyspaces](/docs/management/keyspace).

### Signing up For Enterprise Support
As a user of Grakn KGMS on Google Cloud, you are entitled to [premium enterprise support](...).

<hr style="margin-top: 40px">

### Best Practices
Google Cloud offers a wide range of compute and storage options. What follows is a set of generic recommendations for an optimal choice.

#### Compute options
The optimum machine choice offering a good balance between CPU and memory should be equipped with at least 4 vCPUs and 8 GB of RAM.
Using machines with additional RAM above a 25 GB threshold is not expected to yield significant performance improvements.
Having these bounds in mind, the following machines are recommended because they offer a balanced set of system resources for a range of workloads:
- Standard:
    - n1-standard-4
    - n1-standard-8
    - n1-standard-16
- High-CPU:
    - n1-highcpu-16
    - n1-highcpu-32
- High-memory:
    - n1-highmem-4
    - n1-highmem-8

For more information, please visit the [GC Machine Types](https://cloud.google.com/compute/docs/machine-types)

#### Storage options
For performance, we suggest using SSD persistent disks for majority of use cases. The specific size of persistent disks depends on the volume of data to be processed as well as your application-specific requirements.
It is also possible to use HDD persistent disks. Although these come at a reduced price, their poor performance does not justify their use and we do not recommend them.

For more information on GCE disks, please visit the [GC Disk Docs](https://cloud.google.com/compute/docs/disks)