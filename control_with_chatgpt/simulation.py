SIMULATION_CODE_CHROME = """
# Chromeを起動
software_name = "Chrome"
pyautogui.keyDown('command')
pyautogui.press('m')
pyautogui.keyUp('command')

pyperclip.copy(software_name)
pyautogui.hotkey('command', 'v')
pyautogui.press('enter')
time.sleep(2)

search_text = "Lionel Messi"
time.sleep(2)
pyautogui.hotkey('command', 'l')
pyperclip.copy(search_text)
pyautogui.hotkey('command', 'v')
pyautogui.press('enter')
"""

SIMULATION_CODE_TERMINAL = """
software_name = "Terminal"

pyautogui.keyDown('command')
pyautogui.press('m')
pyautogui.keyUp('command')

pyperclip.copy(software_name)
pyautogui.hotkey('command', 'v')
pyautogui.press('enter')
time.sleep(2)

list_command = "ls"
pyperclip.copy(list_command)
pyautogui.hotkey('command', 'v')
pyautogui.press('enter')
"""


def get_simulation_code(instruction: str) -> str:
    """
    OpenAI APIを利用せず動的実行部のみテストするための関数
    なおSIMULATION CODE自体はOpenAI APIから返されたものをそのまま利用している
    """
    match instruction:
        case _ if "メッシ" in instruction:
            return SIMULATION_CODE_CHROME
        
        case _ if "ターミナル" in instruction:
            return SIMULATION_CODE_TERMINAL

        case _:
            raise ValueError('this instruction is not defined in simulation mode')