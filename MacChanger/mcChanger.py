import subprocess
import optparse
import re  #how we work with regular expressions in python

def get_user_input():
    parse_ob = optparse.OptionParser()
    parse_ob.add_option("-i", "--interface", dest="interface", help="Interface to change")
    parse_ob.add_option("-m", "--mac", dest="inp", help="Desired MAC address")
    return parse_ob.parse_args()


def change_mac_address(interface, inp):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", inp])
    subprocess.call(["ifconfig", interface, "up"])


def control_new_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    newMac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))

    if newMac:
        return newMac.group(0)
    else:
        return None


(inputs, args) = get_user_input()
mac = inputs.inp
face = inputs.interface

change_mac_address(face, mac)
finalMac = control_new_mac(face)

if finalMac == mac:
    print("Success! New MAC address is: " + mac )
else:
    print("ERROR: Try a new address")
