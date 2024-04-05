allowed_packages = ['time', 'pyautogui', 'pyperclip']

def execute(code: str):

    # __builtins__を書き換えることによって想定外のライブラリなどの実行を防ぐ
    import_builtins = {}
    for packages in allowed_packages:
        import_builtins[packages] = __builtins__['__import__'](packages)

    builtins = {
        '__builtins__': import_builtins
    }

    exec(code, builtins, None)