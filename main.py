import argparse
import os
import sys

VFS_NAME = "VFS"  # имя приглашения

class Config: #Класс для хранения конфигурации эмулятора
    def __init__(self):
        self.vfs_path = "./vfs"  # путь к VFS по умолчанию
        self.script_path = None  # путь к скрипту (может и не быть)
        self.vfs_name = VFS_NAME


def parse_arguments(): #Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description='my_emul')#имя, аргумент парсера
    #добавляем в парсер аргумент пути к расположению VFS (настраивается пользователем, путь короче)
    parser.add_argument('--vfs-path',
                        type=str,
                        default="./vfs",
                        help='Путь к физическому расположению VFS')
    #добавляем в парсер аргумент пути к расположению файла (пользователь может не указывать, по умолчанию пусто)
    parser.add_argument('--script',
                        type=str,
                        help='Путь к стартовому скрипту для выполнения')

    return parser.parse_args()#возвращает все эти аргументы

def print_config(config): #Вывод конфигурации при запуске
    print("=== КОНФИГУРАЦИЯ ЭМУЛЯТОРА ===")
    print(f"VFS путь: {config.vfs_path}")#вывод пути
    print(f"Скрипт: {config.script_path if config.script_path else 'Не указан'}")#вывод пути конкретно к файлу
    print("===============================")


def execute_script(script_path, config): #Выполнение стартового скрипта
    if not os.path.exists(script_path):#если нет пути к файлу
        print(f"Ошибка: скрипт '{script_path}' не найден")
        return False

    print(f"\n=== ВЫПОЛНЕНИЕ СКРИПТА: {script_path} ===\n")

    try:
        with open(script_path, 'r', encoding='utf-8') as file:#попытка открыть файл по заданному пути
            lines = file.readlines()

        # перебор строк с 1, удаление пробелов
        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Удаляем комментарии из любой части строки
            if '#' in line:
                line = line.split('#')[0].strip()  # Берем только часть до #

            # Пропускаем пустые строки (после удаления комментариев)
            if not line:
                continue

            # создаем видимость диалога с пользователем
            print(f"{config.vfs_path}> {line}")

            # разделяем строку на команду и аргументы, выполнение команды
            parts = line.split()
            command = parts[0]
            args = parts[1:]

            if command == "exit":
                print("Завершение выполнения скрипта по команде exit")
                break
            else:
                execute_command(command, args, config)
            print()  # Пустая строка между командами

        print(f"\n=== ВЫПОЛНЕНИЕ СКРИПТА ЗАВЕРШЕНО ===\n")
        return True

    # если что-то не так, то сохраняем ошибку как е, а потом сообщаем о проблеме
    except Exception as e:
        print(f"Ошибка при выполнении скрипта: {e}")
        return False

def CreateConfig(args):
    # Создаем и настраиваем конфигурацию
    config = Config()  # объект для хранения настроек
    config.vfs_path = args.vfs_path
    config.script_path = args.script
    config.vfs_name = os.path.basename(args.vfs_path)  # берет только имя папки из пути (например, из /home/user берет user)
    return config

def main():
    # Парсим аргументы командной строки
    args = parse_arguments()
    config=CreateConfig(args)

    # Отладочный вывод конфигурации
    print_config(config)#показывает текущие настройки

    # Если указан скрипт - выполняем его
    if config.script_path:
        if execute_script(config.script_path, config):
            print("Скрипт выполнен. Переход в интерактивный режим...\n")
        else:
            print("Ошибка выполнения скрипта. Завершение работы.")
            return

    # Интерактивный режим (REPL)
    print(f"Добро пожаловать в my_emul! Для выхода введите 'exit'.")

    while True: # Главный цикл REPL
        user_input = input(f"{config.vfs_path}> ").strip()

        if not user_input: # Если пользователь просто нажал Enter, продолжаем цикл заново
            continue

        # Разделяем ввод на команду и аргументы(парсер)
        parts = user_input.split()
        command = parts[0]
        args = parts[1:]  # Все остальное - аргументы

        if command == "exit":
            print("Выход из эмулятора.")
            break

        # Здесь будет общая логика вызова других команд
        else:
            execute_command(command, args, config)


# Функция-роутер для выполнения команд
def execute_command(command, args, config):
    # Словарь команд
    commands = {
        "ls": cmd_ls,
        "cd": cmd_cd,
    }

    if command in commands:

        commands[command](args, config) # Если нашли, вызываем соответствующую функцию, передавая аргументы
    else:
        print(f"{VFS_NAME}: {command}: команда не найдена")

def cmd_ls(args,config):
    print(f"Команда 'ls' вызвана с аргументами: {args}")

def cmd_cd(args,config):
    print(f"Команда 'cd' вызвана с аргументами: {args}")

if __name__ == "__main__":
    main()