Python Mock 学习笔记
===================
    
####hello.py

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    
    __author__ = 'liuzhijun'
    
    import os
    
    
    def rm(filename):
        if os.path.isfile(filename):
            os.remove(filename)
####test_hello.py
    
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    
    import unittest
    
    import mock
    
    from hello import rm
    
    
    class RmTestCase(unittest.TestCase):
        @mock.patch('hello.os.path')
        @mock.patch('hello.os')
        def test_rm(self, mock_os, mock_path):
            mock_path.isfile.return_value = False
            rm("any path")
            print mock_os
            self.assertFalse(mock_os.remove.called, "no call")
            mock_path.isfile.return_value = True
            rm("any path")
            mock_os.remove.assert_called_with("any path")
    
    
    if __name__ == '__main__':
        unittest.main()

*test_rm*函数的第一个参数有靠近该方法最近的那个装饰器提供。      

重构*hello.py*：  
    
    
