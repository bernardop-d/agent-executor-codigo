# Agent Executor — Automação com Agentes de IA

Projeto desenvolvido para estudar e praticar o uso do **Google ADK (Agent Development Kit)** com o modelo **Gemini 2.5 Flash**. A ideia é criar agentes de IA que conseguem fazer tarefas do dia a dia de forma automática, como pesquisar na web, escrever e rodar código Python, ler e criar arquivos, e executar comandos no terminal.

---

## Tecnologias usadas

- Python 3.11+
- Google ADK
- Gemini 2.5 Flash
- Pytest

---

## O que o projeto faz

O projeto tem dois módulos principais:

**agentCoder** — versão inicial com dois agentes:
- Um agente que pesquisa na web usando o Google Search
- Um agente que escreve e executa código Python

**workflowAgent** — versão mais completa com quatro agentes:
- **search_agent**: pesquisa informações na web
- **coding_agent**: escreve e roda código Python
- **file_agent**: lê, cria e lista arquivos no computador
- **shell_agent**: roda comandos no terminal (como `pip install`, `ls`, etc.)

Todos os agentes são coordenados por um **root_agent**, que decide qual agente chamar dependendo da tarefa pedida.

---

## Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/bernardop-d/agent-executor-codigo.git
cd agent-executor-codigo
```

### 2. Crie um ambiente virtual e instale as dependências

```bash
python -m venv .venv
source .venv/bin/activate  # no Windows: .venv\Scripts\activate
pip install google-adk pytest
```

### 3. Configure sua chave da API do Gemini

```bash
export GOOGLE_API_KEY="sua-chave-aqui"
```

> Você pode obter sua chave gratuita em: https://aistudio.google.com/

### 4. Execute o agente

```bash
adk run workflowAgent
```

---

## Como rodar os testes

```bash
pytest tests/ -v
```

---

## Estrutura de pastas

```
agent-executor-codigo/
├── agentCoder/
│   ├── __init__.py
│   └── agent.py
├── workflowAgent/
│   ├── __init__.py
│   ├── agent.py
│   └── tools.py
├── tests/
│   └── test_tools.py
└── README.md
```

---

## O que aprendi com esse projeto

- Como configurar e usar o Google ADK para criar agentes de IA
- Como criar ferramentas (funções Python) que os agentes podem usar
- Como organizar um projeto Python em módulos
- Como escrever testes unitários com Pytest

---

Feito por [Bernardo P. D.](https://github.com/bernardop-d)
