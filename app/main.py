from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr

# --- FastAPI 애플리케이션 생성 ---
app = FastAPI(
    title="Doc QA Agent (Step 1)",
    version="0.1.0",
    description="간단한 문서 질의 응답 에이전트",
)

# CORS (나중에 다른 프론트에서 호출할 수도 있으니 미리 설정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 해커톤용, 일단 전체 허용
    allow_credentials=True,
    allow_methods=["*"], # 모든 메서드 허용
    allow_headers=["*"], # 모든 헤더 허용
)

# --- Health Check Endpoint ---
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# --- Gradio용 간단 Echo 챗봇 (테스트용) ---
def echo_chat(message: str, history: list[tuple[str, str]]):
    """
    지금은 단순 Echo 봇.
    다음 단계에서 LangChain + LangGraph 호출로 바꿉니다.
    """
    reply = f"당신이 보낸 메시지: {message}"
    return reply

# Gradio Blocks/ChatInterface 정의
with gr.Blocks() as gradio_app:
    gr.Markdown("## 📚 Doc QA Agent (Step 1: 서버 골격 테스트)")
    gr.Markdown(
        "이 챗봇은 현재 단순 Echo 봇입니다.\n"
        "다음 단계에서 LangChain + LangGraph 호출로 바꿉니다."
    )

    chat = gr.ChatInterface(
        fn=echo_chat,
        title="Doc QA Agent",
        chatbot=gr.Chatbot(height=400),
        textbox=gr.Textbox(placeholder="여기에 질문을 입력하세요."),
    )

# Gradio를 FastAPI 아래 /ui 경로에 마운트
app = gr.mount_gradio_app(app, gradio_app, path="/ui")


# --- uvicorn 으로 직접 실행할 때 진입점 ---
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
    )