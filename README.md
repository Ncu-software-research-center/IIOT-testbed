# Testbed

## Introduction

Testbed is a DDS (Data Distribution Service) emulator. DDS application developer can create an application prototype with QoS settings in a short time with the Testbed UI, then obtain performance result by doing emulations. With the help of Testbed, the application developer can easily understand several nonfunctional properties of their application design and adjust the design accordingly.

## Machine Requirement

Testbed system consists of 2 different sides—the **front-end** that let the user to interact
with the system’s user interface through a website, and **back-end** that will run all the
emulation experiment and record the database for the system.

* Frontend requires 1 virtual machine (requirement 1)
* 1 Backend requires 1 virtual machine (minimum requirement 1)

The following are hardware resources that can be used after the testing:

```
Host:
  CPU:  2 x Intel(R) Xeon(R) CPU  E5520  @ 2.27GHz
  CPU: 8 cores
  Memory: 16GB
  Storage: 140GB
VM:
  Memory: 1GB
  CPU: 1 core
  Storage: 10GB
```

## Installation

* [Testbed Frontend Document](./testbed_frontend/README.md)
* [Testbed Backend Document](./testbed_backend/README.md)

## Usage

* [Testbed Usage](https://github.com/Airwavess/testbed/tree/master/documents)
