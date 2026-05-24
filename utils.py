import os
import logging

def setup_directories(base_path="project_output"):
    """Creates the standard directory structure for the enterprise report."""
    directories = [
        f"{base_path}/cleaned_data",
        f"{base_path}/reports",
        f"{base_path}/charts",
        f"{base_path}/logs",
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def get_logger(name="AnalyticsLogger", log_file="project_output/logs/pipeline.log"):
    """Sets up a professional logger."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    
    return logger


THEME = {
    "background": "#f4f7f6",
    "text": "#2C3E50",
    "primary": "#2980B9",
    "secondary": "#27AE60",
    "accent": "#E74C3C",
    "muted": "#95A5A6",
    "heatmap_cmap": "YlGnBu",
    "font_family": "sans-serif"
}
