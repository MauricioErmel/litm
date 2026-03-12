"""
Script para dividir o arquivo traduzir.html em múltiplos arquivos de ~250 linhas,
sem quebrar blocos HTML no meio (parágrafos, divs, listas, tabelas, etc).

Estratégia: Percorre o arquivo linha a linha e identifica "pontos seguros de corte",
que são posições entre blocos HTML de nível similar. Nunca corta no meio de uma tag
de bloco aberta (entre <p> e </p>, entre <div> e </div>, etc).
"""

import re
import os

INPUT_FILE = "traduzir.html"
OUTPUT_PREFIX = "traduzir"
TARGET_LINES = 250

# Tags de bloco que NÃO devem ser quebradas no meio.
BLOCK_TAGS = {
    "p", "div", "ul", "ol", "li", "table", "thead", "tbody", "tr",
    "blockquote", "pre", "section", "article", "aside", "nav",
    "header", "footer", "figure", "figcaption", "details", "summary",
    "h1", "h2", "h3", "h4", "h5", "h6"
}


def find_safe_split_points(lines):
    """
    Retorna uma lista de índices de linhas onde é seguro fazer o corte.
    Um ponto é seguro quando não estamos dentro de nenhum bloco que
    não pode ser quebrado (ou seja, depth == 0 para nossos blocos rastreados).
    """
    safe_points = []
    depth = 0  # profundidade de aninhamento em tags de bloco

    for i, line in enumerate(lines):
        # Encontra todas as tags de abertura e fechamento na linha
        # Tag de abertura: <tag ...> (sem ser auto-fechamento />)
        opens = re.findall(r'<(\w+)[\s>/]', line)
        closes = re.findall(r'</(\w+)\s*>', line)

        # Processa aberturas
        for tag in opens:
            tag_lower = tag.lower()
            if tag_lower in BLOCK_TAGS:
                # Verifica se não é auto-fechamento
                # Padrão: <tag ... />
                if not re.search(rf'<{tag}[^>]*/\s*>', line, re.IGNORECASE):
                    depth += 1

        # Processa fechamentos
        for tag in closes:
            tag_lower = tag.lower()
            if tag_lower in BLOCK_TAGS:
                depth -= 1
                if depth < 0:
                    depth = 0  # proteção contra HTML malformado

        # Após processar a linha, se depth == 0, é um ponto seguro de corte
        # (o corte seria APÓS esta linha, ou seja, entre esta e a próxima)
        if depth == 0:
            safe_points.append(i)

    return safe_points


def split_html(input_path, output_prefix, target_lines):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_lines = len(lines)
    print(f"Total de linhas no arquivo: {total_lines}")

    # Encontra pontos seguros de corte
    safe_points = find_safe_split_points(lines)
    print(f"Pontos seguros de corte encontrados: {len(safe_points)}")

    # Determina onde cortar: a cada ~target_lines, escolhe o ponto seguro mais próximo
    cuts = [0]  # início do arquivo
    line_cursor = 0

    while line_cursor + target_lines < total_lines:
        ideal_cut = line_cursor + target_lines

        # Encontra o ponto seguro mais próximo do corte ideal
        best_point = None
        best_distance = float('inf')
        for sp in safe_points:
            if sp <= line_cursor:
                continue  # já passou deste ponto
            distance = abs(sp - ideal_cut)
            if distance < best_distance:
                best_distance = distance
                best_point = sp
            elif sp > ideal_cut + target_lines:
                break  # muito longe, para de procurar

        if best_point is not None and best_point > line_cursor:
            cuts.append(best_point + 1)  # +1 porque o corte é APÓS a linha do safe_point
            line_cursor = best_point + 1
        else:
            # Se não há ponto seguro, força o corte (fallback)
            cuts.append(ideal_cut)
            line_cursor = ideal_cut

    # Gera os arquivos
    output_dir = os.path.dirname(input_path) or "."
    num_parts = len(cuts)
    print(f"\nDividindo em {num_parts} partes:\n")

    for i in range(num_parts):
        start = cuts[i]
        end = cuts[i + 1] if i + 1 < num_parts else total_lines
        part_lines = lines[start:end]
        num_lines = len(part_lines)
        output_name = f"{output_prefix} ({i + 1}).html"
        output_path = os.path.join(output_dir, output_name)

        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(part_lines)

        # Mostra um preview do conteúdo
        preview = ""
        for pl in part_lines:
            stripped = pl.strip()
            if stripped:
                preview = stripped[:80]
                break

        print(f"  {output_name}: linhas {start + 1}-{end} ({num_lines} linhas)")
        print(f"    Início: {preview}")

    print(f"\nConcluído! {num_parts} arquivos criados.")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, INPUT_FILE)

    if not os.path.exists(input_path):
        print(f"Erro: Arquivo '{INPUT_FILE}' não encontrado em {script_dir}")
    else:
        # Remove arquivos de saída anteriores
        for f in os.listdir(script_dir):
            if re.match(rf'^{re.escape(OUTPUT_PREFIX)} \(\d+\)\.html$', f):
                os.remove(os.path.join(script_dir, f))
                print(f"  Removido: {f}")
        print()

        split_html(input_path, OUTPUT_PREFIX, TARGET_LINES)
