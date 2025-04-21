from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography import x509
import requests
import json
import datetime
class CAClient:
    def __init__(self, ca_server, ca_port):
        self.ca_server = ca_server
        self.ca_port = ca_port
        
    def __save_csr_to_file(self, csr, filename):
        try:
            with open(filename, 'wb') as f:
                f.write(csr.public_bytes(serialization.Encoding.PEM))
            print(f"CSR 已保存到 {filename}")
        except Exception as e:
            print(f"保存 CSR 文件时出错: {e}")
            
    def __save_private_key_to_file(self, name, private_key):
        try:
            with open(f"aid/{name}/{name}.key", "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            print(f"私钥已保存到 {name}.key")  # 修改这里，使用name参数而非self.agent_id
        except Exception as e:
            print(f"保存私钥文件时出错: {e}")

    def __generate_private_key(self):
        """
        生成NIST P-384椭圆曲线私钥
        :return: 返回生成的私钥对象
        """
        # 使用SECP384R1曲线生成私钥
        private_key = ec.generate_private_key(ec.SECP384R1())
        return private_key

    def __generate_csr(self, private_key, common_name):
        """
        使用NIST P-384私钥生成证书签名请求(CSR)
        :param private_key: NIST P-384椭圆曲线私钥
        :param common_name: 证书通用名称
        :return: 返回生成的CSR对象
        """
        # 创建 CSR 的主体信息
        csr_builder = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"CN"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"SomeState"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"SomeCity"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"SomeOrganization"),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ]))

        # 添加扩展（可选）
        csr_builder = csr_builder.add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True,
        )

        # 使用私钥对 CSR 进行签名
        csr = csr_builder.sign(private_key, hashes.SHA256(), default_backend())
        return csr
    
    def send_csr_to_server(self, name):
        try:
            # 确保目录存在
            import os
            os.makedirs(f"aid/{name}", exist_ok=True)  # 确保aid/name目录存在
            
            private_key = self.__generate_private_key()
            csr = self.__generate_csr(private_key, name)
            
            csr_pem = csr.public_bytes(serialization.Encoding.PEM).decode('utf-8')
            data = {
                "id": name,
                "csr": csr_pem
            }
            print(f"{self.ca_server}/sign_cert")
            response = requests.post(f"{self.ca_server}/sign_cert", json=data, verify=False)
            print("response",response.status_code)
            if response.status_code == 200:
                # 确保目录存在后再保存文件
                if not os.path.exists(f"aid/{name}"):
                    os.makedirs(f"aid/{name}", exist_ok=True)
                    
                with open(f"aid/{name}/{name}.crt", "wb") as f:
                    print(f"{response.json()}")
                    f.write(response.json()["certificate"].encode('utf-8'))
                    self.__save_csr_to_file(csr, f"aid/{name}/{name}.csr")
                    self.__save_private_key_to_file(name, private_key)
                print(f"证书签名成功并已保存到aid/{name}/目录")
                return True
            else:
                print(f"签名失败: {response.status_code} - {response.json()['error']}")
                return response.json()['error']
        except requests.RequestException as e:
            print(f"发送签名请求时出错: {e}")
            return str(e)
    
    def __load_csr(self,agent_id):
        with open(f"aid/{agent_id}/{agent_id}.csr", "rb") as f:
            csr = x509.load_pem_x509_csr(f.read())
        # 从CSR中提取公钥
        return csr
    
    def __load_private_key(self,agent_id):
        # 加载私钥
        with open(f"aid/{agent_id}/{agent_id}.key", "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )
        return private_key

    def __load_public_key_pem(self,public_key):
        public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
        return public_key_pem

    def __load_certificate_pem(self,agent_id):
        with open(f"aid/{agent_id}/{agent_id}.crt", "rb") as f:
            certificate_pem = f.read().decode('utf-8')
        return certificate_pem
    
    def resign_csr(self,agent_id):
        # 从CSR中提取公钥
        csr = self.__load_csr(agent_id)
        public_key = csr.public_key()
        private_key = self.__load_private_key(agent_id)
        public_key_pem = self.__load_public_key_pem(public_key)

        # 加载原有的证书文件
        certificate_pem = self.__load_certificate_pem(agent_id)
            
        # 获取当前Unix时间戳(毫秒)
        current_time_ms = int(datetime.datetime.now().timestamp() * 1000)
            
        # 准备发送给服务器的数据
        data = {
            "id": agent_id,
            "request_id": f"{current_time_ms}",
            "public_key": public_key_pem
        }
            
        # 发送到服务器
        print(f"发送到服务器:"+self.ca_server + "/resign_cert")
        response = requests.post(self.ca_server + "/resign_cert", json=data, verify=False)
        if response.status_code == 200:
            print(f"{response.json()}")
            if "nonce" in response.json():
                nonce = response.json()["nonce"]
                if nonce:
                    #使用私钥对[公钥+盐]签名，以使服务器信任私钥仍然有效
                    # 使用NIST P-384私钥对nonce进行签名
                    signature = private_key.sign(
                        (public_key_pem + nonce).encode('utf-8'),
                        ec.ECDSA(hashes.SHA256())
                    )
                    csr_pem = csr.public_bytes(serialization.Encoding.PEM).decode('utf-8')
                    data = {
                        "id": agent_id,
                        "request_id": f"{current_time_ms}",
                        "public_key": public_key_pem,
                        "nonce": nonce,
                        "csr": csr_pem,
                        "cert": certificate_pem,
                        "signature": signature.hex()  # 将签名转为十六进制字符串
                    }
                       
                    # 发送到服务器

                    response = requests.post(self.ca_server + "/resign_cert", json=data, verify=False)
                    if response.status_code == 200:
            
                        entrypoint = ";"
                        if 'entrypoint' in response.json():
                            entrypoint = response.json()['entrypoint']
                        with open(f"aid/{agent_id}/{agent_id}.crt", "wb") as f:
                            f.write(response.json()["certificate"].encode('utf-8'))  # 从JSON响应中获取证书内容 
                        entrypoint_array = entrypoint.split(";")
                        return entrypoint_array[0]
                    else:
                        print(f"证书重新签名失败: {response.status_code} - {response.json().get('error', '')}")
                        return None
            else:
                print(f"公钥验证失败: {response.status_code} - {response.json().get('error', '')}")
                return None

