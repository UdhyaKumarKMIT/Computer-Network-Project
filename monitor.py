from scapy.all import *
import time
from collections import defaultdict
from datetime import datetime

# Dictionary to store time spent per domain
domain_time = defaultdict(lambda: {'start': None, 'total_time': 0, 'visit_count': 0})

def display_most_visited():
    while True:
        print("Most visited websites:")
        sorted_domains = sorted(domain_time.items(), key=lambda x: x[1]['visit_count'], reverse=True)
        for domain, data in sorted_domains[:5]:
            print(f"Domain: {domain}, Visits: {data['visit_count']}, Total Time: {data['total_time']} seconds")
        time.sleep(10)


def process_packet(packet):
    # Extract the DNS query for domain
    if packet.haslayer(DNS) and packet.getlayer(DNS).qr == 0:  # DNS query
        domain = packet[DNSQR].qname.decode('utf-8').strip('.')
        
        # Update visit count
        if domain_time[domain]['start'] is None:
            domain_time[domain]['start'] = datetime.now()
        domain_time[domain]['visit_count'] += 1
        
        print(f"Domain visited: {domain}")

def calculate_time_spent():
    # Continuously track time spent on domains
    while True:
        for domain, data in domain_time.items():
            if data['start']:
                now = datetime.now()
                elapsed_time = (now - data['start']).total_seconds()
                domain_time[domain]['total_time'] = elapsed_time
        
        # Sleep for a bit to avoid consuming too much CPU
        time.sleep(1)

def start_sniffing():
    # Start packet sniffing (only on port 53, DNS requests, for simplicity)
    sniff(filter="port 53", prn=process_packet, store=0)

if __name__ == "__main__":
    # Start the time tracking in a separate thread
    import threading
    time_thread = threading.Thread(target=calculate_time_spent)
    time_thread.start()
    time_thread2 = threading.Thread(target=display_most_visited)
    time_thread2.start()

    # Start sniffing packets
    start_sniffing()
    input("Press to exit")
    exit(0)