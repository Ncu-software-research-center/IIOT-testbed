# IIOT Testbed

## Build from source

### Build Steps
- Check Build Dependencies
  - DDS
  - Ubuntu Packages
  - Googletest(Optional)
- Configure Build Options 
- Build Testbed Backend
- Build and Run Unittests

### OS Requirement
OS | VERSION | BIT
:-|:-:|:-:
Ubuntu | 18.04 | 32

### Check Build Dependencies

#### DDS
Vortex OpenSplice 6.9.0

#### Ubuntu Packages
Package | Version
-|-
build-essential | 12.1ubuntu2
libjsoncpp-dev | 1.7.2-1

To install those packages, do:
```bash
sudo apt install build-essential libjsoncpp-dev
```

#### Googletest(Optional)
This one is only require if you wish to run unittests.

To install this package, do:
```bash
sudo apt install cmake
git clone https://github.com/google/googletest.git && mkdir -p googletest/buld
cd googletest/build
cmake .. && make && sudo make install
```

### Configure Build Options: 

Please modify these options in **Makefile** before you build:
- TOPdir : Top directory of Testbed in runtime.

Example:
```Makefile
TOPdir=${HOME}
```

### Build Testbed Backend

```bash
# setup OpenSplice runtime environment, please replace <OpenSplice-release.com> to correct path
source <Vortex_OpenSplice_release.com>
make
```

After build finished, **release** folder and **build** folder will be created.

Contents in **build** folder, including:
- all files needed in build phase.
- object files created after build.

Contents in **release** folder, including:
- emulation : a program used to emulate DDS communication
- agentworker : a service used to receive job from Testbed frontend and do emulation.
- Makefile : a file used to install/uninstall Testbed backend

### Build and Run Unittest
You can do the following unitests:

- test: Test all unitests
- test_dds: Test dds entities and dds qos policies.
- test_loader: Test configuration loader.
- test_loss_rate: Test DDS message loss rate.
- test_measure: Test latency measurement.
- test_monitor: Test resource monitoring tool.
- test_saver: Test emulation report saver.

```bash
source <Vortex_OpenSplice_release.com>
make <test_target>

# example
make test_loss_rate
```

## Remove Build results
Remove **build** folder and **release** folder

```bash
make clean
```
