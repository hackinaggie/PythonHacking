import scapy.all as scapy
from scapy_http import http
import optparse


def get_input():
    parse_ob = optparse.OptionParser()
    parse_ob.add_option("-i", "--interface", dest="interface", help="Interface to use")

    options = parse_ob.parse_args()[0]
    if not options.interface:
        print("Enter an interface!\nExample: -i eth0")
        exit(1)
    else:
        return options


def listen_packets(interface):
    # prn = callback fxn,
    scapy.sniff(iface=interface, store=False, prn=analyze_packets)

def analyze_packets(packet):
    # packet.show()
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)


intFace = get_input().interface
listen_packets(intFace)