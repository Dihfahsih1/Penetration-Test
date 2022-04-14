# Pentesting-with-Python
Various penetration testing tools and aids written in python. Based mostly on ideas and implementations presented in 'Violent Python: A Cookbook for Hackers, Forensic Analysts, Penetration Testers and Security Engineers' by TJ O'Connor and 'Black Hat Python' by Justin Seitz.

Framework branch is an attempt to create simple toolkit utility that enables use of particular tools.

## 1. Network Scanner
A network scanner is an important element for a network administrator as well as a penetration tester. It allows the user to map the network to find devices that are connected to the same network.

In this tutorial, you will learn how to build a simple network scanner using Scapy library in Python.


I will assume you already have it installed, If it isn't the case, feel free to check these tutorials:

There are many ways out there to scan computers in a single network, but we are going to use one of the popular ways which is using ARP requests.

First, we gonna need to import essential methods from scapy:

from scapy.all import ARP, Ether, srp
Second, we gonna need to make an ARP request as shown in the following image:

ARP Request
The network scanner will send the ARP request indicating who has some specific IP address, let's say "192.168.1.1", the owner of that IP address ( the target ) will automatically respond saying that he is "192.168.1.1", with that response, the MAC address will also be included in the packet, this allows us to successfully retrieve all network users' IP and MAC addresses simultaneously when we send a broadcast packet (sending a packet to all the devices in the network).

Note that you can change the MAC address of your machine, so keep that in mind while retrieving the MAC addresses, as they may change from one time to another if you're in a public network.

The ARP response is demonstrated in the following figure:

ARP Response

So, let us craft these packets:

target_ip = "192.168.1.1/24"
### IP Address for the destination
#### create ARP packet
arp = ARP(pdst=target_ip)
### create the Ether broadcast packet
#### ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
#### stack them
packet = ether/arp
Note: In case you are not familiar with the notation "/24" or "/16" after the IP address, it is basically an IP range here, for example, "192.168.1.1/24" is a range from "192.168.1.0" to "192.168.1.255", please read more about CIDR Notation.

Now we have created these packets, we need to send them using srp() function which sends and receives packets at layer 2, we set the timeout to 3 so the script won't get stuck:

result = srp(packet, timeout=3)[0]
result now is a list of pairs that is of the format (sent_packet, received_packet), let's iterate over them:

##### a list of clients, we will fill this in the upcoming loop
clients = []

for sent, received in result:
    # for each response, append ip and mac address to `clients` list
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})
Now all we need to do is to print this list we have just filled:

##### print clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC")
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))

from scapy.all import ARP, Ether, srp

target_ip = "192.168.1.1/24"
##### IP Address for the destination
##### create ARP packet
arp = ARP(pdst=target_ip)
##### create the Ether broadcast packet
##### ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
##### stack them
packet = ether/arp

result = srp(packet, timeout=3, verbose=0)[0]

##### a list of clients, we will fill this in the upcoming loop
clients = []

for sent, received in result:
    # for each response, append ip and mac address to `clients` list
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

##### print clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC")
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))
Here is a screenshot of my result in my personal network:

#### Result Screenshot
Available devices in the network:
IP                  MAC
10.10.118.1         54:7f:ee:6e:0e:fc
10.10.118.10        9c:28:f7:a8:2c:5b
10.10.118.17        c4:c5:63:02:47:c9
10.10.118.46        7c:fd:6b:1a:9c:73
10.10.118.31        dc:ef:ca:d2:fe:70
10.10.118.58        d0:1c:3c:20:0b:f3
10.10.118.47        06:e0:73:cb:4b:e3
10.10.118.125       82:48:c9:e9:20:ed
10.10.118.120       f4:d1:08:28:81:ba
10.10.118.129       42:77:3e:f0:f7:d5
10.10.118.110       e0:24:81:13:fb:c1
10.10.118.90        fe:b6:93:c4:e8:a5
10.10.118.97        10:08:b1:2e:76:d1
10.10.118.127       ee:e6:42:cf:1b:50
10.10.118.135       84:a6:c8:db:41:c4
10.10.118.29        78:3a:6c:ec:1a:cd
10.10.118.98        c4:c5:63:94:88:72
10.10.118.173       ca:68:ae:02:d3:3d
10.10.118.179       58:b1:0f:d8:79:5e
10.10.118.172       86:c2:96:37:c7:73
10.10.118.199       92:b3:12:10:ed:d8
10.10.118.162       20:26:81:02:d8:98
10.10.118.170       5a:5e:56:fb:9b:6c
10.10.118.159       90:56:fc:af:12:c7
10.10.118.189       c8:17:39:83:6e:22
10.10.118.139       d6:88:0c:ee:08:f0
10.10.118.160       d8:fc:93:8d:70:4d
10.10.118.177       b4:b6:76:2f:a7:2e
10.10.118.227       44:d9:e7:d6:50:66
10.10.118.241       66:82:7a:91:23:cb
10.10.118.202       a4:02:b9:3b:ed:18
10.10.118.234       a0:c9:a0:c1:44:2f
10.10.118.247       00:21:6a:62:e9:34
10.10.118.235       fc:aa:b6:44:21:3e

Alright, we are done with this tutorial, see how you can extend this and make it more convenient to replace other scanning tools.
