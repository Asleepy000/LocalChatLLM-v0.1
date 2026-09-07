from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# 导入你封装好的函数
from Ollama_demo import chat_with_ollama

app = FastAPI()

# 跨域，允许本地html访问接口
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_api(req: ChatRequest):
    reply = chat_with_ollama(req.message)
    return {"reply": reply}

# 额外加一个清空对话接口，前端可以调用重置历史
@app.post("/clear")
def clear_context():
    from Ollama_demo import messages
    messages.clear()
    return {"msg":"对话上下文已清空"}

if __name__ == "__main__":
    import uvicorn
    # 必须 --workers=1，否则全局messages会错乱
    uvicorn.run(app, host="127.0.0.1", port=8000, workers=1)
