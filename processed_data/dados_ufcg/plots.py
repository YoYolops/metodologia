import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def save_plots(fig, base_name):
    """Salva a figura apenas em 1080p na pasta ./plots/."""
    plot_dir = './plots/'
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
        
    filename = f"{plot_dir}{base_name}_1080p.png"
    fig.savefig(filename, dpi=140, bbox_inches='tight')
    print(f"Salvo: {filename}")

def plot_data(df, title_tag, file_name):
    """Gera o gráfico padronizado com anos, área da pandemia e legenda inferior."""
    plt.figure(figsize=(15, 9))
    sns.set_style("whitegrid")
    
    cols = ['Alunos Matriculados', 'Professores', 'Ingressantes', 'Graduados']

    # Preparação para o Seaborn (Formato Longo)
    df_melted = df.melt(id_vars=['Período'], value_vars=cols, 
                        var_name='Indicador', value_name='Quantidade')
    
    sns.lineplot(data=df_melted, x='Período', y='Quantidade', 
                 hue='Indicador', marker='o', linewidth=2)

    # --- DESTAQUE DA PANDEMIA ---
    # Sombreamento leve (alpha=0.1) entre 2020.1 e 2022.2
    plt.axvspan('2020.1', '2022.2', color='red', alpha=0.1, label='Período Pandemia (COVID-19)')

    # --- AJUSTE DO EIXO X (Labels de Anos) ---
    periods = df['Período'].unique()
    new_ticks = []
    new_labels = []
    last_year = ""
    for p in periods:
        year = str(p).split('.')[0]
        if year != last_year:
            new_ticks.append(p)
            new_labels.append(year)
            last_year = year

    plt.xticks(ticks=new_ticks, labels=new_labels, rotation=45)
    
    # --- AJUSTE DA LEGENDA (Posição Inferior) ---
    plt.legend(title='Indicadores Acadêmicos', loc='upper center', 
               bbox_to_anchor=(0.5, -0.15), ncol=2, fancybox=True, shadow=True)
    
    plt.title(f'Evolução dos Indicadores UFCG - {title_tag}\nDestaque: Impacto da Pandemia', fontsize=16)
    plt.tight_layout()
    
    save_plots(plt.gcf(), file_name)
    plt.close()

def run_analysis_pipeline():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    all_dfs = []
    
    # Consolidação cronológica
    files = sorted([f for f in os.listdir(current_dir) if f.endswith('.csv')])
    for filename in files:
        df = pd.read_csv(os.path.join(current_dir, filename), encoding='utf-8-sig')
        df['Período'] = os.path.splitext(filename)[0]
        all_dfs.append(df)
    
    if not all_dfs: return
    df_base = pd.concat(all_dfs, ignore_index=True)
    
    # --- 1. PLOT ORIGINAL (Dados Reais) ---
    plot_data(df_base.copy(), "Dados Reais", "ufcg_geral_anual")
    
    # --- 2. PLOT SUAVIZADO TOTAL (Janela de 6 Semestres) ---
    df_smooth_total = df_base.copy()
    cols_to_smooth = ['Alunos Matriculados', 'Professores', 'Ingressantes', 'Graduados']
    
    # Aplica a média móvel em todas as colunas de indicadores
    # window=7 com center=True pega: 3 antes + Atual + 3 depois
    for col in cols_to_smooth:
        df_smooth_total[col] = df_smooth_total[col].rolling(window=7, center=True).mean()
    
    # Remove as bordas nulas (os primeiros e últimos 3 registros da série)
    df_smooth_total = df_smooth_total.dropna(subset=cols_to_smooth)
    
    plot_data(df_smooth_total, "Tendência Suavizada (Janela 6)", "ufcg_geral_total_suavizado")

if __name__ == "__main__":
    run_analysis_pipeline()