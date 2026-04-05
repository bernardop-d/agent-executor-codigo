import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Garante que o Python encontra o módulo workflowAgent
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflowAgent.tools import read_file, write_file, list_directory, run_shell_command


class TestReadFile(unittest.TestCase):

    def test_ler_arquivo_que_existe(self):
        # Cria um arquivo temporário com um texto conhecido
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("olá mundo")
            caminho = f.name

        resultado = read_file(caminho)

        self.assertEqual(resultado, "olá mundo")
        os.unlink(caminho)  # apaga o arquivo temporário

    def test_ler_arquivo_que_nao_existe(self):
        resultado = read_file("/arquivo/que/nao/existe.txt")

        # Deve retornar uma mensagem de erro, não explodir
        self.assertIn("Erro", resultado)


class TestWriteFile(unittest.TestCase):

    def setUp(self):
        # Cria uma pasta temporária para usar nos testes
        self.pasta_temp = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.pasta_temp, ignore_errors=True)

    def test_criar_arquivo_com_conteudo(self):
        caminho = os.path.join(self.pasta_temp, "teste.txt")

        resultado = write_file(caminho, "conteúdo do teste")

        # O arquivo deve existir após a chamada
        self.assertTrue(os.path.exists(caminho))
        self.assertIn("salvo", resultado)

    def test_criar_subpastas_automaticamente(self):
        # O caminho tem uma subpasta que ainda não existe
        caminho = os.path.join(self.pasta_temp, "nova_pasta", "arquivo.txt")

        write_file(caminho, "texto qualquer")

        # A subpasta deve ter sido criada junto com o arquivo
        self.assertTrue(os.path.exists(caminho))


class TestListDirectory(unittest.TestCase):

    def setUp(self):
        self.pasta_temp = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.pasta_temp, ignore_errors=True)

    def test_listar_pasta_com_arquivos(self):
        # Cria dois arquivos na pasta temporária
        open(os.path.join(self.pasta_temp, "a.txt"), "w").close()
        open(os.path.join(self.pasta_temp, "b.txt"), "w").close()

        resultado = list_directory(self.pasta_temp)

        self.assertIn("a.txt", resultado)
        self.assertIn("b.txt", resultado)

    def test_listar_pasta_vazia(self):
        resultado = list_directory(self.pasta_temp)

        self.assertEqual(resultado, "(diretório vazio)")

    def test_listar_pasta_que_nao_existe(self):
        resultado = list_directory("/pasta/que/nao/existe")

        self.assertIn("Erro", resultado)


class TestRunShellCommand(unittest.TestCase):

    def test_rodar_comando_simples(self):
        # O comando echo deve retornar o texto passado
        resultado = run_shell_command('echo "funcionou"')

        self.assertIn("funcionou", resultado)

    def test_timeout_retorna_erro(self):
        import subprocess
        # Simula o que acontece quando o comando demora demais
        with patch("workflowAgent.tools.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="sleep 999", timeout=30)

            resultado = run_shell_command("sleep 999")

        self.assertIn("tempo limite", resultado)


if __name__ == "__main__":
    unittest.main(verbosity=2)
