import random
import json
from datetime import datetime


# Goal of task was to get random + - / *, working with random X, Y values between 0 and 2500
# Output is in correct formal {'X+Y': 'num(X) + num(Y)', 'result': int(X*Y)
class someting:

    def __init__(self):
        self.info = []

    def __call__(self, num_of_examples, **kwargs):
        self.info = []
        for i in range(num_of_examples):
            self.op()
        self.to_text(**kwargs)

    def __setitem__(self, key, value, result):
        temp = {key: value, 'result': result}
        self.info.append(temp)

    def to_text(self, **kwargs):
        if 'file' in kwargs.keys():
            with open(kwargs['file'], 'w') as file:
                json.dump(self.info, file, indent=4)
        else:
            filename = '%s.txt' % str(datetime.now())
            with open(filename, 'w') as file:
                json.dump(self.info, file, indent=4)

    def op(self):
        x = random.randint(0, 2500)
        y = random.randint(0, 2500)
        num = random.randint(0, 3)
        if num is 0:
            self.__setitem__('X*Y', '%s*%s' % (x, y), x*y)
        elif num is 1:
            self.__setitem__('X-Y', '%s-%s' % (x, y), x-y)
        elif num is 2:
            self.__setitem__('X+Y', '%s+%s' % (x, y), x+y)
        else:
            self.__setitem__('X/Y', '%s/%s' % (x, y), x/y)