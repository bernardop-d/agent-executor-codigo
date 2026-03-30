from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search
from google.adk.code_executors import BuiltInCodeExecutor

search_agent = Agent(
    model='gemini-2.5-flash',
    name='search_agent',
    description='Voce é um agente especializado em buscar informações na web via Google Search.',
    instruction="""
                Voce é um agente especializado em buscar informações na web via Google Search.
                Use a ferramenta de busca para responder perguntas do usuario.""",

tools=[google_search],
)

coding_agent = Agent(
    model='gemini-2.5-flash',
    name='coding_agent',
    description='Voce é um agente especializado em escrever e executar código.',
    instruction="""
                Voce é um agente especializado em escrever e executar código.
                Use a ferramenta de execução de código para executat o código que voce escreveu.""",
    code_executor=BuiltInCodeExecutor(),
)
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Voce é o agente principal e orquestrador.',
    instruction="Voce é o agente principal e orquestrador.",
    tools=[AgentTool(agent=search_agent), AgentTool(agent=coding_agent)]

)