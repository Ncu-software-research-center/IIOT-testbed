# IIOT Testbed Backend

## Install Testbed Backend

### Install Steps
- Check Runtime Dependencies
  - DDS
  - Ubuntu Packages
  - Python3 Packages
- Configure Installation Setting
- Configure SSH Key-Based Authentication
- Install Testbed Backend to Runtime Directory
- Install Testbed Backend as Service

### Check Runtime Dependencies

### OS
OS | VERSION | BIT
:-|:-:|:-:
Ubuntu | 18.04 | 32

#### DDS
Vortex OpenSplice 6.9.0

#### Ubuntu Packages
Package | Version
-|-
make | 4.1-6
python3.7 | 3.7.3-2~18.04.1
python3-pip | 9.0.1-2.3~ubuntu1.18.04.1

To install those  packages, do:
```bash
sudo apt install make python3.7 python3-pip
```

#### Python3 Packages
Package | Version
-|-
redis | 3.1.0

To install those packages, do:
``` bash
python3.7 -m pip install redis==3.1.0
```

### Configure Installation Setting

Please modify these options in **Makefile** before you install:
- FRONTENDuser : Testbed Frontend Linux user.
- FRONTENDip : Testbed Frontend IP address.
- REDISpasswd : Redis password.

Make sure these options are correct, Testbed won't work if any of them is wrong.

Example:
```Makefile
FRONTENDuser=testbed
FRONTENDip=127.0.0.1
REDISpasswd=redis_password
```

### Install Testbed Backend to Runtime Directory
```bash
# setup OpenSplice runtime environment, please replace <OpenSplice-release.com> to correct path
source <Vortex_OpenSplice_release.com>
make install
```

### Execute Testbed Backend

After installing Testbed, the executable file will be placed in the `~/testbed/agentworker` directory. You should switch to the `~/testbed/agentworker` directory and then execute the Testbed backend using the following command:

```bash
./agent-wrap.sh
```

## Uninstall
Remove Testbed backend from **TOPdir**

```bash
make clean
```
