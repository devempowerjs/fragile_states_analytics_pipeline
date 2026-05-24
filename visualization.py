import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from utils import get_logger, THEME

logger = get_logger("VisualizationModule")


sns.set_theme(style="whitegrid", rc={"axes.facecolor": THEME["background"], "figure.facecolor": "white"})
plt.rcParams['font.family'] = THEME["font_family"]
plt.rcParams['text.color'] = THEME["text"]
plt.rcParams['axes.labelcolor'] = THEME["text"]
plt.rcParams['xtick.color'] = THEME["text"]
plt.rcParams['ytick.color'] = THEME["text"]

def plot_correlation_matrix(correlation_matrix, output_path):
    logger.info("Generating Correlation Matrix Heatmap...")
    plt.figure(figsize=(12, 10))
    
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    
    sns.heatmap(correlation_matrix, mask=mask, cmap=THEME["heatmap_cmap"], 
                vmax=1.0, vmin=-1.0, center=0, square=True, 
                linewidths=.5, cbar_kws={"shrink": .75}, annot=True, fmt=".2f", annot_kws={"size": 8})
    plt.title('Indicator Correlation Matrix', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_top_bottom_bar(df, metric, title, output_path, ascending=False):
    logger.info(f"Generating Bar Chart: {title}")
    plt.figure(figsize=(10, 6))
    
    data = df.sort_values(by=metric, ascending=ascending).head(10)
    
    colors = [THEME["accent"] if ascending else THEME["primary"]] * 10
    sns.barplot(x=metric, y='Country', data=data, palette=colors)
    
    plt.title(title, fontsize=16, fontweight='bold', pad=15)
    plt.xlabel(metric, fontsize=12)
    plt.ylabel('Country', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    
    for index, value in enumerate(data[metric]):
        plt.text(value, index, f' {value:.1f}', va='center', fontsize=10, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_distribution(df, metric, output_path):
    logger.info(f"Generating Distribution KDE: {metric}")
    plt.figure(figsize=(8, 5))
    sns.histplot(df[metric].dropna(), kde=True, color=THEME["secondary"], stat='density', alpha=0.4, linewidth=0)
    sns.kdeplot(df[metric].dropna(), color=THEME["secondary"], linewidth=2)
    
    plt.title(f'Distribution of {metric}', fontsize=14, fontweight='bold')
    plt.xlabel(metric)
    plt.ylabel('Density')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_scatter_relationships(df, x_metric, y_metric, hue_col, output_path):
    logger.info(f"Generating Scatter Plot: {x_metric} vs {y_metric}")
    plt.figure(figsize=(10, 6))
    
    sns.scatterplot(data=df, x=x_metric, y=y_metric, hue=hue_col, 
                    palette='viridis', s=100, alpha=0.8, edgecolor='w')
    
    plt.title(f'{x_metric} vs. {y_metric}', fontsize=16, fontweight='bold')
    plt.xlabel(x_metric, fontsize=12)
    plt.ylabel(y_metric, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title=hue_col, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def generate_all_visuals(analysis_results, charts_dir="project_output/charts"):
    logger.info("Generating all visual assets...")
    
    if 'correlation_matrix' in analysis_results:
        plot_correlation_matrix(analysis_results['correlation_matrix'], f"{charts_dir}/correlation_heatmap.png")
        
    if 'clustered_data' in analysis_results:
        df = analysis_results['clustered_data']
        plot_top_bottom_bar(df, 'Total', 'Top 10 Most Fragile States', f"{charts_dir}/top_10_fragile.png", ascending=False)
        plot_top_bottom_bar(df, 'Total', 'Top 10 Most Stable States', f"{charts_dir}/top_10_stable.png", ascending=True)
        
        plot_distribution(df, 'Total', f"{charts_dir}/total_score_distribution.png")
        
        if 'E1: Economy' in df.columns and 'P1: State Legitimacy' in df.columns:
            plot_scatter_relationships(df, 'E1: Economy', 'P1: State Legitimacy', 'Risk_Tier', f"{charts_dir}/economy_vs_legitimacy.png")

    logger.info("All visualizations generated.")

if __name__ == "__main__":
    from analysis import perform_analysis
    from cleaning import clean_data
    df = clean_data("practice_data.xlsx")
    results = perform_analysis(df)
    generate_all_visuals(results)
