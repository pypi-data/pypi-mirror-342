from numbers import Number
import requests
import datetime
import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import datetime

from cryptography.hazmat.primitives.asymmetric import ec
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import socket
import threading
import time
from typing import Callable, Optional

from .message_serialize import *

class HeartbeatClient:
    def __init__(self, agent_id: str, server_url: str):
        """心跳客户端类       
        Args:
            agent_id: 代理ID
            server_url: 服务器URL
        """
        self.agent_id = agent_id
        self.server_url = server_url
        self.signature = None
        self.port = 0 #server_port
        self.sign_cookie = 0
        self.udp_socket = None
        self.local_ip = "0.0.0.0"
        self.local_port = 0
        self.server_ip = "127.0.0.1"
        self.heartbeat_interval = 5000
        self.is_running = False
        self.is_sending_heartbeat = False
        self.send_thread: Optional[threading.Thread] = None
        self.receive_thread: Optional[threading.Thread] = None
        self.msg_seq = 0
        self.last_hb = 0
        self.message_listener = None

    def sign_in(self):
        """登录方法"""
        try:
            print("hert Sign in to server...")
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
                #print(f"Sign in to server:{response.json()}")
                # 加载私钥
                #print(f"aid/{self.agent_id}/{self.agent_id}.key")
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
                            print(f"heart Sign in OK: {rj}")
                                
                            if "port" in rj and "sign_cookie" in rj and "signature" in rj:
                                self.server_ip = rj["server_ip"]
                                self.port = int(rj["port"])
                                self.sign_cookie = rj["sign_cookie"]
                                self.signature = rj["signature"]
                                return True
                            else:
                                return False
                        else:
                            print(f"heart Sign in FAILED: {response.status_code} - {response.json().get('error', '')}")
                            return False
            else:
                print(f"heart Sign in failed: {response.status_code} - {response.json().get('error', '')}")
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

    def set_on_recv_invite(self, listener):
        """设置消息监听器"""
        self.on_recv_invite = listener

    def _send_heartbeat(self):
        while self.is_sending_heartbeat and self.is_running:
            try:
                current_time_ms = int(datetime.datetime.now().timestamp() * 1000)  # 获取当前时间戳(毫秒)
                if current_time_ms > (self.last_hb + self.heartbeat_interval):
                    #print('发送心跳消息')
                    self.last_hb = current_time_ms
                    self.msg_seq = self.msg_seq + 1
                    req = HeartbeatMessageReq()
                    req.header.MessageMask = 0
                    req.header.MessageSeq = self.msg_seq
                    req.header.MessageType = 513
                    req.header.PayloadSize = 100
                    req.AgentId = self.agent_id
                    req.SignCookie = self.sign_cookie
                    buf = io.BytesIO()
                    req.serialize(buf)
                    data = buf.getvalue()
                    #print(f"send heartbeat {self.server_ip}")
                    self.udp_socket.sendto(data, (self.server_ip, self.port))
                time.sleep(0.001)  # 休眠1毫秒
            except Exception as e:
                print(f"Heartbeat send error: {str(e)}")

    def _receive_messages(self):
        while self.is_running:
            try:
                data, addr = self.udp_socket.recvfrom(1536)
                #print("recvFrom ok!")
                udp_header, offset = UdpMessageHeader.deserialize(data, 0)
                if udp_header.MessageType == 258:
                    hb_resp, offset = HeartbeatMessageResp.deserialize(data, 0)
                    #print(f"收到心跳回复{hb_resp.NextBeat}")
                    self.heartbeat_interval = hb_resp.NextBeat
                    if self.heartbeat_interval <= 5000:
                        self.heartbeat_interval = 5000
                elif udp_header.MessageType == 259:
                    invite_req, offset = InviteMessageReq.deserialize(data, 0)
                    if self.on_recv_invite is not None:
                        self.on_recv_invite(invite_req)
                        
                    resp = InviteMessageResp()
                    self.msg_seq = self.msg_seq + 1
                    resp.header.MessageMask = 0
                    resp.header.MessageSeq = self.msg_seq
                    resp.header.MessageType = 516
                    resp.AgentId = self.agent_id
                    resp.InviterAgentId = invite_req.InviterAgentId
                    resp.SignCookie = self.sign_cookie
                    buf = io.BytesIO()
                    resp.serialize(buf)
                    data = buf.getvalue()
                    self.udp_socket.sendto(data, (self.server_ip, self.port))

            except Exception as e:
                import traceback
                print(f"hert Receive error: {str(e)}\n完整堆栈跟踪:\n{traceback.format_exc()}")
                
                
                
    def online(self):
        """开始心跳"""
        # 创建并启动心跳线程
        if self.is_running:
            print("Already online")
            return
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((self.local_ip, self.local_port))
        # 获取绑定成功的本地地址信息
        self.local_ip, self.local_port = self.udp_socket.getsockname()
        print(f"UDP socket bound to {self.local_ip}:{self.local_port}")

        self.is_running = True
        self.is_sending_heartbeat = True
        
        self.send_thread = threading.Thread(target=self._send_heartbeat, daemon=True)
        self.receive_thread = threading.Thread(target=self._receive_messages, daemon=True)
        
        self.send_thread.start()
        self.receive_thread.start()
        print("Successfully went online")
    
    def offline(self):
        """停止心跳"""
        # TODO: 实现停止心跳逻辑
        pass
    
    def get_all_public_data(self):
        try:
            ep_url = self.server_url + "/get_all_public_data"
            data = {
                "agent_id": f"{self.agent_id}",
                "signature": self.signature,
            }
            response = requests.post(ep_url, json=data, verify=False)
            if response.status_code == 200:
                print(f"get_all_public_data ok:{response.json()}")
            else:
                print(f"get_all_public_data failed:{response.json()}")
        except Exception as e:
            print(f"get_all_public_data in exception: {e}")

    def get_entrypoint_config(self):
        try:
            ep_url = self.server_url + "/get_entrypoint_config"
            data = {
                "agent_id": f"{self.agent_id}",
                "signature": self.signature,
            }
            response = requests.post(ep_url, json=data, verify=False)
            if response.status_code == 200:
                try:
                    config = response.json()  # 添加try-catch处理JSON解析
                    print(f"get_entrypoint_config ok:{config}")
                    if 'config' in config:
                        if 'heartbeat_server' in config['config']:  # 修正层级结构
                            self.heartbeat_server = config['config']['heartbeat_server']
                        if 'message_server' in config['config']:
                            self.message_server = config['config']['message_server']
                except ValueError as e:
                    print(f"JSON解析错误: {e}, 原始响应: {response.text}")
            else:
                print(f"get_entrypoint_config failed:{response.text}")  # 显示原始响应
        except Exception as e:
            print(f"get_entrypoint_config in exception: {e}")

    def get_agent_public_data(self):
        try:
            ep_url = self.server_url + "/get_agent_public_data"
            data = {
                "agent_id": f"{self.agent_id}",
                "signature": self.signature,
            }
            response = requests.post(ep_url, json=data, verify=False)
            if response.status_code == 200:
                print(f"get_agent_public_data ok:{response.json()}")
            else:
                print(f"get_agent_public_data failed:{response.json()}")
        except Exception as e:
            print(f"get_agent_public_data in exception: {e}")

    def get_agent_private_data(self):
        try:
            ep_url = self.server_url + "/get_agent_private_data"
            data = {
                "agent_id": f"{self.agent_id}",
                "signature": self.signature,
            }
            response = requests.post(ep_url, json=data, verify=False)
            if response.status_code == 200:
                print(f"get_agent_private_data ok:{response.json()}")
            else:
                print(f"get_agent_private_data failed:{response.json()}")
        except Exception as e:
            print(f"get_agent_private_data in exception: {e}")
    def get_heartbeat_server(self):
        return self.heartbeat_server
    def get_message_server(self):
        return self.message_server
