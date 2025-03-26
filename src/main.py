from scapy.all import sr1, IP, ICMP
import time

def scapy_ping(host):
    packet = IP(dst=host)/ICMP()  # Create an ICMP Echo Request
    
    start_time = time.time()
    response = sr1(packet, timeout=2, verbose=False)  # Send and wait for a response
    end_time = time.time()

    rtt = (end_time - start_time) * 1000

    if response:
        print(f"Reply from {host}: Time={rtt:.2f}ms")
    else:
        print(f"Request timed out for {host}")

scapy_ping("8.8.8.8")
# Ping has to run every x amount of time and store the result in database
