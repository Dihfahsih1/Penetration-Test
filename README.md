# Pentesting-with-Python
Various penetration testing tools and aids written in python. Based mostly on ideas and implementations presented in 'Violent Python: A Cookbook for Hackers, Forensic Analysts, Penetration Testers and Security Engineers' by TJ O'Connor and 'Black Hat Python' by Justin Seitz.

Framework branch is an attempt to create simple toolkit utility that enables use of particular tools.

## Pentesting-with-Python
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
# IP Address for the destination
# create ARP packet
arp = ARP(pdst=target_ip)
# create the Ether broadcast packet
# ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
# stack them
packet = ether/arp
Note: In case you are not familiar with the notation "/24" or "/16" after the IP address, it is basically an IP range here, for example, "192.168.1.1/24" is a range from "192.168.1.0" to "192.168.1.255", please read more about CIDR Notation.

Now we have created these packets, we need to send them using srp() function which sends and receives packets at layer 2, we set the timeout to 3 so the script won't get stuck:

result = srp(packet, timeout=3)[0]
result now is a list of pairs that is of the format (sent_packet, received_packet), let's iterate over them:

# a list of clients, we will fill this in the upcoming loop
clients = []

for sent, received in result:
    # for each response, append ip and mac address to `clients` list
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})
Now all we need to do is to print this list we have just filled:

# print clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC")
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))
Full code:

from scapy.all import ARP, Ether, srp

target_ip = "192.168.1.1/24"
# IP Address for the destination
# create ARP packet
arp = ARP(pdst=target_ip)
# create the Ether broadcast packet
# ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
# stack them
packet = ether/arp

result = srp(packet, timeout=3, verbose=0)[0]

# a list of clients, we will fill this in the upcoming loop
clients = []

for sent, received in result:
    # for each response, append ip and mac address to `clients` list
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

# print clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC")
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))
Here is a screenshot of my result in my personal network:

Result Screenshot

Alright, we are done with this tutorial, see how you can extend this and make it more convenient to replace other scanning tools.
