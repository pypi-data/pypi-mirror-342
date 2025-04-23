import sys
import re
class _CustomStdout:
    def __init__(self, original_stdout):
        self.original_stdout = original_stdout

    def write(self, text):
        transformed = self._transform(text)
        self.original_stdout.write(transformed)

    def flush(self):
        self.original_stdout.flush()

    @staticmethod
    def _transform(text):
        #chars_to_upper = {'a', 'c', 'e','i','m','n', 'r'}
        #t = ''.join([c.upper() if c.lower() in chars_to_upper else c for c in text])
        text = re.sub( r'(?i)(american)', lambda m: m.group().upper(),text)
        text = re.sub( r'(?i)(win)',      lambda m: m.group().upper(),text)        
        text = re.sub( r'(?i)(donald)',  lambda m: m.group().upper(),text)
        text = re.sub( r'(?i)(trump)',   lambda m: m.group().upper(),text)
        text = re.sub( r'(?i)(huge)',     lambda m: m.group().upper(),text)
        text = re.sub( r'(?i)(great)',   lambda m: m.group().upper(),text)
        text = re.sub( r'(?i)(make)',    lambda m: m.group().upper(),text)
        text = re.sub( r'(?i)(maga)',    lambda m: m.group().upper(),text)
        text = re.sub( r'(?i)(again)',  lambda m: m.group().upper(),text)
        text = re.sub( r'(?i)(success)',  lambda m: m.group().upper(),text)        
        return re.sub(r'(?i)(trump)',   lambda m: m.group().upper(), text  )

    def __getattr__(self, name):
        return getattr(self.original_stdout, name)

# 替换标准输出
sys.stdout = _CustomStdout(sys.stdout)