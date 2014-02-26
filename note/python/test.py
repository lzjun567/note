class Parrot(object):
    def __init__(self):
        self.__voltage = 10000
    @property
    def voltage(self):
        return self.__voltage + 1

class C(object):
    def __init__(self):
        self._x = None

    def getx(self):
        return self._x
    def setx(self, value):
        self._x = value
    def delx(self):
        del self._x
    x = property(getx, setx, delx, "I'm the 'x' property.")


class MyDescriptor(object):
    def __get__(self, subject_instance, subject_class):
        return (self, subject_instance, subject_class)

    def __set__(self, subject_instance, value):
        print "%r %r %r" (self, subject_instance, value)

my_descriptor = MyDescriptor()

class Spam(object):
    my = my_descriptor

import re

class Email(object):
    
        def __init__(self):
            self._name = ''
    
        def __get__(self, obj, type=None):
            return self._name
    
        def __set__(self, obj, value):
            m = re.match('\w+@\w+\.\w+', value)
            if not m:
                raise Exception('email not valid')
            self._name = value
    
        def __delete__(self, obj):
            del self._name

#class Person(object):
#    email = Email()
    #def __init__(self, email):
    #    m = re.match('\w+@\w+\.\w+', email)
    #    if not m:
    #        raise Exception('email not valid')
    #    self.email = email

#class Person(object):
#
#    def __init__(self):
#        self._email = None
#
#    def get_email(self):
#        return self._email
#
#    def set_email(self, value):
#         m = re.match('\w+@\w+\.\w+', value)
#         if not m:
#             raise Exception('email not valid')
#         self._email = value
#
#    def del_email(self):
#        del self._email
#
#    email = property(get_email, set_email, del_email, 'this is email property')
        

class Person(object):

    def __init__(self):
        self._email = None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
         m = re.match('\w+@\w+\.\w+', value)
         if not m:
             raise Exception('email not valid')
         self._email = value

    @email.deleter
    def email(self):
        del self._email



