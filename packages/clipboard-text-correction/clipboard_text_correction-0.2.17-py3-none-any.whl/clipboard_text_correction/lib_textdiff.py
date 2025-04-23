#!/usr/bin/python3

import difflib
import re


import difflib
import re

def initial_markup(text_old, text_new):
    # Tokenização melhorada para LaTeX
    def tokenize(text):
        # Padrão que captura:
        # 1. Comandos LaTeX (\comando{...})
        # 2. Palavras com apóstrofos/hífens (incluindo apóstrofo curvo)
        # 3. Espaços
        # 4. Pontuação e outros caracteres
        return re.findall(
            r'(\\[a-z]+\{[^}]*\}|[\w’\'\-]+|\s+|[^\w\s])', 
            text,
            flags=re.UNICODE
        )
    
    tokens_old = tokenize(text_old)
    tokens_new = tokenize(text_new)
    
    matcher = difflib.SequenceMatcher(None, tokens_old, tokens_new)
    result = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            result.extend(tokens_new[j1:j2])
            continue
        
        old_text = ''.join(tokens_old[i1:i2])
        new_text = ''.join(tokens_new[j1:j2])
        
        # Sempre usa \replaced, mesmo que um lado esteja vazio
        replacement = r'\replaced{' + new_text + '}{' + old_text + '}'
        
        # Verificação especial para evitar replaced vazios
        if new_text or old_text:
            result.append(replacement)
    
    return ''.join(result)

def simplify_newline_replaced(text):
    """
    Simplifica \replaced{\n}{\n...} para apenas \n
    Exemplo:
    \replaced{\n}{\n   } → \n
    \replaced{\n}{\n\t} → \n
    """
    return re.sub(
        r'\\replaced\{\n\}\{\n\s*\}',  # Padrão: \replaced{\n}{\n...}
        '\n',                          # Substitui por \n
        text
    )

def simplify_to_added(text):
    """
    Transforma \replaced{novo}{} em \added{novo}
    Mantém todos os outros \replaced intactos
    """
    def replacement(match):
        novo_texto = match.group(1)
        velho_texto = match.group(2)
        
        # Se o texto antigo estiver vazio ou só contiver espaços
        if not velho_texto.strip():
            return r'\added{' + novo_texto + '}'
        return match.group(0)  # Mantém o \replaced original
    
    # Regex que captura \replaced{novo}{velho}
    pattern = re.compile(
        r'\\replaced\{(.*?)\}\{(.*?)\}',
        re.DOTALL  # Para capturar quebras de linha
    )
    
    return pattern.sub(replacement, text)

def clean_empty_added(text):
    """
    Remove APENAS \added{} literalmente vazios (nada entre as chaves)
    Mantém \added{ }, \added{\n}, \added{texto}, etc.
    """
    return re.sub(
        r'\\added\{\}',  # Apenas captura \added{} exatamente vazio
        '', 
        text
    )


def clean_whitespace_added(text):
    """
    Remove \added{} que contém apenas espaços em branco (espaços, tabs, quebras de linha),
    mantendo o conteúdo original de espaços.
    Exemplos:
    \added{ } → " "
    \added{\t} → "\t"
    \added{\n} → "\n"
    \added{ \n \n } → " \n \n "
    \added{texto} → mantém \added{texto}
    """
    def replacement(match):
        content = match.group(1)
        # Verifica se contém apenas whitespace (espaços, tabs, quebras de linha)
        if re.fullmatch(r'\s+', content):
            return content  # Mantém os espaços originais
        return match.group(0)  # Mantém o \added intacto
    
    return re.sub(
        r'\\added\{(.*?)\}',
        replacement,
        text,
        flags=re.DOTALL
    )
    
def clean_added_newlines(text):
    """
    Remove tags \added{...} quando contém apenas quebras de linha (\n),
    preservando exatamente o mesmo número de quebras.
    Exemplos:
    \added{\n}       → \n
    \added{\n\n\n}   → \n\n\n
    \added{ texto}   → mantém \added{ texto}
    \added{\n texto} → mantém \added{\n texto}
    """
    def replacement(match):
        content = match.group(1)
        # Verifica se contém APENAS quebras de linha (com ou sem espaços entre elas)
        if re.fullmatch(r'(\s*\n\s*)+', content):
            # Retorna apenas as quebras de linha (preservando quantidade)
            return re.sub(r'[^\n]', '', content)
        return match.group(0)  # Mantém o \added original
    
    return re.sub(
        r'\\added\{(.*?)\}',
        replacement,
        text,
        flags=re.DOTALL
    )

def extract_newlines_from_added(text):
    """
    Move quebras de linha do interior para o exterior de \added{}:
    \added{\nTexto} → \n\added{Texto}
    \added{\n\nTexto} → \n\n\added{Texto}
    Mantém o restante inalterado.
    """
    def replacement(match):
        full_match = match.group(0)
        content = match.group(1)
        
        # Encontra todas as quebras de linha no início do conteúdo
        leading_newlines = re.match(r'^(\n+)', content)
        
        if leading_newlines:
            newlines = leading_newlines.group(1)
            remaining_content = content[len(newlines):]
            return f"{newlines}\\added{{{remaining_content}}}"
        
        return full_match
    
    return re.sub(
        r'\\added\{(\n+.*?)\}',  # Captura \added{\n...} ou \added{\n\n...} etc.
        replacement,
        text,
        flags=re.DOTALL
    )

def simplify_to_deleted(text):
    """
    Transforma \replaced{}{velho} em \deleted{velho}
    Mantém todos os outros \replaced intactos
    """
    def replacement(match):
        new_text = match.group(1)
        old_text = match.group(2)
        
        # Se o novo texto estiver vazio ou só contiver espaços
        if not new_text.strip():
            return r'\deleted{' + old_text + '}'
        return match.group(0)  # Mantém o \replaced original
    
    # Regex que captura \replaced{novo}{velho}
    pattern = re.compile(
        r'\\replaced\{(.*?)\}\{(.*?)\}',
        re.DOTALL  # Para capturar quebras de linha
    )
    
    return pattern.sub(replacement, text)


def mark_text_diff(old_text, new_text):
    step = initial_markup(old_text, new_text)
    #print(step)
    step = simplify_newline_replaced(step)

    step = simplify_to_added(step)

    step = clean_whitespace_added(step)
    step = extract_newlines_from_added(step)
    step = clean_empty_added(step)
    step = clean_added_newlines(step)
    
    step = simplify_to_deleted(step)
    
    return step
    
if __name__ == '__main__':
    old_text = """
In recent years, deep learning has emerged as a promising tool in medical imaging, allowing significant advances in automated diagnosis \cite{chan2020computer} and medical image segmentation \cite{hesamian2019deep}. Several studies have explored its application in kidney stone detection \cite{hameed2021artificial}, prediction of treatment outcomes \cite{suarez2020current}, and estimation of stone composition \cite{kim2022prediction}. Despite these advances, a major problem remains: the scarcity of manually annotated datasets for training and validating segmentation models. This limitation arises from the difficulty of acquiring high-quality labeled data given the expertise required and the time associated with manual annotation.
    """
    new_text = """
In recent years, deep learning has emerged as a promising tool in medical imaging, allowing for significant advances in automated diagnosis \cite{chan2020computer} and medical image segmentation \cite{hesamian2019deep}. Several studies have explored its application in detecting kidney stones \cite{hameed2021artificial}, predicting treatment outcomes \cite{suarez2020current}, and estimating stone composition \cite{kim2022prediction}. Despite these advances, a major problem persists: the scarcity of manually annotated datasets for training and validating segmentation models. This limitation stems from difficulty of acquiring high-quality labeled data, given the expertise required and the time associated with manual annotation.
    """


    step3 = mark_text_diff(old_text, old_text)
    print(step3)
