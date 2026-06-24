from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
import io
import json
import models
from services import gemini_service

def parse_and_clean_csv(csv_text: str) -> pd.DataFrame:
    """
    Parses and cleans raw CSV text, returning a Pandas DataFrame.
    """
    try:
        # Load CSV using pandas
        df = pd.read_csv(io.StringIO(csv_text))
        
        # Clean column names (strip whitespace)
        df.columns = [col.strip() for col in df.columns]
        
        # Clean string columns: strip whitespace
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).str.strip()
            
        # Fill missing numeric values with 0, categorical with 'N/A'
        for col in df.columns:
            if pydtype_is_numeric(df[col]):
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna("N/A")
                
        return df
    except Exception as e:
        raise ValueError(f"Error parsing CSV data: {str(e)}")

def pydtype_is_numeric(series: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(series)

def generate_insights_from_csv(db: Session, csv_text: str, filename: str, question: str = "") -> dict:
    """
    Processes CSV data, calculates statistics using Pandas,
    and calls Gemini to get narrative insights and forecast projection.
    Saves the report to the database.
    """
    df = parse_and_clean_csv(csv_text)
    
    # Calculate statistics
    num_rows = len(df)
    columns = list(df.columns)
    
    # Compute descriptive statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    
    stats_summary = {
        "rows_count": num_rows,
        "columns": columns,
        "numeric_summary": {}
    }
    
    for col in numeric_cols:
        stats_summary["numeric_summary"][col] = {
            "sum": float(df[col].sum()),
            "mean": float(df[col].mean()),
            "min": float(df[col].min()),
            "max": float(df[col].max())
        }
        
    # Build a small text representation of the dataset for Gemini
    # (Send first 15 rows and the stats summary to keep it efficient)
    sample_data = df.head(15).to_dict(orient="records")
    
    context_payload = {
        "statistics": stats_summary,
        "sample_rows": sample_data
    }
    
    # Generate insights using Gemini
    analysis_result = gemini_service.generate_csv_insights(
        csv_data=json.dumps(context_payload),
        question=question
    )
    
    # Save the report in the database
    db_report = models.AnalyticsReport(
        filename=filename,
        analysis_result=analysis_result.get("analysis", ""),
        chart_data_json=json.dumps(analysis_result.get("forecastData", []))
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    # Return structure
    return {
        "report_id": db_report.id,
        "filename": db_report.filename,
        "stats": stats_summary,
        "sample_data": df.head(10).to_dict(orient="records"),
        "analysis": db_report.analysis_result,
        "forecastData": analysis_result.get("forecastData", [])
    }
