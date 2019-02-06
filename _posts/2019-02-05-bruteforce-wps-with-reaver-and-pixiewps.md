---
layout: post
title:  "Brute force WPS with Reaver and pixiewps"
date:   2019-02-05 17:58:00 +0300
comments: true 
categories: [GNULinux]
---

About four years ago a security engineer by the name of [Dominique Bongard](https://twitter.com/reversity) tweeted this:

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">But I can&#39;t believe I am the first one to find this offline attack against WPS. (One try needed). <a href="http://t.co/tVmDIwftaX">pic.twitter.com/tVmDIwftaX</a></p>&mdash; Dominique Bongard (@Reversity) <a href="https://twitter.com/Reversity/status/490978005859454978?ref_src=twsrc%5Etfw">July 20, 2014</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

His words convey his surprise; imagine mine when I found out that my recently-bought router was susceptible to the very same vulnerability: which allowed the WPA key to be cracked in a matter of _seconds_. This post will show you how.

***DISCLAIMER:*** *This is merely a proof of concept for education purposes. Use it only against your own networks and devices! This post is meant to draw more attention to this still unfixed vulnerability.*

## Background

It had already been [shown](https://sviehb.files.wordpress.com/2011/12/viehboeck_wps.pdf) by [Stefan Viehböck](https://twitter.com/sviehb?lang=en) in 2011 that the [WPS](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Setup) protocol was sorely susceptible to online brute force attacks. About _11,000_ PIN guesses and about 6 hours on average were enough to gain unauthorized access to a router. To make matters worse, in 2014 Dominique Bongard published his slides on [Offline bruteforce attack on WiFi Protected Setup](http://archive.hack.lu/2014/Hacklu2014_offline_bruteforce_attack_on_wps.pdf). This offline bruteforce attack allowed the WPA to be cracked in "less than a second". To his credit, Mr. Bongard contacted various vendors about this and concluded his slide with a dire warning: _"Disable WPS now !"_


## Requirements

I will be conducting this on a [Kali GNU/Linux](https://www.kali.org) system, however it should be doable on any GNU/Linux distribution.

# WiFi adapter with monitor mode support

You will need a network adapter which supports _monitor mode_. I am using a 1st version _tp-link TL-WN722N_. You can refer to [here](https://null-byte.wonderhowto.com/how-to/buy-best-wireless-network-adapter-for-wi-fi-hacking-2019-0178550/) and [here](https://www.wirelesshack.org/best-kali-linux-compatible-usb-adapter-dongles.html) to find which dongles support this.

# Aircrack-ng

You are going to need the [Aircrack-ng](https://www.aircrack-ng.org) suite on any project assessing WiFi network security. Their [documentation](https://www.aircrack-ng.org/doku.php?id=getting_started) is really thorough and helpful. Check out the page on [Installing pre-compiled binaries](https://www.aircrack-ng.org/doku.php?id=install_aircrack#installing_pre-compiled_binaries) for installation instructions.

# Reaver

I will be using the community forked of [reaver](https://github.com/t6x/reaver-wps-fork-t6x), because it includes the offline Pixie Dust attack using the tool [pixiewps](https://github.com/wiire-a/pixiewps). Refer to individual pages for library requirements etc...

## Getting Started

Enter `airmon-ng` to list the network adapters attached to your computer. My system has two adapters attached, one is the built-in _Broadcom_ on my MacBook; and the other one is the _Atheros_ chipset in the _tp-link TL-WN722N_ WiFi adapter. I will be using the second one, `wlan1`.

![](/assets/2019-02-05-bruteforce-wps-with-reaver-and-pixiewps/mon0.png)

The command `airmon-ng start wlan1` will put the selected interface on *monitor mode*, and rename it as `wlan1mon`.

![](/assets/2019-02-05-bruteforce-wps-with-reaver-and-pixiewps/mon1.png)

# Scanning

Enter `wash -i wlan1mon` to see the WiFi access points in your range. As you can see, my router has a MAC address `E4:FB:5D:8C:4A:ED` on `Ch 1`, with the chipset vendor _Realtek_. Note that the majority of the routers around share the same chipset, which suggests that they are also vulnerable.

![](/assets/2019-02-05-bruteforce-wps-with-reaver-and-pixiewps/wash.png)

# Brute-force

Noting the _MAC address_ and the _channel_, you can initiate a *pixie dust attack* with the command:

`reaver -i wlan1mon -b E4:FB:5D:8C:4A:ED -KvvNwL -c 1`

Don't forget to replace `wlan1mon` with your monitoring mode interface, `E4:FB:5D:8C:4A:ED` with the MAC address of the router you are attacking, and `-c 1` with the channel of that router. The parameter `-K` enables the *pixie dust attack* option and the rest are just additional parameters I have found to help the procedure. You can learn more by reading the [documentation](https://github.com/t6x/reaver-wps-fork-t6x).

If luck is on your side, or the router is vulnerable, or you are just fast with the arrow up and Enter keys; the command will succeed and you will get the WPS pin. The chances are sometimes you will get stuck on the `[+] Sending EAPOL START request` phase. You can either try the command again, or maybe [change your MAC address](https://github.com/alobbs/macchanger). Also make sure to be as close as possible to the router in question.

![](/assets/2019-02-05-bruteforce-wps-with-reaver-and-pixiewps/wps.png)

After finding the WPS pin of the router (in a crazy short time like 6ms), you can now ask the router to give up its WPA key. This is done again with `reaver` by simply erasing the `-K` option for `pixiedust` and add the pin number via `-p PIN`. Noting the pin number `10666197`, executing `reaver -i wlan1mon -b E4:FB:5D:8C:4A:ED -vvNwL -c 1 -p 10666197` will yield the WPA key.

![](/assets/2019-02-05-bruteforce-wps-with-reaver-and-pixiewps/fin.png)

## Countermeasures

Apparently some vendor companies have implemented measures such as rate limiting and MAC blocking to deal with this vulnerability. The best way to check if your router suffers from this predicament is to launch the attack yourself before someone else does. The best way to prevent this attack, as Mr. Bongard warns: **_"Disable WPS now !"_**. Altough [this](https://arstechnica.com/information-technology/2012/01/hands-on-hacking-wifi-protected-setup-with-reaver/) article from _arstechnica_ suggests that disabling WPS in the UI does not always disable it:

> Having demonstrated the insecurity of WPS, I went into the Linksys' administrative interface and turned WPS off. Then, I relaunched Reaver, figuring that surely setting the router to manual configuration would block the attacks at the door. But apparently Reaver didn't get the memo, and the Linksys' WPS interface still responded to its queries—once again coughing up the password and SSID.
(...)
In a phone conversation, Craig Heffner said that the inability to shut this vulnerability down is widespread. He and others have found it to occur with every Linksys and Cisco Valet wireless access point they've tested. "On all of the Linksys routers, you cannot manually disable WPS," he said. While the Web interface has a radio button that allegedly turns off WPS configuration, "it's still on and still vulnerable."
