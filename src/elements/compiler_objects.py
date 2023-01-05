


class object:
    def __init__(self, val):
        self.val= val
    
    @property
    def value(self):
        return self.val
    
    @property
    def type(self):
        return self.__class__.__name__
    
    def __str__(self):
        return str(self.val)


    #Comparison
    def __eq__(self, other):
        return boolean(self.val == other.val)
    
    def __ne__(self, other):
        return boolean(self.val != other.val)
    
    def __lt__(self, other):
        return boolean(self.val < other.val)
    
    def __le__(self, other):
        return boolean(self.val <= other.val)
    
    def __gt__(self, other):
        return boolean(self.val > other.val)
    
    def __ge__(self, other):
        return boolean(self.val >= other.val)
    
    def __and__(self, other):
        return boolean(self.val and other.val)
    
    def __or__(self, other):
        return boolean(self.val or other.val)
    
    def __xor__(self, other):
        return boolean(self.val ^ other.val)
    
    def __invert__(self):
        return boolean(not self.val)
    


class number(object):
    def __init__(self, val) -> None:
        super().__init__(val)
    
    
    #Arithmetic
    def __add__(self, other):
        calc= self.val + other.val
        if isinstance(calc, int):
            return integer(calc)
        else:
            return decimal(calc)
    
    def __sub__(self, other):
        calc= self.val - other.val
        if isinstance(calc, int):
            return integer(calc)
        else:
            return decimal(calc)
    
    def __mul__(self, other):
        calc= self.val * other.val
        if isinstance(calc, int):
            return integer(calc)
        else:
            return decimal(calc)
    
    def __truediv__(self, other):
        calc= self.val / other.val
        if isinstance(calc, int):
            return integer(calc)
        else:
            return decimal(calc)
    
    def __floordiv__(self, other):
        calc= self.val // other.val
        if isinstance(calc, int):
            return integer(calc)
        else:
            return decimal(calc)
    
    def __mod__(self, other):
        calc= self.val % other.val
        if isinstance(calc, int):
            return integer(calc)
        else:
            return decimal(calc)
    
    def __pow__(self, other):
        calc= self.val ** other.val
        if isinstance(calc, int):
            return integer(calc)
        else:
            return decimal(calc)
    
    #Arithmetic with assignment
    # def __iadd__(self, other):
    #     self.val += other.val
    #     return self
    
    # def __isub__(self, other):
    #     self.val -= other.val
    #     return self
    
    
    #Unary
    def __neg__(self):
        calc= -self.val
        if isinstance(calc, int):
            return integer(calc)
        else:
            return decimal(calc)
    
    def __pos__(self):
        calc= self.val
        if isinstance(calc, int):
            return integer(calc)
        else:
            return decimal(calc)
    
    def __abs__(self):
        calc= abs(self.val)
        if isinstance(calc, int):
            return integer(calc)
        else:
            return decimal(calc)



class integer(number):
    def __init__(self, val) -> None:
        super().__init__(val)

    #return the type with type()



class decimal(number):
    def __init__(self, val) -> None:
        super().__init__(val)



class string(object):
    def __init__(self, val) -> None:
        super().__init__(val)
    
    def __add__(self, other):
        return string(self.val + other.val)
    

class boolean(object):
    def __init__(self, val) -> None:
        super().__init__(val)
    
    def __str__(self):
        return str(self.val).lower()


class array(object):
    def __init__(self, val) -> None:
        super().__init__(val)
    
    def __add__(self, other):
        return array(self.val + other.val)
    
    
    def __len__(self):
        return len(self.val)
    
    def __str__(self):
        l= []
        for i in self.val:
            if type(i) == number:
                l.append(i.value)
            else:
                l.append(str(i))
        return str(l)


# TIME
class time(object):
    '''
    Time class to handle time. It can be converted to days, months and years.
    Only handle integer values.
    Always return the floor value.
    :param name: the time name
    :param time: the time value
    :param type: the time type. Can be 'd' for days, 'm' for months or 'y' for years
    '''
    def __init__(self, val: int, time: str='d'):
        if time not in ['d', 'm', 'y']:
            raise ValueError('Invalid time type')
        if val < 0:
            raise ValueError('Time cannot be negative')
        self.time= time

        if time == 'd':
            super().__init__(val)
        elif time == 'm':
            super().__init__(val * 30)
        elif time == 'y':
            super().__init__(val * 365)
    

    @property
    def days(self):
        return self.val
    
    @property
    def months(self):
        return self.val // 30

    @property
    def years(self):
        return self.val // 365
    
    def __str__(self):
        if self.time == 'd':
            return str(self.days) + ' days'
        elif self.time == 'm':
            return str(self.months) + ' months'
        elif self.time == 'y':
            return str(self.years) + ' years'
    
    def to_days(self):
        '''
        Convert the time to days
        :param time: the time to be converted
        :return: the time converted to days
        '''
        self.time= 'd'
    
    def to_months(self):
        '''
        Convert the time to months
        :param time: the time to be converted
        :return: the time converted to months
        '''
        self.time= 'm'
    
    def to_years(self):
        '''
        Convert the time to years
        :param time: the time to be converted
        :return: the time converted to years
        '''
        self.time= 'y'
