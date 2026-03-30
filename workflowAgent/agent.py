from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search
from google.adk.code_executors import BuiltInCodeExecutor

from .tools import read_file, write_file, list_directory, run_shell_command

# ─── Agente de Busca ────────────────────────────────────────────────────────
search_agent = Agent(
    model="gemini-2.5-flash",
    name="search_agent",
    description="Busca informações atualizadas na web via Google Search.",
    instruction="""
Você é um agente especializado em pesquisa web.
Sempre que receber uma pergunta ou tema, use google_search para buscar
informações relevantes e retorne um resumo claro e objetivo.
""",
    tools=[google_search],
)

# ─── Agente de Código ────────────────────────────────────────────────────────
coding_agent = Agent(
    model="gemini-2.5-flash",
    name="coding_agent",
    description="Escreve, executa e depura código Python.",
    instruction="""
Você é um agente especializado em programação Python.
Escreva código limpo e funcional, execute-o com BuiltInCodeExecutor
e retorne o resultado ou explique os erros encontrados.
""",
    code_executor=BuiltInCodeExecutor(),
)

# ─── Agente de Arquivos ──────────────────────────────────────────────────────
file_agent = Agent(
    model="gemini-2.5-flash",
    name="file_agent",
    description="Lê, escreve e lista arquivos e diretórios do sistema.",
    instruction="""
Você é um agente especializado em manipulação de arquivos.
Use as ferramentas disponíveis para ler, criar ou listar arquivos
conforme solicitado. Sempre confirme o que foi feito.
""",
    tools=[read_file, write_file, list_directory],
)

# ─── Agente de Shell ─────────────────────────────────────────────────────────
shell_agent = Agent(
    model="gemini-2.5-flash",
    name="shell_agent",
    description="Executa comandos shell para automação de tarefas do sistema operacional.",
    instruction="""
Você é um agente especializado em automação via linha de comando.
Execute comandos shell para instalar pacotes, mover arquivos, checar
processos ou qualquer outra tarefa de sistema. Retorne a saída do comando
e explique o resultado.
""",
    tools=[run_shell_command],
)

# ─── Agente Orquestrador ─────────────────────────────────────────────────────
root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Orquestrador principal de automação de workflows.",
    instruction="""
Você é o agente orquestrador principal responsável por automatizar fluxos de trabalho completos.

Seus sub-agentes disponíveis:
- search_agent: pesquisar informações na web
- coding_agent: escrever e executar código Python
- file_agent: ler, escrever e listar arquivos
- shell_agent: executar comandos do sistema operacional

Estratégia de orquestração:
1. Analise a tarefa recebida e identifique quais etapas são necessárias.
2. Delegue cada etapa ao agente mais adequado.
3. Combine os resultados parciais em uma resposta final coesa.
4. Se uma etapa falhar, tente uma abordagem alternativa antes de reportar o erro.

Exemplos de workflows:
- "Pesquise X, escreva um script que processe os dados e salve o resultado" →
  search_agent → coding_agent → file_agent
- "Liste os arquivos da pasta Y e execute o script Z" →
  file_agent → shell_agent
- "Instale a biblioteca X e escreva um exemplo de uso" →
  shell_agent → coding_agent
""",
    tools=[
        AgentTool(agent=search_agent),
        AgentTool(agent=coding_agent),
        AgentTool(agent=file_agent),
        AgentTool(agent=shell_agent),
    ],
)
