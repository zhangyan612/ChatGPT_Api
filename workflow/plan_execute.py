from langchain.chains import LLMMathChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import Tool
from plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)



search = DuckDuckGoSearchAPIWrapper()
llm = OpenAI(temperature=0)
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math",
    ),
]

model = ChatOpenAI(temperature=0)
planner = load_chat_planner(model)
executor = load_agent_executor(model, tools, verbose=True)
agent = PlanAndExecute(planner=planner, executor=executor)

agent.run(
    "Who is the current prime minister of the UK? What is their current age raised to the 0.43 power?"
)