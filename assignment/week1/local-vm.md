# W2.4 - Local Virtual Machine Using Microsoft Hyper-V

## Overview

For this assignment, I created a local Ubuntu Server virtual machine on my Windows laptop using Microsoft Hyper-V.

Virtualization allows a physical computer to provide isolated virtual computing environments that behave like independent machines. In this exercise, Windows 10 Pro remained the host operating system while Ubuntu Server 24.04 LTS ran as the guest operating system. Hyper-V provided the abstraction between the physical CPU, memory, storage, networking, and the Ubuntu guest.

This is an example of a system virtual machine, where a complete guest operating system runs using virtualized hardware resources. This concept is also important in cloud computing because virtual machines are a core compute resource in Infrastructure as a Service (IaaS).

The goal of this exercise was to create a minimal VM, log in successfully, verify that Linux was running under Hyper-V, and document any system-specific issues I encountered.

## System Information

My host computer has the following specifications:

- Manufacturer: Dell Inc.
- Model: Dell Latitude 7480
- Host operating system: Microsoft Windows 10 Pro
- Windows version: 10.0.19045
- Processor: Intel Core i5-7200U @ 2.50 GHz
- Physical CPU cores: 2
- Logical processors: 4
- Physical memory: approximately 8 GB
- Hypervisor: Microsoft Hyper-V
- Guest operating system: Ubuntu Server 24.04 LTS

Because my laptop has only 8 GB of physical memory and a dual-core processor, I used a relatively small VM configuration so that the Windows host could remain responsive.

## Prerequisites

Before creating the VM, I verified that the following software was available:

1. Windows 10 Pro
2. Microsoft Hyper-V
3. Git Bash
4. Ubuntu Server 24.04 LTS ISO image
5. At least 20 GB of available disk space

I verified Git Bash from PowerShell with:

```powershell
Test-Path "C:\Program Files\Git\git-bash.exe"
```

The command returned:

```text
True
```

## Enable Microsoft Hyper-V

Hyper-V was already enabled on my computer.

On Windows 10 Pro, Hyper-V can be enabled using:

**Control Panel > Programs > Turn Windows features on or off > Hyper-V**

After selecting Hyper-V, Windows may require a restart.

It can also be enabled from an Administrator PowerShell terminal with:

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
```

After installation, I opened **Hyper-V Manager** from the Windows Start menu.

## Create the Ubuntu Virtual Machine

In Hyper-V Manager, I selected:

**New > Virtual Machine**

I created a VM named:

```text
ubuntu-24-04-local
```

I used the following configuration:

| Setting | Configuration |
| --- | --- |
| VM name | ubuntu-24-04-local |
| Generation | Generation 2 |
| Startup memory | 2048 MB |
| Dynamic memory | Enabled |
| Virtual processors | 1 |
| Virtual hard disk | 20 GB |
| Network | Default Switch |
| Guest OS | Ubuntu Server 24.04 LTS |

I selected these values because my Dell Latitude 7480 has approximately 8 GB of RAM and only two physical CPU cores. Assigning modest resources allowed both Windows and Ubuntu to operate without placing excessive load on the laptop.

## Install Ubuntu Server

I attached the Ubuntu Server 24.04 LTS ISO file to the virtual DVD drive and started the VM.

During the Ubuntu installation I:

1. Selected the default Ubuntu Server installation.
2. Used the 20 GB virtual hard disk created by Hyper-V.
3. Configured the hostname as `ubuntu-local`.
4. Created a local Linux user account.
5. Installed the OpenSSH server.
6. Completed the installation and rebooted the VM.

## Log In and Verify the VM

After Ubuntu restarted, I logged in with the account created during installation.

My terminal prompt appeared as:

```text
stephanie@ubuntu-local:~$
```

I verified that Linux was running inside Hyper-V using commands such as:

```bash
uname -a
lscpu
free -h
df -h
```

The `lscpu` output identified:

```text
Hypervisor vendor: Microsoft
Virtualization type: full
```

This confirmed that Ubuntu was running as a virtual machine under Microsoft Hyper-V.

## Proof of Successful Login

The screenshot below shows a successful login to the Ubuntu VM and a command executed from the Linux terminal.

![Successful Ubuntu VM Login](vm-login.png)

## System-Specific Quirks and Problems

### Limited Host Resources

My Dell Latitude 7480 has approximately 8 GB of RAM and a dual-core Intel processor. Because of this, I did not allocate a large amount of memory or CPU resources to the VM.

I used 2048 MB of startup memory, Dynamic Memory, and one virtual processor. Hyper-V later reduced the amount of memory actively assigned to Ubuntu when the VM was lightly loaded, which demonstrated how Dynamic Memory adjusts resources based on demand.

### Ubuntu Reboot Problem

After the Ubuntu installation completed, the VM initially displayed a failure message during reboot.

The Ubuntu installation ISO was still associated with the virtual DVD drive. I opened:

**Hyper-V Manager > VM Settings > SCSI Controller > DVD Drive**

and removed the ISO from the DVD drive.

I then powered the VM off and started it again. Ubuntu successfully booted from the virtual hard disk.

### Secure Boot

Because I used a Generation 2 VM, Secure Boot was enabled. For Ubuntu, the Secure Boot template can be set to:

```text
Microsoft UEFI Certificate Authority
```

### Screenshot Keyboard Capture

While the Hyper-V Virtual Machine Connection window had control of the keyboard, Windows screenshot shortcuts did not always behave normally.

I released focus from the VM and used the Windows Snipping Tool to capture the terminal instead.

## Shutting Down the VM

The VM can be shut down from Ubuntu with:

```bash
sudo shutdown now
```

A graceful shutdown is preferable to using Hyper-V's **Turn Off** option because Turn Off is similar to suddenly removing power from a physical computer.

## What I Learned

This exercise helped me understand virtualization as more than simply installing another operating system on my laptop.

My Dell Latitude 7480 provided the physical CPU, memory, disk, and network resources. Microsoft Hyper-V acted as the hypervisor and abstracted these physical resources so that Ubuntu Server could operate as an independent guest operating system.

The exercise demonstrated one of the major benefits of virtualization: multiple computing environments can use the same physical hardware while remaining logically separated. It also showed why resource allocation matters because every virtual machine ultimately shares the finite resources of the physical host.

This helped me connect local virtualization to cloud computing. Infrastructure as a Service providers use the same general idea at a much larger scale by providing virtualized compute, storage, and networking resources on demand rather than requiring every user to purchase and maintain separate physical servers.

My `lscpu` output also identified Microsoft as the hypervisor vendor and reported the virtualization type as `full`, which provided direct evidence that Ubuntu was running inside a virtualized environment.

## Contribution

If I discover an error or outdated instruction in the official Cloud Computing lecture notes, I can contribute a correction instead of creating a separate competing tutorial.

The general contribution process is:

1. Fork or obtain access to the lecture-notes repository.
2. Clone the repository locally.
3. Create a new branch for the correction.
4. Edit and test the affected documentation.
5. Commit the changes with a clear commit message.
6. Push the branch to GitHub.
7. Open a pull request explaining the problem and the proposed correction.

