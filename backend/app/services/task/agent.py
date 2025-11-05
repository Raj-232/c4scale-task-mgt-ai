from langchain_google_genai import ChatGoogleGenerativeAI
from services.task.tools import create_task, list_tasks, update_task, delete_task, filter_tasks
from schemas.task import CreateTaskInput,DeleteTaskInput,UpdateTaskInput,FilterTasksInput
from langchain.tools import StructuredTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from utils.config_env import config_env
# Initialize Memory

memory = MemorySaver()

# 1. Define the System Prompt (Instructions)
system_prompt_text = (
    "You are a helpful and efficient **Task Management Agent**. Your primary function "
    "is to manage the user's to-do list by using the provided tools. "
    
    "**Strict Rules:**\n"
    "1. You MUST call a tool for any request involving task creation, listing, updating, or deletion.\n"
    "2. Be concise and professional in your final response.\n"
    "3. Only use the `task_id` for tasks that have been successfully created or listed. Never guess an ID.\n"
    "4. If a user asks a general question (e.g., 'How are you?'), answer directly without using a tool."
)

# 2. Define the Prompt Template
# This structure is standard for tool-calling agents in LangChain.
prompt = ChatPromptTemplate.from_messages(
    [
        # System Message: Sets the persona and rules
        ("system", system_prompt_text),
        
        # Chat History Placeholder: Required for conversationownal memory (even if you don't use it yet)
        MessagesPlaceholder(variable_name="chat_history"),
        
        # Human Input: The current user query
        ("human", "{input}"),
        
        # Agent Scratchpad: Required for the agent's internal thought process and tool execution history
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)
# configure Gemini API
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3,google_api_key=config_env.google_api_key)

# Update Tool definitions
tools = [
    StructuredTool.from_function( # <-- CHANGE 1
        name="create_task",
        func=create_task,
        description="Create a new task with a title, description, priority, and optional due date.",
        args_schema=CreateTaskInput
    ),
    StructuredTool.from_function( # <-- CHANGE 2
        name="update_task", 
        func=update_task, 
        description="Update task fields", 
        args_schema=UpdateTaskInput
    ),
    StructuredTool.from_function( # <-- CHANGE 3
        name="delete_task", 
        func=delete_task, 
        description="Delete a task by ID", 
        args_schema=DeleteTaskInput
    ),
    # For list_tasks, which takes no arguments, you can still use StructuredTool for consistency, 
    # but the simple Tool might also work. StructuredTool.from_function is safer.
    StructuredTool.from_function( # <-- CHANGE 4
        name="list_tasks", 
        func=list_tasks, 
        description="List all existing tasks"
        # No args_schema needed if list_tasks() takes no arguments
    ),
    StructuredTool.from_function(
        name="filter_tasks",
        func=filter_tasks,
        description="Filter tasks by status, priority, or due_date (YYYY-MM-DD)",
        args_schema=FilterTasksInput
    ),
]

agent_app = create_react_agent(
    llm,
    tools=tools,
    prompt=prompt,
    checkpointer=memory,
)