# aws-utils

## Setup newly created EC2 instance

### Mount EFS

First, update and reboot instance.

```
sudo apt update
sudo reboot
```

Wait a few seconds and reconnect with ssh. Then run

```
sudo apt-get -y install nfs-common
```

Create a mount directory for your EFS and set access rights.

```
sudo mkdir /mnt/efs
sudo chmod 777 /mnt/efs
```

Mount your EFS. Lookup the DNS name of your EFS and use in the command below. It most likely has a format similar to this: `fs-013e1f3bdc7dfb4aa.efs.eu-north-1.amazonaws.com`.

```
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport <Replace with your EFS DNS Name>:/ /mnt/efs
```
