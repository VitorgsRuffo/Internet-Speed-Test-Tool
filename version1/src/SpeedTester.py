from TcpSpeedTester import TcpSpeedTester
from UdpSpeedTester import UdpSpeedTester


# classes
class SpeedTester:
    def __init__(self, src_address, dst_address, execution_mode: str):
        self.tcp_speed_tester = TcpSpeedTester(src_address, dst_address, execution_mode)
        self.udp_speed_tester = UdpSpeedTester(src_address, dst_address, execution_mode)

    def run(self):
        print("\n\nWelcome to VW internet speed test tool!\n")
        self.tcp_speed_tester.run()
        self.udp_speed_tester.run()
