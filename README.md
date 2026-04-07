# Agent Executor — Sistema Multi-Agente com Google ADK

Sistema de orquestração de agentes de IA com **Google ADK** e **Gemini 2.5 Flash**. O usuário descreve um problema em linguagem natural e o sistema decide, de forma autônoma, quais agentes especialistas acionar e em que sequência.

---

## O Problema

Automatizar tarefas que exigem múltiplas capacidades — pesquisar na web, escrever código, executar scripts, manipular arquivos — normalmente requer pipelines fixos e hardcoded. A proposta deste projeto é criar um sistema que **decide o fluxo em tempo de execução**, com base na intenção do usuário.

## Decisões de Arquitetura

### Por que Multi-Agente em vez de um único agente?

Um único agente com todas as ferramentas acumula contexto desnecessário e toma decisões mais lentas. A separação por especialidade permite que cada agente seja otimizado para sua tarefa e que o agente raiz foque exclusivamente em orquestração e delegação.

### O Ciclo de Raciocínio (ReAct Loop)

O root_agent opera em ciclo: recebe a tarefa, analisa a intenção, escolhe o agente especialista, recebe o resultado parcial e decide se precisa de outro agente. Esse loop continua até a resolução completa.

### Isolamento de Execução de Código

O coding_agent não apenas gera código — ele executa o código Python gerado. O código roda em subprocess controlado, com captura de stdout/stderr para feedback ao orquestrador.

---

## Arquitetura dos Agentes

root_agent (orquestrador)
├── search_agent: pesquisa na web via Google Search
├── coding_agent: gera e executa código Python em subprocess isolado
├── file_agent: lê, cria e lista arquivos locais
└── shell_agent: executa comandos no terminal

---

## Stack

Tecnologia | Papel
Python 3.11+ | Linguagem principal
Google ADK | Framework de orquestração de agentes
Gemini 2.5 Flash | Modelo de linguagem para raciocínio dos agentes
Pytest | Testes unitários das ferramentas

---

## Como Rodar

1. Clone o repositório: git clone https://github.com/bernardop-d/agent-executor-codigo.git
2. Crie um ambiente virtual: python -m venv .venv && source .venv/bin/activate
3. Instale as dependências: pip install google-adk pytest
4. Configure a chave: export GOOGLE_API_KEY="sua-chave-aqui" (obtenha em https://aistudio.google.com/)
5. Execute o sistema: adk run workflowAgent
6. Para rodar os testes: pytest tests/ -v

---

## Estrutura do Projeto

agent-executor-codigo/
├── agentCoder/        # Versão inicial: pesquisa + código
│   ├── __init__.py
│   └── agent.py
├── workflowAgent/     # Versão completa: 4 agentes + orquestrador
│   ├── __init__.py
│   ├── agent.py       # Definição dos agentes e root_agent
│   └── tools.py       # Ferramentas disponíveis para os agentes
├── tests/
│   └── test_tools.py
└── README.md

---

Feito por Bernardo P. D. — linkedin.com/in/bernardop-d/
