import argparse
from pathlib import Path

#
from advys_estrutura.utils import criar_arquivo, adiciona_linha_ao_arquivo
from advys_estrutura.config import DIR_DESENVOLVIMENTO_REDE, IMAGENS_PY


#
def criar_caminhos_imagem(dir_imagens:Path, arquivo_imagens_py,iniciar=True):
    if iniciar:
        criar_arquivo(arquivo_imagens_py)
    for item in dir_imagens.iterdir():
        if item.is_file() and item.suffix == ".png":
            linha = f"{item.stem[4:]} = home / '{item.relative_to(Path.home())}'"
            adiciona_linha_ao_arquivo(linha, arquivo_imagens_py)

        if item.is_dir():
            criar_caminhos_imagem(item, arquivo_imagens_py, iniciar= False)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Gera atualiza o arquivo imagens.py")
    parser.add_argument("-ci", "--caminho_imagens", help="Caminho para pasta de imagens")
    args = parser.parse_args()


    dir_imagens = DIR_DESENVOLVIMENTO_REDE / "Imagens"
    dir_imagens = Path.home() / "Documents" / "Estrutura" / "Imagens"
    if args.caminho_imagens:
        dir_imagens = Path(args.caminho_imagens)


    criar_caminhos_imagem(dir_imagens, IMAGENS_PY)