import pyshark
capture = pyshark.LiveCapture(interface='Ethernet', use_json=True)

for i in capture:
    print(i.dns.qry.name)