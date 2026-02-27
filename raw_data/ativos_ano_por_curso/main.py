import os
import pandas as pd
import numpy as np

# --- Funções de Manipulação de Dados ---

def instantiate_dataframe(file_path):
    try:
        # skiprows=2: Pula as duas primeiras linhas do arquivo CSV
        # sep=None: Detecta automaticamente se é vírgula ou ponto-e-vírgula
        df = pd.read_csv(
            file_path, 
            skiprows=2, 
            sep=None, 
            engine='python', 
            encoding='utf-8-sig'
        )
        return df
    except Exception as e:
        print(f"Erro ao ler {file_path}: {e}")
        return None

def remove_empty_rows(df):
    """Transforma strings vazias em NaN e remove as linhas."""
    if df is not None:
        # Garante que células com espaços ou vazias sejam tratadas como nulas
        df_replaced = df.replace(r'^\s*$', np.nan, regex=True)
        return df_replaced.dropna(how='any')
    return None

def save_to_destination(df, destination_path):
    try:
        df.to_csv(destination_path, index=False, encoding='utf-8-sig')
        return True
    except Exception as e:
        print(f"Erro ao salvar em {destination_path}: {e}")
        return False

# --- Lógica de Organização ---

def get_new_name(filename):
    try:
        # Mantém a parte após o primeiro '_'
        return filename.split('_', 1)[1]
    except IndexError:
        return filename

def process_and_move_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.abspath(os.path.join(
        current_dir, '..', '..', 'processed_data', 'ativos_ano_por_curso'
    ))

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(current_dir):
        # Processa apenas CSVs e ignora o próprio script Python
        if filename.endswith('.csv') and filename != os.path.basename(__file__):
            source_path = os.path.join(current_dir, filename)
            
            # 1. Carregar pulando as 2 primeiras linhas
            df = instantiate_dataframe(source_path)
            if df is None: continue
            
            # 2. Limpar strings vazias remanescentes
            df_clean = remove_empty_rows(df)
            
            # 3. Salvar no destino com novo nome
            new_name = get_new_name(filename)
            final_path = os.path.join(target_dir, new_name)
            
            if save_to_destination(df_clean, final_path):
                print(f"Processado: {filename} -> {new_name}")

if __name__ == "__main__":
    process_and_move_data()