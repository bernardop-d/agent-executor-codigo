# 🤖 Agent Executor — Plataforma de Automação Multi-Agente

> **Automatize fluxos de trabalho complexos com uma arquitetura de agentes inteligentes orquestrados por LLM (Gemini 2.5 Flash), capaz de pesquisar na web, escrever e executar código Python, manipular arquivos e rodar comandos de sistema — tudo de forma autônoma e encadeada.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Agent%20Development%20Kit-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://google.github.io/adk-docs/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Licença](https://img.shields.io/badge/Licença-MIT-green?style=for-the-badge)](LICENSE)
[![Testes](https://img.shields.io/badge/Testes-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](tests/)

---

## 📌 O Problema que Este Projeto Resolve

Tarefas modernas de engenharia e automação raramente são simples ou isoladas. Elas envolvem múltiplas etapas: pesquisar informações na web, processar dados com código, salvar resultados em arquivos e executar comandos no sistema operacional.

Ferramentas tradicionais exigem que o desenvolvedor orquestre cada etapa manualmente. O **Agent Executor** resolve isso com uma arquitetura multi-agente que **delega, encadeia e executa** essas etapas de forma autônoma, a partir de uma única instrução em linguagem natural.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|---|---|---|
| **Python** | 3.11+ | Linguagem principal |
| **Google ADK** | Latest | Framework de desenvolvimento de agentes |
| **Gemini 2.5 Flash** | Latest | Modelo LLM para raciocínio dos agentes |
| **Pytest** | 7+ | Suite de testes unitários |
| **subprocess** | stdlib | Execução segura de comandos shell |
| **os** | stdlib | Manipulação de sistema de arquivos |

---

## ✨ Funcionalidades Principais

- **🔍 Pesquisa Inteligente na Web** — O `search_agent` utiliza a ferramenta nativa `google_search` do ADK para buscar e sumarizar informações atualizadas em tempo real.
- **💻 Escrita e Execução de Código** — O `coding_agent` é equipado com `BuiltInCodeExecutor`, permitindo escrever código Python, executá-lo em sandbox e retornar resultado ou diagnóstico de erro.
- **📁 Manipulação de Arquivos** — O `file_agent` expõe ferramentas para leitura (`read_file`), escrita (`write_file`) e listagem (`list_directory`) de arquivos e diretórios.
- **🐚 Automação via Shell** — O `shell_agent` executa comandos do sistema operacional com timeout configurável e captura de stderr, ideal para instalar dependências e gerenciar processos.
- **🧠 Orquestração Inteligente** — O `root_agent` analisa a tarefa, decompõe em sub-tarefas e delega a cada agente especializado de forma sequencial e adaptativa.
- **♻️ Resiliência a Falhas** — O orquestrador tenta abordagens alternativas antes de reportar um erro ao usuário.

---

## 🏗️ Arquitetura e Design de Software

O projeto segue o padrão **Hierarchical Multi-Agent Architecture**, onde um agente orquestrador coordena sub-agentes especializados.

```
                        ┌──────────────────┐
                        │   root_agent     │  ← Orquestrador (Gemini 2.5 Flash)
                        └────────┬─────────┘
                                 │ Delegação via AgentTool
              ┌──────────────────┼──────────────────┬──────────────┐
              ▼                  ▼                  ▼              ▼
     ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐
     │ search_agent │  │ coding_agent │  │  file_agent  │  │shell_agent │
     │ google_search│  │ BuiltInCode  │  │  read_file   │  │run_shell   │
     │              │  │ Executor     │  │  write_file  │  │_command    │
     └──────────────┘  └──────────────┘  │ list_dir     │  └────────────┘
                                         └──────────────┘
```

**Decisões de Design:**

- **AgentTool Pattern**: Cada sub-agente é encapsulado como uma ferramenta do agente raiz, permitindo composição limpa e extensível.
- **Separation of Concerns (SRP)**: Cada agente tem uma única responsabilidade bem definida — nenhum agente faz mais do que deveria.
- **Tool Abstraction Layer**: As funções em `tools.py` são funções puras com tipagem estática, docstrings no padrão Google e tratamento de exceções centralizado, facilitando testes com mock.
- **Evolução Modular**: O repositório possui dois módulos independentes — `agentCoder` (v1 simples) e `workflowAgent` (v2 completo) — demonstrando capacidade de evolução incremental de arquitetura.

---

## ⚙️ Instalação e Execução

### Pré-requisitos

- Python 3.11 ou superior
- Conta no [Google AI Studio](https://aistudio.google.com/) com chave de API Gemini

### 1. Clone o repositório

```bash
git clone https://github.com/bernardop-d/agent-executor-codigo.git
cd agent-executor-codigo
```

### 2. Crie e ative o ambiente virtual

```bash
# Linux / macOS
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install google-adk pytest pytest-cov
```

### 4. Configure a chave de API

```bash
export GOOGLE_API_KEY="sua-chave-aqui"
```

### 5. Execute o agente

```bash
# Agente completo (recomendado)
adk run workflowAgent

# Agente básico (versão inicial)
adk run agentCoder
```

### Exemplo de fluxo executado

```
> Pesquise sobre Pandas, escreva um script que crie um DataFrame e salve em output.csv

[search_agent]  → Buscando documentação do Pandas...
[coding_agent]  → Escrevendo e executando o script Python...
[file_agent]    → Salvando output.csv no diretório atual...
✅ Concluído! Arquivo salvo em: ./output.csv
```

---

## 🧪 Como Executar os Testes

O projeto inclui uma suite de testes unitários cobrindo todas as ferramentas do `workflowAgent`.

### Executar todos os testes

```bash
pytest tests/ -v
```

### Executar com relatório de cobertura

```bash
pytest tests/ -v --cov=workflowAgent --cov-report=term-missing
```

### Saída esperada

```
tests/test_tools.py::TestReadFile::test_ler_arquivo_existente PASSED
tests/test_tools.py::TestReadFile::test_arquivo_inexistente_retorna_erro PASSED
tests/test_tools.py::TestWriteFile::test_escrever_cria_arquivo_com_conteudo PASSED
tests/test_tools.py::TestWriteFile::test_escrever_cria_diretorios_pai PASSED
tests/test_tools.py::TestListDirectory::test_listar_retorna_entradas_ordenadas PASSED
tests/test_tools.py::TestListDirectory::test_listar_diretorio_vazio PASSED
tests/test_tools.py::TestListDirectory::test_listar_caminho_invalido_retorna_erro PASSED
tests/test_tools.py::TestRunShellCommand::test_executar_comando_simples PASSED
tests/test_tools.py::TestRunShellCommand::test_executar_comando_com_stderr PASSED
tests/test_tools.py::TestRunShellCommand::test_timeout_retorna_erro PASSED

10 passed in 0.84s
```

---

## 📂 Estrutura do Projeto

```
agent-executor-codigo/
│
├── agentCoder/                  # Módulo v1: agente básico (busca + execução de código)
│   ├── __init__.py
│   └── agent.py                 # search_agent, coding_agent, root_agent
│
├── workflowAgent/               # Módulo v2: arquitetura multi-agente completa
│   ├── __init__.py
│   ├── agent.py                 # 4 sub-agentes + orquestrador
│   └── tools.py                 # Ferramentas de I/O e shell (funções puras e testáveis)
│
├── tests/                       # Suite de testes unitários (Pytest)
│   ├── __init__.py
│   └── test_tools.py            # Cobertura das ferramentas do workflowAgent
│
├── .gitignore
└── README.md
```

---

## 🔮 Próximos Passos (Roadmap)

- [ ] Interface REST via **FastAPI** para receber tarefas via HTTP
- [ ] **Persistência de histórico** de sessões dos agentes em banco de dados
- [ ] **GitHub Actions** para CI/CD com execução automática dos testes
- [ ] Agente de **análise de dados** com suporte a Pandas e Matplotlib
- [ ] Publicação como pacote no **PyPI**

---

## 👨‍💻 Autor

**Bernardo P. D.**
- GitHub: [@bernardop-d](https://github.com/bernardop-d)
- Email: contato.bernardopd@gmail.com

---

<p align="center">Feito com ☕ e Python</p>
