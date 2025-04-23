from calendar import c
from email import message
import json
from tokenize import group
from openai import chat
import requests
import asyncio
from agentid import message_client
from agentid.entrypoint_client import EntrypointClient
from agentid.heartbeat_client import HeartbeatClient
from agentid.message_client import MessageClient
from agentid.db.db_mananger import DBManager
from agentid.group_chat import GroupChat  # 使用完整路径导入
from dataclasses import dataclass
from typing import Literal, Optional, Union, Dict, List
import typing


@dataclass
class Artifact:
    identifier: str
    title: str
    type: Literal[
        'application/vnd.ant.code',
        'text/markdown',
        'text/html',
        'image/svg+xml',
        'application/vnd.ant.mermaid',
        'application/vnd.ant.react'
    ]
    language: Optional[str] = None

@dataclass
class AssistantMessageBlock:
    type: Literal['text','content', 'search', 'reasoning_content', 'error']
    status: Literal['success', 'loading', 'cancel', 'error', 'reading', 'optimizing']
    timestamp: int
    content: Optional[str] = None
    extra: Optional[Dict[str, Union[str, int, List[dict]]]] = None
    artifact: Optional[Artifact] = None

class AgentId:
    
    def __init__(self, agent_id: str,ep_aid:str,ep_url: str):
        self.aid = agent_id
        self.ep_aid = ep_aid
        if ep_url.startswith("http") == False:
            self.ep_url = "https://"+ep_url  # 移除末尾的杠
        else:
            self.ep_url = ep_url
        self.ep_url = "https://localhost:2222/api/entrypoint"
        self.avaUrl = ""
        self.name = ""
        self.description = ""
        self.ep = EntrypointClient(agent_id,self.ep_url)
        # self.message_client = None  # 添加消息客户端属性
        self.message_clinent = {}
        self.groupchat_map={}
        self.message_client = MessageClient(self.aid,self.ep.get_message_server())
        self.async_message_listener_func = None  # 添加消息监听器属性
        self.hbc = None
        self.s = None
        self.db_manager = DBManager(self.aid)
    
    def set_avaUrl(self,avaUrl):
        self.avaUrl = avaUrl
        return self
    
    def set_name(self,name):
        self.name = name
        return self
    
    def set_description(self,description):
        self.description = description
        return self
    
    def get_agentid_info():
        return {
            'aid':self.aid,
            'name':self.name,
            'description':self.description,
            'avaUrl':self.avaUrl,
            'ep_aid':self.ep_aid,
            'ep_url':self.ep_url,
        }
    
    def get_message_list(self,session_id,page=1, page_size=10):
        return self.db_manager.get_message_list(self.aid,session_id,page,page_size)

    def recive_message(self, listener):
        """
        设置消息监听器
        :param listener: 消息监听器函数，格式为 func(message_data)
        """
        self.message_listener_func = listener
    
    def recive_message_async(self, listener: typing.Callable[[dict], typing.Awaitable[None]]):
        """
        设置异步消息监听器
        :param listener: 异步消息监听器函数，格式为 async func(message_data: dict) -> None
        """
        if not asyncio.iscoroutinefunction(listener):
            raise TypeError("监听器必须是异步函数(async def)")
        print("设置异步消息监听器")
        self.async_message_listener_func = listener
    
    def message_listener(self, listener):
        """消息监听器装饰器"""
        self.message_listener_func = listener
        return listener

    def async_message_listener(self, listener):
        """异步消息监听器装饰器"""
        if not asyncio.iscoroutinefunction(listener):
            raise TypeError("监听器必须是异步函数(async def)")
        self.async_message_listener_func = listener
        return listener
    
    def create_chat_group(self, name, subject, to_aid_list):
        """创建与多个agent的会话
        :param name: 群组名称
        :param subject: 群组主题
        :param to_aid_list: 目标agent ID列表
        :return: 会话ID或None
        """
        print(f"创建会话开始，参与者: {to_aid_list}")
        try:
            # 确保message_client已初始化
            if self.message_client is None:
                self.message_client = MessageClient(self.aid,self.ep.get_message_server())
                self.message_client.sign_in()  # 确保登录状态                
            # 调用message_client创建群组并添加参与者
            groupchat = self.message_client.create_group_chat(name, subject)
            if groupchat is None:
                print("创建会话失败，可能是网络问题或其他错误")
                return None
            groupchat.set_on_message_recive(self.__agentid_message_listener)
            self.groupchat_map[groupchat.session_id] = groupchat
            print(f"创建会话成功，会话ID为：{groupchat.session_id}")
            self.db_manager.create_conversation(self.aid,groupchat.session_id,groupchat.identifying_code,name, "public",to_aid_list)
            return groupchat.session_id
        except Exception as e:
            import traceback
            print(f"创建会话失败: {str(e)}\n完整堆栈跟踪:\n{traceback.format_exc()}")
            return None
        
    def invite_member(self, session_id, to_aid):
        groupchat = self.groupchat_map.get(session_id)
        if self.message_client is None:
            self.message_client = MessageClient(self.aid,self.ep.get_message_server())
            self.message_client.sign_in()  # 确保登录状态
        if groupchat is not None:
            return groupchat.invite_member(to_aid)
            
        
    
    def get_conversation_list(self,aid,main_aid,page,page_size):
        return self.db_manager.get_conversation_list(aid,main_aid,page,page_size)


    
    def send_message(self, aid, to_aid_list: list, sessionId: str, message: Union[AssistantMessageBlock, list[AssistantMessageBlock], dict]):
        if sessionId == "":
            return False
            
        # 处理对象转换为字典
        if isinstance(message, (AssistantMessageBlock, dict)):
            message_data = message.__dict__ if hasattr(message, '__dict__') else message
        elif isinstance(message, list):
            message_data = [msg.__dict__ if hasattr(msg, '__dict__') else msg for msg in message]
        groupchat = self.groupchat_map.get(sessionId)
        if self.message_client != None:
            groupchat.send_msg(json.dumps(message_data), to_aid_list[0], "")
            self.db_manager.insert_message(
                "user", self.aid, sessionId, self.aid, "", 
                to_aid_list[0], json.dumps(message_data), "text", "sent"
            )
            return True
        else:
            print("消息发送失败")
            return False
    
    def connect2entrypoint(self):
        """连接到接入点服务器"""
        self.ep.sign_in()
        #实现连接逻辑
        return self.ep
    
    def connect2entrypoint_other_url(self,server_url: str):
        """连接到接入点服务器"""
        self.ep = EntrypointClient(self.aid,server_url)
        self.ep.sign_in()
        # 实现连接逻辑
        return self.ep
    
    def __heart_message_listener(self, invite_req):
        print("心跳服务器监听到新消息")
        # 使用pprint打印格式化信息
        from pprint import pprint
        print("收到邀请请求详细信息:")
        pprint(vars(invite_req) if hasattr(invite_req, '__dict__') else invite_req)
        # 使用对象属性访问而不是字典下标
        session_id = invite_req.SessionId if hasattr(invite_req, 'SessionId') else None
        groupchat = self.groupchat_map.get(session_id)
        if groupchat is None:
            groupchat = self.message_client.create_group_chat_with_session(session_id)
            print("李文江收到消息:"+session_id)
            self.groupchat_map[session_id] = groupchat
        groupchat.on_recv_invite(invite_req)
        groupchat.set_on_message_recive(self.__agentid_message_listener)
    
    def __agentid_message_listener(self, data):
        print("消息服务器监听到新消息")
        print(data)
        session_id = data["session_id"]
        message_id = data["message_id"]
        if "name" in data:
            name = data["name"]
        else:
            name = ""
        
        sender = data["sender"]
        receiver = data["receiver"]
        print("json化message")
        message = json.loads(data["message"]) if isinstance(data["message"], str) else data["message"]
        print(message)
        if isinstance(message, list):
            self.__insert_group_chat(self.aid,session_id,"",name)
            self.db_manager.insert_message("assistant",self.aid,session_id,sender, message_id, receiver, data["message"], "text", "success")
        else:
            message_list = []  # 修改变量名避免与内置list冲突
            message_list.append(message)
            self.__insert_group_chat(self.aid,session_id,"",name)
            self.db_manager.insert_message("assistant",self.aid,session_id,sender, message_id, receiver, json.dumps(message_list), "text", "success")
        print("新消息插入数据库成功.........")
        if hasattr(self, 'async_message_listener_func'):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.async_message_listener_func(data))
                loop.close()
            except Exception as e:
                import traceback
                print(f"异步消息处理异常: {str(e)}\n完整堆栈跟踪:\n{traceback.format_exc()}")
        elif hasattr(self, 'message_listener_func'):
            try:
                self.message_listener_func(data)
            except Exception as e:
                import traceback
                print(f"消息处理异常: {str(e)}\n完整堆栈跟踪:\n{traceback.format_exc()}")
    
    def __insert_group_chat(self,aid,session_id,identifying_code,name):
        conversation =  self.db_manager.get_conversation_by_id(aid,session_id)
        if conversation is None:
            # identifying_code,name, type,to_aid_list
            self.db_manager.create_conversation(aid,session_id,identifying_code,name,"public",[])
        return
                
    def online(self):
        if self.ep == None:
            print("请先连接到接入点服务器")
            return False
        if self.hbc != None:
            self.hbc.offline()
            self.hbc.sign_out()
        
        self.ep.get_entrypoint_config()
        print("连接到心跳服务器:"+self.aid)
        self.hbc = HeartbeatClient(self.aid,self.ep.get_heartbeat_server())
        self.hbc.set_on_recv_invite(self.__heart_message_listener)
        if self.hbc.sign_in():
            self.hbc.online()
    
    def offline(self):
        """离线状态"""
        if self.hbc != None:
            self.hbc.offline()
            self.hbc.sign_out()