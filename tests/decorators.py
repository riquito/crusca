# builtins
from functools import wraps
import inspect
from os.path import dirname, join


def provider(dataProvider):
    """Search for a method named `dataProvider` and run the decorated method
    once per each item returned by the provider. Each item is a tuple whose
    values will be used as the test method *args.
    """
    def dec(func):
        @wraps(func)
        def wrapper(self):
            for args in getattr(self, dataProvider)():
                with self.subTest(args=args):
                    func(self, *args)
        return wrapper
    return dec


def fixtureFile(fileName):
    """Search for the file named `filName` inside the directory FIXTURES_DIR
    declared at class level. Read its content and pass it as an argument to
    the test method.
    """
    def dec(func):
        @wraps(func)
        def wrapper(self):
            classFsPath = dirname(inspect.getsourcefile(self.__class__))
            fixtureFilePath = join(classFsPath, self.FIXTURES_DIR, fileName)
            text = ''
            with open(fixtureFilePath, mode='r', encoding='utf-8') as fp:
                text = fp.read()
            return func(self, text)
        return wrapper
    return dec
