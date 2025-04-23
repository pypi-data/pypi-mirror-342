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
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class GroupChat:
    def __init__(self, agent_id: str, server_url: str,signature,session_id = ""):
        """心跳客户端类        
        Args:
            agent_id: 代理ID
            server_url: 服务器URL
        """
        self.agent_id = agent_id
        self.server_url = server_url
        self.signature = signature
        self.ws_thread: Optional[threading.Thread] = None
        self.msg_seq = 0
        self.session_id = session_id
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
    
    def set_session_id(self, session_id: str):
        self.session_id = session_id
        self.session_created = threading.Event()
        print(f"set_session_id: {session_id}")
        
    def set_on_message_recive(self, on_message_recive):
        self.on_message_recive = on_message_recive
    
    def __on_create_chat_group_ack(self, js):
        if "session_id" in js and "status_code" in js and "message" in js and "identifying_code" in js:
            self.session_id = js["session_id"]
            self.identifying_code = js["identifying_code"]
            if js["status_code"] == 200 or js["status_code"] == "200":
                self.session_created.set()
                print(f"create_chat_group_ack: {js}")
                return self.session_id, self.identifying_code
            else:
                print(f"create_chat_group_ack failed: {js}")
                return None, None
        else:
            print("收到的消息中不包括session_id字段，不符合预期格式")
            return None, None
        
    def __ws_handler(self):
        """
        WebSocket客户端定时发送消息函数
        :param url: WebSocket服务器URL（ws://或wss://开头）
        :param message: 要定时发送的消息内容
        :param interval: 发送间隔时间（秒），默认5秒
        """
        def on_message(ws, message):
            """接收到服务器消息时的处理函数"""
            #print(f"message_client收到消息: {message}")
            # 如果需要解析 JSON 数据，可以使用 json.loads(message)
            js = json.loads(message)
            if "cmd" not in js or "data" not in js:
                print("收到的消息中不包括cmd字段，不符合预期格式")
                return
            cmd = js["cmd"]
            if cmd == "create_chat_group_ack":
                return self.__on_create_chat_group_ack(js["data"])
            elif cmd == "chat_group_message":
                if self.on_message_recive is not None:
                    self.on_message_recive(js["data"])
                else:
                    print("on_message_recive is None")
            else:
                print(f"cmd = {cmd}")
            
        def on_error(ws, error):
            """连接发生错误时的处理函数"""
            print(f"连接错误: {error}")
            self.ws_error = error
            self.ws_connected.set()
            self.is_running = False

        def on_close(ws, close_status_code, close_msg):
            """连接关闭时的处理函数"""
            print("WebSocket 连接已关闭")
            self.is_running = False

        def on_open(ws):
            """连接建立后的处理函数，用于发送初始消息"""
            print("WebSocket 连接已建立")
            self.ws_connected.set()
            if self.last_msg is not None and self.last_receiver is not None and self.last_session_id is not None and self.last_ref_msg_id is not None:
                self.send_msg(self.last_msg, self.last_receiver, self.last_session_id, self.last_ref_msg_id)
                self.last_msg = None
                self.last_receiver = None
                self.last_session_id = None
                self.last_ref_msg_id = None

            if self.last_invite_req is not None:
                self.send_join_chat_group_req(self.last_invite_req)
                self.last_invite_req = None
                

        # 创建 WebSocket 客户端实例
        ws = websocket.WebSocketApp(
            self.ws_url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        self.ws = ws   
        # 启动WebSocket连接（阻塞当前线程）
        ws.run_forever(
            sslopt={
                "cert_reqs": ssl.CERT_NONE,       # 禁用证书验证
                "check_hostname": False           # 忽略主机名不匹配
            }
        )
    def start(self):
        if self.is_running:
            print("MessageClient is already running.")
            return
        if self.signature is None:
            print("message Sign in failed, cannot start WebSocket connection")
            return
                
        # 确保URL格式正确
        ws_url = self.server_url.rstrip('/')  # 移除末尾斜杠
        ws_url = ws_url.replace("https://", "wss://").replace("http://", "ws://")
        ws_url = ws_url + f"/chatgroup?agent_id={self.agent_id}&signature={self.signature}"
        
        print(f"message Connecting to WebSocket URL: {ws_url}")  # 调试日志
        self.ws_url = ws_url
        self.is_running = True
        self.ws_thread = threading.Thread(target=self.__ws_handler, daemon=True)
        self.ws_thread.start()
    
    def stop(self):
        if not self.is_running:
            print("message MessageClient is not running.")
            return
        self.is_running = False
        if self.ws is not None:
            self.ws.close()
        self.ws_thread.join()
        self.ws = None
        self.ws_thread = None

    def create_chat_group(self, group_name: str, subject: str, group_type: str = "public"):
        print(f"create_chat_group: {group_name}, {subject}, {group_type}")
        if not self.is_running:
            print("未建立长连接，正在建立连接...")
            self.start()
            # 等待连接结果
            self.ws_connected.wait()
            if self.ws_error is not None:
                print(f"message WebSocket连接失败: {self.ws_error}")
                return None
        try:
            print("检查WebSocket连接状态")
            if self.ws.sock and self.ws.sock.connected:  # 检查WebSocket连接状态是否正常
                data = {
                    "cmd" : "create_chat_group_req",
                    "data" : {
                        "request_id": f"{int(time.time() * 1000)}",
                        "type": f"{group_type}",
                        "group_name": f"{group_name}",
                        "subject": f"{subject}",
                        "timestamp": f"{int(time.time() * 1000)}"
                    },
                }
                msg = json.dumps(data)
                self.session_id = ""
                self.session_created = threading.Event()
                self.ws.send(msg)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 发送消息: {msg}")
                if not self.session_created.wait(timeout=1):  # 设置1秒超时
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]创建会话超时")
                    return None,None
                return self.session_id, self.identifying_code
            else:
                print(f"WebSocket连接失败")
                return None,None
        except Exception as e:
            print(f"发送消息时发生错误: {str(e)}")
            return None,None

    def close_chat_group(self, session_id: str):
        pass

    #只有有收到invite时才会加入，不能主动加放，只能在被invite时才能加入
    # def join_chat_group(self, session_id: str, invite_code: str):
    #    pass
    def send_join_chat_group_req(self, invite_req: InviteMessageReq):
        if not self.is_running:
            print("未建立长连接，正在建立连接...")
            self.start()
            # 等待连接结果
            self.ws_connected.wait()
            if self.ws_error is not None:
                print(f"WebSocket连接失败: {self.ws_error}")
                return None
            
        if self.ws is None:
            print("WebSocket connection is not established.")
            return False
        if self.ws.sock is None or not self.ws.sock.connected:
            print("WebSocket connection is not established.")
            return False
        try:
            if self.ws.sock and self.ws.sock.connected:  # 检查WebSocket连接状态是否正常
                data = {
                    "cmd" : "join_chat_group_req",
                    "data" : {
                        "session_id": invite_req.SessionId,
                        "request_id": f"{int(time.time() * 1000)}",
                        "inviter_agent_id": invite_req.InviterAgentId,
                        "invite_code": invite_req.InviteCode,
                        "last_msg_id": "0"
                    },
                }
                msg = json.dumps(data)
                self.ws.send(msg)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 发送消息: {msg}")
                return True
        except Exception as e:
            print(f"发送消息时发生错误: {str(e)}")
            return False

    def reject_invite_req(self, invite_req: InviteMessageReq):
        pass
    
    def leave_chat_group(self, session_id: str):
        pass

    def invite_member(self, acceptor_aid: str):
        if self.ws is None:
            print("WebSocket connection is not established.")
            return False
        if self.ws.sock is None or not self.ws.sock.connected:
            print("WebSocket connection is not established.")
            return False
        try:
            if self.ws.sock and self.ws.sock.connected:  # 检查WebSocket连接状态是否正常
                data = {
                    "cmd" : "invite_agent_req",
                    "data" : {
                        "session_id": self.session_id,
                        "request_id": f"{int(time.time() * 1000)}",
                        "inviter_id": self.agent_id,
                        "acceptor_id": acceptor_aid,
                        "invite_code": self.identifying_code,
                    },
                }
                msg = json.dumps(data)
                self.ws.send(msg)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 发送消息: {msg}")
                return True
        except Exception as e:
            print(f"发送消息时发生错误: {str(e)}")
            return False

    def eject_member(self,  eject_aid: str):
        if self.ws is None:
            print("WebSocket connection is not established.")
            return False
        if self.ws.sock is None or not self.ws.sock.connected:
            print("WebSocket connection is not established.")
            return False
        try:
            if self.ws.sock and self.ws.sock.connected:  # 检查WebSocket连接状态是否正常
                data = {
                    "cmd" : "eject_agent_req",
                    "data" : {
                        "session_id": f"{self.session_id}",
                        "request_id": f"{int(time.time() * 1000)}",
                        "eject_agent_id": self.agent_id,
                        "identifying_code": self.identifying_code,
                    },
                }
                msg = json.dumps(data)
                self.ws.send(msg)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 发送消息: {msg}")
                return True
        except Exception as e:
            print(f"发送消息时发生错误: {str(e)}")
            return False

    def get_member_list(self):
        if self.ws is None:
            print("WebSocket connection is not established.")
            return False
        if self.ws.sock is None or not self.ws.sock.connected:
            print("WebSocket connection is not established.")
            return False
        try:
            # SessionId       string `json:"session_id"`
            # RequestId       string `json:"request_id"`
            if self.ws.sock and self.ws.sock.connected:  # 检查WebSocket连接状态是否正常
                data = {
                    "cmd" : "get_member_list",
                    "data" : {
                        "session_id": f"{self.session_id}",
                        "request_id": f"{int(time.time() * 1000)}",
                    },
                }
                msg = json.dumps(data)
                self.ws.send(msg)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 发送消息: {msg}")
                return True
        except Exception as e:
            print(f"发送消息时发生错误: {str(e)}")
            return False

    def send_msg(self, msg: str, receiver: str, ref_msg_id : str = ""):
        if not self.is_running:
            print("未建立长连接，正在建立连接...")
            self.start()
            # 等待连接结果
            self.ws_connected.wait()
            if self.ws_error is not None:
                print(f"WebSocket连接失败: {self.ws_error}")
                return None
            
        if self.ws is None:
            print("WebSocket connection is not established.")
            return False
        if self.ws.sock is None or not self.ws.sock.connected:
            print("WebSocket connection is not established.")
            return False


        try:
            if self.ws.sock and self.ws.sock.connected:  # 检查WebSocket连接状态是否正常
                data = {
                    "cmd" : "chat_group_message",
                    "data" : {
                        "session_id": self.session_id,
                        "ref_msg_id": ref_msg_id,
                        "sender": f"{self.agent_id}",
                        "receiver": receiver,
                        "message": msg,
                        "timestamp": f"{int(time.time() * 1000)}"
                    },
                }
                msg = json.dumps(data)
                self.ws.send(msg)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 发送消息: {msg}")
                return True
            else:
                self.last_msg = msg
                self.last_receiver = receiver
                self.last_session_id = self.session_id
                self.last_ref_msg_id = ref_msg_id
                return False
        except Exception as e:
            print(f"发送消息时发生错误: {str(e)}")
            return False

    def on_recv_invite(self, invite_req):
        print(f"收到加入群聊请求：InviterAgentId={invite_req.InviterAgentId}, InviteCode={invite_req.InviteCode}, SessionId={invite_req.SessionId}, MessageServer={invite_req.MessageServer}")
        #self.last_invite_req = invite_req
        if self.signature is None:#如果没有登录，先登录
            print("====没有登录，先登录===")
            return
        self.ws_connected = threading.Event()
        self.start()
        self.ws_connected.wait(timeout=1)
        self.send_join_chat_group_req(invite_req)
