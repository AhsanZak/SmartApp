"""
Excel file processor
"""
from typing import Dict, Any
import pandas as pd
import os

from processors.base_processor import BaseProcessor


class ExcelProcessor(BaseProcessor):
    """Processor for Excel files"""
    
    def supports(self, file_extension: str) -> bool:
        """Check if Excel is supported"""
        return file_extension.lower() in ["xlsx", "xls", "csv"]
    
    def process(self, file_path: str) -> Dict[str, Any]:
        """
        Process Excel file and extract data
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            file_ext = file_path.split(".")[-1].lower()
            
            if file_ext == "csv":
                # Read CSV
                df = pd.read_csv(file_path)
                sheets = {"Sheet1": df}
            else:
                # Read Excel
                sheets = pd.read_excel(file_path, sheet_name=None)
            
            # Convert data to text
            text = ""
            for sheet_name, df in sheets.items():
                text += f"\n\n=== {sheet_name} ===\n\n"
                text += df.to_string(index=False)
                text += f"\n\nSummary: {len(df)} rows, {len(df.columns)} columns\n"
                text += f"Columns: {', '.join(df.columns)}\n"
            
            # Get metadata
            total_rows = sum(len(df) for df in sheets.values())
            total_cols = sum(len(df.columns) for df in sheets.values())
            
            metadata = {
                "sheets": len(sheets),
                "total_rows": total_rows,
                "total_columns": total_cols,
                "file_size": os.path.getsize(file_path),
                "file_type": file_ext
            }
            
            return {
                "text": text.strip(),
                "metadata": metadata
            }
            
        except Exception as e:
            raise Exception(f"Error processing Excel: {str(e)}")

