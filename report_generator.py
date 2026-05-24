import os
import datetime
from jinja2 import Environment, FileSystemLoader, Template
from utils import get_logger

logger = get_logger("ReportGenerator")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise Analytics Report: Fragile States Index</title>
    <style>
        :root {
            --primary-color: #2980B9;
            --secondary-color: #27AE60;
            --background: #f4f7f6;
            --text-color: #2C3E50;
            --card-bg: #ffffff;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--background);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }
        header {
            background-color: var(--primary-color);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .container {
            width: 85%;
            margin: 0 auto;
            max-width: 1200px;
            padding: 40px 0;
        }
        .section {
            background: var(--card-bg);
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .section h2 {
            color: var(--primary-color);
            border-bottom: 2px solid var(--background);
            padding-bottom: 10px;
            margin-top: 0;
        }
        .kpi-container {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
        }
        .kpi-card {
            background: var(--primary-color);
            color: white;
            flex: 1;
            margin: 0 10px;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .kpi-card h3 { margin: 0; font-size: 1.2em; opacity: 0.9; }
        .kpi-card p { margin: 10px 0 0; font-size: 2em; font-weight: bold; }
        
        .chart-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .chart-box {
            text-align: center;
        }
        .chart-box img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            border: 1px solid #eee;
        }
        .full-width-chart {
            text-align: center;
            margin-top: 20px;
        }
        .full-width-chart img {
            max-width: 80%;
            border-radius: 8px;
            border: 1px solid #eee;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: var(--primary-color);
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        footer {
            text-align: center;
            padding: 20px;
            color: var(--muted);
            font-size: 0.9em;
            background-color: var(--card-bg);
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <header>
        <h1>Enterprise Data Analytics Report</h1>
        <p>Fragile States Index Analysis | Generated on {{ date }}</p>
    </header>

    <div class="container">
        
        <div class="section">
            <h2>Executive Summary</h2>
            <div class="kpi-container">
                <div class="kpi-card">
                    <h3>Total Countries Analyzed</h3>
                    <p>{{ total_countries }}</p>
                </div>
                <div class="kpi-card" style="background: #E74C3C;">
                    <h3>Highest Risk Score</h3>
                    <p>{{ highest_score }} ({{ most_fragile_country }})</p>
                </div>
                <div class="kpi-card" style="background: #27AE60;">
                    <h3>Lowest Risk Score</h3>
                    <p>{{ lowest_score }} ({{ most_stable_country }})</p>
                </div>
            </div>
            <p>This automated enterprise report provides a comprehensive analysis of the Fragile States Index dataset. The data was cleaned, anomalies were handled, and machine learning (K-Means Clustering) was applied to categorize countries into distinct risk tiers.</p>
        </div>

        <div class="section">
            <h2>Rankings Overview</h2>
            <div class="chart-grid">
                <div class="chart-box">
                    <h3>Top 10 Most Fragile States</h3>
                    <img src="../charts/top_10_fragile.png" alt="Top 10 Fragile">
                </div>
                <div class="chart-box">
                    <h3>Top 10 Most Stable States</h3>
                    <img src="../charts/top_10_stable.png" alt="Top 10 Stable">
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Statistical Distributions & Clustering</h2>
            <p>Countries were grouped into 4 distinct risk tiers based on 12 socio-economic and political indicators using K-Means Clustering.</p>
            <div class="chart-grid">
                <div class="chart-box">
                    <img src="../charts/total_score_distribution.png" alt="Score Distribution">
                </div>
                <div class="chart-box">
                    <img src="../charts/economy_vs_legitimacy.png" alt="Economy vs Legitimacy">
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Indicator Correlations</h2>
            <p>The correlation matrix below illustrates the relationships between various pressures, such as economic inequality, state legitimacy, and demographic pressures. A value closer to 1.0 indicates a strong positive correlation.</p>
            <div class="full-width-chart">
                <img src="../charts/correlation_heatmap.png" alt="Correlation Matrix">
            </div>
        </div>
        
        <div class="section">
            <h2>Data Sample (Top 5 Fragile)</h2>
            {{ top_5_html | safe }}
        </div>

    </div>

    <footer>
        &copy; {{ year }} Mayank Raj (devempowerjs) All rights reserved. | <a href="https://github.com/devempowerjs" target="_blank">GitHub Profile</a>
    </footer>
</body>
</html>
"""

def generate_html_report(analysis_results, output_path="project_output/reports/executive_summary.html"):
    logger.info("Generating HTML Report...")
    
    df = analysis_results.get('clustered_data')
    if df is None:
        logger.error("No clustered data found to generate report.")
        return
        
    top_fragile = analysis_results['top_10_fragile']
    top_stable = analysis_results['top_10_stable']
    
    template = Template(HTML_TEMPLATE)
    
    html_content = template.render(
        date=datetime.datetime.now().strftime("%B %d, %Y"),
        year=datetime.datetime.now().year,
        total_countries=len(df),
        highest_score=top_fragile.iloc[0]['Total'],
        most_fragile_country=top_fragile.iloc[0]['Country'],
        lowest_score=top_stable.iloc[0]['Total'],
        most_stable_country=top_stable.iloc[0]['Country'],
        top_5_html=top_fragile.head(5)[['Country', 'Rank', 'Total', 'Risk_Tier']].to_html(index=False, classes='table table-striped')
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    logger.info(f"HTML Report successfully saved to {output_path}")
    return output_path

def generate_pdf_report(html_path, output_path="project_output/reports/executive_summary.pdf"):
    logger.info("Attempting to generate PDF Report using Playwright...")
    try:
        import playwright.sync_api
        sync_playwright = playwright.sync_api.sync_playwright
        
        abs_html_path = f"file:///{os.path.abspath(html_path).replace(chr(92), '/')}"
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(abs_html_path, wait_until='networkidle')
            page.pdf(path=output_path, format="A4", print_background=True, margin={'top': '20px', 'right': '20px', 'bottom': '20px', 'left': '20px'})
            browser.close()
            
        logger.info(f"PDF Report successfully saved to {output_path}")
    except ImportError:
        logger.error("Playwright is not installed. Skipping PDF generation.")
    except Exception as e:
        logger.error(f"Failed to generate PDF: {e}")

if __name__ == "__main__":
    from analysis import perform_analysis
    from cleaning import clean_data
    df = clean_data("practice_data.xlsx")
    results = perform_analysis(df)
    html_path = generate_html_report(results)
    if html_path:
        generate_pdf_report(html_path)
