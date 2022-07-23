import base64
read_f = open('forLight.png', 'rb')
b64string = base64.b64encode(read_f.read()).decode('utf-8')
read_f.close()
write_f = open('image.py', 'a')
write_f.write(f'light = \'{b64string}\'\n')
write_f.close()