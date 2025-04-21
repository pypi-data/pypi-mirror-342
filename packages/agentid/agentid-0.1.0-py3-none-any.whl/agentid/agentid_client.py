from datetime import date
import socket
import json
import string

from agentid.db.db_mananger import DBManager

from agentid.agentid import AgentId
from .ca_client import CAClient


class AgentIdCilent:
    """
    agentid客户端
    用于创建aid，加载aid,获取aid授权列表,管理aid
    示例用法:
    """
    def __init__(self, ca_server='https://localhost:2200/api/ca', timeout=10):
        """
        初始化客户端
        :param ca_server: 证书服务器地址(必须包含http://或https://)
        :param timeout: 连接超时时间(秒)
        """
        # 确保ca_server以http://或https://开头
        if not ca_server.startswith(('http://', 'https://')):
            ca_server = 'http://' + ca_server
        self.ca_server = ca_server.rstrip('/')  # 移除末尾的斜杠
        self.timeout = timeout
        self.ca_client = CAClient(ca_server, timeout)
        self.db_manager = DBManager()
        
    def get_agentid_list(self):
        list = self.db_manager.get_agentid_list()
        return list
    
    def update_aid_info(self, aid, avaUrl, name, description):
        self.db_manager.update_aid_info(aid, avaUrl, name, description)
        return True
    
    def load_aid(self, agent_id: string):
        try: 
            print(f"尝试加载agent_id: {agent_id}")  # 打印尝试加载的agent_id，调试用
            result = self.db_manager.load_aid(agent_id)
            if not result or len(result) < 2:  # 检查返回结果是否有效
                print(f"未找到agent_id: {agent_id} 或数据不完整")
                return None
            print(f"加载agent_id: {agent_id} 成功")  # 打印成功信息，调试用
            print(result)
            ep_aid, ep_url = result[0], result[1]  # 安全获取前两个值
            avaUrl = result[2] if len(result) > 2 else ""
            name = result[3] if len(result) > 3 else ""
            description = result[4] if len(result) > 4 else ""
            
            if ep_aid and ep_url:
                return AgentId(agent_id, ep_aid, ep_url)
                
            ep_url = self.ca_client.resign_csr(agent_id)
            if ep_url:
                self.db_manager.update_aid(agent_id, "ep_aid", ep_url)
                agentid = AgentId(agent_id, "ep_aid", ep_url)
                agentid.set_avaUrl(avaUrl)
                agentid.set_name(name)
                agentid.set_description(description)
                return agentid
        except Exception as e:
            print(f"加载和验证密钥对时出错: {str(e)}")
            return None
    
    def create_aid(self,aid):
        """连接到服务器"""
        # 生成 Ed25519 私钥
        print("向服务端申请创建aid")
        result = self.ca_client.send_csr_to_server(aid)
        if result == True:
            return self.db_manager.create_aid(aid)
        return result
            
    def connect2entryport(self, agentid:AgentId, entryport: string):
        """通过connect2entrypoint可以连接到任何接入服务器,将验证你的身份"""
        return
    
    def send_message(self, agentid: AgentId, message: dict):
        """
        发送消息到指定的agentid
        :param agentid: AgentId对象
        :param message: 消息字典
        :return: 发送成功返回True，失败返回False
        """
        try:
            # 连接到服务器 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.ca_server, 5001))  # 连接到服务器端口5001
                s.settimeout(self.timeout)  # 设置超时时间
                # 发送消息
                s.sendall(json.dumps(message).encode())
                # 接收服务器响应
                response = s.recv(1024).decode()
                if response == "OK":
                    return True
                else:
                    return False
        except socket.error as e:
            raise ServerConnectionError(f"连接到服务器失败: {e}")
    
