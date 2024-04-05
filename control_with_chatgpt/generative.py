import os
import openai
from sandbox import execute
from simulation import get_simulation_code

openai.api_key = os.environ['OPEN_AI_API_KEY']
is_simulation = os.environ.get('SIMULATION', False)

system_instrcution = """
あなたはPC(macOS)の自動操作をするエージェントとして振る舞ってください。
PC内のブラウザやエディタなどのソフトウェアを起動し、そのソフトウェアを操作する役割です。

今PCに入っている代表的なソフトウェアを以下に列挙します。
もちろんこれ以外にも多数のソフトウェアがインストールされています。

ブラウザ - Chrome
エディタ - Visual Studio Code
プレゼン - PowerPoint

ソフトウェアの起動方法にはLauncherを使用します

1. Laucherをショートカットキーであるcommand+mで起動する
2. 起動したLauncherにソフトウェア名(e.g. Chrome)を入力してEnterを押下する

以下にいつくたのコマンドの呼び出しをサンプルとして紹介します。
なおimport文は実行時に自動で追加するため、生成されるコードには実装しないことを注意してください。
もしimport文が含まれていた場合には実行時エラーとなります。

Chromeを起動させる
Launcher経由でソフトウェアを起動する
```
software_name = "Chrome"
pyautogui.keyDown('command')
pyautogui.press('m')
pyautogui.keyUp('command')

pyperclip.copy(software_name)
pyautogui.hotkey('command', 'v')
pyautogui.press('enter')
time.sleep(2)
```

Chromeで検索する
```
# こちらのほうが汎用的に対応できる
# ただし事前に画像が必要なため今回は採用していない
# search_pos = pyautogui.locateOnScreen("img/search.png", confidence=0.1)
# pyautogui.click(search_pos)

# Chromeのショートカットを利用して検索にフォーカスする
pyautogui.hotkey('command', 'l')

pyperclip.copy(search_text)
pyautogui.hotkey('command', 'v')

pyautogui.press('enter')
```

テキストエディタで文字列を入力する
```
# New Tab
pyautogui.hotkey('command', 'n')

pyperclip.copy(search_text)
pyautogui.hotkey('command', 'v')
```

エージェントを終了させる
```
pyautogui.hotkey('control', 'c')
```

あなたはこのようなコードを組み合わせて、指示に従ってPCを操作してください
"""

def get_code_from_openai(instruction: str) -> str:
    # Code実行部を確認するためのシミュレーションコード
    if is_simulation:
        return get_simulation_code(instruction)
    
    if instruction != '':
        try:
            response = openai.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system', 'content': system_instrcution},
                    {'role': 'user', 'content': instruction},
                ],
                temperature=0.2,
            )
            return response.choices[0].message.construct
        except:
            pass
    
    return ''


def get_code_from_response(response: str) -> str:
    if '```' in response:
        code = response[response.index('```') + 3:]
        if '```' in code:
            code = code[:code.index('```')]
        if code.startswith('python'):
            code = code[len('python'):]
        elif code.startswith('\n'):
            pass
        else:
            return ''
        return code.strip()
    return response


def run_code_from_generative_ai(code: str):
    try:
        execute(code)
    except Exception as e:
        print('code running error', e)

def sanitize_code(code: str) -> str:
    filtered_code = '\n'.join(line for line in code.split('\n') if not line.strip().startswith('import'))
    return filtered_code


def control_from_ai(instruction: str):
    if instruction != '':
        response = get_code_from_openai(instruction)
        code = get_code_from_response(response)
        if code != '':
            code = sanitize_code(code)
            # print('\n'.join(['>>> ' + c for c in code.split('\n')]))

            run_code_from_generative_ai(code)