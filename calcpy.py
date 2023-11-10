checkNumber = lambda x: isinstance(x, (int, float, complex))
checkOperation = lambda x: isinstance(x, (Add, Mul, Pow))

class Add():
    def __init__(self, a, b):
        if isinstance(a, str):
            try:
                a = int(a)
            except ValueError:
                a = Expr(a)
        if isinstance(b, str):
            try:
                b = int(b)
            except ValueError:
                b = Expr(b)
        self.__a = a
        self.__b = b

    def evalf(self, n=10):
        if checkOperation(self.__a):
            self.__a = self.__a.evalf(n)
        
        if checkOperation(self.__b):
            self.__b = self.__b.evalf(n)

        return round(self.__a + self.__b, n)
    
    def __repr__(self):
        return f'Add({str(self.__a)}, {str(self.__b)})'

    def __str__(self):
        return f'Add({str(self.__a)}, {str(self.__b)})'

class Mul():
    def __init__(self, a, b):
        if isinstance(a, str):
            a = Expr(a)
        if isinstance(b, str):
            b = Expr(b)
        self.__a = a
        self.__b = b

    def evalf(self, n=10):
        if checkOperation(self.__a):
            self.__a = self.__a.evalf(n)
        
        if checkOperation(self.__b):
            self.__b = self.__b.evalf(n)

        return round(self.__a * self.__b, n)

    def __repr__(self):
        return f'Mul({str(self.__a)}, {str(self.__b)})'

    def __str__(self):
        return f'Mul({str(self.__a)}, {str(self.__b)})'

class Pow():
    def __init__(self, base, power, mod=None):
        if isinstance(base, str):
            base = Expr(base)
        if isinstance(power, str):
            power = Expr(power)
        self.__base = base
        self.__power = power
        self.__mod = mod

    def evalf(self, n=10):
        if checkOperation(self.__base):
            self.__base = self.__base.evalf(n)
            
        if checkOperation(self.__power):
            self.__power = self.__power.evalf(n)

        return round(pow(self.__base, self.__power, self.__mod), n)

    def __repr__(self):
        return f'Pow({str(self.__base)}, {str(self.__power)})'

    def __str__(self):
        return f'Pow({str(self.__base)}, {str(self.__power)})'

from typing import NewType
Operation = NewType('Operation', (Add, Mul, Pow))
Number = NewType('Number', (int, float, complex))

class Expr():
    def __init__(self, expr: (str, Operation, Number)):
        '''
        (str -> Expr) or just (Operation or Number)
        '''
        if isinstance(expr, str):
            expr = self.text2expr(expr)

        self.__expr = expr

    @staticmethod
    def text2expr(string):
        def spliting(string, sign):
            length = len(string)
            array = []
            bracket = 0
            start = 0
            for i in range(length):
                if string[i] == '(':
                    bracket += 1
                    
                elif string[i] == ')':
                    bracket -= 1

                if bracket == 0:
                    if string[i] == '+':
                        array.append(string[start: i])
                        start = i+1
            else:
                array.append(string[start: length])
                             
            return array

        def arr2expr(array, func):
            length = len(array)
            if length != 1:
                expr = func(array[0], array[1])
                for b in range(2, length):
                    expr = func(expr, array[b])
                    
                return expr
                
            else:
                return array[0]
        
        expr = arr2expr(spliting(string, '+'), Add) #Add
        return expr
    
    def __repr__(self):
        return f'{self.__expr}'

    def __str__(self):
        return str(self.__expr)

    def evalf(self, n=10):
        if isinstance(self.__expr, (Add, Mul, Pow)):
            value = self.__expr.evalf(n)
            
        elif isinstance(self.__expr, (int, float, complex)):
            value = self.__expr

        return value        

print(Expr('1+1+5+6+7+8').evalf())
