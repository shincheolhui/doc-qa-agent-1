````markdown
# 📚 Doc QA Agent (Step 1)

> LangChain + LangGraph + FAISS + gpt-4o-mini 기반  
> “문서 Q&A 에이전트”를 개발하기 위한 **1단계: FastAPI + Gradio 서버 골격**

이 단계에서는 **기본 서버 구조 및 UI만 구성**되어 있으며,  
다음 단계에서 LangChain / LangGraph / OpenAI / FAISS 기반 문서 Q&A 기능을 추가합니다.

---

## 🚀 1. 프로젝트 클론

```powershell
cd C:\Users\clush\ai-agent-hackathon
git clone <이 저장소의 Git 주소> doc-qa-agent
cd doc-qa-agent
````

---

## 🐍 2. Python 가상환경 생성

> Python **3.11.x** 버전을 권장합니다.
> (Windows 11 Pro + Cursor 2.0.64 환경 기준)

```powershell
# Python 3.11로 가상환경 생성
py -3.11 -m venv .venv
```

---

## ⚙️ 3. 가상환경 활성화

```powershell
.\.venv\Scripts\Activate.ps1
```

> ⚠️ 만약 다음과 같은 오류가 발생한다면:
>
> ```
> 이 시스템에서 스크립트를 실행할 수 없으므로 ...
> ```
>
> 아래 명령으로 임시 허용 후 다시 실행하세요:
>
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .\.venv\Scripts\Activate.ps1
> ```

---

## 📦 4. 의존성 설치

```powershell
# pip 최신화
python -m pip install --upgrade pip

# 프로젝트 패키지 설치
pip install -r requirements.txt
```

설치가 완료되면 주요 라이브러리들이 다음과 같이 세팅됩니다.

| 분류            | 패키지                                              | 버전      |
| ------------- | ------------------------------------------------ | ------- |
| Web Framework | fastapi                                          | 0.121.0 |
| Server        | uvicorn                                          | 0.38.0  |
| UI            | gradio                                           | 5.49.1  |
| Core AI Stack | langchain 1.0.4 / langgraph 1.0.2 / openai 2.7.1 |         |
| Vector DB     | faiss-cpu                                        | 1.12.0  |
| Utility       | python-dotenv, pypdf, tiktoken 등                 |         |

---

## 🔑 5. 환경 변수 (.env) 설정

루트 디렉터리에 `.env` 파일을 생성하고 아래 내용 작성:

```env
OPENAI_API_KEY=여기에_본인_API_키_입력
OPENAI_BASE_URL=https://api.openai.com/v1
```

> 1단계에서는 OpenAI API를 직접 호출하지 않지만,
> 다음 단계(LangChain + LangGraph 연동)에서 바로 사용합니다.

---

## 📁 6. 프로젝트 구조

```bash
doc-qa-agent/
│  .env
│  requirements.txt
│
├─.venv/
│
├─app/
│  │  __init__.py
│  │  main.py              # FastAPI + Gradio 서버 엔트리
│  │
│  └─rag/
│      __init__.py         # LangGraph/FAISS 코드 추가 예정
│
└─data/
    └─docs/                # PDF/TXT 문서 저장 폴더
```

---

## ▶️ 7. 서버 실행

가상환경이 활성화된 상태에서:

```powershell
uvicorn app.main:app --reload
```

정상 실행 시 출력 예시:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

---

## 🌐 8. 동작 확인

### ✅ 헬스체크

브라우저에서 [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) 접속 →
다음과 같은 JSON이 나오면 정상:

```json
{"status": "ok"}
```

### 💬 Gradio 챗 UI

브라우저에서 [http://127.0.0.1:8000/ui](http://127.0.0.1:8000/ui) 접속 →
간단한 챗 인터페이스가 열립니다.

> 지금은 단순 Echo 챗봇으로,
> 입력한 문장을 그대로 되돌려줍니다.
> (예: “안녕하세요” → “당신이 보낸 메시지: 안녕하세요”)

---

## 🧱 9. 코드 개요

### app/main.py

* **FastAPI** 서버 인스턴스 생성
* `/health` 엔드포인트
* **Gradio Blocks** 기반 챗봇 UI
* Gradio를 FastAPI 경로 `/ui`로 마운트

```python
app = FastAPI(title="Doc QA Agent (Step 1)", version="0.1.0")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

def echo_chat(message: str, history: list[tuple[str, str]]):
    return f"당신이 보낸 메시지: {message}"

with gr.Blocks() as gradio_app:
    gr.ChatInterface(fn=echo_chat, title="Doc QA Agent")

app = gr.mount_gradio_app(app, gradio_app, path="/ui")
```

---

## 🔮 10. 다음 단계 로드맵

이 저장소는 **Step 1 (서버 골격)** 버전입니다.
아래 순서로 확장해 나가면 완전한 문서 Q&A Agent를 구현할 수 있습니다.

| 단계     | 내용                             | 주요 파일                                |
| ------ | ------------------------------ | ------------------------------------ |
| Step 2 | 문서 로드 + 임베딩 + FAISS 인덱스 생성     | `app/rag/vectorstore.py`             |
| Step 3 | LangGraph 기반 RAG 플로우 구축        | `app/rag/graph.py`                   |
| Step 4 | Gradio UI에서 문서 업로드 + 실시간 Q&A   | `app/main.py`                        |
| Step 5 | OpenAI gpt-4o-mini 연동 및 RAG 튜닝 | `.env`, `vectorstore.py`, `graph.py` |

---

## 🧰 11. 트러블슈팅

| 문제                  | 원인                            | 해결 방법                                                        |
| ------------------- | ----------------------------- | ------------------------------------------------------------ |
| `.ps1` 실행 보안 오류     | PowerShell ExecutionPolicy 제한 | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| 포트 8000 충돌          | 이미 다른 프로세스 사용 중               | `uvicorn app.main:app --reload --port 8001`                  |
| `pip install` 버전 충돌 | 특정 의존성 불일치                    | 최신 pip으로 재설치: `python -m pip install --upgrade pip`          |
