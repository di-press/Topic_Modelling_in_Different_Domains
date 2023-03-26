"""
Este script utiliza a API do ArXiv através de uma biblioteca em Python
para baixar vários artigos do site ArXiv. Foram selecionadas algumas categorias
arbitrárias. Após realizar o download de alguns milhares de papers por categoria,
estes passam pela etapa de pré-processamento, em que o formato de texto retornado
(usualmente LaTeX para o conteúdo dos artigos) é processado e vários artefatos
irrelevantes são removidos, como comandos LaTeX (por exemplo, $$ e \mathbf),
caracteres matemáticos e/ou letras do alfabeto grego utilizadas para representar
variáveis matemáticas.

Após baixar e processar o conjunto de dados, o resultado se encontra na pasta
arxiv-files, e pode ser utilizado por algoritmos de análise textual.
"""
import pathlib
import re
import shutil
import string
from typing import Iterable

import arxiv
from pylatexenc.latex2text import LatexNodes2Text

def main():
    categories_to_query = {
        "graphics": "cs.GR",
        "vision": "cs.CV",
        "robotics": "cs.RO",
        "artificial-intelligence": "cs.AI",
        "machine-learning": "cs.LG",
        "differential-geometry": "math.DG",
        "numerical-analysis": "math.NA",
        "quantum-physics": "quant-ph",
        "medical-physics": "physics.med-ph",
        "genomics": "q-bio.GN"
    }

    arxiv_papers_path = pathlib.Path("arxiv-files")
    for category, arxiv_category in categories_to_query.items():
        arxiv_search = arxiv.Search(
            query=arxiv_category,
            max_results=3000,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        category_path = arxiv_papers_path / category
        category_path.mkdir(parents=True, exist_ok=True)
        for query_idx, query_result in enumerate(arxiv_search.results()):
            # Título do paper em texto cru. O título é processado tanto para facilitar a
            # a leitura do arquivo quanto para permitir que o título seja usado como nome
            # do arquivo de saída do texto.
            raw_title = query_result.title
            processed_title = raw_title.strip().lower()
            # Remove as pontuações do título
            processed_title = re.sub(r"[^\w\s]", "", processed_title)
            simplified_title = re.split(": |\s", processed_title)
            paper_title = '-'.join(simplified_title)
            
            # Retorna o Abstract do paper baixado em formato cru para ser processado.
            # O Abstract retornado possui caracteres e comandos LaTeX e precisa ser
            # processado.
            raw_latex_abstract = query_result.summary
            
            # Processamento do texto contendo comandos LaTeX para formato de texto
            # simples.
            try: 
                text_abstract = convert_latex_to_plain_text(raw_latex_abstract)
            except:
                print(f"Unexpected error on category {category}, paper: {raw_title}.\nAbstract: {raw_latex_abstract}")
                return
            
            # No entanto, o texto simples sem LaTeX ainda pode conter caracteres não-imprimíveis
            # e caracteres matemáticos que usam formato não-ASCII e precisa ser processado mais
            # uma vez.
            processed_abstract = remove_nonprintable_characters(text_abstract)

            # Escreve o texto lido para um arquivo. O número da query descreve a ordenação decrescente
            # de submissão dos arquivos, isto é, o arquivo 1 foi o mais recentemente submetido no ArXiv
            # na categoria, o arquivo 2 foi o segundo mais recentemente submetido etc.
            paper_filepath = category_path / f"{query_idx+1}.{paper_title}.txt"

            with paper_filepath.open("w") as paper_file:
                paper_file.write(processed_abstract)
            shutil.make_archive("arxiv-papers", "zip", root_dir=arxiv_papers_path)
            return
    
    shutil.make_archive("arxiv-papers", "zip", root_dir=arxiv_papers_path)

def erase_patterns(raw_string: str, patterns_to_replace: Iterable) -> str:
    """
    Remove um conjunto de padrões de uma string, retornando a string processada.

    Args
        raw_string (str): string para ser processada.
        patterns_to_replace (Iterable): Iterável contendo padrões a serem removidos
        da string de entrada raw_string.

    Returns
        processed_string (str): string pós-processamento, em que os padrões de patterns_to_replace
        foram removidos.
    """
    processed_string = raw_string
    for pattern in patterns_to_replace:
        processed_string = processed_string.replace(pattern, "")
    
    return processed_string

def convert_latex_to_plain_text(raw_string: str) -> str:
    """
    Converte uma string contendo caracteres e comandos LaTeX para uma
    string com texto simples.

    Args
        raw_string (str): string de entrada contendo caracteres e comandos LaTeX.
    
    Returns
        (str): string processada para texto simples, com caracteres e comandos LaTeX
        removidos.
    """
    # https://github.com/phfaist/pylatexenc/issues/58
    # De acordo com a issue da biblioteca, alguns comandos de LaTeX ainda não estão
    # 100% suportados e não são plenamente convertidos. Isso pode gerar uma Exception.
    # Então, implementamos uma função que remove manualmente alguns trechos de LaTeX.
    intermediate_string = erase_patterns(raw_string, ("\href", "\\url", "\email"))
    return LatexNodes2Text().latex_to_text(intermediate_string)

def remove_nonprintable_characters(raw_string: str) -> str:
    """
    Retorna a string fornecida sem caracteres não-imprimíveis.

    Args
        raw_string (str): string para ser processada.
    
    Returns
        (str): string pós-processamento, sem caracteres não-imprimíveis.
    """
    printable = set(string.printable)
    # Filtra apenas os caracteres da string de entrada e que também pertencem ao conjunto
    # de caracteres que podem ser impressos
    return ''.join(filter(lambda character: character in printable, raw_string))

if __name__ == "__main__":
    main()