import scapy.all as scapy
import optparse

# steps:
#   1) arp request
#   2) broadcast
#   3) response

# scapy.ls(scapy.ARP()) prints the attributes of any scapy method
#   we used on ARP & Ether to know what args to specify, like pdst & dst


def get_input():
    parse_ob = optparse.OptionParser()
    parse_ob.add_option("-r", "--range", dest="ipRange", help="Desired IP range to scan.")

    (user_input, args) = parse_ob.parse_args()

    if not user_input.ipRange:
        print("Enter an ip range to scan like -r 33.33.33.1/24")
        exit(1)
    return user_input.ipRange


def scan_process(ip_range):
    # range to scan
    arp_request_packet = scapy.ARP(pdst=ip_range)

    # what to broadcast
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    # combine both packets, this is specified in the scapy docs
    combined_packet = broadcast_packet / arp_request_packet
    # actually broadcast it and assign result to tuple
    (answered_list, unanswered_list) = scapy.srp(combined_packet, timeout=1)

    # scapy defined function to display results prettily to user
    answered_list.summary()


# main
ip_range = get_input()
scan_process(ip_range)
