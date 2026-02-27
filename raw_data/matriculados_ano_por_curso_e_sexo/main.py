import os
import re
import pandas as pd
import io

def clean_raw_text(file_path):
    """Filtra as linhas e remove os 8 dígitos iniciais para alinhar as colunas."""
    header = "Curso,Feminino,Masculino,Total\n"
    cleaned_lines = [header]
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            if re.match(r'^\d{8}', line):
                # Remove os 8 dígitos e a vírgula/espaço subsequente
                content_only = line[9:] if line[8] == ',' else line[8:]
                cleaned_lines.append(content_only.strip() + "\n")
    return "".join(cleaned_lines)

def transform_course_name(course_name):
    """Limpeza avançada e padronização de nomes (Letras, Pedagogia, etc)."""
    text = str(course_name).upper()
    
    # --- REGRA DE UNIFICAÇÃO POR PALAVRA-CHAVE ---
    # Se o curso contiver qualquer uma dessas palavras, vira apenas a palavra
    keywords_to_unify = ['LETRAS', 'PEDAGOGIA']
    
    for key in keywords_to_unify:
        if key in text:
            return key
    
    # --- LIMPEZA PADRÃO (Para os outros cursos) ---
    # 1. Deletar parênteses (fechados e soltos)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\(\S*', '', text)
    
    # 2. Deletar apenas a ÚLTIMA letra maiúscula isolada (Turno)
    augmented = f" {text} "
    matches = list(re.finditer(r'\s([A-Z])\s', augmented))
    if matches:
        start, end = matches[-1].span()
        augmented = augmented[:start] + " " + augmented[end:]
        text = augmented
    
    # 3. Limpeza final: hífens e normalização de espaços
    text = text.replace('-', ' ')
    text = " ".join(text.split())
    
    return text

def run_enrollment_pipeline():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.abspath(os.path.join(
        current_dir, '..', '..', 'processed_data', 'matriculados_ano_por_curso_e_sexo'
    ))

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(current_dir):
        if filename.endswith('.csv') and filename != os.path.basename(__file__):
            source_path = os.path.join(current_dir, filename)
            
            raw_content = clean_raw_text(source_path)
            df = pd.read_csv(io.StringIO(raw_content), sep=',', engine='python')

            if all(col in df.columns for col in ['Curso', 'Feminino', 'Masculino', 'Total']):
                # Aplica transformações e unificações
                df['Curso'] = df['Curso'].apply(transform_course_name)
                
                # Conversão numérica para garantir a soma correta
                for col in ['Feminino', 'Masculino', 'Total']:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

                # Fusão: Agrupa por 'Curso' (agora com Pedagogia e Letras unificados) e soma
                df_fused = df.groupby('Curso', as_index=False).agg({
                    'Feminino': 'sum',
                    'Masculino': 'sum',
                    'Total': 'sum'
                })
                
                final_path = os.path.join(target_dir, filename)
                df_fused.to_csv(final_path, index=False, encoding='utf-8-sig')
                print(f"Processado: {filename}")

if __name__ == "__main__":
    run_enrollment_pipeline()