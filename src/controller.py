import os
import json
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.auth.keygen import keygen

KEY_PATH = "data/adbkey"
KEY_EVENTS = "data/key_events.json"
TV_IP = "192.168.0.12"


class Controller:
    def __init__(self):
        if not self.load_key():
            self.gen_key()
            self.load_key()
        self.load_events()

    def load_events(self, path=KEY_EVENTS):
        """
        Load in the event dictionary
        """
        if not os.path.isfile(path):
            print(f"No key event file found at {path}")
        with open(path) as file:
            self.events = json.load(file)

    def load_key(self, path=KEY_PATH):
        """
        Load a key from the path provided,
        returns true if a key was found and false if not
        """
        if not os.path.isfile(path):
            print(f"No private key found")
            return False

        if not os.path.isfile(path + ".pub"):
            print(f"No public key found")
            return False

        with open(path) as file:
            private = file.read()
        with open(path + ".pub") as file:
            public = file.read()

        self.credentials = PythonRSASigner(public, private)
        print(f"Successfully loaded key at {path}")
        return True

    def gen_key(self, path=KEY_PATH):
        """
        Generate a key at the desired path
        """
        print(f"Generating new key at {path}")
        keygen(path)

    def connect(self, device_ip, port=5555):
        self.device = AdbDeviceTcp(device_ip, port, default_transport_timeout_s=10)

        try:
            self.device.close()
        except:
            print(f"There was an issue to connecting to the device at {device_ip}")
        else:
            self.device.connect(rsa_keys=[self.credentials], auth_timeout_s=10)
            print(f"Connected to device at {device_ip}")

        return self.device

    def key_event_by_id(self, id):
        command = bytes(f"input keyevent {id}", "utf-8")
        self.device._service(b"shell", command)
        # print()

    def key_event(self, key):
        self.key_event_by_id(self.events["key_events"][key])


def main():
    controller = Controller()
    ## run this as mainfile to test commands
    # controller.connect(TV_IP)
    # controller.key_event("key_mute")
    # controller.key_event("key_captions")


if __name__ == "__main__":
    main()
