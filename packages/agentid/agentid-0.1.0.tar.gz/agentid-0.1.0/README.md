# Server Message Client

一个简单的Python库，用于连接连接Au互联网络的库

## 安装

```bash
pip install server-message
```

## 使用示例

```python
from server_message import MessageClient

# 使用上下文管理器自动管理连接
with MessageClient(host='example.com', port=8080) as client:
    client.send_message({
        'type': 'alert',
        'content': '系统警告信息',
        'priority': 'high'
    })
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