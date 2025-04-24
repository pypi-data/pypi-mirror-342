from typing import Dict, List, Optional, Any
import time
from openai import AsyncOpenAI
from mcp import ClientSession
from .config import Config

# 全局变量
mcp_session: Optional[ClientSession] = None
_openai_client = None

# 用户会话存储
user_sessions: Dict[str, Dict] = {}

# 按会话ID组织文件
session_files: Dict[str, Dict[str, Any]] = {}

class UserSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: List[Dict] = []
        self.created_at = time.time()
        self.last_active = time.time()

def create_user_session(session_id: str) -> UserSession:
    """创建新的用户会话"""
    session = UserSession(session_id)
    user_sessions[session_id] = session
    return session

def get_user_session(session_id: str) -> Optional[UserSession]:
    """获取用户会话"""
    return user_sessions.get(session_id)

def update_user_session(session_id: str, messages: List[Dict]):
    """更新用户会话消息"""
    if session_id in user_sessions:
        user_sessions[session_id].messages = messages
        user_sessions[session_id].last_active = time.time()

def store_file_info(session_id: str, file_info: Any):
    """存储文件信息到会话
    
    Args:
        session_id: 会话ID
        file_info: 文件信息对象
    """
    if session_id not in session_files:
        session_files[session_id] = {}
    session_files[session_id][file_info.file_id] = file_info

def get_session_files(session_id: str) -> Dict[str, Any]:
    """获取会话的文件信息
    
    Args:
        session_id: 会话ID
        
    Returns:
        Dict[str, Any]: 文件信息字典
    """
    return session_files.get(session_id, {})

def cleanup_inactive_sessions():
    """清理不活跃的会话和文件"""
    current_time = time.time()
    inactive_threshold = 86400  # 1天不活跃则清理
    
    # 清理不活跃的会话
    for session_id in list(user_sessions.keys()):
        session = user_sessions[session_id]
        if current_time - session.last_active > inactive_threshold:
            # 删除会话
            del user_sessions[session_id]
            # 删除会话相关的文件
            if session_id in session_files:
                del session_files[session_id]

def get_openai_client():
    """获取OpenAI客户端，如果不存在则创建
    
    Returns:
        OpenAI: OpenAI客户端
    """
    global _openai_client
    if _openai_client is None:
        # 验证配置
        Config.validate()
        
        # 创建OpenAI客户端
        _openai_client = AsyncOpenAI(
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.OPENAI_BASE_URL
        )
    return _openai_client

def set_mcp_session(session: ClientSession):
    """设置MCP会话"""
    global mcp_session
    mcp_session = session

def get_mcp_session() -> Optional[ClientSession]:
    """获取MCP会话"""
    return mcp_session 