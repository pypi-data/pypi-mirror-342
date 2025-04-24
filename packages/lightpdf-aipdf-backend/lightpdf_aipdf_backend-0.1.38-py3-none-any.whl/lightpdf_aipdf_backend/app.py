from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from contextlib import asynccontextmanager
from typing import List, Optional
from uuid import uuid4
import json

from .models import ChatRequest, Message, FileInfo
from .file_handler import handle_batch_file_upload
from .chat_handler import process_messages, generate_chat_response
from .utils import async_generator_to_json_stream
from .state import cleanup_inactive_sessions, store_file_info

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 应用启动时的初始化
    yield
    # 应用关闭时的清理
    cleanup_inactive_sessions()

# 创建FastAPI应用
app = FastAPI(title="LightPDF AI助手API", lifespan=lifespan)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """API根路径"""
    return {"message": "LightPDF AI助手 API已启动"}

@app.post("/api/upload")
async def upload_file(
    files: List[UploadFile] = File(None),
    session_id: Optional[str] = Header(None, alias="Session-ID"),
    extends: Optional[str] = None
):
    """处理文件上传请求
    
    Args:
        files: 要上传的文件列表
        session_id: 会话ID
        extends: 可选的文件信息列表JSON字符串，用于直接保存并返回文件信息
    """
    # 准备响应头
    headers = {
        "Cache-Control": "no-cache, no-transform",
        "X-Accel-Buffering": "no"  # 禁用Nginx缓冲
    }

    # 如果没有session_id，创建新的
    if not session_id:
        session_id = str(uuid4())
        headers["Set-Session-ID"] = session_id
    
    # 处理extends参数 - 如果提供了extends参数，直接解析并返回
    if extends:
        try:
            file_info_list = json.loads(extends)
            # 转换为FileInfo对象
            results = []
            for info in file_info_list:
                file_info = FileInfo(
                    file_id=info.get("file_id"),
                    filename=info.get("filename"),
                    content_type=info.get("content_type"),
                    path=info.get("path")
                )
                # 存储文件信息到会话
                store_file_info(session_id, file_info)
                results.append(file_info)
            
            # 将FileInfo对象转换为字典
            results_dict = [result.model_dump() for result in results]
            
            return JSONResponse(
                content=results_dict,
                headers=headers
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"解析extends参数失败: {str(e)}")
    
    # 如果没有extends参数，执行常规的文件上传处理
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="未提供文件且未提供extends参数")
        
    # 使用批量处理函数处理所有文件
    results = await handle_batch_file_upload(files, session_id)
    
    # 将FileInfo对象转换为字典
    results_dict = [result.model_dump() for result in results]
    
    return JSONResponse(
        content=results_dict,
        headers=headers
    )

@app.post("/api/chat")
async def chat(
    request: ChatRequest,
    session_id: Optional[str] = Header(None, alias="Session-ID")
):
    """处理聊天请求"""
    try:
        # 准备响应头
        headers = {
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no"  # 禁用Nginx缓冲
        }
        
        # 如果没有session_id，创建新的
        if not session_id:
            session_id = str(uuid4())
            headers["Set-Session-ID"] = session_id
        
        # 创建一个用户消息
        user_message = Message(
            role="user",
            content=request.content,
            file_ids=request.file_ids,
            file_infos=request.file_infos
        )
        
        # 处理消息
        processed_messages = await process_messages(session_id, [user_message])
        
        # 生成响应
        return StreamingResponse(
            async_generator_to_json_stream(generate_chat_response(session_id, processed_messages, instructions=request.instructions)),
            media_type="application/x-ndjson",
            headers=headers
        )
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(status_code=500, detail=f"LightPDF AI助手处理错误: {error_msg}") 