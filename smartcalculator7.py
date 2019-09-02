from enum import Enum

class TokenType(Enum):
    NUMBER = 1
    IDENTIFIER = 2
    ASSIGNMENT = 3
    OPERATOR = 4
    UNKNOWN = 5
    
    
class Token:

    def __init__(self, ttype, value):
        self.ttype = ttype
        self.value = value

class InvalidAssignment(Exception):
    pass
    
class InvalidIdentifier(Exception):
    pass
    
class InvalidExpression(Exception):
    pass
        
class UnknownVariable(Exception):
    pass
    
class Stack:
    def __init__():
        self.storage = []
        
    def pop():
        return self.storage.pop()
        
    def push(x):
        self.storage.append(x)
        
    
    

def read_token(s, i):
    if s[i].isdigit():
        return read_number(s, i)   
    elif s[i].isalpha():
        return read_identifier(s, i)
    elif (s[i] in "+-"):
        return read_operators(s, i)
    elif (s[i] == "="):
        return read_assignment(s, i)
    else:
        return read_unknown(s, i)

def skip_whitespaces(s, i):
    while (i < len(s)) and (s[i] == " "):
        i += 1
    return i   

def read_number(s, i):
    
    tmp = ""
    while ((i < len(s)) and (s[i].isdigit())):
        tmp += s[i]
        i += 1
    return(i, Token(TokenType.NUMBER, int(tmp)))
    

def read_identifier(s, i):
    tmp = ""
    while (i < len(s)) and (s[i].isalnum()):
        tmp += s[i]
        i += 1
    return (i, Token(TokenType.IDENTIFIER, tmp))
    
def valid_identifier(name):
    for ch in name:
       if (not ch.isalpha()):
           return False
    return True
    
def read_assignment(s, i):
    if (i < len(s)) and (s[i] == "="):
        i += 1
    return (i, Token(TokenType.ASSIGNMENT, "="))
    
def switch(op):
    if (op == " +"):
        return "-"
    elif (op == "-"):
        return "+"
    return None

def read_operators(s, i):
    op = None
    '''while (i < len(s)) and (s[i] in " +-"):
        if (op is None) and (s[i] != " "):
            op = s[i]
        elif (s[i] == "-"):
            op = switch(op)
        i += 1'''
    if (i < len(s)) and (s[i] in "+-"):
        op = s[i]
        i += 1             
    return (i, Token(TokenType.OPERATOR, op))

def read_unknown(s, i):
    tmp = ""
    while (i < len(s)) and (s[i] not in " +-="):
        tmp += s[i]
        i += 1 
    return (i, Token(TokenType.UNKNOWN, tmp))       

def do_operation(x, y, op):
    if (op == "+"):
        return x + y
    elif (op == "-"):
        return x - y
        
  
def find_assignment(tokens):
    if len(tokens) == 0:
        return False
    for i in range(len(tokens)):
        if tokens[i].ttype == TokenType.ASSIGNMENT:
            if (tokens[0].ttype != TokenType.IDENTIFIER):
                raise InvalidAssignment
            if (not valid_identifier(tokens[0].value)):
                raise InvalidIdentifier
            if (i != 1):
                raise InvalidAssignment        
        
            rhs = tokens[2:]
            if (len(rhs) == 0) or (find_assignment(rhs)):
                raise InvalidAssignment
            try:
                 variables[tokens[0].value] = evaluate(rhs)
            except (InvalidIdentifier):
                raise InvalidAssignment
            except (InvalidExpression):
                raise InvalidAssignment        
        
            return True           

    

    
def evaluate(tokens):
    result = 0
    op = "+"
    if len(tokens) == 0:
        return None
    for i in range(0, len(tokens)):
        t = tokens[i]
        if (t.ttype == TokenType.IDENTIFIER):
            if (not valid_identifier(tokens[0].value)):
                raise InvalidIdentifier
            if (not t.value in variables):
                raise UnknownVariable
            elif (i > 0) and (tokens[i - 1].ttype != TokenType.OPERATOR):
                raise InvalidExpression
            result = do_operation(result, variables[t.value], op)
        elif (t.ttype == TokenType.NUMBER):
            if (i > 0) and (tokens[i - 1].ttype != TokenType.OPERATOR):
                raise InvalidExpression
            result = do_operation(result, t.value, op)
        elif (t.ttype == TokenType.OPERATOR):
            if (i > 0) and (tokens[i - 1].ttype == TokenType.OPERATOR):
                raise InvalidExpression
            op = t.value
        else:
            raise InvalidExpression
    if (tokens[-1].ttype == TokenType.OPERATOR):
        raise InvalidExpression 
    #print(result)   
    return result
            
        
   


help_string = "The program calculates the sum of numbers"
unknown_command_string = "Unknown command"
invalid_expression_string = "Invalid expression"

variables = {}

while (True):
    user_input = input().strip()
    if len(user_input) == 0:
        continue  

    if (user_input.startswith("/")):        
        cmd_str = user_input 
        if cmd_str == "/help":
             print(help_string)
        elif (cmd_str == "/exit"):
             print("Bye!")
             break
        else:
            print(unknown_command_string)
        
    else:   
        result = 0
        tokens = []
        i = 0
        while (i < len(user_input)):            
            (i, t) = read_token(user_input, i)
            tokens.append(t)
            i = skip_whitespaces(user_input, i)
        #print([(t.ttype, t.value) for t in tokens])   
        try:    
            if (not find_assignment(tokens)):
                r = evaluate(tokens)
                if (not r is None):
                   print(r)
        except (InvalidIdentifier):
            print("Invalid identifier")
        except (InvalidAssignment):
            print("Invalid assignment") 
        except (UnknownVariable):
            print("Unknown variable")      
        except (InvalidExpression):
            print("Invalid expression")
            
        

        
        
            

