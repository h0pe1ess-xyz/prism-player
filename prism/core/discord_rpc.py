import sys
import struct
import json
import time
import socket
import os
import uuid

class DiscordRPC:
    def __init__(self, client_id):
        self.client_id = client_id
        self.sock = None
    
    def connect(self):
        if sys.platform == 'linux' or sys.platform == 'darwin':
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            paths = [
                os.environ.get('XDG_RUNTIME_DIR', '/tmp') + '/discord-ipc-0',
                '/run/user/' + str(os.getuid()) + '/discord-ipc-0',
                '/run/user/' + str(os.getuid()) + '/snap.discord/discord-ipc-0',
                '/tmp/discord-ipc-0'
            ]
            for path in paths:
                if os.path.exists(path):
                    try:
                        self.sock.connect(path)
                        self.handshake()
                        return True
                    except Exception:
                        pass
        return False
    
    def send_payload(self, op, payload):
        if not self.sock: return
        payload_json = json.dumps(payload).encode('utf-8')
        header = struct.pack('<II', op, len(payload_json))
        try:
            self.sock.sendall(header + payload_json)
        except:
            self.sock = None
            
    def handshake(self):
        self.send_payload(0, {'v': 1, 'client_id': self.client_id})
        try:
            self.sock.recv(1024)
        except:
            pass
            
    def set_activity(self, state, details, start_timestamp=None):
        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": os.getpid(),
                "activity": {
                    "state": state,
                    "details": details,
                    "timestamps": {"start": int(start_timestamp)} if start_timestamp else {},
                    "assets": {
                        "large_image": "default",
                        "large_text": "Prism Player"
                    }
                }
            },
            "nonce": str(uuid.uuid4())
        }
        self.send_payload(1, payload)

# You can replace this with your own Discord Application ID
# Go to https://discord.com/developers/applications to create one
CLIENT_ID = '123456789012345678' 
rpc = DiscordRPC(CLIENT_ID)

def update_presence(title, artist, elapsed):
    global rpc
    if not rpc.sock:
        rpc.connect()
    if rpc.sock:
        start_ts = time.time() - elapsed
        rpc.set_activity(state=artist, details=title, start_timestamp=start_ts)

def clear_presence():
    global rpc
    if rpc.sock:
        rpc.send_payload(1, {
            "cmd": "SET_ACTIVITY",
            "args": {"pid": os.getpid()},
            "nonce": str(uuid.uuid4())
        })
