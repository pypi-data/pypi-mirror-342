from ..tools import operators
import datetime

__all__ = ["Unit", "Line", "Area", "Volume", "Capacity", "Duration", "Version", "datetime", "operators"]

class Unit:
    """
        The unit class.It can use in science calculate.

        :Example:  
        >>> Unit(1,'a')
        '1a'

        :param int number: Your Unit number.
        :param str unit: Your Unit unit.
        :param str = "" type: Your Unit type.
    """
    conversion_list = {}
    def __init__(self, number: int, unit: str, type: str = ""): 
        self.type = type
        self.number = number
        self.unit = unit
        self.data = [self.number, self.unit]
        self.unit_list = []
        self.unit_conversion = []
        for k, v in self.conversion_list.items(): 
            self.unit_list.append(k)
            self.unit_conversion.append(v)

    def conversion(self, end_unit: str): 
        '''
        Convert your unit.
        Before use it,please set the conversion list.

        :Example: 
        >>> a = Unit(1,'a')
        >>> a.set_con(a = 1, b = 100)
        >>> a.conversion('b')
        '0.01b'

        :param str end_unit: The unit you want to convert into.
        :return: Convert the unit.
        :rtype: Unit.
        '''
        number = self.number  *  (self.conversion_list[self.unit] / self.conversion_list[end_unit])
        unit = end_unit
        return self.create_new(number, unit)

    def syn_type(self, other): 
        """
        If two Unit's type is same,the other's conversion list is self conversion list..

        :raises TypeError: You input is not a Unit class.
        """
        if isinstance(other, self.__class__): 
            if self.type == other.type: 
                other.conversion_list = self.conversion_list
        else: 
            raise TypeError("value '"+str(other)+"' is "+str(type(other))+", not Unit class")

    def set_con(self,  **list): 
        "Set the conversion list."
        self.conversion_list = {}
        self.unit_conversion = []
        self.unit_list = []
        for k, v in list.items(): 
            self.conversion_list[k] = v
            self.unit_conversion.append(v)
            self.unit_list.append(k)

    def append_con(self,  **list): 
        "Append the conversion list."
        for k, v in list.items(): 
            self.conversion_list[k] = v
            self.unit_conversion.append(v)
            self.unit_list.append(k)

    def delete_con(self, keys): 
        "Delete the conversion list."
        indexs = self.unit_list.index(keys)
        del self.conversion_list[keys]
        del self.unit_list[indexs]
        del self.unit_conversion[indexs]

    def set_attr(self, value: list[int, str], conversion_unit: bool = False): 
        '''
        It can use the same type Unit too.
        Set the Unit is input unit.

        :Example: 
        >>> a = Unit(1,'a')
        >>> b = Unit(1,'b')
        >>> a.set_con(a = 1, b = 100)
        >>> a.set_attr(b)
        '100a'
        >>> a.set_attr(b,True)
        '1b'
        >>> a.set_attr([20,'a'])
        '20a'

        :param list[int,str] | Unit class value: Unit you want to set.
        :param bool = False conversion: If you want to set the unit too,set this variable True.
        :return: The input Unit class
        :rtype: Unit
        '''
        if isinstance(value, self.__class__): 
            self.syn_type(value)
            number = value.number
            if conversion_unit: 
                unit = value.unit
            else: 
                unit = self.unit
            return self.create_new(number, unit)
        elif isinstance(value, list): 
            if value[1] in self.conversion_list: 
                unit = value[1]
                number = value[0]
                return self.create_new(number, unit)
            else: 
                raise KeyError("key'"+self.unit+"'is not in this class")
        else: 
            raise TypeError("value '"+str(value)+"' is"+str(type(value))+", not Unit or list.")

    def setone(self, unit: str): 
        '''
        Set the unit is 1, else correspond change.

        :param str unit: Unit you want to convert.
        '''
        temp_dict = self.conversion_list
        for k, v in self.conversion_list.items(): 
            temp_dict[k] = v/self.conversion_list[unit]
        self.conversion_list = temp_dict

    def __create_new(self, num: int, unit: str): 
        '''
        If you create a Unit class when inherit is Unit(recommed use this unit when you create create a Unit class).
        Clone a new unit.

        :return: A new Unit class.
        :rtype: Unit
        '''
        n = self.__class__(num, unit, self.type)
        self.syn_type(n)
        return n

    def change_attr(self, func, value: list[int, str]): 
        """
        It can use the same type Unit too.
        Change the Unit.

        :Example: 
        >>> a = Unit(1,'a')
        >>> b = Unit(1,'b')
        >>> a.set_con(a = 1, b = 100)
        >>> a.change_attr(operators.matical.add,b)
        '101a'
        >>> a.change_attr(operators.matical.add,[20,'a'])
        '21a'

        :param function func: The control function.It is in operators.matical.
        :param list[int,str] | Unit class value: The change value.
        :return: The changed Unit class
        :rtype: Unit
        """
        if isinstance(value, self.__class__): 
            self.syn_type(value)
            number = func(self.number, value.conversion(self.unit).number)
            return self.create_new(number, self.unit)
        elif isinstance(value, list): 
            if value[1] in self.conversion_list: 
                value[0]  *= self.conversion_list[value[1]] / self.conversion_list[self.unit]
                number = func(self.number, value[0])
                return self.create_new(number, self.unit)
            else: 
                raise KeyError("key'"+value[1]+"'is not in this class")
        else: 
            raise TypeError("value '"+str(value)+"' is"+str(type(value))+", not Unit or list.")

    def operator(self, func, value: list[int, str]) -> bool: 
        """
        Value can Unit too.
        Operator the unit.

        :Example: 
        >>> a = Unit(1,'a')
        >>> b = Unit(1,'b')
        >>> a.set_con(a = 1, b = 100)
        >>> a.operator(operators.comparison.gt, b)
        False
        >>> a.operator(operators.comparison.le, [20, 'a'])
        True

        :param function func: The control function.It is in operators.comparison.
        :param list[int,str] | Unit class value: The change value.
        :return: The operator Unit class result.
        :rtype: bool
        """
        if isinstance(value, self.__class__): 
            self.syn_type(value)
            op = func(self.number, value.conversion(self.unit).number)
        elif isinstance(value, list): 
            if value[1] in self.conversion_list: 
                value[0]  *= (self.conversion_list[value[1]] / self.conversion_list[self.unit])
                op = func(self.number, value[0])
            else: 
                raise KeyError("key'"+value[1]+"'is not in this class")
        else: 
                raise TypeError("value '"+str(value)+"' is"+str(type(value))+", not Unit or list.")
        return op

    @property
    def attributes(self): 
        return f"{'attributes': -^30}\nnum = {self.number}\nunit = {self.unit}\ntype = {self.type}\nconversion = {self.conversion_list}"

    def set_num(self, other: int): 
        '''
        value can Unit too.
        Set the number.
        '''
        if isinstance(other, self.__class__): 
            number = other.number
        elif isinstance(other, int): 
            number = other
        else: 
            raise TypeError("value '"+str(other)+"' is"+str(type(other))+", not Unit or int.")
        return self.create_new(number, self.unit)

    def set_unit(self, other: str): 
        '''
        Value can Unit too.
        Set the unit.
        '''
        save_unit = self.unit
        if isinstance(other, self.__class__): 
            unit = other.unit
        elif isinstance(other, str): 
            unit = other
        else: 
            raise TypeError("value '"+str(other)+"' is"+str(type(other))+", not Unit or str.")
        if self.unit not in self.conversion_list: 
            self.unit = save_unit
            raise KeyError("key '"+self.unit+"'not in conversion list.")
        return self.create_new(self.number, unit)

    def __iter__(self): 
        return iter(self.data)

    def __getitem__(self, index): 
        return self.data[index]

    def __add__(self, value: list): 
        return self.change_attr(operators.matical.add, value)

    def __sub__(self, value: list): 
        return self.change_attr(operators.matical.sub, value)

    def __mul__(self, value: int): 
        number = self.number * value
        return self.create_new(number, self.unit)

    def __truediv__(self, value: int): 
        number = self.number/value
        return self.create_new(number, self.unit)

    def __floordiv__(self, value: int): 
        number = self.number//value
        return self.create_new(number, self.unit)

    def __radd__(self, value: list): 
        return self.change_attr(operators.matical.add, value)

    def __rsub__(self, value: list): 
        return self.change_attr(operators.matical.sub, value)

    def __rmul__(self, value: int): 
        number = self.number * value
        return self.create_new(number, self.unit)

    def __rtruediv__(self, value: int): 
        number = self.number/value
        return self.create_new(number, self.unit)

    def __rfloordiv__(self, value: int): 
        number = self.number//value
        return self.create_new(number, self.unit)

    def __lshift__(self, other): 
        '''
        Value can Unit too.
        If num is Unit, set the self unit the other unit, same as set_unit(other)
        If num is int, set the unit left the other.
        '''
        if isinstance(other, self.__class__): 
            unit = other.unit
        elif isinstance(other, int): 
            unit = self.unit_list[self.unit_list.index(self.unit) - other]
        else: 
            raise TypeError("value '"+str(other)+"' is"+str(type(other))+", not Unit or int.")
        return self.create_new(self.number, unit)

    def __rlshift__(self, other): 
        '''
        Value can Unit too.
        If num is Unit, set the self unit the other unit, same as set_unit(other)
        If num is int, set the unit left the other.
        '''
        if isinstance(other, int): 
            return other<<self.number
        else: 
            raise TypeError("value '"+str(other)+"' is"+str(type(other))+", not Unit or int.")

    def __rshift__(self, other): 
        '''
        Value can Unit too.
        If num is Unit, set the self unit the other unit, same as other.set_unit(self)
        If num is int, set the unit right the other.
        '''
        if isinstance(other, self.__class__): 
            other.set_unit(self)
        elif isinstance(other, int): 
            unit = self.unit_list[self.unit_list.index(self.unit) + other]
        else: 
            raise TypeError("value '"+str(other)+"' is"+str(type(other))+", not Unit or int.")
        return self.create_new(self.number, unit)

    def __rrshift__(self, other): 
        '''
        Value can Unit too.
        If num is Unit, set the self unit the other unit, same as other.set_unit(self)
        If num is int, set the unit right the other.
        '''
        if isinstance(other, int): 
            return other >> self.number
        else: 
            raise TypeError("value '"+str(other)+"' is"+str(type(other))+", not int.")

    def __eq__(self, value: list): 
        return self.operator(operators.comparison.eq, value)

    def __ne__(self, value: list): 
        return self.operator(operators.comparison.ne, value)

    def __lt__(self, value: list): 
        return self.operator(operators.comparison.lt, value)

    def __gt__(self, value: list): 
        return self.operator(operators.comparison.gt, value)

    def __le__(self, value: list): 
        return self.operator(operators.comparison.le, value)

    def __ge__(self, value: list):     
        return self.operator(operators.comparison.ge, value)

    def __neg__(self): 
        return self.create_new(self.number, self.unit)

    def __pos__(self): 
        return self.create_new(self.number, self.unit)

    def __str__(self): 
        return str(self.number) + self.unit

    def __repr__(self): 
        return str(self.number) + self.unit

    def __hash__(self):
        return hash(self.data)

class Point: 
    def __init__(self): 
        pass

class Line(Unit): 
    def __init__(self, number, unit): 
        self.conversion_list = {
            "nm": 1/1000 ** 2, "um": 1/1000, "mm": 1, "cm": 10, "dm": 100, "m": 1000, "km": 1000 * 1000,
            "AU": 149_597_870.7 * 1000 ** 2, "ly": 63241.1 * 149_597_870.7 * 1000 ** 2, "pc": 206264.8 * 149_597_870.7 * 1000 ** 2, "mpc": 100_0000 * 206264.8 * 149_597_870.7 * 1000 ** 2,
            "in": 2540, "ft": 12 * 2540, "yd": 36 * 2540, "mi": 63660 * 2540, "nmi": 1.852 * 1000 ** 2
        }
        self.number = number
        self.unit = unit
        self.type = "area"
        if self.unit not in self.conversion_list: 
            raise KeyError("key'"+self.unit+"'is not in this class")

class Area(Unit): 
    def __init__(self, number, unit): 
        self.conversion_list = {
            "nm2": 1/1000 ** 4, "um2": 1/1000 ** 2, "mm2": 1, "cm2": 100, "dm2": 10000, "m2": 10000 * 100, "are": 10000 ** 2, "ha": 10000 ** 2 * 100, "km2": 10000 ** 3,
            "in2": 2540 ** 2, "ft2": (12 * 2540) ** 2, "mi2": (63660 * 2540) ** 2, "acre2": 4046_8564_22.4
        }
        self.number = number
        self.unit = unit
        self.type = "area"
        if self.unit not in self.conversion_list: 
            raise KeyError("key'"+self.unit+"'is not in this class")

    def scale(self, value: int): 
        self.number *= (value ** 2)
        return self

    def __mul__(self, value: int): 
        assert isinstance(value, int)
        self.number *= (value ** 2)
        return self

    def __truediv__(self, value: int): 
        assert isinstance(value, int)
        self.number/= (value ** 2)
        return self

class Volume(Unit): 
    def __init__(self, number, unit): 
        self.conversion_list = {
            "nm3": 1/1000 ** 6, "um3": 1/1000 ** 3, "mm3": 1, "cm3": 1000, "dm3": 1000 ** 2, "m3": 1000 ** 3, "km3": 1000 ** 6,
            "in3": 2540 ** 3, "ft3": (12 * 2540) ** 3, "mi3": (63660 * 2540) ** 3
        }
        self.number = number
        self.unit = unit
        self.type = "volume"
        if self.unit not in self.conversion_list: 
            raise KeyError("key'"+self.unit+"'is not in this class")

    def scale(self, value: int): 
        self.number *= (value ** 3)
        return self

    def __mul__(self, value: int): 
        assert isinstance(value, int)
        self.number *= (value ** 3)
        return self

    def __truediv__(self, value: int): 
        assert isinstance(value, int)
        self.number/= (value ** 3)
        return self

    @property
    def capacity(self): 
        return Capacity(self.conversion("dm3").number, "L")

class Capacity(Unit): 
    def __init__(self, number, unit): 
        self.conversion_list = {
            "ml": 1, "L": 1000,
            "oz": 29.6, "dr": 29.6 * 0.125, "pt": 16 * 29.6, "tbsp": 14.8, "cup": 48 * 14.8, "gal": 128 * 29.6, "tsp": 14.8/3,

        }
        self.number = number
        self.unit = unit
        self.type = "capacity"
        if self.unit not in self.conversion_list: 
            raise KeyError("key'"+self.unit+"'is not in this class")

    @property
    def volume(self): 
        return Volume(self.conversion("L").number, "dm3")

class Duration(Unit): 
    def __init__(self, number: int, unit: str): 
        self.conversion_list = {"ms": 1, "s": 1000, "h": 60000, "d": 60000 * 24, "u": 60000 * 24 * 365/4, "y": 60000 * 24 * 365, "a": 60000 * 24 * 365 * 10, "c": 60000 * 24 * 365 * 100}
        self.number = number
        self.unit = unit
        self.type = "time"
        if self.unit not in self.conversion_list: 
            raise KeyError("key'"+self.unit+"'is not in this class")

class Weight(Unit): 
    def __init__(self, number: int, unit: str): 
        self.conversion_list = {}
        self.number = number
        self.unit = unit
        self.type = "weight"
        if self.unit not in self.conversion_list: 
            raise KeyError("key'"+self.unit+"'is not in this class")

class Time: 
    def __init__(self): 
        pass

class Version: 
    '''use to write project version.'''
    def __init__(self,  *version): 
        self.version_list = [str(i) for i in version]
        self.version = ".".join(self.version_list)

    def __iter__(self): 
        return iter(self.version_list)

    def __getitem__(self, index): 
        return self.version_list[index]

    def __len__(self): 
        return len(self.version_list)

    def __repr__(self): 
        return self.version
