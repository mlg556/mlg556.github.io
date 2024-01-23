---
title: "Raspberry Pi Headless Setup"
date: 25 June 2019
---

This post is about how to setup your _Raspberry Pi_ in a headless configuration, so you can plug it in to your main computer and SSH into it. I will be using macOS Mojave 10.14.4 and a [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/), but most of this should work on any *\*nix* system and any relatively new Raspberry Pi.

# Installing the OS

You will first download the image file for _Raspbian_, and then burn it into an SD card (minimum of 8 GB should be fine) which your Raspberry Pi will boot from.

Here is the download page for [Raspbian OS](https://www.raspberrypi.org/downloads/raspbian/), since this is a headless setup, you will install the _Lite_ version: which is lightweight and does not have a desktop included. After downloading the `.zip` file, extract it to a `.img` and burn this disk image to the SD card using [balenaEtcher](https://www.balena.io/etcher/). You _can_ use `dd` if you want, but I have found _Etcher_ to be faster and more reliable.

# Enabling SSH and Internet Sharing

After the burning process is complete, take out the SD card and plug it again. You will see a partition named `boot` show up: we are going to edit some files here to enable SSH and the ability to share your computer's internet connection with the Raspberry Pi.

On a terminal, `cd` into this partition.

* First create an empty file named `ssh` via `touch ssh`.

* After this, open the file named `config.txt` and at the end of this file append the parameter `dtoverlay=dwc2`.

* Finally, open the file named `cmdline.txt`, and after parameter `rootwait`, add `modules-load=dwc2,g_ether`. Be careful with the spaces: the parameter  `modules-load=dwc2,g_ether` must have spaces at the beginning and the end, separating it from other parameters, but should contain no spaces itself.

Now on your Macbook, go to `System Preferences > Sharing`, enable the tick of `Internet Sharing`. When you connect your Pi, check the tick on `RNDIS/Ethernet Gadget`. It should look something like this:

![](images/internet_sharing.png)

# Enabling SSH Root Login

Now that we have enabled SSH, you can plug in the SD card to your Raspberry Pi, and connect it via USB. You can then SSH into it by `ssh pi@raspberrypi.local` with password `raspberry`. Once you are logged in you can:

* `sudo passwd root` to change the root user password.
* edit the file`/etc/ssh/sshd_config` and change `PermitRootLogin` to `yes`.

After this, reboot the machine by `sudo reboot`. Give it a few seconds to boot-up, and then SSH into the root user by `ssh root@raspberrypi.local`, entering the password you had set.

# Creating New User

Now that you have root access, you can add/remove users easily.

* First remove the default user `pi` and its home directory by `userdel -r pi`.
* Enter `useradd -m NEW_USER` to create a new user with home directory replacing `NEW_USER`.
* Enter `passwd NEW_USER` to set a password for the user.
* For some reason, the new user is initialised to use the `sh` shell. We want to change this to `bash` by `usermod --shell /bin/bash NEW_USER`
* Finally, add your new user to the `sudoers` list by `adduser NEW_USER sudo`

# Changing Device Name

The default device name is `raspberrypi`, which can cause confusion if there are multiple Pi's at play. To change this, (preferably while still logged in to the root user):

* Enter `hostname NEW_HOSTNAME` to change the hostname.
* On most systems, you also have to edit the files at `/etc/hostname` and `/etc/hosts` to reflect this change. Simply replace every `raspberrypi` with `NEW_HOSTNAME`.

# Enabling SSH Login Without Password

Since you will presumably be SSH'ing into your Pi from the same computer all the time, it becomes cumbersome after a while to enter the password. To go around this, we will create a public/private RSA keypair which will allow us to authenticate our computer to the Pi without entering the password each time.

* On your computer, and with the Pi connected, run `ssh-keygen` to generate this pair (the default path for the generated file is `~/.ssh/id_rsa`, which works just fine).

* To copy this pair to your Pi, enter `ssh-copy-id -i NEW_USER@NEW_HOSTNAME.local` for the regular user and  `ssh-copy-id -i root@NEW_HOSTNAME.local` again for the root user.

Now, you can SSH into the Pi from your computer anytime without entering the user passwords.

$\space$
