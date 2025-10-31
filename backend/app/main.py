
from fastapi import FastAPI,WebSocket
from fastapi.middleware.cors import CORSMiddleware
from utils.db_connection import engine, Base
from utils.config_env import ConfigEnv
from utils.logger import logger
from services.task.agent import agent_app
from routes.task import router
import uuid
# Initialize the settings
configEnv = ConfigEnv()
# Print the settings to verify
logger.info(f"Settings Loaded: {configEnv.model_dump()}")

app = FastAPI(
    title="c4scale AI-ML-Management App service",
    description="APIs for all c4scale AI-ML-Management application.",
    root_path="/api/v1",
    version="1.0.0",
)

# Allow all origins — can be restricted in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint."""
    return {"status": "OK", "message": "Service is healthy."}


@app.websocket("/chat")
async def chat_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_text("🤖 Task Agent connected. You can ask me to create, list, or update your tasks.")

    # Create a unique thread ID for this connection to persist conversation memory
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        try:
            # Wait for message from frontend
            msg = await ws.receive_text()


            # Use LangGraph's streaming output mode (for multi-turn chat)
            async for event in agent_app.astream(
                {"messages": [{"role": "user", "content": msg}]},
                config,
                stream_mode="values",
            ):
                # Extract last message and forward only AI outputs to avoid echoing the user
                last = event["messages"][-1]
                try:
                    last_type = getattr(last, "type", "")
                    last_content = getattr(last, "content", None)
                    if last_type in ("ai", "assistant") and last_content:
                        await ws.send_text(last_content)
                except Exception:
                    # Fallback: do nothing on unknown event shapes
                    pass

        except Exception as e:
            print(f"⚠️ WebSocket error: {e}")
            break