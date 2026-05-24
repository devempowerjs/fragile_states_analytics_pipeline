import os
import time
from utils import setup_directories, get_logger
from cleaning import clean_data, save_styled_excel
from analysis import perform_analysis, save_analysis_excel
from visualization import generate_all_visuals
from report_generator import generate_html_report, generate_pdf_report

logger = get_logger("MainPipeline")

def main():
    start_time = time.time()
    logger.info("==================================================")
    logger.info("STARTING ENTERPRISE DATA ANALYTICS PIPELINE")
    logger.info("==================================================")

    
    logger.info("Step 1: Setting up directory structure...")
    setup_directories()

    input_file = "practice_data.xlsx"
    if not os.path.exists(input_file):
        logger.error(f"Input file {input_file} not found. Exiting.")
        return

    
    logger.info("Step 2: Cleaning and Preprocessing Data...")
    df_cleaned = clean_data(input_file)
    save_styled_excel(df_cleaned, "project_output/cleaned_data/cleaned_fragile_states_2023.xlsx")

    
    logger.info("Step 3: Performing Statistical & Trend Analysis...")
    analysis_results = perform_analysis(df_cleaned)
    save_analysis_excel(analysis_results, "project_output/reports/analysis_results.xlsx")

    
    logger.info("Step 4: Generating Visualizations...")
    generate_all_visuals(analysis_results, "project_output/charts")

    
    logger.info("Step 5: Generating Final Executive Reports...")
    html_report = generate_html_report(analysis_results, "project_output/reports/executive_summary.html")
    if html_report:
        generate_pdf_report(html_report, "project_output/reports/executive_summary.pdf")

    elapsed_time = time.time() - start_time
    logger.info("==================================================")
    logger.info(f"PIPELINE COMPLETED SUCCESSFULLY IN {elapsed_time:.2f} SECONDS.")
    logger.info("==================================================")

if __name__ == "__main__":
    main()
