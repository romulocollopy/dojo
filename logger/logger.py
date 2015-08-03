import unittest
from datetime import datetime


class Logger:

    path = "/home/romulocollopy/dev/projects/coding-dojo/logger/log.tmp"

    def __call__(self, _func):

        def _logger(*args, **kwargs):
            inicio = datetime.now()
            result = _func(*args, **kwargs)
            fim = datetime.now()
            self.log('{} demorou {}'.format(_func.__name__, fim - inicio))
            return result
        return _logger

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def log(self, message, now=None):
        now = now or datetime.now()
        with open(self.path, 'a') as fd:
            fd.write('{} - {}\n'.format(now, message))


class LoggerTestCase(unittest.TestCase):

    def setUp(self):
        self.logfile = "/home/romulocollopy/dev/projects/coding-dojo/logger/log.tmp"
        self.now = datetime.now()

    def test_is_singelton(self):
        logger = Logger()
        logger2 = Logger()
        is_equal = logger is logger2
        self.assertTrue(is_equal)

    def test_write_message(self):
        logger = Logger()
        logger.log('primeiro_log', self.now)
        with open(self.logfile, 'r') as lf:
            message = lf.readlines()[-1]
        exp_message = '{} - {}\n'.format(self.now, 'primeiro_log')
        self.assertEqual(exp_message, message)

    def test_call_decorator(self):
        def func(x):
            return x
        logger_obj = Logger()
        self.assertNotEqual(logger_obj(func), func)

    def test_loga_freestyle(self):
        logger = Logger()

        @logger
        def func(x):
            for i in range(999999):
                i**20
            return x

        func(100)

if __name__ == '__main__':
    unittest.main()
