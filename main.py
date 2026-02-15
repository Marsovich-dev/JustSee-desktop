
from MainProgram import MainProgram
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--autorun', action="store_true", help="Autorun by system")
args = parser.parse_args()

program = MainProgram()

if args.autorun:
    print()
    print("Это консоль программы Just See!")
    print("Если вы это видите, значит очередь обоев закончилась. Откройте главное окно программы (с настройкми), чтобы создать новую очередь")
    print()
    print("Это окно закроется автоматически через 10 сек.")
    print("Вы также можете закрыть его вручную.")
    print()
    program.update()

else:
    program.view()
