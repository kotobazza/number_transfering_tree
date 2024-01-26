def old_description():
    """
    # этот алгоритм гарантированно выдает число или слово ERROR, если фраза неправильна
    # для работы потребуется алгоритм перевода фразы в список токенов
    # 
    # список токенов обрабатывается корректно, и корректно возвращает ERROR или число
    # 
    # #


    # UPDATE date(29/10)
    # Код гарантированно выдает число от 0 до 999 или ошибку, если фраза неправильая
    # TODO: hunderts - токен. Сейчас код выдает нерпавильную ошибку при неправильно написанном токене сотен
    # В начале он опишет, что токен написан неправильно, но если сотню написать в середине, будет получена странная ошибка как EMPTY HUNDERT\ein hundert
    # TODO: перестройка кода на полноценный полиморфизм (изменение ноды с добавлением ей функции, которую нужно выполнить с числом, чтобы оно могло нормально поменяться)
    # 
    # #

    # UPDATE
    # Теперь происходит полноценная обработка. 
    # Осталась серьезная проблема в архитектуре. 
    # Если два потомка имеют одинаковый вариант значений, выводится только вариант для первого значения, но не для второго
    # 
    # Реализуется пока с помощью кастыля
    # 
    # #
    """

# UPDTAE date(29/10)
# Считается завершенным, требует тестирований
# 
# 
# #

"""
Обязательно требуется, чтобы дерево строилось от класса Root к классу Node.
Запуск обработки нескольких деревьев возможен только с помощью класса Root

"""



class Types:
    hundert = {'hundert':100}
    
    ones_middle  = {'ein':1, 'zwei':2, 'drei':3, 'vier':4, 'fünf':5, 'sechs':6, 'sieben':7, 'acht':8, 'neun':9, 'funf':5}
    ones_ending = {'funf':5, 'eins':1, 'zwei':2, 'drei':3, 'vier':4, 'fünf':5, 'sechs':6, 'sieben':7, 'acht':8, 'neun':9}
    nulls = {'null': 0, 'nil':0, 'zero':0}
    first_ten = {'zwolf':12, 'funfzehn': 15, 'zehn':10, 'elf':11, 'zwölf':12, 'dreizehn':13, 'vierzehn':14, 'fünfzehn':15, 'sechzehn':16, 'siebzehn':17, 'achtzehn':18, 'neunzehn':19}
    tens = {'dreisig':30, 'funfzig':50, 'zwanzig':20, 'dreißig':30, 'vierzig':40, 'fünfzig':50, 'sechzig':60, 'siebzig':70, 'achtzig':80, 'neunzig':90}
    und = {'und': 0}

    def __init__(self):  

        self.anytype = dict()
        self.anytype.update(self.hundert)
        self.anytype.update(self.ones_middle)
        self.anytype.update(self.ones_ending)
        self.anytype.update(self.first_ten)
        self.anytype.update(self.tens)
        self.anytype.update(self.und)
        self.anytype.update(self.nulls)



types = Types()


def DefineWordType(word:str):
        if word in types.anytype:
            if word in types.hundert:
                return "Hundert"
            if word in types.und:
                return 'Und'
            if word in types.ones_ending:
                return 'Число формата единиц'
            if word in types.ones_middle:
                return 'Число формата единиц'
            if word in types.nulls:
                return "Число формата нулей"
            if word in types.first_ten:
                return 'Число формата 10-19'
            if word in types.tens:
                return "Число формата десятков"
        else:
            return "Неизвестное слово" #не принадлежит ни одному типу


def find_deepest_value(arr, counter):
    if isinstance(arr, list):
        deepest = None  
        maxLevel = counter
        for item in arr:
            value, a = find_deepest_value(item, counter+1)  
            if a>maxLevel:  
                deepest = value
                maxLevel = a
        return deepest, maxLevel
    else:
        return arr, counter


class Node():
    childs:list
    value:dict
    name:str
    NodeType:int
    ErrorNotEnough:str
    PendingChilds: list
    delimetr:str
    ChangeFunction: callable

    def __init__(self, name:str, value:dict, childs:list, func:callable, nodetype=1):
        self.childs = childs
        self.value = value
        self.name = name
        self.NodeType = nodetype
        self.PendingChilds = [child.name for child in childs]
        self.ChangeFunction = func


    def recursivebypass(self, number:list, index, counter, errlst) -> (int, int, int):
        #print("  "*index, "TEST ", self.name, " INDEX: ", index, " COUNTER: ", counter)

        
        if self.NodeType == 0 and len(number) == index:
            #найден правильный конец - выход из обработки дерева
            return (counter, 1, -1) 
        
        if self.NodeType == 0 and len(number) > index: 
            #после конца листа идут еще слова
            return (0, -1, index)

        
        if self.NodeType == 1 and len(number) == index:  
            #не хватает слов на обработку варианта (возникает, когда слова должны быть но их нет)
            return (0, -1, index) 
        
        if number[index] not in self.value.keys():
            #слово не находится в возможных значениях 
            return (0, -1, index)
        
        

        t = -1
        errls = []

        for child in self.childs:
            errl = []
            a, b, level = child.recursivebypass(number, index+1, self.ChangeFunction(counter, self.value[number[index]]), errl)
            if b==1:
                return (a, b, level)
            if b == -1:
                
                if len(number) == level:
                    errl.append(f"После {self.name} идет Конец фразы")
                else:
                    typ = DefineWordType(number[level])
                    if typ == "Hundert" or typ == "Und":
                        errl.append(f"После {self.name} идет {typ}")
                    else:
                        errl.append(f"После {self.name} идет {typ}: '{number[level]}'")
            
            if t < level: 
                t=level
            errls.append(*errl)
            
        errlst.append(errls)
        # ни один потомок не вернул 1 как кода отсутствия ошибки - необрабатываемый вариант
        return (0, 0, t)
        


class Root(Node):
    def __init__(self, name:str, value:dict, childs:list, func:callable, nodetype=1):
        super().__init__(name, value, childs, func, nodetype)
    
    def recursivebypass(self, number:list):
        #print("LEVEL: ROOT\n\n")
        t = "ERROR"
        errlist = []

        for child in self.childs:
            errlst = []
            counter, b, level = child.recursivebypass(number, 0, 0, errlst)
            if b == 1:
                t = counter
                break
            errlist.append([level, errlst])
        if not isinstance(t, int):
            t = find_deepest_value(errlist, 0)[0]
            if t == 0:
                t = -1
        if t == -1:
            typ = DefineWordType(number[0])
            return f"В начале фразы идет {typ}: '{number[0]}'"
        return t



        

def germanNumbersConverter(string:str):
    string = string.lower()
    numbers = string.split()

    summator = lambda counter, val: counter+val
    multiplier = lambda counter, val: counter*val
    
    a = Types()

    anytype = a.anytype

    type_end = Node("Конец фразы", dict(), [], summator, nodetype=0) #конец дерева

    type_tens = Node("Числа формата десятков", a.tens, [type_end], summator)
    type_und = Node("Und", a.und, [type_tens], summator)
    type_firstTen = Node("Числа формата 10-19", a.first_ten, [type_end], summator)
    type_onesMiddle = Node("Числа формата единиц", a.ones_middle, [type_und], summator)
    type_onesEnding = Node("Числа формата единиц", a.ones_ending, [type_end], summator)
    type_hundert = Node("Hundert", a.hundert, [type_tens, type_firstTen, type_onesEnding, type_end, type_onesMiddle], multiplier)
    type_onesHunderted = Node("Числа формата единиц", a.ones_middle, [type_hundert], summator)
    type_nulls = Node("Числа формата нулей", a.nulls, [type_end], summator)

    root = Root("Root", a.anytype, [type_nulls, type_onesEnding, type_firstTen, type_tens, type_onesMiddle, type_onesHunderted], summator)

    #кастыль

    type_onesMiddle.PendingChilds.append("Hundert")
    type_onesHunderted.PendingChilds.append('Und')


    #конец кастыля

    return root.recursivebypass(numbers)

    
if __name__ == "__main__":

    number = "eidn hundert ein und zwanzig"
    print(germanNumbersConverter(number))





