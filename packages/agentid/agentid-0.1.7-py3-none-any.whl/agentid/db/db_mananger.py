import json
import sqlite3
from cryptography.hazmat.primitives import serialization
class DBManager:
    
    def __init__(self,aid=""):
        self.conn = sqlite3.connect("agentid_data.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.aid = aid
        self._create_table()
        if self.aid != "":
            self.create_table(self.aid)
    
    def _create_table(self):
        # 身份表，TODO 需考虑加密..
        # self.cursor.execute("""DELETE FROM agentids""")
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS agentids (
            aid TEXT PRIMARY KEY, 
            ep_aid TEXT,
            ep_url TEXT,
            avaUrl TEXT,
            name TEXT,
            description TEXT)
        ''')
       
        self.conn.commit()
    
    def create_table(self,aid):
        import hashlib
        # 生成aid的MD5哈希作为表名前缀
        aid_md5 = hashlib.md5(aid.encode('utf-8')).hexdigest()
        conversation_table = f"conversation_{aid_md5}"
        messages_table = f"messages_{aid_md5}"
        chat_config_table = f"chat_config_{aid_md5}"
        # self.cursor.execute(f"DROP TABLE IF EXISTS {conversation_table}")
        
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {conversation_table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            identifying_code TEXT NOT NULL,
            main_aid TEXT NOT NULL,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        # self.cursor.execute(f"DROP TABLE IF EXISTS {messages_table}")
        
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {messages_table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,  -- 关联到对话表的id
            role TEXT NOT NULL,  -- 消息发送者,
            message_aid TEXT NOT NULL, 
            parent_message_id INTEGER,  -- 关联到父消息的id
            to_aids TEXT NOT NULL,  -- 消息发送者,
            content TEXT NOT NULL,  -- 消息内容,
            type TEXT NOT NULL,  -- 消息状态，如"sent", "received",
            status TEXT NOT NULL,  -- 消息状态，如"error", "success",
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {chat_config_table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,  
            aid TEXT NOT NULL,  
            avaurl TEXT,
            description TEXT, 
            post_data TEXT
        )''')
        self.conn.commit()
        
    
    
    def update_aid_info(self, aid, avaUrl, name, description):
        try:
            self.cursor.execute('''UPDATE agentids SET avaUrl =?, name =?, description =? WHERE aid =?''', (avaUrl, name, description, aid))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"update_aid_info数据库操作失败: {str(e)}")
            return False
    
    def create_conversation(self, aid,session_id,identifying_code,name, type,to_aid_list:list):
        try:
            self.create_table(aid)
            import hashlib
            aid_md5 = hashlib.md5(aid.encode('utf-8')).hexdigest()
            conversation_table = f"conversation_{aid_md5}"
            chat_config_table = f"chat_config_{aid_md5}"
            main_aid = to_aid_list[0]
            
            # 修正参数数量，确保5个值对应5个占位符
            self.cursor.execute(f'''INSERT INTO {conversation_table} (session_id,identifying_code,main_aid,name,type) VALUES (?,?,?,?,?)''', 
                              (session_id, identifying_code, main_aid, name, type))
            
            for to_aid in to_aid_list:
                self.cursor.execute(f'''INSERT INTO {chat_config_table} (session_id,aid,avaurl,description, post_data) VALUES (?,?,?,?,?)''', 
                                    (session_id,to_aid,"","",""))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"create_conversation数据库操作失败: {str(e)}")
    
    def insert_message(self, role,aid,conversation_id, message_aid, parent_message_id, to_aids, content, type, status):
        try:
            import hashlib
            import json
            aid_md5 = hashlib.md5(aid.encode('utf-8')).hexdigest()
            messages_table = f"messages_{aid_md5}"
            # 将json.dump改为json.dumps
            self.cursor.execute(f'''INSERT INTO {messages_table} (session_id, role,message_aid, parent_message_id, to_aids, content, type, status) VALUES (?,?,?,?,?,?,?,?)''',
                                (conversation_id, role,message_aid, parent_message_id, to_aids, content, type, status))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"insert_message数据库操作失败: {str(e)}")
    
    def load_aid(self, aid):
        try:
            self.cursor.execute('''SELECT ep_aid, ep_url,avaUrl,name,description FROM agentids WHERE aid = ?''', (aid,))
            result = self.cursor.fetchone()
            if result:
                return result[0], result[1],result[2],result[3],result[4]
            else:
                return None, None,None,None,None
        except sqlite3.Error as e:
            print(f"load_aid数据库操作失败: {str(e)}")
            return None, None,None,None,None

    def create_aid(self, aid,ep_aid = "",ep_url = "",avaUrl = "",name = "",description=""):
        try:
            # 将私钥和CSR序列化为PEM格式字符串            
            self.cursor.execute('''INSERT INTO agentids (aid, ep_aid, ep_url,avaUrl,name,description) 
                                VALUES (?,?,?,?,?,?)''', 
                                (aid, ep_aid , ep_url,avaUrl,name,description))
            self.conn.commit()
            return ""
        except sqlite3.Error as e:
            print(f"save_aid数据库操作失败: {str(e)}")
            return str(e)
            
    def update_aid(self, aid, ep_aid, ep_url):
        try:
            self.cursor.execute('''UPDATE agentids SET ep_aid =?, ep_url =? WHERE aid =?''', (ep_aid, ep_url, aid))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"update_aid数据库操作失败: {str(e)}")
            return False
    
    def get_agentid_list(self):
        try:
            self.cursor.execute('''SELECT aid FROM agentids''')
            return [row[0] for row in self.cursor.fetchall()]  # 提取每个元组的第一个元素
        except sqlite3.Error as e:
            print(f"get_agentid_list数据库操作失败: {str(e)}")
            return []

    def get_conversation_by_id(self, aid, conversation_id):
        try:
            import hashlib
            import json
            aid_md5 = hashlib.md5(aid.encode('utf-8')).hexdigest()
            conversation_table = f"conversation_{aid_md5}"
            self.cursor.execute(f'''SELECT id, session_id,identifying_code,main_aid,name,type FROM {conversation_table} WHERE id =?''', (conversation_id,))
            result = self.cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'session_id': result[1],
                    'identifying_code': result[2],
                    'main_aid': result[3],
                    'name': result[4],
                    'type': result[5]
                }
            else:
                return None
        except sqlite3.Error as e:
            print(f"get_conversation_by_id数据库操作失败: {str(e)}")
            return None
          
    def get_conversation_list(self, aid, main_aid, page=1, page_size=10):
        try:
            offset = (page - 1) * page_size
            import hashlib
            import json
            aid_md5 = hashlib.md5(aid.encode('utf-8')).hexdigest()
            conversation_table = f"conversation_{aid_md5}"
            
            self.cursor.execute(
                f'''SELECT id, session_id, identifying_code, name, type, timestamp 
                    FROM {conversation_table} 
                    WHERE main_aid = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ? OFFSET ?''', 
                (main_aid, page_size, offset))
            
            # 将查询结果转换为字典列表
            columns = ['id', 'session_id', 'identifying_code', 'name', 'type', 'timestamp']
            results = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            
            # 返回JSON格式字符串
            return results
            
        except sqlite3.Error as e:
            print(f"get_conversation_list数据库操作失败: {str(e)}")
            return []
    
    def get_conversation_messages(self, conversation_id):
        try:
            self.cursor.execute('''SELECT id, aid, content, timestamp FROM messages WHERE conversation_id =? ORDER BY timestamp ASC''', (conversation_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"get_conversation_messages数据库操作失败: {str(e)}")
            return []
    
    def get_conversation_config(self, conversation_id):
        try:
            self.cursor.execute('''SELECT id, aid, avaurl, description, post_data FROM chat_config WHERE conversation_id =?''', (conversation_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"get_conversation_config数据库操作失败: {str(e)}")
            return []

    def add_conversation_config(self, conversation_id, aid, avaurl, description, post_data):
        try:
            self.cursor.execute('''INSERT INTO chat_config (conversation_id, aid, avaurl, description, post_data) VALUES (?,?,?,?,?)''', (conversation_id, aid, avaurl, description, post_data))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"add_conversation_config数据库操作失败: {str(e)}")
            return None

    def update_conversation_config(self, config_id, avaurl, description, post_data):
        try:
            self.cursor.execute('''UPDATE chat_config SET avaurl = ?, description = ?, post_data = ? WHERE id = ?''', (avaurl, description, post_data, config_id))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"update_conversation_config数据库操作失败: {str(e)}")
            return False
    
    def get_message_list(self, aid, session_id, page=1, page_size=10):
        try:
            offset = (page - 1) * page_size
            import hashlib
            import json
            aid_md5 = hashlib.md5(aid.encode('utf-8')).hexdigest()
            messages_table = f"messages_{aid_md5}"
            
            # 修正SQL语句，移除多余的括号
            self.cursor.execute(
                f'''SELECT id, session_id,role,message_aid, parent_message_id, to_aids, content, type, status, timestamp
                    FROM {messages_table}
                    WHERE session_id = ? 
                    ORDER BY timestamp ASC LIMIT ? OFFSET ?''', 
                (session_id, page_size, offset))
            
            # 将查询结果转换为字典列表
            columns = ['id','session_id','role','message_aid', 'parent_message_id', 'to_aids', 'content', 'type', 'status', 'timestamp']
            results = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            # 返回JSON格式字符串
            return results
        except sqlite3.Error as e:
            print(f"get_message_list数据库操作失败: {str(e)}")
            return []
        # return [dict(row) for row in self.cursor.fetchall(
    