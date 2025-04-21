import re
"""
define code block object
init with language and code
"""

class CodeBlock:
    def __init__(self, language, code):
        self.language = language
        self.code = code

## the object can be created from a string
## where the language and code can be extracted by regex
## the language is the first word after the ``` as in the ```language\n``
## the code is the content between the ```language\n``` and ```

def create_code_block(response):
    ## there could be multiple code blocks in the response
    ## extract all the code blocks
    code_blocks = re.findall(r"```(.*?)\n(.*?)\n```", response, re.DOTALL)
    ## logging the code blocks
    formatted_code_blocks = []
    for language, code in code_blocks:
        # Wrap the code in a function to ensure it can be compiled
        formatted_code = "def execute_code():\n    " + code.strip().replace('\n', '\n    ') + "\nexecute_code()"
        formatted_code_blocks.append(CodeBlock(language.strip(), formatted_code))
    return formatted_code_blocks
