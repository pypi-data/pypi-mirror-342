from inspect import signature
from numbers import Number
import requests
import datetime
import requests
from .message_serialize import InviteMessageReq
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import datetime
from cryptography.hazmat.primitives.asymmetric import ec
import websocket
import threading
import time
import ssl
import json
from typing import Callable, Optional
from agentid.group_chat import GroupChat  # 修改为从agentid包导入
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class MessageClient:
    def __init__(self, agent_id: str, server_url: str):
        """心跳客户端类        
        Args:
            agent_id: 代理ID
            server_url: 服务器URL
        """
        self.agent_id = agent_id
        self.server_url = server_url
        self.signature = None
        self.ws_thread: Optional[threading.Thread] = None
        self.msg_seq = 0
        self.session_id = ""
        self.identifying_code = ""
        self.is_running = False
        self.ws = None
        self.ws_url = ""
        self.last_invite_req = None
        self.last_msg = None
        self.last_receiver = None
        self.last_session_id = None
        self.last_ref_msg_id = None

         # 等待WebSocket连接建立或出错
        self.ws_connected = threading.Event()
        self.session_created = threading.Event()
        self.on_message_recive = None
        self.ws_error = None
        
    def set_on_message_recive(self, on_message_recive):
        self.on_message_recive = on_message_recive
    
    def sign_in(self):
        """登录方法"""
        try:
            hb_url = self.server_url + "/sign_in"
            # 获取当前Unix时间戳(毫秒)
            current_time_ms = int(datetime.datetime.now().timestamp() * 1000.0)
            
            # 准备发送给服务器的数据
            data = {
                "agent_id": f"{self.agent_id}",
                "request_id": f"{current_time_ms}",
            }
            response = requests.post(hb_url, json=data, verify=False)
            if response.status_code == 200:
                print(f"{response.json()}")
                # 加载私钥
                print(f"aid/{self.agent_id}/{self.agent_id}.key")
                with open(f"aid/{self.agent_id}/{self.agent_id}.key", "rb") as f:
                    private_key = serialization.load_pem_private_key(
                        f.read(),
                        password=None
                    )
                # 加载原有的证书文件
                with open(f"aid/{self.agent_id}/{self.agent_id}.crt", "rb") as f:
                    certificate_pem = f.read().decode('utf-8')
                # 从证书中提取公钥并转换为PEM格式
                cert = x509.load_pem_x509_certificate(certificate_pem.encode('utf-8'))
                public_key = cert.public_key()
                public_key_pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ).decode('utf-8')
                if "nonce" in response.json():
                    nonce = response.json()["nonce"]
                    if nonce:
                        #使用私钥对[盐]签名，以使服务器信任私钥仍然有效
                        signature = private_key.sign(
                            nonce.encode('utf-8'),
                            ec.ECDSA(hashes.SHA256())
                        )
                        data = {
                            "agent_id": f"{self.agent_id}",
                            "request_id": f"{current_time_ms}",
                            "nonce": nonce,
                            "public_key": public_key_pem,
                            "cert": certificate_pem,
                            "signature": signature.hex()  # 将签名转为十六进制字符串
                        }
                        #print(f"{data}")
                        # 发送到服务器
                        response = requests.post(hb_url, json=data, verify=False)
                        if response.status_code == 200:
                            rj = response.json()
                            print(f"Sign in OK: {rj}")
                                
                            if "signature" in rj:
                                self.signature = rj["signature"]
                                return True
                            else:
                                return False
                        else:
                            print(f"Sign in FAILED: {response.status_code} - {response.json().get('error', '')}")
                            return False
            else:
                print(f"Sign in failed: {response.status_code} - {response.json().get('error', '')}")
                return False
        except Exception as e:
            print(f"Sign in exception: {e}")
            return False
    
    def sign_out(self):
        """登出方法""" 
        try:
            if self.signature is None:
                print("sign_out failed: signature is None")
                return
            hb_url = self.server_url + "/sign_out"
            data = {
                "agent_id": f"{self.agent_id}",
                "signature": self.signature,
            }
            response = requests.post(hb_url, json=data,verify=False)
            if response.status_code == 200:
                print(f"sign_out ok:{response.json()}")
            else:
                print(f"sign_out failed:{response.json()}")
        except Exception as e:
            print(f"sign_out in exception: {e}")

    def create_group_chat(self,name, subject):
        if self.signature is None:
            self.sign_in()
        groupchat = GroupChat(self.agent_id, self.server_url,self.signature)
        groupchat.create_chat_group(name, subject)
        return groupchat

    def create_group_chat_with_session(self,session_id):
        if self.signature is None:
            self.sign_in()
        groupchat = GroupChat(self.agent_id, self.server_url,self.signature,session_id)
        groupchat.set_session_id(session_id)
        return groupchat
        
        
