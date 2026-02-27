import os
import pandas as pd
import numpy as np
import re

# --- Funções de Manipulação de Dados ---

def clean_string_spaces(text):
    """
    Remove hífens, remove espaços nas bordas e garante apenas 
    um espaço simples entre as palavras.
    """
    # 1. Remove o caractere de hífen '-'
    text = text.replace('-', ' ')
    
    # 2. Divide a string em palavras (o split() sem argumentos remove múltiplos espaços/tabs)
    # 3. Junta as palavras com um único espaço
    return ' '.join(text.split())

def process_course_metadata(df):
    if df is None or 'Curso' not in df.columns:
        return df

    def extract_logic(row):
        course_name = str(row['Curso'])
        course_upper = course_name.upper()
        
        # --- 1. Lógica do TIPO ---
        if '(LIC)' in course_upper or '(LICENCIATURA)' in course_upper:
            tipo = 'LIC'
        elif '(BAC)' in course_upper or '(' not in course_upper:
            tipo = 'BAC'
        else:
            tipo = 'OUTRO'
            
        # --- 2. Lógica do TURNO (Última Ocorrência) ---
        augmented_name = f" {course_name} "
        all_matches = re.findall(r'\s([A-Z])\s', augmented_name)
        turno = all_matches[-1] if all_matches else 'D'
            
        # --- 3. LIMPEZA PROFUNDA DO NOME DO CURSO ---
        # Remove parênteses e conteúdo
        clean_name = re.sub(r'\(.*?\)', '', course_name)
        # Remove letras isoladas (Turnos)
        clean_name = re.sub(r'\s[A-Z]\s', ' ', f" {clean_name} ")
        # Aplica a normalização de hífens e espaços
        clean_name = clean_string_spaces(clean_name)
        
        return pd.Series([clean_name, tipo, turno])

    # Aplica a lógica e atualiza/cria as colunas
    df[['Curso', 'Tipo', 'Turno']] = df.apply(extract_logic, axis=1)
    return df

def instantiate_dataframe(file_path):
    try:
        return pd.read_csv(file_path, skiprows=2, sep=None, engine='python', encoding='utf-8-sig')
    except Exception as e:
        print(f"Erro ao ler {file_path}: {e}")
        return None

def remove_empty_rows(df):
    if df is not None:
        df_replaced = df.replace(r'^\s*$', np.nan, regex=True)
        return df_replaced.dropna(how='any')
    return None

# --- Pipeline de Execução ---

def run_cleaning_pipeline():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.abspath(os.path.join(
        current_dir, '..', '..', 'processed_data', 'ativos_ano_por_curso'
    ))

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(current_dir):
        if filename.endswith('.csv') and filename != os.path.basename(__file__):
            source_path = os.path.join(current_dir, filename)
            
            df = instantiate_dataframe(source_path)
            if df is None: continue
            
            # Executa a limpeza e extração de metadados
            df = process_course_metadata(df)
            df_clean = remove_empty_rows(df)
            
            new_name = filename.split('_', 1)[1] if '_' in filename else filename
            final_path = os.path.join(target_dir, new_name)
            
            df_clean.to_csv(final_path, index=False, encoding='utf-8-sig')
            print(f"Normalizado e Processado: {new_name}")

if __name__ == "__main__":
    run_cleaning_pipeline()