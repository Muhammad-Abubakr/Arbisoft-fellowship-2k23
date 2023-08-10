import pathlib
# p = Path('.')

# print([x for x in p.iterdir() if x.is_dir])

# print(list(p.glob('*/*.txt')))

# p = Path('/etc')
# q = p / 'init.d' / 'reboot'
# print(q)
# print(q.resolve())

# print(q.is_absolute())
# print(q.is_dir())
# print(q.exists())

user_input_string = 'file://tasks/pathlib_practice/script.py'
user_input_string_2 = 'hello there'

def send_file(user_message: str):
    if user_message.strip().startswith('file://'):
        file_path = user_message.strip().split(':')[1].strip('/')
        
        path = pathlib.Path(file_path)
        
        print(path.absolute().as_uri())
        
        if path.exists:
            print(f"{path} exists")
            
            with open(path, 'r', encoding="utf-8") as file:
                file_data = file.read()
                
                print(file_data.encode('utf-8'))
            
        else:
            print(f"{path} not exists")
            
        
        print(path)
    else:
        print(user_message)
        
send_file(user_message=user_input_string)
send_file(user_message=user_input_string_2)
