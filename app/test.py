try:
    from os import getcwd
except Exception as e:
    print(f'Error! Some Modules are Missing  : {e}')

print(getcwd())