from pythonds.basic.stack import Stack
import numpy as np

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
functions = {"sin", "cos", "tan", "arctan", "exp", "ln", "lg"}
operations = {"^", "*", "/", "+", "-"}
prec = {"UN_MINUS": 5, "POWER": 4, "MULTIPLY": 3, "DIVIDE": 3, "PLUS": 2, "MINUS": 2, "RBR": 1}


class TOKEN_TYPE:
    NUMBER: str = None
    VARIABLE: str = None
    OPERATION: str = None
    LBR: str = None
    RBR: str = None
    NONE: str = None


class Token:
    type_token = None
    value = None
    operation_type = None
    function_args = None


def reverse_string(s):
    return s[::-1]


def split_(s):
    l = []
    for c in s:
        l.append(c)
    return l


def char_to_str(s):
    return " ".join(s)


def is_char(token):
    if not(is_number(token)) and token != '(' and token != ')' and token not in prec:
        return True
    return False


def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


def is_function_(tokens):
    s = ""
    tmp_list = tokens.copy()
    tmp_list.reverse()
    for k in tmp_list:
        if k.type_token == 'OPERATION' or k.type_token is None or k.type_token == 'LBR':
            s = reverse_string(s)
            if s in functions:
                return len(s), s, True
            else:
                return 0, None, False

        s += k.value


def is_var(tokens):
    s = ""
    tmp_list = tokens.copy()
    tmp_list.reverse()
    # print_tokens(tmp_list)
    for k in tmp_list:
        if k.type_token == 'OPERATION' or k.type_token is None or k.type_token == 'LBR':
            s = reverse_string(s)
            return len(s), s, True

        s += k.value
    return 0, None, False


def get_float(tokens):
    s = ""
    tmp_list = tokens.copy()
    tmp_list.reverse()
    for k in tmp_list:
        if k.type_token != 'NUMBER':
            s = reverse_string(s)
            s += "."
            return len(s)-1, s, True

        s += k.value
    return 0, None, False


def get_tokens(expr):

    old_token = Token()
    tokens = [old_token]
    copy_expr = expr
    n_arg = 0
    len_num = 0
    for c in expr:
        if n_arg > 0:
            n_arg -= 1
            copy_expr = copy_expr[1:]
            continue
        if len_num > 0:
            len_num -= 1
            continue
        token = Token()
        copy_expr = copy_expr[1:]
        if c == ' ' or c == '\t':
            continue
        token.value = c
        if c == '.':
            if old_token.type_token == 'NUMBER':
                len_num, nums, check = get_float(tokens)
                if not check:
                    print("Неверный ввод1")
                    return None, False
                for k in range(len_num):
                    tokens.pop(-1)
                # num = 1
                for k in copy_expr:
                    if not is_number(k):
                        break
                    nums += k
                    copy_expr = copy_expr[1:]

                len_num = len(nums) - len_num - 1
                # for k in range(len_num-1):
                #     copy_expr = copy_expr[1:]
                old_token.value = nums
                old_token.type_token = 'NUMBER'
                tokens.append(old_token)
                continue
        elif c in operations:
            token.type_token = 'OPERATION'
            if c == '*':
                if old_token.operation_type == 'MULTIPLY':
                    tokens.pop(-1)
                    c = '**'
                    token.operation_type = 'POWER'
                else:
                    token.operation_type = 'MULTIPLY'
            elif old_token.type_token == 'LBR' or old_token.type_token == 'OPERATION':
                token.operation_type = 'UN_MINUS'
            elif c == '^':
                c = '**'
                token.operation_type = 'POWER'
            elif c == '/':
                token.operation_type = 'DIVIDE'
            elif c == '+':
                token.operation_type = 'PLUS'
            elif c == '-':
                token.operation_type = 'MINUS'
            token.value = c

        elif is_char(c):
            token.type_token = 'VARIABLE'
        elif is_number(c) and old_token.type_token == 'VARIABLE':
            n_c, var, check = is_var(tokens)
            if not check:
                print("Неверный ввод0")
                return None, False
            while n_c > 0:
                tokens.pop(-1)
                n_c -= 1
            old_token.value = var + c
            old_token.type_token = 'VARIABLE'
            tokens.append(old_token)
            continue

        elif is_number(c):
            token.type_token = 'NUMBER'
        elif c == '(':
            token.type_token = 'LBR'
            if old_token.type_token != 'OPERATION' and old_token.type_token is not None:
                n_f, fun, check = is_function_(tokens)
                if not check:
                    print("Неверный ввод1")
                    return None, False
                for k in range(n_f):
                    tokens.pop(-1)

                args = ""
                num = 1
                for k in copy_expr:
                    if k == '(':
                        num += 1
                    if k == ')':
                        num -= 1
                        if num == 0:
                            old_token.function_args = args
                            break
                    args += k
                if old_token.function_args is None:
                    print("Неверный ввод2")
                    return None, False
                n_arg = len(args)
                old_token.value = fun
                old_token.type_token = 'FUNCTION'
                tokens.append(old_token)

        elif c == ')':
            token.type_token = 'RBR'

        old_token = token
        tokens.append(token)
    return tokens, True


def parse_function(token):
    tmp_token = split_(token)
    c_prev = None
    for c in token:
        if c_prev == '(':
            tmp_token.pop(-1)
            tmp_token = char_to_str(tmp_token)
            token = infixToPostfix(tmp_token)
            return token
        tmp_token.remove(c)
        c_prev = c


def is_function(token):
    l = ""
    for c in token:
        if c == '(':
            break
        l += c

    if l in functions:
        return l, True
    return "", False


def infixToPostfix(infixexpr):
    opStack = Stack()
    postfixList = []
    prev_token = Token()
    args_len = 0
    tokenList, check_ = get_tokens(infixexpr)
    if not check_:
        return None, False
    tokenList.pop(0)

    for token in tokenList:
        if args_len > 0:
            args_len -= 1
            continue
        if token.type_token == 'VARIABLE' or \
           token.type_token == 'NUMBER':
            postfixList.append(token)
        elif token.type_token == 'FUNCTION':
            args, check = infixToPostfix(token.function_args)
            if not check:
                return None, False
            token.function_args = args
            args_len = 2
            postfixList.append(token)
        elif token.type_token == 'LBR':
            opStack.push(token)
        elif token.type_token == 'RBR' and not opStack.isEmpty():
            topToken = opStack.pop()
            while topToken.type_token != 'LBR':
                postfixList.append(topToken)
                topToken = opStack.pop()
        elif token.type_token == 'OPERATION':

            if not opStack.isEmpty():
                operation = opStack.peek().operation_type
            else:
                operation = None
            while not opStack.isEmpty() and operation is not None and \
                    (prec[opStack.peek().operation_type] >= prec[token.operation_type]):
                postfixList.append(opStack.pop())
            opStack.push(token)
        elif token.type_token is None:
            continue

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())

    return postfixList, True


def postfixEval(postfixExpr):
    operandStack = Stack()
    tokenList = postfixExpr
    for token in tokenList:
        if token.type_token == 'NUMBER':
            operandStack.push(float(token.value))
        elif token.type_token == 'VARIABLE':
            operandStack.push(token.value)
        elif token.type_token == 'FUNCTION':
            args = postfixEval(token.function_args)
            # token.function_args = args
            result = doMath(token, args, None)
            operandStack.push(result)
        else:
            operand2 = operandStack.pop()
            operand1 = operandStack.pop()
            result = doMath(token, operand1, operand2)
            operandStack.push(result)
    return operandStack.pop()


def doMath(op, op1, op2):
    if op.value == "*":
        return op1 * op2
    elif op.value == "/":
        return op1 / op2
    elif op.value == "+":
        return op1 + op2
    elif op.value == "-":
        return op1 - op2

    elif op.value == "sin":
        return np.sin(op1)
    elif op.value == "cos":
        return np.cos(op1)
    elif op.value == "tan":
        return np.tan(op1)
    elif op.value == "arctan":
        return np.arctan(op1)
    elif op.value == "exp":
        return np.exp(op1)
    elif op.value == "ln":
        return np.log(op1)
    elif op.value == "lg":
        return np.log10(op1)


def print_tokens(express):
    for i in express:
        if i.value is not None:
            if i.type_token == 'FUNCTION':
                print_tokens(i.function_args)
            print(i.value, end=' ')
