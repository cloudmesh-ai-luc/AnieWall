Git-ID -> AnieWall

*  Accounts: [https://piazza.com/class/mt5rkdsycb31c3/post/12]

## Week 4 Tasks (Due Sep 24, 2026, 9am)

- [x] Assignment W4.1: VM on local machine via Makefile

    - [x] Pick a local VM framework and ensure it is installed. Multipass 1.16.3 was used on Windows.
    - [x] Write a Makefile with the necessary targets to manage a single VM.
    - [x] Configure and demonstrate management of multiple machines using the configurable `NAME` variable.
    - [x] Organize local and cloud Makefiles in separate directories.
    - [x] [W4.1 Local VM Assignment](https://github.com/cloudmesh-ai-luc/AnieWall/tree/main/assignments/week4/local)

- [x] Assignment W4.2: VM on Jetstream 2

    - [x] Install the OpenStack command-line client using `pipx`.
    - [x] Configure Jetstream access through `clouds.yaml`.
    - [x] Write a Makefile with the necessary targets to manage a Jetstream VM.
    - [x] Configure and demonstrate management of multiple Jetstream VMs using the same Makefile.
    - [x] Check the work into the repository.
    - [x] [W4.2 Jetstream Assignment](https://github.com/cloudmesh-ai-luc/AnieWall/tree/main/assignments/week4/jetstream)

- [x] Assignment W4.3: VM on Chameleon Cloud

    - [x] Use the OpenStack command-line client for Chameleon Cloud.
    - [x] Install and verify `python-chi` in a Python virtual environment.
    - [x] Configure Chameleon access through `clouds.yaml`.
    - [x] Create a KVM@TACC flavor reservation for the required VM resources.
    - [x] Write a Makefile with the necessary targets to manage a Chameleon VM.
    - [x] Configure and demonstrate management of multiple Chameleon VMs using the same Makefile.
    - [x] Check the work into the repository.
    - [x] [W4.3 Chameleon Cloud Assignment](https://github.com/cloudmesh-ai-luc/AnieWall/tree/main/assignments/week4/chameleon)

- [ ] Assignment W4.4: Review Python

    - [x] Set up and use a Python virtual environment with `venv`.
    - [x] Ensure the OpenStack command-line tool is installed using `pipx`.
    - [x] Review the use of `pip install` and `pipx install`.
    - [ ] Review import statements and create a program using `os.system("ls")`.
    - [ ] Review how to create a `__main__` block.
    - [ ] Review how to write a Python function.
    - [ ] Review how to pass command-line arguments to a Python program using `click`.
    - [ ] Review running shell commands from Python using `os.system()` and `subprocess.run()`.
    - [ ] Complete the W4.4 Python review documentation.

    Did the Python review take more than 3 hours?

    - [ ] Yes
    - [ ] No

## Week 4 Self-Assessment

Assignments W4.1 through W4.3 were completed and documented in separate directories for the local Multipass, Jetstream 2, and Chameleon Cloud environments.

The local assignment demonstrated VM lifecycle automation with Multipass and a Makefile. The same Makefile was successfully used to manage more than one virtual machine by overriding the `NAME` variable.

The Jetstream assignment extended the same Makefile-based approach to an OpenStack cloud environment. OpenStack authentication was configured through `clouds.yaml`, and multiple Jetstream virtual machines were successfully managed using one Makefile.

The Chameleon assignment required additional configuration because KVM@TACC used a reservation-specific flavor. A lease was created for two `m1.small` instances, the generated reservation flavor was incorporated into the Makefile, and multiple Chameleon virtual machines were successfully created and managed. The `python-chi` package was also installed and verified in a Python virtual environment.

The most significant challenges involved configuring the OpenStack environments correctly, combining the Jetstream and Chameleon entries in `clouds.yaml`, working with Chameleon application credentials, and understanding the KVM@TACC reservation workflow. These issues were resolved through command-line verification and incremental testing before VM creation.

The Week 4 work strengthened understanding of Makefile automation, OpenStack CLI usage, cloud-specific VM configuration, virtual environments, and management of multiple virtual machines across local and cloud platforms.

Assignment W4.4 remains in progress. The virtual-environment, `pip`, and `pipx` portions have already been exercised during W4.2 and W4.3, while the remaining Python review topics will be completed separately.

## Week 3

* [x] Assignment W3.1: VM on Jetstream (Due Sep 17, 2026, 9am)
  * [x] Start a VM on Jetstream and follow the tutorial provided.
  * [x] Reviewed the tutorial; no issues requiring a pull request were identified.
  * [x] Document the activity with a screenshot of the terminal (800x600).
  * [x] [vms.md] [https://github.com/cloudmesh-ai-luc/AnieWall/blob/main/assignments/week3/vms.md]


* [x] Assignment W3.2: VM on Chameleon Cloud (Due Sep 17, 2026, 9am)
  * [x] Set your preferred time zone in Chameleon settings.
  * [x] Make sure you have a key in your `.ssh` dir on your laptop and upload the public key to Chameleon.
  * [x] Explore the portal and browse around to develop a plan first.
  * [x] Make a reservation not exceeding 1 hour.
  * [x] Start up a VM using a Chameleon Cloud image for Ubuntu 24.04 using the smallest image size possible.
  * [x] Document the activity with a screenshot of the terminal (800x600).
  * [x] [vms.md] [https://github.com/cloudmesh-ai-luc/AnieWall/blob/main/assignments/week3/vms.md]


* [ ] Assignment W3.3: OPTIONAL: VM on public cloud (Due Sep 17, 2026, 9am)
  * [ ] Optional: Create a VM on a cloud of your choice (AWS, Azure, Google) using the free tier.
  * [ ] Document with screenshots how you created your account, ensuring sensitive information is blurred out.
  * [ ] [VM.MD](https://github.com/cloudmesh-ai-luc/YOURREPO/blob/main/assignments/week3/vm.md)


* [x] Assignment W3.4: Compare (Due Sep 17, 2026, 9am)
  * [x] Compare your experience between starting a VM on your local machine vs using Chameleon Cloud.
  * [x] Put all assignment answers into: [https://github.com/cloudmesh-ai-luc/AnieWall/tree/main/assignments/week3]
  * [x] [vms.md] [https://github.com/cloudmesh-ai-luc/AnieWall/blob/main/assignments/week3/vms.md]
     
* [x] Assignment W3.5: README.md (Due Sep 17, 2026, 9am)
  * [x] LINK to README: [https://github.com/cloudmesh-ai-luc/AnieWall/blob/main/README.md]

* [x] Assignment W3.6 git from commandline
  * [x] Pull request: [https://github.com/cloudmesh-ai-luc/AnieWall/pull/2]

## Week 2
  
* [x] Assignment W2.1: Google Account, Piazza Account post cleanup (Due Sep 10, 2026, 9am)
  * [x] Locate your account post in Piazza and add your google account.
  * [x] Correct your Chameleon ID to the registered email.
  * [x] Fix your subject line to `Firstname Lastname (lucid@luc.edu)`.


* [x] Assignment W2.2: GitHub Repository (Due Sep 10, 2026, 9am)
  * [x] Verify that you can write into a file in your assigned GitHub repository.
  * [x] Put something useful into the README such as your first and last name. [https://github.com/cloudmesh-ai-luc/AnieWall/blob/main/README.md]
  * [x] Upload your public key. [Public SSH Key] [https://github.com/AnieWall.keys]


* [x] Assignment W2.3: Backup Your Computer (Due Sep 10, 2026, 9am)
  * [x] Write a one‑paragraph explanation (4–6 sentences) on why backing up a computer is important. 
  * [x] List three real‑world consequences of not having a backup.
  * [x] Choose one backup method and outline the setup steps.
  * [x] Create a weekly backup schedule (day, time, what to back up).
  * [x] Research an example from cloud computing where a missing backup strategy led to issues and write a short incident case.
  * [x] Backup Assignment [https://github.com/cloudmesh-ai-luc/AnieWall/blob/50a7978692ac9ef1374c88cd51ce5d513616db52/assignments/week2/backup.md]


* [x] Assignment W2.4: Local VM (Due Sep 10, 2026, 9am)
  * [x] Windows: Install a terminal on Windows (Git Bash/WSL). [Used Git Bash on Windows]
  * [x] Pick a hypervisor (VirtualBox, VMware, Hyper-V, Multipass). [Microsoft Hyper-V]
  * [x] Create and start a minimal VM (e.g., Ubuntu 22.04).
  * [x] Capture proof of login with a terminal screenshot (≤ 800×600 px) showing your prompt and a command.
  * [x] Write/update the tutorial in `assignments/week1/local-vm.md`
        - (Local VM Tutorial) [https://github.com/cloudmesh-ai-luc/AnieWall/blob/50a7978692ac9ef1374c88cd51ce5d513616db52/assignments/week1/local-vm.md]
  * [x] VM Login Screenshot. [https://github.com/cloudmesh-ai-luc/AnieWall/blob/50a7978692ac9ef1374c88cd51ce5d513616db52/assignments/week1/vm-login.png]


* [x] Assignment W2.5: Project proposal (Due Sep 10, 2026, 9am)
  * [x] Start working towards a project proposal and fill out administrative fields and text. [https://github.com/cloudmesh-ai-luc/AnieWall/blob/50a7978692ac9ef1374c88cd51ce5d513616db52/project.md]


# Week 1

  * [x] Assignment W1.1: What hardware do you have? (Past Due)
    - Dell Latitude 7480 laptop with an Intel Core i5-7200U 2.50 GHz dual-core processor, 8 GB RAM
  * [x] Fill out the LUC Hardware Questionnaire.
        - LUC Hardware Questionnaire: [https://docs.google.com/forms/d/e/1FAIpQLSdxxTnj8JFrrbREcM0wQ7B9nGmqpYfBPRddhKnGE7e7Dui_lA/viewform]


* [x] Assignment W1.2: Lecture review (Past Due)
  * [x] Review all sections under LECTURES -> INTRODUCTIONS and post questions on Piazza.


* [x] Assignment W1.3: Look over the assignment sections (Past Due)
  * [x] Review all sections under ASSIGNMENTS (Overview and weekly sections).


* [x] Assignment W1.4: Create class accounts (Past Due)
  * [x] Create an account on access-ci.org.
  * [x] Create an account on chameleoncloud.org.
  * [x] Set up a GitHub account.
  * [x] Post account information to Piazza under the accounts category. [https://piazza.com/class/mt5rkdsycb31c3/post/12]


* [x] Assignment W1.5: Work ahead: Refresh knowledge about Python and Linux (Past Due)
  * [x] Review optional material in the class documentation.


* [ ] Assignment W1.6: Improve the Web Site (Past Due)
  * [ ] Update errors or notify instructors throughout the semester.

