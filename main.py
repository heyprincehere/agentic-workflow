import os
from typing import TypedDict, List, Literal
from langgraph.graph import StateGraph
from langchain.agents import Tool, initialize_agent, AgentType
from openai import OpenAI

# ✅ Load API key from Streamlit Secrets first, fallback to .env
try:
    import streamlit as st
    openrouter_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    openrouter_key = os.getenv("OPENAI_API_KEY")

# ✅ Setup OpenRouter Client
client = OpenAI(
    api_key=openrouter_key,
    base_url="https://openrouter.ai/api/v1",
)

# ✅ Call OpenRouter
def call_openrouter(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="anthropic/claude-3-haiku",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenRouter: {str(e)}"

# ✅ LangGraph State
class GraphState(TypedDict):
    input: str
    tasks: List[str]
    results: List[str]
    feedback: Literal["good", "retry"]

# ✅ Step 1: Planner
def plan_agent(state: GraphState) -> dict:
    prompt = f"Split this task into 3-5 clear subtasks: {state['input']}"
    response = call_openrouter(prompt)
    tasks = [line.strip("-• ") for line in response.strip().split("\n") if line.strip()]
    return {"tasks": tasks}

# ✅ Step 2: Refiner
def refine_agent(state: GraphState) -> dict:
    prompt = f"""You are a task refining agent.

Improve the following tasks based on user input "{state['input']}":

{state['tasks']}

Return improved tasks only, one per line."""
    response = call_openrouter(prompt)
    refined = [line.strip("-• ") for line in response.strip().split("\n") if line.strip()]
    return {"tasks": refined}

# ✅ Step 3: Executor
def tool_agent(state: GraphState) -> dict:
    completed = []
    for task in state["tasks"]:
        answer = call_openrouter(f"Complete this task: {task}")
        completed.append(answer.strip())
    return {"results": completed}

# ✅ Step 4: Reflection
def reflection_agent(state: GraphState) -> dict:
    results = "\n".join(state["results"])
    prompt = f"""You are a quality control agent.

Review these answers:
{results}

Were these answers helpful, accurate, and complete?

Respond with one word only: "good" or "retry"
"""
    judgment = call_openrouter(prompt).lower()
    return {"feedback": "retry"} if "retry" in judgment else {"feedback": "good"}

# ✅ Build LangGraph
graph = StateGraph(GraphState)
graph.add_node("Planner", plan_agent)
graph.add_node("Refiner", refine_agent)
graph.add_node("Executor", tool_agent)
graph.add_node("Reflector", reflection_agent)

graph.set_entry_point("Planner")
graph.add_edge("Planner", "Refiner")
graph.add_edge("Refiner", "Executor")
graph.add_edge("Executor", "Reflector")
graph.add_conditional_edges("Reflector", lambda state:
    "Executor" if state.get("feedback") == "retry" else "end"
)
graph.set_finish_point("Reflector")

# ✅ Compile and Run
app = graph.compile()

if __name__ == "__main__":
    user_input = input("Enter your task: ")
    try:
        result = app.invoke({"input": user_input})
        print("\n🎉 Final Output:")
        for i, r in enumerate(result["results"], 1):
            print(f"{i}. {r}")
    except Exception as e:
        print("\n❌ Workflow Failed:")
        print(e)
