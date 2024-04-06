### (偽)AGIに騙されないためのコードTips

このコードは今後出てくるであろう偽AGIに騙されないように作成したサンプルコードです
簡易なchatGPTの応用でこういうことが出来るということを勉強会で周知するために作りました

#### やれること

やりたいことをInputするとそれに従ってAIが画面を操作してそれを実現しています
例えばメッシをインターネットで検索するよう指示すると、あたかも人間のようにPCを操作してChoromeを起動/検索これを実現しています

#### 裏側の仕組み

仕組みは非常に簡単でinputされた自然言語を元にコードを生成して、それを実行しているだけです
コードではpyautoguiを使っているため画面を操作しているように見えるだけですね

##### コツ

1. Prompt

- 鉄板として一番最初に役割を定義しています
  - [あなたはPC(macOS)の自動操作をするエージェントとして振る舞ってください。]と言うのがそれに当たります
- 次にSoftwareの起動方法を定義しています
  - 今回はAlfredを使って起動させています
  - ショートカットキーにcommnand+mを割り当てているので、それで起動してSoftware名を入力させています
- Few-shot Learningとして題材とそのサンプルコードを用意しています
  - これによってSoftwareの起動や検索の仕方を明確に指示して、自分の環境に対応できるようにしています

```
Chromeを起動させる
Launcher経由でソフトウェアを起動する
\```
software_name = "Chrome"
pyautogui.keyDown('command')
pyautogui.press('m')
pyautogui.keyUp('command')

pyperclip.copy(software_name)
pyautogui.hotkey('command', 'v')
pyautogui.press('enter')
time.sleep(2)
\```
```

2. 動的実行

- LLMから生成したCodeを実行するため、対策をしなければ何でも出来る巨大なセキュリティホールとなります
- そのためproduction環境では権限制御やCloud Functionなど限定され閉じれる環境での実行が必須です
- また今回はその上でimportを制限して想定外の挙動をできないように工夫しています
  - まあpyautogui使っている時点で何でも出来るので今回は意味はないのですがサンプルということで...

```
def execute(code: str):

    # __builtins__を書き換えることによって想定外のライブラリなどの実行を防ぐ
    import_builtins = {}
    for packages in allowed_packages:
        import_builtins[packages] = __builtins__['__import__'](packages)

    builtins = {
        '__builtins__': import_builtins
    }

    exec(code, builtins, None)
```





