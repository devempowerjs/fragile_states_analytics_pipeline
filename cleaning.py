import pandas as pd
import numpy as np
from utils import get_logger

logger = get_logger("CleaningModule")

def clean_data(input_path):
    logger.info(f"Loading data from {input_path}")
    try:
        df = pd.read_excel(input_path)
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        raise

    
    logger.info("Standardizing column names...")
    original_columns = df.columns.tolist()
    df.columns = [col.strip().replace("\n", " ") for col in df.columns]
    
    if 'Rank' in df.columns:
        logger.info("Cleaning Rank column...")
        df['Rank'] = df['Rank'].astype(str).str.replace(r'\D', '', regex=True)
        df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
        
    missing_counts = df.isnull().sum()
    if missing_counts.sum() > 0:
        logger.warning(f"Found missing values:\n{missing_counts[missing_counts > 0]}")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        df.fillna("Unknown", inplace=True)
        logger.info("Missing values imputed.")

    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    if len(df) < initial_rows:
        logger.info(f"Removed {initial_rows - len(df)} duplicate rows.")

    logger.info("Validating indicator boundaries (0 to 10)...")
    indicator_cols = [col for col in df.columns if ":" in col]
    for col in indicator_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].clip(lower=0, upper=10)

    logger.info("Data cleaning completed successfully.")
    return df

def save_styled_excel(df, output_path):
    logger.info(f"Saving styled Excel to {output_path}")
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Cleaned Data', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Cleaned Data']
        
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#2980B9',
            'font_color': 'white',
            'border': 1
        })
        
        cell_format = workbook.add_format({'border': 1})
        
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
        for col_num, col_name in enumerate(df.columns):
            column_len = max(df[col_name].astype(str).map(len).max(), len(col_name)) + 2
            worksheet.set_column(col_num, col_num, min(column_len, 30), cell_format)
            
        if 'Total' in df.columns:
            total_col_idx = df.columns.get_loc('Total')
            col_letter = chr(65 + total_col_idx)
            worksheet.conditional_format(f'{col_letter}2:{col_letter}{len(df)+1}',
                                      {'type': 'data_bar', 'bar_color': '#E74C3C'})
                                      
    logger.info("Styled Excel saved successfully.")

if __name__ == "__main__":
    from utils import setup_directories
    setup_directories()
    df_clean = clean_data("practice_data.xlsx")
    save_styled_excel(df_clean, "project_output/cleaned_data/cleaned_fragile_states_2023.xlsx")
