from g4f.client import Client
from g4f.models import gpt_4o_mini
from commitly.prompt import (
    PROMPT,
    PROMPT_FACT,
    STYLE_COMMIT,
    FORMAT_COMMIT,
    RECOMMANDATION
)
from subprocess import run
from pathlib import Path
from commitly.exceptions.diffEmptyException import DiffEmptyException
from json import loads


class Commitly:
    """
    Commitly automatically generates a commit message based on the current staged changes (diff).
    """

    def __init__(self, model=gpt_4o_mini, file_temp="commit.txt", lang="fr"):
        """
        Initialize the Commitly client with a model and temporary file to store the message.
        """
        self.client = Client()
        self.model = model
        self.file_temp = Path(file_temp)
        self.lang = lang

    def get_prompt(self, 
            style_commit: str = None,
            format_commit: str = None,
            recommandation_commit: str = None,
            fact:bool=False
            ) -> str:
        """
        Format the system prompt using commit style, format, and custom recommendations.
        """
        style_commit = style_commit or STYLE_COMMIT
        format_commit = format_commit or FORMAT_COMMIT
        recommandation_commit = recommandation_commit or RECOMMANDATION

        return (PROMPT_FACT if fact else PROMPT).format(
            STYLE_COMMIT=style_commit,
            FORMAT_COMMIT=format_commit,
            RECOMMANDATION=recommandation_commit
        )

    def add(self, file: str) -> bool:
        """
        Add a file to the git staging area.
        """
        return self._run_cmd(f"git add {file}", return_code=True) == 0

    def generate_commit_message(self, 
            style_commit: str = None, 
            format_commit: str = None, 
            recommandation_commit: str = None, 
            ticket: str = None,
            fact: bool = False
            ) -> dict|list[dict]:
        """
        Generate the commit message using the AI model based on current staged diff.
        """
        diff = self._run_cmd("git diff --cached")

        if not diff.strip():
            raise DiffEmptyException("No changes found in staged files.")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.get_prompt(style_commit, format_commit, recommandation_commit, fact)},
                {"role": "user", "content": f"""{{ "diff": "{diff}", {f"ticket {ticket}," if ticket else ''} "langue": "{self.lang}" }}"""},
            ],
            web_search=False
        )
        
        content = response.choices[0].message.content.strip()

        if not fact:
            content = {
                "commit": content,
                'files': self.file_stage()
            }
        else: 
            try:
                content = loads(content)
            except: 
                content = {
                    "commit": content,
                    'files': self.file_stage()
                }
            
        return content

    def save_message_to_file(self, message: str) -> bool:
        """
        Save the generated commit message into the temporary file.
        """
        try:
            # Remove null bytes that can cause Git to fail
            message = message.replace('\x00', '')

            with self.file_temp.open("w", encoding="utf-8", newline='\n') as f:
                f.write(message)

            return True
        except Exception as e:
            print(f"Error saving commit message: {e}")
            return False

    def commit(self) -> bool:
        """
        Commit changes using the saved message from the temporary file.
        """
        success = self._run_cmd(f"git commit -F {self.file_temp.absolute()}", return_code=True) == 0
        self.file_temp.unlink(missing_ok=True)  # Clean up the temp file
        return success

    def _run_cmd(self, cmd: str, return_code: bool = False):
        """
        Internal method to run shell commands. Returns either output or exit code.
        """
        result = run(cmd, capture_output=True, text=True, shell=True,encoding='utf-8',)
        output = result.stdout or ""
        return result.returncode if return_code else output.strip()

    def push(self):
        """
        Push the latest commit to the remote repository.
        """
        self._run_cmd("git push")

    def unstage(self, file: str):
        """
        Unstage a file (remove from staging area).
        """
        self._run_cmd(f"git reset {file}")
        
    def file_stage(self, ):
        """
        file stage 
        """
        return self._run_cmd(f"git diff --name-only --cached").strip().splitlines()
