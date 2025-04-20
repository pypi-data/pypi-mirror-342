# src/c66/__init__.py
from inspect import currentframe, getframeinfo
from ast import parse, unparse

# pp
def pp(*args):
    # 抓呼叫這個函數的那一行程式碼
    frame = currentframe().f_back
    code_context = getframeinfo(frame).code_context
    if not code_context:
        for arg in args:
            print(arg)
        return

    code_line = code_context[0].strip()
    
    try:
        # 解析 AST 拿到呼叫 pp 裡面的參數原始碼
        tree = parse(code_line)
        call = tree.body[0].value  # 假設這行是一個 expression
        arg_sources = [unparse(arg) for arg in call.args]
    except Exception:
        # fallback
        arg_sources = [f'arg{i}' for i in range(len(args))]

    for name, value in zip(arg_sources, args):
        print(f"{name}: {value}")

# pps
def pps(*args):
    # 抓呼叫這個函數的那一行程式碼
    frame = currentframe().f_back
    code_context = getframeinfo(frame).code_context
    if not code_context:
        for arg in args:
            try:
                print(f"{arg.shape}")
            except AttributeError:
                print(f"{arg} has no shape attribute")
        return

    code_line = code_context[0].strip()
    
    try:
        # 解析 AST 拿到呼叫 pps 裡面的參數原始碼
        tree = parse(code_line)
        call = tree.body[0].value  # 假設這行是一個 expression
        arg_sources = [unparse(arg) for arg in call.args]
    except Exception:
        # fallback
        arg_sources = [f'arg{i}' for i in range(len(args))]

    for name, value in zip(arg_sources, args):
        try:
            print(f"{name}'s shape: {value.shape}")
        except AttributeError:
            print(f"{name} has no shape attribute")
            

# new print
import builtins
import functools

# 儲存原始的 print 函數
_original_print = builtins.print

# 全局 debug 變量，預設為 True
show_print = True

# 定義新的 print 函數
@functools.wraps(_original_print)
def custom_print(*args, **kwargs):
    if show_print:
        return _original_print(*args, **kwargs)
    return None

# 將 custom_print 暴露為包的 print 函數
print = custom_print