import os
import json
import subprocess
import sys
import platform
import signal
import subprocess

PASS_FILE = os.path.expanduser("~/.throttler_passcode")

class DomainThrottler:
    def __init__(self):
        self.throttle_list = {}
        self.addon_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mitm_throttle.py")

    def check_admin_code(self):
        if not os.path.exists(PASS_FILE):
            print("No admin code set. Please create one:")
            code = input("> ").strip()
            with open(PASS_FILE, "w") as f:
                f.write(code)
            print("Admin code saved.\n")

        for attempt in range(3):
            print("Enter admin code to continue:")
            input_code = input("> ").strip()
            with open(PASS_FILE, "r") as f:
                saved_code = f.read().strip()
            if input_code == saved_code:
                print("✅ Access granted.\n")
                return
            else:
                print("❌ Invalid code.")
        
        print("Too many failed attempts. Exiting.")
        sys.exit(1)

    def reset_admin_code(self):
        print("Enter current admin code to reset:")
        input_code = input("> ").strip()
        with open(PASS_FILE, "r") as f:
            saved_code = f.read().strip()
        if input_code == saved_code:
            print("Enter new admin code:")
            new_code = input("> ").strip()
            with open(PASS_FILE, "w") as f:
                f.write(new_code)
            print("✅ Admin code reset successfully.")
            sys.exit(0)
        else:
            print("❌ Incorrect code. Exiting.")
            sys.exit(1)

    def get_user_input(self):
        print("=== SiteSloth: a Domain-based Internet Throttler ===")
        print("Enter websites to slow (comma-separated):")
        websites = input("> ").strip().split(',')

        print("\nEnter throttle speed (Kbps):")
        while True:
            speed = input("> ").strip()
            if speed.isdigit():
                speed = int(speed)
                break
            print("Please enter a valid number")

        for w in websites:
            domain = w.strip().lower()
            if domain:
                self.throttle_list[domain] = speed

    def save_config(self):
        with open("throttle_config.json", "w") as f:
            json.dump(self.throttle_list, f)
        print(f"Saved config: {self.throttle_list}")

    def launch_mitmproxy(self):
        print("\nLaunching mitmproxy (headless)...")
        proc = subprocess.Popen(
            ["mitmdump", "-s", self.addon_script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        try:
            while True:
                cmd = input("\nType 'exit', 'website', 'speed', or 'help': ").strip().lower()
                if cmd == "help":
                    print("\nAvailable commands:")
                    print("- exit   : Stop the program (requires passcode)")
                    print("- website: Change throttled websites (requires passcode)")
                    print("- speed  : Change throttle speed (requires passcode)")
                    print("- help   : Show this help message")
                    continue

                if cmd in ["exit", "website", "speed"]:
                    print(f"Enter admin code to proceed with {cmd}:")
                    input_code = input("> ").strip()
                    with open(PASS_FILE, "r") as f:
                        saved_code = f.read().strip()
                    if input_code != saved_code:
                        print("❌ Incorrect passcode.")
                        continue

                    if cmd == "exit":
                        print("✅ Passcode accepted. Exiting...")
                        proc.terminate()
                        proc.wait()
                        return

                    elif cmd == "website":
                        print("✅ Passcode accepted. Enter new websites (comma-separated):")
                        websites = input("> ").strip().split(',')
                        self.throttle_list = {w.strip().lower(): self.throttle_list[next(iter(self.throttle_list))] for w in websites if w.strip()}
                        self.save_config()
                        print("✅ Websites updated. Restarting mitmdump...")
                        proc.terminate()
                        proc.wait()
                        proc = subprocess.Popen(
                            ["mitmdump", "-s", self.addon_script],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                    elif cmd == "speed":
                        print("✅ Passcode accepted. Enter new throttle speed (Kbps):")
                        while True:
                            speed = input("> ").strip()
                            if speed.isdigit():
                                speed = int(speed)
                                break
                            print("Please enter a valid number")
                        self.throttle_list = {k: speed for k in self.throttle_list}
                        self.save_config()
                        print("✅ Speed updated. Restarting mitmdump...")
                        proc.terminate()
                        proc.wait()
                        proc = subprocess.Popen(
                            ["mitmdump", "-s", self.addon_script],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                else:
                    print("Unknown command. Type 'help' to see available commands.")
        except KeyboardInterrupt:
            print("\nCtrl+C detected. Use 'exit' command to quit.")
            self.launch_mitmproxy()

    def run(self):
        if "--reset-code" in sys.argv:
            self.reset_admin_code()
        
        self.check_admin_code()
        self.get_user_input()
        self.save_config()
        self.launch_mitmproxy()

if __name__ == "__main__":
    if platform.system() != "Windows":
        if os.geteuid() != 0:
            print("Please run with sudo (required for mitmproxy cert and proxy setup).")
            sys.exit(1)

    DomainThrottler().run()
