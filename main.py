VFS_NAME = "VFS"  # имя приглашения

def main():
    print(f"Добро пожаловать в my_emul! Для выхода введите 'exit'.")

    while True: # Главный цикл REPL
        user_input = input(f"{VFS_NAME}> ").strip()

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
            execute_command(command, args)


# Функция-роутер для выполнения команд
def execute_command(command, args):
    # Словарь команд
    commands = {
        "ls": cmd_ls,
        "cd": cmd_cd,
    }

    if command in commands:

        commands[command](args) # Если нашли, вызываем соответствующую функцию, передавая аргументы
    else:
        print(f"{VFS_NAME}: {command}: команда не найдена")

def cmd_ls(args):
    print(f"Команда 'ls' вызвана с аргументами: {args}")

def cmd_cd(args):
    print(f"Команда 'cd' вызвана с аргументами: {args}")

if __name__ == "__main__":
    main()