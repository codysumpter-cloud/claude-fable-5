import os

class InfrastructureSecurityScanner:
    def __init__(self):
        """Initializes the security audit parser engine."""
        pass

    def read_config_file(self, file_path: str) -> str:
        """
        Reads system logs, network configurations, or docker manifests 
        locally to isolate processing within the operating system.
        """
        if not os.path.exists(file_path):
            return f"Error: Target file '{file_path}' not found."
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def build_audit_prompt(self, context_data: str) -> str:
        """Wraps the target configuration raw text into an actionable security audit prompt."""
        return (
            f"Analyze the following infrastructure data for vulnerabilities, zero-days, "
            f"misconfigurations, or cryptographic flaws:\n\n"
            f"--- START DATA ---\n{context_data}\n--- END DATA ---\n\n"
            f"Provide professional hardening instructions based on this data."
        )
