import subprocess
import os
from pathlib import Path

class MotionCaller:
    def __init__(self):
        # 获取TcpClient的绝对路径
        self.bin_path = str(Path(__file__).parent / "bin" / "TcpClient")
        if not os.path.exists(self.bin_path):
            raise FileNotFoundError(f"TcpClient binary not found at {self.bin_path}")

    def send_command(self, ip: str, port: int, command: str, timeout: str) -> str:
        try:
            result = subprocess.run(
                [self.bin_path, ip, str(port), command, str(timeout)],
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command failed: {e.stderr}")
    def run_check(self):
        print("cordymotioncaller installed.")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="Server IP address")
    parser.add_argument("port", help="Server port", type=int)
    parser.add_argument("command", help="Command to send")
    parser.add_argument("timeout", help="Connection timeout(ms)")
    args = parser.parse_args()

    client = MotionCaller()
    print(client.send_command(args.ip, args.port, args.command, args.timeout))

if __name__ == "__main__":
    main()