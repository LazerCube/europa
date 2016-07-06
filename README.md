
# Requirements

## Fabric
```
sudo aptitude install fabric
```

### Using fabric

```
fab <localhost/remote> <full_install/full_upgrade/full_upgrade>
```

## SSH
```
sudo apt-get update
sudo apt-get install openssh-server
sudo ufw allow 25000
```

### Configure SSH

Begin by opening the configuration file with your text editor as root:

```
nano /etc/ssh/sshd_config
```


#### Change default port
Then, change default port number.
```
Port 22
```
**After**
```
Port 25000
```


#### Disable root login
Next, we need to find the line that looks like this:

**Before**
```
PermitRootLogin yes
```
**After**
Modify this line to "no" like this to disable root login:

```
PermitRootLogin no

```

#### Reload SSH
```
service ssh restart
```
