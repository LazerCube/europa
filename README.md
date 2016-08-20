
# Requirements

## Fabric
```
sudo aptitude install fabric
```

### Using fabric

*   `fab <localhost/remote> <full_install/full_upgrade/full_upgrade>`
*   When installing for the first time you must define a django config file to use.
    In order to do this put `:"<local/production/staging>"` after the your install command.
    For Example: `fab remote full_install:"production"` to use your project with its production settings.


## SSH
```
sudo apt-get update
sudo apt-get install openssh-server
sudo ufw allow 22/2500
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


## Creating new user

```
sudo adduser django
sudo gpasswd -a django sudo
```
