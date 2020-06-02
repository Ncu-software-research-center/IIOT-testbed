# Testbed Usage

## Introduction to IIOT Testbed

Welcome to the User’s Manual of IIOT Testbed System. This document will help user to
understand how to use all features of Testbed System Dashboard. We will begin with a
brief description of concepts that tightly correlated with the system. Then we will guide
you step by step to use the new features.

### Glossary of Terms

| ID  | Terms                            | DEFINITION                                                                                                                                                                                    |
| --- | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Testbed                          | The name of the system.                                                                                                                                                                       |
| 2   | Profile                          | A design of dataflow diagram that contains entities such as Devices, Topics, and relationships among them.                                                                                    |
| 3   | Device                           | An entity that represents any electronics equipment. In the Profile it has a role either as a Publisher or Subscriber or even both.                                                           |
| 4   | Publisher                        | An entity that produce a message.                                                                                                                                                             |
| 5   | Subscriber                       | An entity that consume a message.                                                                                                                                                             |
| 6   | Topic                            | Basic unit that define what kind of message structure exchanged between entities (Publisher-Subscriber) in DDS.                                                                               |
| 7   | Relationship                     | A relationship between a Device and a Topic. The relation could be defined as Publisher (Device ‘a’ Publish message to Topic ‘x’) or Subscriber (Device ‘b’ subscribe message to Device ‘y’). |
| 8   | Emulation                        | The experiment process that implements the profile setting with a certain data setting. This process utilizes virtual machine to represent the devices in Profile.                            |
| 9   | Requirements                     | The constraints set by the user to see the performance of certain Profile setting. Consist of loss rate and latency.                                                                          |
| 10  | Loss Rate                        | A constraint that define how many number of messages failed to be transmitted from a Publisher to Subscriber. Using percentage.                                                               |
| 11  | Latency (Time needed to deliver) | A constraint that define how many number of message can be transmitted from a Publisher to a Subscriber. Using milliseconds.                                                                  |
| 12  | Quality of Service               | A set of policies/rules about how data is shared in DDS system.                                                                                                                               |
| 13  | Data Setting                     | A set of data that define 2 parameters for profile setting which are message size (bytes) and frequency (message/seconds).                                                                    |


### Basic ideas

- **DDS** **(Data Distribution Services)**, is an important agreement for the information transmission on industrial networking, while the Prism Tech Vortex is the main leader in implementing DDS. National Central University, based on years of experience with ADLINK Technology proposed a test platform development plan for the industry’s production line in-depth study based on DDS and Prism Tech Vortex of industrial networking materials .
- **Testbed Website**, is a web application that will help creating development plan of IIoT system based on DDS.

### Goals

The system is developed to emulate the deployment of the plant and run it under different hardware parameters and software settings to find the optimal configuration under limited resources. This system has various features to support previous goals.

- **DSAL Management**, create and edit your own design of data flow diagram that represent the system plant you want to build using DSAL.
- **Emulation**, run a experiment on your DSAL setting to see the system’s performance.
- **Performance Report**, check the result of previous experiment with related performance data.

### Target Users

The users who mainly use this system would be people that have a basic understanding of DDS and its correlated concepts. Specifically, the user of this system could be divided into two types of user.

- **Factory Planner** : use this platform to understand the number of Gateway, Sensors, and the layout, whether it can meet the latency threshold or not.
- **Student** : use this platform to study how the profile setting and its correlated performance result.

---

## How to Use Testbed?

Testbed system consists of 2 different sides—the **front-end** that let the user to interact
with the system’s user interface through a website, and **back-end** that will run all the
emulation experiment and record the database for the system.

![The steps of using Testbed](https://i.imgur.com/Dk52hwf.png)

### Step 1: Login to Dashboard

![Use%20Manual/Untitled.png](https://i.imgur.com/3TMTUPa.png)

### Step 2: Create a DSAL file

![Use%20Manual/1._Click_new_button.jpg](https://i.imgur.com/RFcW56Q.jpg)

When using Testbed for the first time, there is no DSAL file stored in the system. The user must create a new DSAL file and use this DSAL file for DDS emulation. First, the user clicks on the "DSAL file" of the left section to go to the page that manages all DSAL files, and clicks "New" to enter the and edit page.

![Use%20Manual/2._select_a_template.jpg](https://i.imgur.com/I7zrQ1w.jpg)

Next, the user needs to enter the description format of the DDS emulation in the DSAL editor, and Testbed provides the Template as a reference. The user can click the Template drop-down menu and select a Template as the modified sample.

![Use%20Manual/4._Save_DSAL.jpg](https://i.imgur.com/NvUjULo.jpg)

After the user has finished editing, the DSAL file name must be entered in the upper left corner. After inputting, the user can click the "Save" button in the lower right corner to save the DSAL file.

### Step 3: Open Emulation page and load DSAL file

![Use%20Manual/5._select_a_DSAL.jpg](https://i.imgur.com/FTWAqyD.jpg)

Before performing the DDS simulation, the user must confirm that at least a DSAL file exists in the system. If there is no DSAL file established, then refer to the first step, the user needs to create a new DSAL file. After it's confirmed that there is a DSAL file, the user can click on the left "Emulation" to enter the DDS emulation setting page. First, the user clicks the drop-down menu in "Load DSAL" and selects a DSAL file stored in Testbed to be load.

![Use%20Manual/6._click_load_button.jpg](https://i.imgur.com/HhqZ0pp.jpg)

After selecting the DSAL file, the user must remember to click the "Load" button on the right to load the DSAL file selected by the user from the database.

### Step 4: Visualization

![Use%20Manual/7._DSAL_visualization.jpg](https://i.imgur.com/lBUBdFk.jpg)

After the system loads the DSAL file, it will visualize the way the DDS simulates the entity to transfer the data. The user can visually determine whether the DSAL file will be used for the DDS emulation or not.

### Step 5: Check if there have enough devices to do emulation

![Use%20Manual/Untitled%201.png](https://i.imgur.com/ldJSM5h.png)

Before performing the DDS emulation, the user has to confirm whether the Testbed backend machine that is currently waiting for the task is sufficient, and the information will be displayed at the top of the Emulation page.

### Step 6: Input emulation time and report name

![Use%20Manual/8._Input_report_name_and_emulation_time.jpg](https://i.imgur.com/HhqZ0pp.jpg)

Finally, the user needs to enter the name of the performance report stored after the DDS emulation is completed and how long the DDS emulation will take, in seconds.

### Step 7: Run emulation

![Use%20Manual/9._Click_button_to_run_emulation.jpg](https://i.imgur.com/UDQDlRz.jpg)

After clicking the button in the lower right corner, the Testbed system will begin to perform DDS emulation.

![Use%20Manual/Untitled%202.png](https://i.imgur.com/7yzuj84.png)

If the user wants to confirm the execution status of the DDS emulation task, he can click the "Taskboard" on the left corner to enter the task management page. The system will display the current status of the task, the file name reported by the system, and how long it takes for the task to be completed.

### Step 8: Check the performance report

![Use%20Manual/11._Check_Performance_report.jpg](https://i.imgur.com/TjzDekN.jpg)

After the execution is completed, the user can click the “Performance Report” button on the left to enter the Performance report page, and select the emulation execution report of the DDS to be shown.

After the user selects a DDS emulation report, the system displays the bar graph of Loss rate below, and can view the detailed report form.

![Use%20Manual/12._Check_performance_report.jpg](https://i.imgur.com/o7DRLQE.png)

### Step 9: Optimize QoS Setting

![](https://i.imgur.com/HNPWikE.png)

In the Performance report section, you can choose the optimization strategy on the left side of each Topic report. After selecting the optimization strategy, click the Optimization button in the upper right corner. The system will give QoS suggestions based on Topic based on the strategy selected by the user.

![](https://i.imgur.com/h84iLI2.png)

## How to write DSAL ?

This section will show examples of using DSAL to define DDS QoS policies, define DDS entities, define DDS communication structures, and reuse defined DDS QoS policies, as well as DDS entities, and provide a complete example of using DSAL.

1. [Define a DDS QoS policy example](./DSAL/1.%20Define%20a%20DDS%20QoS%20policy%20example.md)
2. [Defining DDS Entity Examples](./DSAL/2.%20Defining%20DDS%20Entity%20Examples.md)
3. [Example of DDS communication structure](./DSAL/3.%20Example%20of%20DDS%20communication%20structure.md)
4. [Complete DSAL example](./DSAL/4.%20Complete%20DSAL%20example.md)
