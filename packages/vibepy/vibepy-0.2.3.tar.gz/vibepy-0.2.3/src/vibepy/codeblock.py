import re
import logging
"""
define code block object
init with language and code
"""

class CodeBlock:
    def __init__(self, language, code):
        self.language = language
        self.code = code
        logging.debug(f"Created CodeBlock with language: {language}")
        logging.debug(f"Code content:\n{code}")

## the object can be created from a string
## where the language and code can be extracted by regex
## the language is the first word after the ``` as in the ```language\n``
## the code is the content between the ```language\n``` and ```

def create_code_block(response):
    ## there could be multiple code blocks in the response
    ## extract all the code blocks
    logging.debug(f"Creating code blocks from response:\n{response}")
    code_blocks = []
    current_block = None
    current_language = None
    current_code = []
    
    for line in response.split('\n'):
        if line.startswith('```'):
            if current_block is None:
                # Start of a new code block
                current_language = line[3:].strip()
                current_code = []
                current_block = True
                logging.debug(f"Starting new code block with language: {current_language}")
            else:
                # End of current code block
                if current_language and current_code:
                    code = '\n'.join(current_code)
                    # Only wrap Python code in a function
                    if current_language.lower() == 'python':
                        formatted_code = "def execute_code():\n    " + code.strip().replace('\n', '\n    ') + "\nexecute_code()"
                    else:
                        formatted_code = code.strip()
                    logging.debug(f"Created code block with language: {current_language}")
                    logging.debug(f"Code content:\n{formatted_code}")
                    code_blocks.append(CodeBlock(current_language, formatted_code))
                current_block = None
        elif current_block is not None:
            current_code.append(line)
    
    logging.debug(f"Created {len(code_blocks)} code blocks")
    return code_blocks
