from agency_swarm.tools import BaseTool
from pydantic import Field
from pygments import highlight
from pygments.lexers import SolidityLexer, VyperLexer
from pygments.formatters import TerminalFormatter
import solcx
import vyper

class SmartContractDevelopmentTool(BaseTool):
    """
    A tool for writing and testing smart contract code in Solidity and Vyper.
    It provides functionalities for syntax highlighting, code compilation, and error checking.
    """

    language: str = Field(
        ..., description="The programming language of the smart contract. Supported values are 'solidity' and 'vyper'."
    )
    code: str = Field(
        ..., description="The smart contract code to be processed."
    )

    def run(self):
        """
        Executes the tool's main functionality: syntax highlighting, code compilation, and error checking.
        """
        if self.language.lower() == 'solidity':
            return self._process_solidity()
        elif self.language.lower() == 'vyper':
            return self._process_vyper()
        else:
            return "Unsupported language. Please use 'solidity' or 'vyper'."

    def _process_solidity(self):
        # Syntax highlighting
        highlighted_code = highlight(self.code, SolidityLexer(), TerminalFormatter())
        
        # Compile the Solidity code
        try:
            solcx.install_solc('0.8.0')  # Ensure the compiler version is installed
            compiled_sol = solcx.compile_source(self.code, output_values=['abi', 'bin'])
            return f"Syntax Highlighting:\n{highlighted_code}\nCompilation Successful: {compiled_sol}"
        except Exception as e:
            return f"Syntax Highlighting:\n{highlighted_code}\nCompilation Error: {str(e)}"

    def _process_vyper(self):
        # Syntax highlighting
        highlighted_code = highlight(self.code, VyperLexer(), TerminalFormatter())
        
        # Compile the Vyper code
        try:
            compiled_vyp = vyper.compile_code(self.code, ['abi', 'bytecode'])
            return f"Syntax Highlighting:\n{highlighted_code}\nCompilation Successful: {compiled_vyp}"
        except Exception as e:
            return f"Syntax Highlighting:\n{highlighted_code}\nCompilation Error: {str(e)}"