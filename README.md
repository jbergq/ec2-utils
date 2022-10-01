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
```

Mount your EFS. Lookup the DNS name of your EFS and use in the command below. It most likely has a format similar to this: `fs-013e1f3bdc7dfb4aa.efs.eu-north-1.amazonaws.com`.

```
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport <Replace with your EFS DNS Name>:/ /mnt/efs
```

```
sudo chmod -R 777 /mnt/efs
```

### Add SSH key

It can be convenient to store your SSH keys inside your EFS. If this is the case, you need to add them to your ssh-agent in order for them to work.

```
touch ~/.ssh/config
nano ~/.ssh/config
```

Inside of the file, paste the following:

```
Host github.com
 HostName github.com
 IdentityFile /path/to/ssh/id_rsa
```

Where `/path/to/ssh/id_rsa` can for example be `/mnt/efs/.ssh/id_rsa`.

### Setup git

Run the following commands to configure your git user:

```
git config --global user.name "FIRST_NAME LAST_NAME"
git config --global user.email "MY_NAME@example.com"
```

## (Optional) Install Python virtual environment

### virtualenv, pip

To install virtualenv and pip in the new instance, run

```
sudo apt install python3.8-venv
sudo apt update
sudo apt install python3-pip
```

To create a new virtual environment, run

```
python3.8 -m venv /path/to/venv
```

### mamba

```
conda init bash
mamba create -n nameofmyenv
conda activate nameofmyenv
```
