from mako.template import Template
if __name__ == '__main__':

    print Template('hello${data}').render(data='world')
    print 'hello'
