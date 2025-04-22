# Server Message Client

将一个agent连接到agent网络中把

## 安装

```bash
pip install agentid
```

## 核心方法使用说明

```python
from agentid.agentid_client import AgentIdCilent,AgentId

# 初始化AgentIdCilent
agentid_client = AgentIdCilent("CA服务器")

# 创建aid
aid_str = input("请输入申请创建的aid（name.证书服务器）: ")
is_success = agentid_client.create_aid(aid_str)
# 加载aid
agentid = agentid_client.load_aid(aid_str)
#获取aid列表
aid_list = agentid_client.get_agentid_list()

# 连接到心跳服务器
agentid.connect2entrypoint()

# 设置消息的异步回调
agentid.recive_message_async(sync_message_handler)

#设置消息的同步回调
agentid.recive_message(message_handler)

# aid 上线
agentid.online() 

```

## 功能特性

- 简单的服务器连接管理
- 自动JSON消息序列化
- 支持上下文管理器协议
- 自定义异常处理
- 线程安全

## 开发

安装开发依赖:

```bash
pip install -r requirements.txt
```

运行测试:

```bash
python -m pytest tests/
```

## 许可证

MIT