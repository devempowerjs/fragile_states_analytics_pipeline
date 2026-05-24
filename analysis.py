import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from utils import get_logger

logger = get_logger("AnalysisModule")

def perform_analysis(df):
    logger.info("Starting statistical analysis and clustering...")
    analysis_results = {}

    logger.info("Calculating summary statistics...")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    summary_stats = df[numeric_cols].describe().T
    summary_stats['skewness'] = df[numeric_cols].skew()
    analysis_results['summary_stats'] = summary_stats

    logger.info("Calculating correlations...")
    indicator_cols = [col for col in df.columns if ":" in col]
    if indicator_cols:
        correlation_matrix = df[indicator_cols].corr()
        analysis_results['correlation_matrix'] = correlation_matrix
    else:
        logger.warning("No indicator columns found for correlation.")
    logger.info("Performing K-Means clustering...")
    if len(indicator_cols) > 0:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df[indicator_cols].fillna(0))
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        df['Risk_Cluster_ID'] = kmeans.fit_predict(X_scaled)
        cluster_means = df.groupby('Risk_Cluster_ID')['Total'].mean().sort_values(ascending=False)
        labels = ['Alert', 'Warning', 'Stable', 'Sustainable']
        cluster_map = {cluster_id: label for cluster_id, label in zip(cluster_means.index, labels)}
        df['Risk_Tier'] = df['Risk_Cluster_ID'].map(cluster_map)
        
        analysis_results['clustered_data'] = df
        
        top_10_fragile = df.nlargest(10, 'Total')
        top_10_stable = df.nsmallest(10, 'Total')
        analysis_results['top_10_fragile'] = top_10_fragile
        analysis_results['top_10_stable'] = top_10_stable
        
        logger.info("Analysis completed.")
    else:
        logger.warning("Clustering skipped due to missing indicator columns.")
        analysis_results['clustered_data'] = df

    return analysis_results

def save_analysis_excel(analysis_results, output_path):
    logger.info(f"Saving analysis to {output_path}")
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        if 'clustered_data' in analysis_results:
            analysis_results['clustered_data'].to_excel(writer, sheet_name='Clustered Data', index=False)
        if 'summary_stats' in analysis_results:
            analysis_results['summary_stats'].to_excel(writer, sheet_name='Summary Statistics')
        if 'correlation_matrix' in analysis_results:
            analysis_results['correlation_matrix'].to_excel(writer, sheet_name='Correlation Matrix')
        if 'top_10_fragile' in analysis_results:
            analysis_results['top_10_fragile'][['Country', 'Rank', 'Total', 'Risk_Tier']].to_excel(writer, sheet_name='Top 10 Fragile', index=False)
        if 'top_10_stable' in analysis_results:
            analysis_results['top_10_stable'][['Country', 'Rank', 'Total', 'Risk_Tier']].to_excel(writer, sheet_name='Top 10 Stable', index=False)
        
        workbook = writer.book
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            worksheet.set_column('A:A', 20)
            worksheet.set_column('B:Z', 15)
            
    logger.info("Analysis Excel saved.")

if __name__ == "__main__":
    from cleaning import clean_data
    df = clean_data("practice_data.xlsx")
    results = perform_analysis(df)
    save_analysis_excel(results, "project_output/reports/analysis_results.xlsx")
