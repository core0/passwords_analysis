# -*- coding:utf-8 -*-

import os, sys, re
from operator import itemgetter

##работа с длинами пароля
def show_lenpass(diction,length,minmax):
    mass = []
    ##обход всех значений и сравнение с заданой длиной, в зависимости от minmax сравнивается больше или меньше
    for k in diction.values():
        ##больше
        if(minmax):
            if(len(k)>=length):
                mass.append(k)
        else:##меньше
            if(len(k)<length):
                mass.append(k)
    ##вывод результата
    if(minmax):
        print u"Кол-во паролей >"+str(length) , len(mass)
    else:
        print u"Кол-во паролей <"+str(length) , len(mass)
    return mass

## пароль цифры
def show_pass_isnumber(diction):
    mass = []
    for k in diction.values():
        ##если в пароле только цифры
        ##парсим цыфры и сравниваем длину
        if(len(re.findall(r'\d+',k))>0):
            if(len(k)==len(re.findall(r'\d+',k)[0])):
                mass.append(k)
    return mass

## пароль буквы
def show_pass_alpha(diction):
    mass = []
    for k in diction.values():
        ##если в пароле только алфавитные символы
        ##парсим буквы и сравниваем длину
        if(len(re.findall(r'[a-zA-ZА-Яа-я]+',k))>0):
            if(len(k)==len(re.findall(r'[a-zA-ZА-Яа-я]+',k)[0])):
                mass.append(k)
    return mass

##пароль цифры буквы
def show_pass_other(diction):
    mass = []
    for k in diction.values():
        ##парсим и сравниваем длину если в пароле только буквы и цифры
        find_d = re.findall(r'\d',k)
        find_w = re.findall(r'[a-zA-ZА-Яа-я]',k)
        if(len(find_w)>0 and len(find_d)>0):
            if(len(re.findall(r'\w+',k))>0):
                if(len(k)==len(re.findall(r'\w+',k)[0])):
                    mass.append(k)
    return mass


##повторяющиеся пароли
def pass_dubl(diction):
    ##все значения паролей
    passw = diction.values()
    res = []

    for k in passw:
        ##если пароль встречает >1 в главном массиве и его еще нет в результирующем то добавляем его у результирующий
        if(passw.count(k)>1 and res.count(k)<1):
            res.append(k)
    return res

## максимально повторяющийся пароль
def pass_dubl_max(diction):
    passw = diction.values()
    c=0
    res = ''
    for k in passw:
        ##если пароль k встречается в главном массиве >c и длина пароля >0(защита от пустых паролей)
        if(passw.count(k)>c and len(k.strip())>0):
            ##запоминаем это число
            c = passw.count(k)
            ##запоминаем пароль и число повторений
            res=k+" - "+str(c)
    return res

##число паролей с количеством "с" цифр в конце слова
def pass_last_num(diction,c):
    mass = []

    for k in diction.values():
        ##если длина пароля больше, кол-ва цифр которых мы ищем в конце
        temp=''
        if(len(k)>c+1):
            ##парсим значение
            z=k[:len(k)-c]
            if z.isalpha():
                temp = re.findall(r'\w+\d{'+str(c)+'}',k)
            ##если значение нашлось и длина его равна длине пароля, добавляем элемент
            if(len(temp)>0):
                    mass.append(k)
    return mass

##кол-во паролей в верхнем регистре
def pass_inUPPER(diction):
    mass = []
    for k in diction.values():

        if(len(k)>0):
            ##если в верхнем регистре
            if(k.isupper()):
                mass.append(k)
    return mass

##кол - во паролей в нижнем регистре
def pass_INlower(diction):
    mass = []
    for k in diction.values():
        if(len(k)>0):
            ##если в нижнем регистре
            if(k.islower()):
                mass.append(k)
    return mass

##кол-во паролей в смешаном регистре
def pass_inlowerUPPER(diction):
    ##число верхнего и нежнего регистра, найденое путем вычитания из общего кол-ва
    ##паролей суммы паролей только в нижним и только в верхнем регистре
    r = len(diction) - (len(pass_INlower(diction))+len(pass_inUPPER(diction)))
    return r

##кол-во паролей похожим на номер телефона
def pass_is_phone(diction):
    ##значения всех паролей
    dat = diction.values()
    result = []
    for item in dat:
        ##парсим возможные вырианты телефонных номеров
        tm = re.findall(r'^\d{7}$',item)
        result+=tm
        tm = re.findall(r'^\d{6}$',item)
        result+=tm
        tm = re.findall(r'^89\d{9}$',item)
        result+=tm
        tm = re.findall(r'^9\d{9}$',item)
        result+=tm
        tm = re.findall(r'^49\d{8}$',item)
        result+=tm
    ##извлекаем уникальные
    result = list(set(result))
    return result

## имя пароля = имени почты
def show_identical_pass_email(diction):
    mass = []
    for k in diction:
        ##Добавляем только если имя пользователя равно паролю или если имя пользователя равно инвертированному паролю
        if(diction[k]==k.split('@')[0] or diction[k]==k.split('@')[0][::-1]):
            mass.append(diction[k])
    return mass

def show_identical_pass_in_email(diction):
    mass = []
    for k in diction:
        ##Добавляем только если имя пользователя содержит в себе парол или если имя пользователя содержит в себе инвертированный парол
        if(k.split('@')[0].find(diction[k])>0 or k.split('@')[0].find(diction[k][::-1])>0):
            mass.append(diction[k])
    return mass

def show_identical_email_in_pass(diction):
    mass = []
    for k in diction:
        ##Добавляем только если пароль содержит в себе имя пользователя или пароль содержит в себе инвертированное имя пользователя
        if(diction[k].find(k.split('@')[0])>0 or diction[k].find(k.split('@')[0][::-1])>0):
            mass.append(diction[k])
    return mass
######################
def show_count_pass_copy_date(diction):
    dat = diction.values()
    ##парсим дату
    result = []
    for item in dat:
        if(len( re.findall(r'[1-31][1-12]\d{4}',item))>0):
            if(len(item)==len(re.findall(r'[1-31][1-12]\d{4}',item)[0])):
                result.append(item)

    ##извлекаем уникальные
    result = list(set(result))
    return result


def checkascii(stok):
    for i in stok:
        if ord(i) > 126:
            return True
    return False



def c_pass_on_russia(diction):
    dat = diction.values()
    res = 0
    ff = []
    for k in dat:
        try:
            '''##поиск русских слов
            temp = re.findall('[А-Яа-я]*',k)
            ##если значение найдено
            if temp:
                ##если значение равно по длине паролю
                if(temp[0]==k):
                    ff.append(k)
                    res +=1'''
            if(checkascii(k)):
                res +=1
                pass

        except():
            print
    for g in ff:
        try:
            print g.decode('utf-8')
        except(UnicodeEncodeError):
            print 'error'


    return res

def c_pass_on_NOTrussia(diction):
    dat = diction.values()
    res = 0
    for k in dat:
        temp =re.findall(r'[a-zA-Z]*',k)
        ##если значение найдено
        if(len(temp)>0):
            ##если значение равно по длине паролю
            if(len(temp[0])==len(k)):
                res +=1
    return res

def show_set_share(diction,finds_list,ispass):
    print
    ps = diction.values()
    c = 0
    f={}
    mas_ki = {}
    for w in finds_list:
        cnt = ps.count(w)
        if(cnt>0):
            c+=1
            f[w]=cnt
    hh = sorted(f.items(), key=itemgetter(1),reverse=True)
    if(ispass):
        for p in hh:
            print p[0].decode('utf-8'),'-',p[1]
    else:
        i=0
        for k in hh:
            print k[0].decode('utf-8'),'-',k[1]
            i+=1
            if(i==2):break
    print '-'*10

    return c

def get_mail_serv(diction):
    ##получаем список почтовых ящиков
    serv = diction.keys()
    servers = []

    for h in serv:
        ## вырезаем имена почтовых серверов и добавляем в массив
        domen = h.split('@')[1]
        if(h.count('.')>0 and len(h)>4 and len(domen.split('.')[0])>0):
            servers.append(domen)
    ##удаляем дубликаты
    uniq_d = list(set(servers))

    for i in uniq_d:
        print i,' - ', servers.count(i)

    return uniq_d

def get_dubl_name(diction):
    names = diction.keys()
    nm = []
    for h in names:
        ## вырезаем имя пользователя
        nm.append(h.split('@')[0])
    ##удаляем дубликаты
    nm = list(set(nm))
    return len(names) - len(nm)

def rasp_pass20(diction):
    ps = diction.values()
    res={}
    for p in ps:
        res[p]=ps.count(p)
    hh = sorted(res.items(), key=itemgetter(1),reverse=True)
    i=0
    for k in hh:
        if i==20:
            break
        i+=1
        print k[0].decode('utf-8'),'-',k[1]


##############################################################################
print 'working...'
##открываем файл
mails = open("log02.txt",'r').read()
##создаем словарь

mlps = {}
##массив для плохих паролей
incorrect = []

ms = mails.split()

for k in ms:
    ##создаем словарь email - password
    if(k.find('@') > 0 and k.find('.')>0 ):
        try:
            ##заполняем словарь
            ##имя пользователя и имя почтового сервера должно быть больше 0 и имя сервера содержать точку
            mail =k.split(":")[0]
            pas = k.split(":")[1]
            dmn = mail.split('@')[1]

            dmn1 = dmn.split('.')[1]
            dmn2 =dmn.split('.')[0]
            if(len(mail)>0 and len(pas)>0 and pas.count(' ')==0 and mail.count("@")>0 and dmn.count(".")>0 and len(dmn2)>0 and len(dmn1)>0):
                mlps[k.split(":")[0]]=k.split(":")[1]
            else:
                incorrect.append(k)
        except:##если не содержит : тогда заносим в список плохих
            incorrect.append(k)
    else:##если не содержит знака @ заносим в список плохих
        incorrect.append(k)


##всего записей
print u"Всего =", len(mlps)
print u"Некорректных =", len(incorrect)

##длины паролей
for c_ln in range(11):
    if(c_ln == 9):
        show_lenpass(mlps,8,1)
        continue
    if(c_ln == 10):
        show_lenpass(mlps,14,1)
        continue
    if(c_ln<2):
        continue
    show_lenpass(mlps,c_ln,0)


only_number = len(show_pass_isnumber(mlps))
only_numb_word = len(show_pass_other(mlps))

print u'Число паролей в которых только цифры:',only_number
print u'Число паролей в которых только буквы:',len(show_pass_alpha(mlps))
print u'Число паролей в которых только цифры и буквы:',len(show_pass_other(mlps))


rus = c_pass_on_russia(mlps)
eng = c_pass_on_NOTrussia(mlps)
com = len(mlps) -(rus+eng) - only_numb_word
print u'Кол-во паролей на русском:', rus
print u'Кол-во паролей на английском:', eng
print u'Кол-во паролей на русском и англиском:', com


print u'Самый повторяющийся пароль: ',pass_dubl_max(mlps)
print
print u'Число повторяющихся паролей(в порядке убывания)',
print
rasp_pass20(mlps)
print
print u'Повторяющихся паролей: ',len(pass_dubl(mlps))
print
print u"Число паролей у которых в концe", 1 ,u"число: ", len(pass_last_num(mlps,1))
print u"Число паролей у которых в концe", 2 ,u"числа: ", len(pass_last_num(mlps,2))
print u"Число паролей у которых в концe", 3 ,u"числа: ", len(pass_last_num(mlps,3))
print u"Число паролей у которых в концe", 4 ,u"числа: ", len(pass_last_num(mlps,4))


print u"Число паролей в нижнем регистре: ", len(pass_INlower(mlps))
print u"Число паролей в верхнем регистре: ", len(pass_inUPPER(mlps))
print u"Число паролей в смешанном регистре: ", pass_inlowerUPPER(mlps)

print u"Число паролей похожих на номера телефонов", len(pass_is_phone(mlps))

print u'Число паролей совпадающих с именем почты:', len(show_identical_pass_email(mlps))
print u'Число паролей выходящих в имя почты:', len(show_identical_pass_in_email(mlps))
print u'Число паролей в которых входит имя почты:', len(show_identical_email_in_pass(mlps))


print u'Чилос паролей похожих на даты: ',len(show_count_pass_copy_date(mlps))

names = open('names.txt','r').read().split()
animals = open('animals.txt','r').read().split()
sports = open('sports.txt','r').read().split()
cumirs = open('cumirs.txt','r').read().split()
noobpass = open('pass.txt','r').read().split()

print u'Число паролей совпадающих с именами:', show_set_share(mlps,names,0)
print
print u'Число паролей содержащих название животных:', show_set_share(mlps,animals,0)
print
print u'Число паролей содержащих имена спорт клубов:', show_set_share(mlps,sports,0)
print
print u'Число паролей содержащих имена кумиров:', show_set_share(mlps,cumirs,0)
print
print u'Число паролей содержащих распространенные пароли:', show_set_share(mlps,noobpass,1)
print

un = len(get_mail_serv(mlps))
print u'Число разных почтовых серверов:',un
print u'Число дубликатов почтовых серверов:', len(mlps)-un
print u'Число дубликатов имен почты:',get_dubl_name(mlps)