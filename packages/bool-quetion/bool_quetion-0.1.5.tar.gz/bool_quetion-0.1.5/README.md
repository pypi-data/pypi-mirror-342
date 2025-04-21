# bool_quetion
## Module for asking yes/no or accept/cancel questions.

### Installing
Install on Debian 11 or older:

`pip install bool_quetion`

Install on Debian 12 and later:

`pipx install bool_quetion`

### Using the code in Python 3.x
~~~
names = []
reply = True
while reply:
    element = input ('Enter the full name: ')
    names.append(element)
    for name in names:
        print (name)
    reply = true_false('Do you wish to continue?', ['Yes', 'no'])
else:
    reply = True
~~~

It is also possible to highlight the characters that can be entered.

`reply = true_false('Do you wish to continue?', ['Yes', 'no'], True)`
