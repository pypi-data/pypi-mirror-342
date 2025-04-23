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

class EntrypointClient:
    
    def __init__(self, agent_id: str, server_url: str):
        """心跳客户端类        
        Args:
            agent_id: 代理ID
            server_url: 服务器URL
        """
        self.agent_id = agent_id
        self.server_url = server_url
        self.signature = None
        self.heartbeat_server = ""
        self.message_server = ""
   
    def sign_in(self):
        """登录方法"""
        try:
            hb_url = self.server_url + "/sign_in"
            print(f"Sign in to {hb_url}")
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
                with open(f"aid/{self.agent_id}/{self.agent_id}.key", "rb") as f:
                    private_key = serialization.load_pem_private_key(
                        f.read(),
                        password=None
                    )
                #加载原有的证书文件
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
    
    def post_public_data(self,json_path):
        try:
            import json
            with open(json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            ep_url = self.server_url + "/post_agent_public_data"
            data = {
                "agent_id": f"{self.agent_id}",
                "signature": self.signature,
                "data": data,
            }
            response = requests.post(ep_url, json=data, verify=False)
            if response.status_code == 200:
                print(f"post_public_data ok:{response.json()}")
            else:
                print(f"post_public_data failed:{response.json()}")
        except Exception as e:
            print(f"post_public_data in exception: {e}")

    def post_private_data(self, data):
        try:
            ep_url = self.server_url + "/post_agent_private_data"
            data = {
                "agent_id": f"{self.agent_id}",
                "signature": self.signature,
                "data": data,
            }
            response = requests.post(ep_url, json=data, verify=False)
            if response.status_code == 200:
                print(f"post_private_data ok:{response.json()}")
            else:
                print(f"post_private_data failed:{response.json()}")
        except Exception as e:
            print(f"post_private_data in exception: {e}")
            
    
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
            print(f"get_entrypoint_config:{ep_url}")
            data = {
                "agent_id": f"{self.agent_id}",
                "signature": self.signature,
            }
            response = requests.post(ep_url, json=data, verify=False)
            if response.status_code == 200:
                try:
                    config = response.json()
                    if isinstance(config.get('config'), str):  # 处理config是字符串的情况
                        import json
                        config['config'] = json.loads(config['config'])
                    if 'config' in config:
                        if 'heartbeat_server' in config['config']:
                            self.heartbeat_server = config['config']['heartbeat_server']
                            print(f"heartbeat_server:{self.heartbeat_server}")
                        if 'message_server' in config['config']:
                            self.message_server = config['config']['message_server']
                            print(f"heartbeat_server:{self.message_server}")
                except (ValueError, AttributeError) as e:
                    print(f"JSON解析错误: {e}, 原始响应: {response.text}")
            else:
                print(f"get_entrypoint_config failed:{response.json()}")
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