
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
```

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

---

## ☁️ 12. GitHub 업로드 방법 (저장 및 협업용)

이 섹션은 프로젝트를 처음 클론받은 뒤,  
로컬에서 작업한 내용을 자신의 GitHub 저장소로 올리는 방법을 설명합니다.  
(Windows + Git Bash 환경 기준)

---

### 1️⃣ Git 초기화

프로젝트 루트에서 Git 저장소를 초기화합니다.

```bash
git init
````

### 2️⃣ 사용자 정보 설정 (최초 1회만)

Git은 커밋 작성자의 이름과 이메일이 필요합니다.

```bash
git config --global user.name "your_name"
git config --global user.email "your_email@example.com"
```

설정 확인:

```bash
git config --list
```

---

### 3️⃣ .gitignore 추가

가상환경, 캐시, 환경변수 파일 등은 제외합니다.
(이미 `.gitignore` 파일이 포함되어 있다면 건너뛰어도 됩니다.)

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.log

# Virtual environment
.venv/
env/
venv/

# Environment variables
.env

# OS / IDE
.DS_Store
Thumbs.db
.idea/
.vscode/
cursor.json
```

---

### 4️⃣ 변경사항 커밋

```bash
git add .
git commit -m "Step 1: FastAPI + Gradio skeleton for Doc QA Agent"
```

---

### 5️⃣ GitHub에 새 저장소 만들기

1. [https://github.com/shincheolhui](https://github.com/shincheolhui) 접속
2. **Repositories → New**
3. 저장소 이름 입력: 예) `doc-qa-agent-1`
4. ⚠️ README, .gitignore, LICENSE **생성하지 않기**
5. **Create repository** 클릭

---

### 6️⃣ 원격 저장소 연결

GitHub에서 생성된 주소를 복사해서 붙여넣습니다.
SSH 사용 권장 (HTTPS는 회사망에서 SSL 문제 발생 가능)

```bash
git remote add origin git@github.com:shincheolhui/doc-qa-agent-1.git
git branch -M master
```

---

### 7️⃣ SSH 포트 443 설정 (회사망에서 SSH 22번 차단된 경우)

SSH 연결이 차단된다면 아래 설정을 추가합니다.

```bash
nano ~/.ssh/config
```

아래 내용을 추가:

```text
Host github.com
  HostName ssh.github.com
  User git
  Port 443
  IdentityFile ~/.ssh/id_ed25519
  TCPKeepAlive yes
  IdentitiesOnly yes
```

---

### 8️⃣ GitHub에 SSH 키 등록 (최초 1회만)

```bash
# SSH 키 생성 (없을 때만)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 공개키 확인
cat ~/.ssh/id_ed25519.pub
```

한 줄로 출력되는 전체 내용을 GitHub → **Settings → SSH and GPG keys → New SSH key** 에 붙여넣기.

---

### 9️⃣ SSH 연결 테스트

```bash
ssh -T git@github.com
```

성공 시:

```
Hi <your_name>! You've successfully authenticated, but GitHub does not provide shell access.
```

이 메시지가 출력되면 OK ✅

---

### 🔟 푸시 (업로드)

```bash
git push -u origin master
```

성공 로그 예시:

```
Enumerating objects: 10, done.
Counting objects: 100% (10/10), done.
Writing objects: 100% (10/10), 4.72 KiB | 1.57 MiB/s, done.
To github.com:<your_name>/doc-qa-agent-1.git
 * [new branch]      master -> master
branch 'master' set up to track 'origin/master'.
```

이제 [https://github.com/shincheolhui/doc-qa-agent-1](https://github.com/shincheolhui/doc-qa-agent-1)
에서 코드가 확인됩니다 🎉

---

### ♻️ 이후 업데이트 시

작업 내용을 수정하고 다음 명령으로 버전 관리하세요.

```bash
git add .
git commit -m "Update: added vectorstore.py for FAISS index generation"
git push
```

---

### 🧰 참고

* 회사망에서 HTTPS Push 시 SSL 오류 발생 시:

  ```bash
  git config http.sslVerify false
  ```

  (보안상 권장되지 않음. SSH를 사용하는 것이 더 안전함.)

* 다른 PC에서 새로 클론받으려면:

  ```bash
  git clone git@github.com:shincheolhui/doc-qa-agent-1.git
  cd doc-qa-agent-1
  ```

---

📘 **요약**

| 항목        | 명령어                                                          |
| --------- | ------------------------------------------------------------ |
| Git 초기화   | `git init`                                                   |
| 커밋        | `git add . && git commit -m "메시지"`                           |
| 원격 저장소 추가 | `git remote add origin git@github.com:shincheolhui/저장소명.git` |
| 푸시        | `git push -u origin master`                                  |
| SSH 연결 확인 | `ssh -T git@github.com`                                      |

---

> 💡 **Tip:**
> SSH 키 방식(443포트)은 회사망 환경에서도 안정적으로 작동하며,
> HTTPS 방식보다 인증 문제를 덜 겪습니다.
> (특히 “SSL certificate problem” 에러가 뜨는 환경에서 필수!)

```

---

이제 `README.md`의 마지막 부분에 위 내용을 붙여넣으면,  
다른 개발자도 **“GitHub 업로드 / 협업 절차를 그대로 재현”** 할 수 있게 됩니다.  

원하신다면 제가 이 섹션이 포함된 **최종 통합 README 전체 버전**도 바로 만들어드릴까요?
```
