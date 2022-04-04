import sys
import socket
import time
import math

def generate_test_string(packet_size):
    string = "teste de rede *2022*"
    times = math.ceil(packet_size/len(string))
    final_string = ""
    final_string = final_string.join([string]*times)
    final_string = final_string[:500]
    return bytes(final_string, 'ascii')


def udp_download_test(src_address, max_testing_time, packet_size):
    #initializing variables...
    download_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    download_socket.bind((src_address[0], src_address[1]))
    packets_received = 0

    #performing test...
    print("\nTesting download...")
    start_time = time.time()

    while True:
        bytes_read, _ = download_socket.recvfrom(packet_size)
        if bytes_read.decode() == "end":
            break
        packets_received += 1
    
    test_time = round(time.time() - start_time, 2)

    #calculating report variables...
    packets_sent, dst_address = download_socket.recvfrom(packet_size)
    packets_sent = int(packets_sent.decode())
    lost_packets = abs(packets_sent - packets_received)
    download_socket.sendto((str(lost_packets)).encode(), dst_address)
    download_socket.close()

    bits_received = packet_size * packets_received * 8
    bits_per_sec = round(bits_received / test_time)
    prefix = ''

    if bits_per_sec // 10**9 > 0:
        bits_per_sec = round(bits_per_sec / 10**9, 2)
        prefix = 'G'
    elif bits_per_sec // 10**6 > 0:
        bits_per_sec = round(bits_per_sec / 10**6, 2)
        prefix = 'M'
    elif bits_per_sec // 10**3 > 0:
        bits_per_sec = round(bits_per_sec / 10**3, 2)
        prefix = 'K'
    
    bytes_transferred = packet_size * packets_received
    b_prefix = ''
    if bytes_transferred // 10**9 > 0:
        bytes_transferred = round(bytes_transferred / 10**9, 2)
        b_prefix = 'G'
    elif bytes_transferred // 10**6 > 0:
        bytes_transferred = round(bytes_transferred / 10**6, 2)
        b_prefix = 'M'
    elif bytes_transferred // 10**3 > 0:
        bytes_transferred = round(bytes_transferred / 10**3, 2)
        b_prefix = 'K'

    # formatting result format    
    print("Test finished!")
    print("\nReport:")
    print("------------")
    print(f"\t{prefix}bits/s: {bits_per_sec}")
    print(f"\tpackets/s: {'{0:,}'.format(round(packets_received / test_time, 2)).replace(',','.')}")
    print(f"\ttotal packets transferred: {'{0:,}'.format(packets_received).replace(',','.')}")
    print(f"\ttotal bytes transferred: {'{0:,}'.format(bytes_transferred).replace(',','.')}{b_prefix}")
    print(f"\ttest time: {test_time} seg")
    print(f"\tlost packets: {lost_packets}")


def udp_upload_test(dst_address, max_testing_time, packet_size):
    #initializing variables...
    upload_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    buffer = generate_test_string(packet_size)
    packets_sent = 0

    #performing test...
    print("\nTesting upload...")
    start_time = time.time()

    while (time.time() - start_time) < max_testing_time:
        upload_socket.sendto(buffer, dst_address)
        packets_sent += 1
    
    test_time = round(time.time() - start_time, 2)
    upload_socket.sendto("end".encode(), dst_address)

    time.sleep(1)
    #calculating report variables...
    upload_socket.sendto((str(packets_sent)).encode(), dst_address)
    lost_packets, _ = upload_socket.recvfrom(packet_size) 
    lost_packets = int(lost_packets.decode())
    upload_socket.close()

    bits_sent = packet_size * packets_sent * 8
    bits_per_sec = round(bits_sent / test_time)
    prefix = ''

    if bits_per_sec // 10**9 > 0:
        bits_per_sec = round(bits_per_sec / 10**9, 2)
        prefix = 'G'
    elif bits_per_sec // 10**6 > 0:
        bits_per_sec = round(bits_per_sec / 10**6, 2)
        prefix = 'M'
    elif bits_per_sec // 10**3 > 0:
        bits_per_sec = round(bits_per_sec / 10**3, 2)
        prefix = 'K'
        
    bytes_transferred = packet_size * packets_sent
    b_prefix = ''
    if bytes_transferred // 10**9 > 0:
        bytes_transferred = round(bytes_transferred / 10**9, 2)
        b_prefix = 'G'
    elif bytes_transferred // 10**6 > 0:
        bytes_transferred = round(bytes_transferred / 10**6, 2)
        b_prefix = 'M'
    elif bytes_transferred // 10**3 > 0:
        bytes_transferred = round(bytes_transferred / 10**3, 2)
        b_prefix = 'K'

    # formatting result format    
    print("Test finished!")
    print("\nReport:")
    print("------------")
    print(f"\t{prefix}bits/s: {bits_per_sec}")
    print(f"\tpackets/s: {'{0:,}'.format(round(packets_sent / test_time, 2)).replace(',','.')}")
    print(f"\ttotal packets transferred: {'{0:,}'.format(packets_sent).replace(',','.')}")
    print(f"\ttotal bytes transferred: {'{0:,}'.format(bytes_transferred).replace(',','.')}{b_prefix}")
    print(f"\ttest time: {test_time} seg")
    print(f"\tlost packets: {lost_packets}")


def main():
    argvlen = len(sys.argv)
    if argvlen < 6:
        print(f"Invalid execution format.\nUsage: python3 {sys.argv[0]} src_ip src_port dst_ip dst_port (-d | -u)\n\t-d: download test\n\t-u: upload test")
        quit(1)

    # getting execution arguments...
    src_ip = sys.argv[1]
    src_port = sys.argv[2]
    dst_ip = sys.argv[3]
    dst_port = sys.argv[4]
    execution_mode = sys.argv[5]

    # setting configs
    max_testing_time = 20.00
    packet_size = 500

    if execution_mode == '-d':
        udp_download_test((src_ip, int(src_port)), max_testing_time, packet_size)
    elif execution_mode == '-u':
        udp_upload_test((dst_ip, int(dst_port)), max_testing_time, packet_size)
    else:
        print(f"Invalid execution format.\nUsage: python3 {sys.arg[0]} src_ip src_port dst_ip dst_port (-d|-u)\n\t-d: download test\n\t-u: upload test")
        quit(1)


if __name__ == "__main__":
    main()
