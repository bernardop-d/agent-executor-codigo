import os
import subprocess


def read_file(path: str) -> str:
    """Lê o conteúdo de um arquivo e retorna como string.

    Args:
        path: Caminho absoluto ou relativo do arquivo.

    Returns:
        Conteúdo do arquivo ou mensagem de erro.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erro ao ler arquivo: {e}"


def write_file(path: str, content: str) -> str:
    """Escreve conteúdo em um arquivo (cria ou sobrescreve).

    Args:
        path: Caminho do arquivo a ser escrito.
        content: Conteúdo a ser gravado.

    Returns:
        Mensagem de sucesso ou erro.
    """
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Arquivo salvo em: {path}"
    except Exception as e:
        return f"Erro ao escrever arquivo: {e}"


def list_directory(path: str = ".") -> str:
    """Lista arquivos e pastas de um diretório.

    Args:
        path: Caminho do diretório. Padrão é o diretório atual.

    Returns:
        Lista de arquivos e pastas ou mensagem de erro.
    """
    try:
        entries = os.listdir(path)
        result = []
        for entry in sorted(entries):
            full = os.path.join(path, entry)
            kind = "DIR" if os.path.isdir(full) else "FILE"
            result.append(f"[{kind}] {entry}")
        return "\n".join(result) if result else "(diretório vazio)"
    except Exception as e:
        return f"Erro ao listar diretório: {e}"


def run_shell_command(command: str) -> str:
    """Executa um comando shell e retorna stdout + stderr.

    Args:
        command: Comando a ser executado no shell.

    Returns:
        Saída do comando (stdout e stderr combinados).
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout
        if result.stderr:
            output += f"\n[stderr]\n{result.stderr}"
        return output.strip() or "(sem saída)"
    except subprocess.TimeoutExpired:
        return "Erro: comando excedeu o tempo limite de 30 segundos."
    except Exception as e:
        return f"Erro ao executar comando: {e}"
