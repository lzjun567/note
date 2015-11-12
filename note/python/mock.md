MagicMock


    >>> from mock import MagicMock
    >>> thing = ProductionClass()
        # 可以指定返回值
    >>> thing.method = MagicMock(return_value=3)
    >>> thing.method(3, 4, 5, key='value')
    3
        # make assertion about how they have been used
    >>> thing.method.assert_called_with(3, 4, 5, key='value')
    
    # 执行异常
    mock = Mock(side_effect=KeyError('foo'))