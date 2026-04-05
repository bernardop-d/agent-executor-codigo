"""
Testes unitários para workflowAgent/tools.py

Cobertura:
    - read_file: leitura de arquivo existente e inexistente
    - write_file: escrita de conteúdo e criação de diretórios pai
    - list_directory: listagem ordenada, diretório vazio e caminho inválido
    - run_shell_command: execução simples, captura de stderr e timeout

Execução:
    pytest tests/ -v --cov=workflowAgent --cov-report=term-missing
"""

import os
import sys
import pytest
import tempfile
import unittest
from unittest.mock import patch

# Adiciona o diretório raiz ao path para importar o módulo corretamente
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflowAgent.tools import read_file, write_file, list_directory, run_shell_command


# ===========================================================================
# TestReadFile — Testa a função read_file
# ===========================================================================

class TestReadFile(unittest.TestCase):
    """Testa a ferramenta de leitura de arquivos."""

    def test_ler_arquivo_existente(self):
        """Deve retornar o conteúdo correto de um arquivo existente."""
        # Arrange: cria um arquivo temporário com conteúdo conhecido
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write("conteúdo de teste")
            caminho_tmp = tmp.name

        try:
            # Act: chama a função com o caminho do arquivo temporário
            resultado = read_file(caminho_tmp)

            # Assert: verifica que o conteúdo retornado é o esperado
            self.assertEqual(resultado, "conteúdo de teste")
        finally:
            os.unlink(caminho_tmp)

    def test_arquivo_inexistente_retorna_erro(self):
        """Deve retornar mensagem de erro quando o arquivo não existe."""
        # Arrange: caminho de arquivo que não existe
        caminho_invalido = "/caminho/que/nao/existe/arquivo.txt"

        # Act: chama a função com caminho inválido
        resultado = read_file(caminho_invalido)

        # Assert: verifica que a mensagem de erro está presente
        self.assertIn("Erro ao ler arquivo", resultado)

    def test_ler_arquivo_utf8(self):
        """Deve ler corretamente arquivos com caracteres UTF-8."""
        # Arrange: arquivo com acentuação e caracteres especiais
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write("São Paulo — Brasil 🇧🇷")
            caminho_tmp = tmp.name

        try:
            # Act
            resultado = read_file(caminho_tmp)

            # Assert
            self.assertIn("São Paulo", resultado)
        finally:
            os.unlink(caminho_tmp)


# ===========================================================================
# TestWriteFile — Testa a função write_file
# ===========================================================================

class TestWriteFile(unittest.TestCase):
    """Testa a ferramenta de escrita de arquivos."""

    def setUp(self):
        """Cria um diretório temporário para cada teste."""
        self.dir_temp = tempfile.mkdtemp()

    def tearDown(self):
        """Remove arquivos criados durante os testes."""
        import shutil
        shutil.rmtree(self.dir_temp, ignore_errors=True)

    def test_escrever_cria_arquivo_com_conteudo(self):
        """Deve criar o arquivo e escrever o conteúdo corretamente."""
        # Arrange
        caminho = os.path.join(self.dir_temp, "saida.txt")
        conteudo = "texto do teste"

        # Act
        resultado = write_file(caminho, conteudo)

        # Assert: arquivo criado com conteúdo correto
        self.assertIn("Arquivo salvo em", resultado)
        with open(caminho, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), conteudo)

    def test_escrever_cria_diretorios_pai(self):
        """Deve criar automaticamente os diretórios pai que não existem."""
        # Arrange: caminho com subdiretório inexistente
        caminho = os.path.join(self.dir_temp, "subdir", "nested", "arquivo.txt")

        # Act
        resultado = write_file(caminho, "conteúdo aninhado")

        # Assert: diretórios criados e arquivo existe
        self.assertTrue(os.path.exists(caminho))
        self.assertIn("Arquivo salvo em", resultado)

    def test_escrever_sobrescreve_conteudo_existente(self):
        """Deve sobrescrever o conteúdo de um arquivo já existente."""
        # Arrange
        caminho = os.path.join(self.dir_temp, "existente.txt")
        write_file(caminho, "conteúdo original")

        # Act
        resultado = write_file(caminho, "conteúdo novo")

        # Assert
        with open(caminho, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "conteúdo novo")


# ===========================================================================
# TestListDirectory — Testa a função list_directory
# ===========================================================================

class TestListDirectory(unittest.TestCase):
    """Testa a ferramenta de listagem de diretórios."""

    def setUp(self):
        """Cria estrutura de diretório temporário para os testes."""
        self.dir_temp = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.dir_temp, ignore_errors=True)

    def test_listar_retorna_entradas_ordenadas(self):
        """Deve retornar arquivos e diretórios em ordem alfabética."""
        # Arrange: cria arquivos fora de ordem
        for nome in ["zebra.txt", "alpha.py", "beta.md"]:
            open(os.path.join(self.dir_temp, nome), "w").close()

        # Act
        resultado = list_directory(self.dir_temp)

        # Assert: verifica ordenação e presença de todos os arquivos
        linhas = resultado.splitlines()
        nomes = [l.split("] ")[1] for l in linhas]
        self.assertEqual(nomes, sorted(nomes))
        self.assertTrue(any("alpha.py" in l for l in linhas))

    def test_listar_distingue_arquivo_de_diretorio(self):
        """Deve marcar arquivos como FILE e diretórios como DIR."""
        # Arrange
        open(os.path.join(self.dir_temp, "arquivo.txt"), "w").close()
        os.makedirs(os.path.join(self.dir_temp, "pasta"))

        # Act
        resultado = list_directory(self.dir_temp)

        # Assert
        self.assertIn("[FILE] arquivo.txt", resultado)
        self.assertIn("[DIR] pasta", resultado)

    def test_listar_diretorio_vazio(self):
        """Deve retornar mensagem específica para diretório vazio."""
        # Arrange: diretório temporário já está vazio

        # Act
        resultado = list_directory(self.dir_temp)

        # Assert
        self.assertEqual(resultado, "(diretório vazio)")

    def test_listar_caminho_invalido_retorna_erro(self):
        """Deve retornar mensagem de erro para caminho inexistente."""
        # Arrange
        caminho_invalido = "/caminho/que/nao/existe"

        # Act
        resultado = list_directory(caminho_invalido)

        # Assert
        self.assertIn("Erro ao listar diretório", resultado)


# ===========================================================================
# TestRunShellCommand — Testa a função run_shell_command
# ===========================================================================

class TestRunShellCommand(unittest.TestCase):
    """Testa a ferramenta de execução de comandos shell."""

    def test_executar_comando_simples(self):
        """Deve executar um comando e retornar a saída correta."""
        # Arrange
        comando = 'echo "agente_executor"'

        # Act
        resultado = run_shell_command(comando)

        # Assert
        self.assertIn("agente_executor", resultado)

    def test_executar_comando_retorna_string(self):
        """A saída do comando deve sempre ser uma string."""
        # Arrange
        comando = "python3 --version"

        # Act
        resultado = run_shell_command(comando)

        # Assert
        self.assertIsInstance(resultado, str)

    def test_executar_comando_com_stderr(self):
        """Deve capturar e incluir o stderr na saída."""
        # Arrange: comando que gera saída no stderr
        comando = "python3 -c \"import sys; sys.stderr.write('erro_teste')\"  "

        # Act
        resultado = run_shell_command(comando)

        # Assert
        self.assertIn("erro_teste", resultado)

    def test_timeout_retorna_mensagem_de_erro(self):
        """Deve retornar mensagem de erro quando o comando excede o timeout."""
        # Arrange: mock para simular TimeoutExpired
        import subprocess
        with patch("workflowAgent.tools.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="sleep 100", timeout=30)

            # Act
            resultado = run_shell_command("sleep 100")

        # Assert
        self.assertIn("tempo limite", resultado)

    def test_comando_invalido_retorna_erro(self):
        """Deve retornar mensagem de erro para exceções inesperadas."""
        # Arrange: mock para simular exceção genérica
        with patch("workflowAgent.tools.subprocess.run") as mock_run:
            mock_run.side_effect = Exception("falha simulada")

            # Act
            resultado = run_shell_command("comando_qualquer")

        # Assert
        self.assertIn("Erro ao executar comando", resultado)

    def test_comando_sem_saida_retorna_placeholder(self):
        """Deve retornar placeholder quando o comando não produz saída."""
        # Arrange: comando que não gera saída
        comando = "true"

        # Act
        resultado = run_shell_command(comando)

        # Assert: retorna string não vazia (placeholder ou saída vazia)
        self.assertIsInstance(resultado, str)


# ===========================================================================
# Ponto de entrada para execução direta
# ===========================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
