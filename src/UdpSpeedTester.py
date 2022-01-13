import socket
import time

class UdpSpeedTester:
    def __init__(self, src_address, dst_address):
        self.download_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.download_socket.bind((src_address[0], int(src_address[1])))
        self.dst_address = dst_address
        self.upload_socket = None
        self.max_testing_time = 10.00
        self.packet_size = 1024


    def run_upload_test(self):
        self.upload_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.upload_socket.settimeout(0.1)
        buffer = bytes(self.packet_size)
        packets_sent = 0
        lost_packets = 0

        #synchronization...
        self.upload_socket.sendto("ok".encode(), self.dst_address)
        try:
            self.upload_socket.recvfrom(1024) 
        except:
            self.upload_socket.sendto("crash".encode(), self.dst_address)
            print("error01: could not start udp upload test due to a network problem.")
            return 

        start_time = time.time()
        print("\nTesting upload...")
        while (time.time() - start_time) < self.max_testing_time:
            self.upload_socket.sendto(buffer, self.dst_address)
            packets_sent += 1
            try:
                self.upload_socket.recvfrom(1024) 
            except:
                lost_packets += 1
        self.upload_socket.sendto("end".encode(), self.dst_address)
        self.upload_socket.close()
        self.upload_socket = None

        test_time = round(time.time() - start_time, 2)
        print("Upload finished!")
        print("\nTest report:")
        print("------------")
        print(f"\tbits/s: {round(((self.packet_size * packets_sent * 8) / test_time) / 1024, 2)}K")
        print(f"\tpackets/s: {round(packets_sent / test_time, 2)}")
        print(f"\ttotal bytes transferred: {(self.packet_size * packets_sent)/1024}K")
        print(f"\ttest time: {test_time} seg")
        print(f"\tlost packets: {lost_packets}")


    def run_download_test(self):
        packets_received = 0
        lost_packets = 0
        #synchronization...
        _, address = self.download_socket.recvfrom(1024)
        self.download_socket.sendto("ok".encode(), address)
        self.download_socket.settimeout(0.1)
        
        start_time = time.time()
        print("\nTesting download...")
        while True:
            try:
                bytes_read, address = self.download_socket.recvfrom(1024)
                if bytes_read.decode() == "end":
                    break
                elif bytes_read.decode() == "crash":
                    print("error02: could not finish udp download test due to a network problem.")
                    return 
                    
                self.download_socket.sendto("ok".encode(), address)
                packets_received += 1
            except:
                lost_packets += 1
        
        self.download_socket.close()
        test_time = round(time.time() - start_time, 2)
        print("Download finished!")
        print("\nTest report:")
        print("------------")
        print(f"\tbits/s: {round(((self.packet_size * packets_received * 8) / test_time) / 1024, 2)}K")
        print(f"\tpackets/s: {round(packets_received / test_time, 2)}")
        print(f"\ttotal bytes transferred: {(self.packet_size * packets_received)/1024}K")
        print(f"\ttest time: {test_time} seg")
        print(f"\tlost packets: {lost_packets}")
    
    
    
    def run(self, execution_type):
        if execution_type == "-df":
            self.run_download_test()
            self.run_upload_test()
        else:
            self.run_upload_test()
            self.run_download_test()
