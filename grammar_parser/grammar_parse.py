import sys
import io
from antlr4 import *
from KotlinLexer import KotlinLexer
from KotlinParser import KotlinParser
from KotlinParserListener import KotlinParserListener


class FunctionListener(KotlinParserListener):
    def __init__(self):
        self.functions = []

    def enterClassDeclaration(self, ctx):
        # Access the token stream from the parser
        #token_stream = ctx.parser.getTokenStream()
        if hasattr(ctx.classBody(), "classMemberDeclaration"):
            #return
        # Loop through each function/method in the class
            for method in ctx.classBody().classMemberDeclaration():
                if hasattr(method, 'functionDeclaration') and method.functionDeclaration():
                    func_ctx = method.functionDeclaration()
                    print(func_ctx.identifier().getText())
                    self.enterFunctionDeclaration(func_ctx)
                if hasattr(method, "classBody") and method.classBody():
                    print(method.classBody())

    def enterFunctionDeclaration(self, ctx:KotlinParser.FunctionDeclarationContext):
        
        if hasattr(ctx.identifier(), 'getText'):
            function_name = ctx.identifier().getText()
        else:

            function_name = ""
        
        # Docstring extraction
        token_stream = ctx.parser.getTokenStream()
        index = ctx.start.tokenIndex

        
        docstring = ""
        for i in range(max(0, index - 10), index):
            token = token_stream.get(i)
            if token.channel == 1 and token.type == 2: # Hidden channel, type 2 means block comment
                docstring = token.text
                
        # Function name and parameters
        parameters = [(param_ctx.parameter().simpleIdentifier().getText(), param_ctx.parameter().type().getText()) for param_ctx in ctx.functionValueParameters().functionValueParameter()] if ctx.functionValueParameters() else []
        signature = f"fun {function_name}({', '.join([f'{name}: {type}' for name, type in parameters])})"

        # Function body
        body_tokens = []
        if hasattr(ctx, 'functionBody') and ctx.functionBody():
            body_start_index = ctx.functionBody().start.tokenIndex
            body_stop_index = ctx.functionBody().stop.tokenIndex

            # Retrieve all tokens from start to stop index, including hidden tokens
            
            for i in range(body_start_index, body_stop_index + 1):
                token = token_stream.get(i)
                if token.channel == 1:
                    if token.type == 4: # If hidden channel take only 4th type which is whitespaces
                        body_tokens.append(token.text)
                else:
                    body_tokens.append(token.text)
        
            
        # Store the function info
        self.functions.append((function_name, signature, docstring, "".join(body_tokens)))
    

def parse_kotlin(file_path):
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # Redirect stdout and stderr to nowhere
    #sys.stdout = io.StringIO()
    #sys.stderr = io.StringIO()
    input_stream = FileStream(file_path, encoding='utf-8')
    lexer = KotlinLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = KotlinParser(stream)
    tree = parser.kotlinFile()

    # Create the listener
    listener = FunctionListener()

    # Walk the parse tree with the listener
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    # Output the functions found
    return listener.functions

# Test the parser with an example input
if __name__ == '__main__':
    file_path = "/home/maxfactor/Documents/Transformers/GigaFile.kt"  
    
    functions = parse_kotlin(file_path)

    for name, sign, docstring, body in functions:
        print(f"{sign}\n{docstring}\n{body}")
        print("="*50)