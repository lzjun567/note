Python测试指南
================================
####测试的种类
#####单元测试
#####集成测试
#####系统测试

####Doctest：最简单的测试工具
1. 创建一个名为test.txt的文件
2. 插入以下文本到文件中
        
        this is a simple doctest that checks some of Python's arithmetic operations
        >>> 2+2
        4
        >>> 3*3
        10
3. 现在就可以运行doctest了，进入该文件所在目录的命令行
4. 运行：(此方法治适用于python2.6及以上版本)

        python -m doctest test.txt
5. 运行后会看到如下结果：

        **********************************************************************
        File "text.txt", line 4, in text.txt
        Failed example:
            3*3
        Expected:
            10
        Got:
            9
        **********************************************************************
        1 items had failures:
           1 of   2 in text.txt
        ***Test Failed*** 1 failures.

####Doctest的语法 
`>>>`开头的代码将会发送给python解释器，`...`作为代码下一行的追加，允许嵌套一些复杂的代码块语句到doctest中去。




####使用单元测试写基础测试

    class RomanNumeralConverter(object):
        def __init__(self, roman_numeral):
            self.roman_numeral = roman_numeral
            self.digit_map = {
                                "M":1000, 
                                "D":500,
                                "C":100,
                                "L":50,
                                "X":10,
                                "V":5,
                                "I":1
                            }
        def convert_to_decimal(self):
            val = 0
            for char in self.roman_numeral:
                val += self.digit_map[char]
            return val

    import unittest
    class RomanNumeralConverterTest(unittest.TestCase):
        def test_parsing_millenia(self):
            value = RomanNumeralConverter("M")
            self.assertEquals(1000, value.convert_to_decimal())
            
        def test_no_roman_numeral(self):
            value = RomanNumeralConverter(None)
            self.assertRaises(TypeError, value.convert_to_decimal)

        def test_empty_roman_numeral(self):
            value = RomanNumeralConverter("")
            self.assertTrue(value.convert_to_decimal() == 0)
            self.assertFalse(value.convert_to_decimal() > 0)

尽可能使用assertEquals  

    setUp(self)
    tearDown(self)

每执行一个测试用例，就会执行一遍setUp和tearDown方法  

    setUpClass/tearDownClass

unittest模块提供了TestLoader().loadTestFromTestCase，可以自动地获取所有test*方法到一个测试套件中去。这个测试套件通过unittest的TextTestRunner运行。TextTestRunner是unittest仅有的Runner。  

    if __name__ == "__main__":
        import sys
        suite = unittest.TestSuite()
