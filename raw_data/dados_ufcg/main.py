import os

def process_files_simply():
    # 1. Configuração de caminhos
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.abspath(os.path.join(
        current_dir, '..', '..', 'processed_data', 'dados_ufcg'
    ))

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 2. Iteração sobre os arquivos
    for filename in os.listdir(current_dir):
        if filename.endswith('.csv') and filename != os.path.basename(__file__):
            source_path = os.path.join(current_dir, filename)
            
            # Define o novo nome (últimos 10 caracteres)
            new_name = filename[-10:]
            destination_path = os.path.join(target_dir, new_name)

            try:
                # 3. Processamento direto de texto
                with open(source_path, 'r', encoding='utf-8-sig') as f_in:
                    # Lê todas as linhas
                    lines = f_in.readlines()
                
                # Escreve de volta ignorando a primeira linha (índice 0)
                with open(destination_path, 'w', encoding='utf-8-sig', newline='') as f_out:
                    f_out.writelines(lines[1:])
                
                print(f"Processado: {filename} -> {new_name}")

            except Exception as e:
                print(f"Erro ao processar {filename}: {e}")

if __name__ == "__main__":
    process_files_simply()