from foo import a


if __name__=='__main__':
    a = 2
    import foo
    print foo.a
