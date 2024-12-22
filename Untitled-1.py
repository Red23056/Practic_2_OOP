import xml.etree.ElementTree as ET
#D:\address.csv
#D:\address.xml

import csv
import time
import os

class csv_file:
    def __init__(self, file): 
        self.file = file
        self.data = self.csv_parser()

    def csv_parser(self):
        with open(self.file, mode='r', encoding='utf-8') as file:
            mass = list()
            csv_file = csv.DictReader(file, delimiter=';')
            for element in csv_file:
                mass.append((element['city'], element['street'], element['house'], element['floor']))
            return mass
        
class xml_file:
    def __init__(self, file):
        self.file = file
        self.data = self.xml_parser()
        
    def xml_parser(self):
        mass = list()
        tree = ET.parse(self.file)
        root = tree.getroot()
        for item in root.findall('item'):
            mass.append((item.get('city'), item.get('street'), item.get('house'), item.get('floor')))   
        return mass
        
    
class file_reader:
    def __init__(self, file):
        self.file = file
        if self.file.endswith('.xml'):
            xml = xml_file(self.file)
            self.data = xml.xml_parser()

        else:
            csv = csv_file(self.file)
            self.data = csv.csv_parser()        

        self.repeats, self.floor_counter = self.data_processor()

    def data_processor(self):
        repeats = dict()
        floor_counter = dict()
        for element in self.data:
            if ((element[0], element[1], element[2]) in repeats):
                repeats[(element[0], element[1], element[2])] += 1

            else:
                repeats[(element[0], element[1], element[2])] = 0

            if (element[0] in floor_counter):
                floor_counter[element[0]][int(element[3])-1] += 1

            else:
                floor_counter[element[0]] = list()
                for i in range(5):
                    floor_counter[element[0]].append(0)

        return repeats, floor_counter

    def print_resualts(self):
        print("Повторения: ")
        for element in self.repeats:
            if (self.repeats[element] > 0):
                print(element[0], element[1], element[2], "\nКоличество повторений:", self.repeats[element]+1)
        print("Количество домов по этажам:")
        for element in self.floor_counter:
            print("Город:", element)
            for i in range(5):
                print("Максимальный этаж", str(i+1) + "количество домов:", self.floor_counter[element][i])

def user_interface():
    work = True
    print('Введите директорию файла или "end" для завершения работы')
    while (work):
        file_name = input()
        if (file_name == "end"):
            work = False
        elif not os.path.exists(file_name):
            print("Файл не найден")
        else:
            start_time = time.time()
            
            if file_name.endswith('.xml') or file_name.endswith('.csv'):
                file = file_reader(file_name)
                print("Время выполнения программы:", time.time() - start_time)
                file.print_resualts()
                work = False;    
            else:
                print("Недопустимый формат файла")

user_interface()
