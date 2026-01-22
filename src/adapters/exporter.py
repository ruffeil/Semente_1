import os
from datetime import datetime

class DataExporter:
    @staticmethod
    def save_to_markdown(presentation_text, branch):
        """Gera o arquivo para o NotebookLM ou Cliente."""
        os.makedirs('reports', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"reports/REPORT_{branch}_{timestamp}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(presentation_text)
        
        return filename
