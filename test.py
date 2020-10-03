from main import Messenger

m = Messenger()
m.send_message('1', 'N')
m.send_message('1', 'N')
m.send_message('1', 'N')

print(m.get_messages())


m2 = Messenger()
m2.send_message('2', 'N')
m2.send_message('2', 'N')
m2.send_message('2', 'N')

print(m2.get_messages())
