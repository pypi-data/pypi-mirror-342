# zennix/core/readme.py

from zennix.core.utils.llm.groq_client import generate_response

class ZennixReadme:
    def __init__(self, project_path: str, model: str = "llama-3.3-70b-versatile"):
        self.project_path = project_path
        self.model = model

    def scan_codebase(self) -> dict:
        """Scans the project files to understand its structure and key modules."""
        # You’d use os.walk(), maybe parse imports
        return {
            "project_name": "Zennix",
            "modules": ["core", "cli", "llm"],
            "main_usage": "Automates project scaffolding with LLMs"
        }

    def generate_prompt(self, context: dict) -> str:
        """Creates a prompt based on codebase structure."""
        return f"""
        Write a professional README.md for a Python library called {context['project_name']}.
        It includes modules: {', '.join(context['modules'])}. 
        It helps developers scaffold projects (generate README, requirements, test stubs, etc.) using LLMs.
        Include sections like: Introduction, Features, Installation, Usage, CLI, Contribution, License.
        """

    def create_readme(self, output_path="data/"):
        context = self.scan_codebase()
        prompt = self.generate_prompt(context)
        readme_content = generate_response(user_prompt=prompt, llm_model=self.model)

        return readme_content
        
        
