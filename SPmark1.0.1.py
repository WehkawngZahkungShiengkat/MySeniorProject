# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 22:34:36 2020

@author: wehkawng Zahkung Shiengkat (wez)
"""
import re
import sqlite3
from sqlite3 import Error
from datetime import date
import csv 
 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn

def LoadWDt(wordIn):
    database = r"FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    executeStr = "SELECT * FROM wordsLibrary WHERE word == '" + wordIn + "'"
    cur.execute(executeStr)
    rows = cur.fetchall()
    LoadDtL = []
    for row in rows:
        WordT = str(row)
        WordT = re.sub('None',"'None'",WordT)
        wordTid = re.findall(r"\d+",WordT)
        #print(wordTid)
        for wfound in wordTid:
            wfound = str(wfound)
            Cto = "'"+wfound+"'"
            WordT = re.sub(wfound,Cto,WordT)
        #print(WordT)
        WordT = re.sub("[\(|\)]","",WordT)
        WordT = re.sub("', '","',,,'",WordT)
        WordT = WordT.split(',,,')
        Dln = []
        for w in WordT:
            w = re.sub("'","",w)
            Dln.append(w)
        WordT = Dln
        LoadDtL.append(WordT)
    return LoadDtL

def getWordType(DtIn):
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    executeStr = "SELECT Wtype FROM wordsLibrary WHERE word == '" + DtIn + "'"
    cur.execute(executeStr)
    rows = cur.fetchall()
    LoadDtL = []
    for row in rows:
        row = str(row)
        row = re.sub("[\(|\)|\'|\,]","",row)
        LoadDtL.append(row)
    #print(LoadDtL)
    if LoadDtL != []:
        availablel = ['Noun','placeRW','directway','Time']
        filterL = ''
        for t in LoadDtL:
            if t in availablel:
                filterL = t
        if filterL == '':
            toreturn = 'None'
        else:
            toreturn = filterL
    else:
        toreturn = 'NotFount'
    return toreturn

def checkInput(getIn1):
    getIn1 = re.sub('nhpa','hpa',getIn1)
    getIn = getIn1.split()
    #print(getIn[len(getIn)-1],len(getIn)-1)
    if getIn[len(getIn)-1] == 'e':
        getIn.remove('e')
    qw1 = 'i'
    qw2 = 'kun'
    qw3 = 'hpa' #what and why == ganing
    qw4 = 'kadai'
    qw5 = 'galoi'
    qw6 = 'ganang'
    qw7 = 'gara' #which where how (kaning (place: shara, kaw, makau, )    
    qw8 = 'ganing'
    qw9 = 'ta'
    #qw10 = 'ai'
    qw11 = 'baw'
    qw12 = 'rai'
    qw13 = 'na'
    qw14 = 'ma'
    qw15 = 'sa'
    qw16 = 'taw'
    qw17 = 're'
    qw18 = 'sai'
    qw19 = 'kade'
    #qwl = [qw1,qw2,qw3,qw4,qw5,qw6,qw7,qw8,qw9,qw10,qw11,qw12,qw13,qw14,qw15,qw16,qw17]
    Specialqwl = [qw2,qw9,qw12,qw13,qw15,qw16,qw18]
    Endword = [qw1,qw2,qw9,qw12,qw13,qw14,qw15,qw16,qw17,qw18]
    qwl = [qw1,qw2,qw3,qw4,qw5,qw6,qw7,qw8,qw19]
    qwlStore = {}
    keywords = []
    wwhCheck = {}    
    
    preW = ''
    for word in getIn:
        if word == getIn[len(getIn)-1]:
            if preW in Specialqwl:
                qwlStore[word] = getIn.index(word)
                #print(getIn[len(getIn)-2])
            elif word in Endword:
                qwlStore[word] = getIn.index(word)
        else:
            if word in qwl:
                qwlStore[word] = getIn.index(word)
            elif preW in qwl and word == qw11:
                qwlStore[word] = getIn.index(word)
        preW = word
        
    if len(list(qwlStore.keys())) > 0:
        
        qWords1 = list(qwlStore.keys())
        if qw1 in qWords1 or (qw2 in qWords1 and len(qWords1) < 2) : #i (sh) kun is in the sentence
            inputType = "y/nQuestion"
        elif qw3 in qWords1 and len(qWords1) > 1: #hpa is not the only question word
            if getIn[qwlStore[qw3]+1] == qw11:
                wordofwhy = ['majaw',qw12,qw13]
                if getIn[qwlStore[qw3]+2] == qw12 and getIn[qwlStore[qw3]+2] != qw13:
                    inputType = "whQuestionWhat" 
                elif getIn[qwlStore[qw3]+2] in wordofwhy:
                    inputType = "whQuestionWhy"
                    qwlStore[getIn[qwlStore[qw3] + 2]] = getIn.index(getIn[qwlStore[qw3] + 2])
                else: 
                    inputType = "whQuestionWhat"
            else:
                wordofwhy = ['majaw',qw12,qw13]
                if getIn[qwlStore[qw3]+1] == qw12 and getIn[qwlStore[qw3]+1] != qw13:
                    inputType = "whQuestionWhat" 
                elif getIn[qwlStore[qw3]+1] in wordofwhy:
                    inputType = "whQuestionWhy"
                    qwlStore[getIn[qwlStore[qw3] + 1]] = getIn.index(getIn[qwlStore[qw3] + 1])
                else: 
                    inputType = "whQuestionWhat"
        elif qw4 in qWords1 and len(qWords1) > 0: # kadai is not the only question word
            inputType = "whQuestionWho"
        elif qw5 in qWords1 and len(qWords1) > 0: # galoi is not the only question word
            inputType = "whQuestionWhen"
        elif qw19 in qWords1 and len(qWords1) > 0:
            timeword = False
            for wl in getIn:
                z = getWordType(wl)
                if z == 'Time':
                    timeword = True
                    print(getIn)
                    getIn.remove(wl)
            if timeword == True:
                inputType = "whQuestionWhen"
            else:
                inputType = "HowMuch"
        elif qw6 in qWords1 and len(qWords1) > 0:
            inputType = "whQuestionWhere"
            if getIn[qwlStore[qw6]+1] == 'na':
                qwlStore[getIn[qwlStore[qw6] + 1]] = getIn.index(getIn[qwlStore[qw6] + 1])
        elif qw7 in qWords1 and len(qWords1) > 0: # gara is not the only question word
            inputType = "whQuestion3"
            rNoAdd = 1
            if getIn[qwlStore[qw7]+1] == qw11:
                rNoAdd = 2
            if getIn[qwlStore[qw7]+rNoAdd] not in qWords1:
                wwhCheck[getIn[qwlStore[qw7]+rNoAdd]] = getWordType(getIn[qwlStore[qw7]+rNoAdd])
                #print(wwhCheck)
                if getIn[qwlStore[qw7]+rNoAdd] in wwhCheck.keys():
                    if wwhCheck[getIn[qwlStore[qw7]+rNoAdd]] == 'placeRW':
                        inputType = "whQuestionWhere"
                        qwlStore[getIn[qwlStore[qw7] + rNoAdd]] = getIn.index(getIn[qwlStore[qw7] + rNoAdd])
                    elif wwhCheck[getIn[qwlStore[qw7]+rNoAdd]] == 'Noun':
                        if rNoAdd == 1:
                            inputType = "whQuestionWhich"
                            qwlStore[getIn[qwlStore[qw7] + rNoAdd]] = getIn.index(getIn[qwlStore[qw7] + rNoAdd])
                        else:
                            inputType = "whQuestionWhat"
                    elif wwhCheck[getIn[qwlStore[qw7]+rNoAdd]] == 'directway':
                        inputType = "whQuestionHow"
                        qwlStore[getIn[qwlStore[qw7] + rNoAdd]] = getIn.index(getIn[qwlStore[qw7] + rNoAdd])
                    elif wwhCheck[getIn[qwlStore[qw7]+rNoAdd]] == 'Time':
                        inputType = "whQuestionWhen"
                    elif wwhCheck[getIn[qwlStore[qw7]+rNoAdd]] == 'None':
                        inputType = "whQuestionWhich"
                else:
                    inputType = "whQuestionWhich"
            else:
                inputType = "whQuestionWhich"
        else:
            inputType = "Sentence"
        #print(qwlStore.keys())
        for word in getIn:
            if word not in qwlStore.keys():
                keywords.append(word)
    else:
        inputType = "Sentence"
        qWords = []
        for word in getIn:
            keywords.append(word)
    
    #TO see what words have been processed 
    qwlStore = dict(sorted(qwlStore.items(), key=lambda x: x[1]))
    #print(qwlStore)
    if len(list(qwlStore.keys())) > 0:
        qWords = list(qwlStore.keys())[0]  
        keepTrack = list(qwlStore.keys())[0]  
        for wordR in qwlStore.keys():
            if wordR != keepTrack:
                DifferenceBetween = abs(qwlStore[wordR]-qwlStore[keepTrack])
                if DifferenceBetween == 1:
                    qWords += " " + wordR
                else:
                    qWords += " "+"__ "+ wordR
            keepTrack = wordR
    else:
        if list(qwlStore.keys()) == []:
            qWords = '-'
        else:
            qWords = list(qwlStore.keys())[0] 
    ###view processed words function
    
    #print(inputType,qWords,keywords)
    return inputType,keywords
    
def getDate():
    while True:
        try: 
            YearIn = int(input("> Galoi shaning hta shangai ai rai? \n: "))
            if YearIn > 1900 and YearIn < 2020:
                break
            else:
                print ("> Shangai nhtoi shaning ndai hpe nmai hkap la ai.")
        except:
            print("> Shangai shaning hpe hti hkum san san hte sha ka ya rit.")
    #return YearIn
    while True:
        MonthIn = input("> Shangai Shata galoi rai? \n: ")
        try:
            MonthIn = int(MonthIn)
            if MonthIn > 0 and MonthIn < 13:
                break
            else: 
                print("> Shangai shata hti hkum ka ai njaw taw ai.")
        except:
            MonthIn = MonthIn.lower()
            if re.match("^jan.*",MonthIn): MonthIn = 1; break
            elif re.match("^feb.*",MonthIn): MonthIn = 2; break
            elif re.match("^mar.*",MonthIn): MonthIn = 3; break
            elif re.match("^apr.*",MonthIn): MonthIn = 4; break
            elif re.match("^may.*",MonthIn): MonthIn = 5; break
            elif re.match("^jun.*",MonthIn): MonthIn = 6; break
            elif re.match("^jul.*",MonthIn): MonthIn = 7; break
            elif re.match("^aug.*",MonthIn): MonthIn = 8; break
            elif re.match("^sep.*",MonthIn): MonthIn = 9; break
            elif re.match("^oct.*",MonthIn): MonthIn = 10; break
            elif re.match("^nov.*",MonthIn): MonthIn = 11; break
            elif re.match("^dec.*",MonthIn): MonthIn = 12; break
            else:
                print("> Shangai shata hpe hti hkum san san hte sha ka ya rit.")
    while True:
        try:
            DayIn = int(input("> Shangai nhtoi shani gaw gade ya shani rai? \n: "))
            m30 = [4,6,9,11]
            m31 = [1,3,5,7,8,10,12]
            if MonthIn in m30:
                if DayIn <= 30: break
                else: print("> Shata man %d kaw nhtoi %d ya shani nnga ai." %(MonthIn,DayIn))
            if MonthIn in m31:
                if DayIn <= 31: break
                else: print("> Shata man %d kaw nhtoi %d ya shani nnga ai." %(MonthIn,DayIn))
            if MonthIn == 2:
                Febds = 28
                if YearIn%4 == 0:
                    Febds = Febds + 1
                if DayIn <= Febds: break
                else: print("> Shata man %d kaw nhtoi %d ya shani nnga ai." %(MonthIn,DayIn))
            else: 
                print("> Shata man %d kaw nhtoi %d ya shani nnga ai." %(MonthIn,DayIn))
            
        except:
            print("> Shangai nhtoi hpe hti hkum san san hte sha ka ya rit.")
    Date = [str(YearIn),str(MonthIn),str(DayIn)]
    dateJ = '-'.join(Date)
    return dateJ

def CheckDoB(DateIn):
    DoB = re.findall(r'\b\d+\b',DateIn)
    today = str(date.today())
    TodayD =re.findall(r'\b\d+\b',today)
    if TodayD[1][0] == '0':
        y = TodayD[0]
        m = TodayD[1][1]
        d = TodayD[2]
        TodayD = [y,m,d]
    if (DoB[1],DoB[2]) == (TodayD[1],TodayD[2]):
        birthday = True
    else: 
        birthday = False
    return birthday

def getUserid():
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute('SELECT Userid FROM UserInfo')
    row = cur.fetchone()
    test1 = str(row)
    test1 = re.sub("[\(|\)|\,]","",test1)
    return test1

def GetcheckUname():
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    getUname = input("> Ndai app kaw login na matu Username ka bang ya rit: ")
    Ustring = 'SELECT Username FROM LogIn where Username = "' + getUname + '"'
    cur.execute(Ustring)
    row = cur.fetchone()
    while True:
        if row != None:
            print("\n> laga username hpe jang lata ya rit.")
            getUname = input("> Ndai app kaw login na matu Username ka bang ya rit: ")
            Ustring = 'SELECT Username FROM LogIn where Username = "' + getUname + '"'
            cur.execute(Ustring)
            row = cur.fetchone()
        else:
            break
    return getUname

def GetcheckPwd():
    getpwd1 = input ("> username na matu password :")
    getpwd2 = input ("> password shateng na matu kalang bai ka bang ya rit :")
    while True:
        if getpwd1 == getpwd2:
            pwd = getpwd1
            break
        elif getpwd2 == "12":
            pwd = GetcheckPwd()
            break
        else:
            print("> Kalang bai ka bang ai password shawng na bang da ai password hte nbung taw ai.")
            getpwd2 = input ("password shateng na matu kalang bai ka bang ya rit \
                             (shing nrai)password nnan na bai galaw na nga yang 12 ngu kabang ya rit :")
    return pwd

def loadData(idIn):
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    Dload = 'SELECT Myubawhpan, HtinggawMying, ShingtengMying, ShagaMying, ShangaiNhtoi, \
    Buga, NgaShara, NgasharaMungdan FROM UserInfo where Userid = ' + idIn
    cur.execute(Dload)
    row = cur.fetchone()
    Dl = str(row)
    
    Dl = re.sub('[\(|\)|]','',Dl)
    Dl = re.sub("', '","',,,'",Dl)
    Dl = Dl.split(',,,')
    Dln = [idIn]
    for s in Dl:
        s = re.sub("'","",s)
        Dln.append(s)
    Dl = Dln
    return Dl

def SignUptoLogIn():
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute('SELECT Userid FROM UserInfo ORDER by Userid DESC')
    row = cur.fetchone()
    idForU = str(row)
    idForU = re.sub("[\(|\)|\,]","",idForU)
    uID = idForU
    getUname = GetcheckUname()
    getPwd = GetcheckPwd()
    RuNuP = '("' + getUname + '","' + getPwd + '","' + uID +  '")'
    cur.execute('insert into LogIn (Username, Userpwd, Userid) values '+
               RuNuP)
    conn.commit()
    return loadData(uID)

def SignUp():
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()
    Lname = input("Nang hpa baw a Myu rai: ")
    Mname = input("Htinggaw Mying gaw hpa rai: ")
    Fname = input("Shingteng mying gaw hpa rai: ")
    Nname = input("Manang ni gara hku shaga ma rai: ")
    date_entry = getDate()
    Buga = input("Daidaw Buga gaw gara kaw na rai: ")
    NgaShara = (input("Ya gara Mare(Myo) kaw nga taw ai rai: ")).lower()
    NgasharaMungdan = (input("Gara mungdan kaw nga ai rai: ")).lower()
    while True:
        print("> Npu na madun da ai hku rai sai nga yang (Rai Sai) ngu dip bang ya rit.")
        print("> Shing nrai bai galai mayu yang ma seng ang ai hti hkum san san hpe sha dip bang ya rit.")
        print("> Lama na myit galai mat na account ye nhpaw shi na nga yang ma Nrai Sai ngut dip bang ya rit.")
        print("1. Myu mying         :",Lname)
        print("2. Htinggaw mying    :",Mname)
        print("3. Shingteng mying   :",Fname)
        print("4. Shaga mying       :",Nname)
        print("5. Shangai nhtoi     :",date_entry)
        print("6. Daidaw Buga       :",Buga)
        print("7. Ya nga ai myo mare:",NgaShara)
        print("8. Ya nga ai mungdan :",NgasharaMungdan)
        uChoice = input(":|")
        if re.search("\d",uChoice):
            if uChoice == '1':
                Lname = input("> Nang hpa baw a Myu rai: ")
            elif uChoice == '2':
                Mname = input("> Htinggaw Mying gaw hpa rai: ")
            elif uChoice == '3' or uChoice == '4':
                Fname = input("> Shingteng mying gaw hpa rai: ")
            elif uChoice == '5':
                Nname = input("> Manang ni gara hku shaga ma rai: ")
            elif uChoice == '6':
                Buga = input("> Daidaw Buga gaw gara kaw na rai: ")
            elif uChoice == '7':
                NgaShara = input("> Ya gara Mare(Myo) kaw nga taw ai rai: ")
            elif uChoice == '8':
                NgasharaMungdan = input("> Gara mungdan kaw nga ai rai: ")
        else:
            uChoice = uChoice.lower()
        if not re.search(r'nrai',uChoice):
            if (re.search(r"\Wum\W",uChoice) or re.search(r"rai",uChoice)) or (re.search(r"um",uChoice) or (re.search(r"rai",uChoice)and(re.search(r"rai\W",uChoice)))):
                break
        
        
    
    confirm = input('Lahta na htai da ai hku rai sai i? Myit hkrum yang "ok" ngu ka ya rit. \n:')
    confirm = confirm.lower()
    if 'ok' in confirm:
        stringIn =  '("' + Lname + '","' + Mname + '","' + Fname + '","' + Nname + '","' + date_entry + '","' + Buga + '","' + NgaShara + '","' + NgasharaMungdan + '")'
        cur.execute('insert into UserInfo (Myubawhpan, HtinggawMying, ShingtengMying, ShagaMying, ShangaiNhtoi, Buga, NgaShara,NgasharaMungdan) values '+
                   stringIn)
        conn.commit()
        return SignUptoLogIn()
    else:
        return 'pat'
    
def LogIn():
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    getUname = input("Username: ")
    GetD = 'SELECT Userpwd FROM LogIn where Username = "' + getUname +'"'
    cur.execute(GetD)
    row = cur.fetchone()
    while True:
        if row != None:
            upwd = str(row)
            upwd = re.sub("[\(|\)|\,|\']","",upwd)
            getPwd = input("Password: ")
            loop = 0
            while getPwd != upwd:
                print("> password njaw nga ai, kalang bai jaw hkra bang ya rit")
                #print(upwd,getPwd)
                getPwd = input("Password: ")
                loop += 1
                if loop == 3:
                    return "pat"
            break
        else:
            print("> username %s nga ai nnga ai"%(getUname))
            getUname = input("Username: ")
            GetD = 'SELECT Userpwd FROM LogIn where Username = "' + getUname +'"'
            cur.execute(GetD)
            row = cur.fetchone()
    GetD = 'SELECT Userid FROM LogIn where Username = "' + getUname +'"'
    cur.execute(GetD)
    row = cur.fetchone()
    Uid = str(row)
    Uid = re.sub("[\(|\)|\,]","",Uid)
    #print(Uid)
    return loadData(Uid)

def loadBType():
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    executeStr = "SELECT wordID,word FROM wordsLibrary WHERE ParentWid == 29 AND wordID != 29"
    cur.execute(executeStr)
    rows = cur.fetchall()
    LoadDtL = {}
    for row in rows:
        row = str(row)
        row = re.sub("[\(\)\']","",row)
        row = row.split(", ")
        row[0] = int(row[0])
        LoadDtL[row[1]] = row[0]
    return LoadDtL
    
def getUserLocation(userid):
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    userid = str(userid)
    #print(userid)
    executeStr = 'SELECT NgaShara,NgasharaMungdan FROM UserInfo WHERE Userid == ' + userid 
    #print(executeStr)
    cur.execute(executeStr)
    row = cur.fetchone()
    row = str(row)
    row = re.sub("[\(\)\']","",row)
    row = row.split(", ")
    return row[0],row[1]

def getUserName(userid):
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    userid = userid
    executeStr = 'SELECT Myubawhpan, HtinggawMying, ShingtengMying FROM UserInfo WHERE Userid == ' + userid 
    cur.execute(executeStr)
    row = cur.fetchone()
    row = str(row)
    row = re.sub("[\(\)\']","",row)
    row = re.sub(",","",row)
    return row

def GetCityCountry(uidin):
    city, country = getUserLocation(uidin)
    Bcity = input(":|")
    Bcity = Bcity.lower()
    if (re.search(r"\Wum\W",Bcity) or re.search(r"\Wre\W",Bcity)) or (re.search(r"um",Bcity) or (re.search(r"re",Bcity)and(re.search(r"\Wre",Bcity)))):
        Bcity = city
        Bcountry = country
    else:
        Bcity = input("> Seng hpaw da ai Myo mare mying hpe mying san san - \n:|")
        Bcountry = input("> Seng hpaw da ai Mungdan mying - \n:|")
    return Bcity,Bcountry

def GetproductsL():
    product = (input("> Langai hpang langai dip bang ya rit. Ngut yang Ngut sai ngu ka ban ya rit. \n:|")).lower()
    products = product
    count = 0
    while True:
        if re.search(r"\sngut\s",product) or re.search(r"ngut",product):
            break
        else:
            if count>0:
                products += ","+product
        count +=1
        product = (input("> Langai hpang langai dip bang ya rit. Ngut yang Ngut sai ngu ka ban ya rit. \n:|")).lower()
    return products

def getBtype():
    LoadB = loadBType()
    LoadBlist = list(LoadB.keys())
    print("> Ya yang jahpan mai bang ai seng hpan ni gaw - ")
    for x in range(len(LoadBlist)):
        print(x+1,".",LoadBlist[x])
    while True:
        check = 1
        while check == 1:
            Btype = input("> Madu na seng hpan hpe lahta na seng hpan hti hkum hpe sha ka bang let lata ya rit. \n:|")
            try:
                Btype = int(Btype)
                check = 0
            except:
                print("> Chyeju hte, ")
        
        if Btype-1 < len(LoadBlist):
            break
        else:
            print("> Hti hkum",Btype,"la hta na kaw nnga shi ai.")  
    
    return LoadB[LoadBlist[Btype-1]],[LoadBlist[Btype-1]]

def BusinessCreate(uInid):
    BtypeID, Btype = getBtype()
    Bname = (input("> Seng mying gaw hpa nga rai? Nnga yang seng madu a mying bang ya rit. \n:|")).lower()
    OpenT = input("> Seng hpaw hpang ai ten hkying kade kaw rai? \n:|")
    CloseT = input("> Seng pat ten hkying kade kaw rai? \n:|")
    city, country = getUserLocation(uInid)
    print("> Seng hpaw da ai gaw ",city,"kaw re i?")
    bcity,bcountry = GetCityCountry(uInid)
    print("> Seng kaw nga ai lusha hpan ni hpe tsun dan rit.")
    Products =  GetproductsL() 
    priceMax = input("> Seng kaw na manu hpu dik htum lusha gaw gade dang re rai? \n:|")
    priceMin = input("> Seng kaw na manu hkyem sa dik htum lusha gaw gade dang re rai? \n:|")
    bcontact = input("> Seng de matut mahkai na matu phone(sh)social app account hpe ka bang da ya rit. \n:|")
    BDescrib = input("> Seng na lam hpe manam ni chye hkra kadun dawk sang lang dan rit. Nnga yang ma nnga ai ai lam tsun dan ya rit. \n:|")
    Bowner = getUserName(uInid)
    #l = [Bname,BtypeID,OpenT,CloseT,bcity,bcountry,priceMin,priceMax,Products,BDescrib,Bowner]    
    
    while True:
        print("> Npu na madun da ai hku rai sai nga yang Rai Sai ngu dip bang ya rit.")
        print("> Shing nrai bai galai mayu yang ma hti hkum san san hpe sha dip bang ya rit.")
        print("> Lama na myit galai na Seng a lam hpe app ntsa nkam mara sai nga yang mu Nrai Sai ngu na dip bang ya rit.")
        print("1. Seng baw hpan         :",Btype)
        print("2. Seng Mying            :",Bname)
        print("3. Seng nga ai Myo mare  :",bcity)
        print("4. Seng nga ai mungdan   :",bcountry)
        print("5. Seng hpaw hpang ai ten:",OpenT)
        print("6. Seng pat ai ten       :",CloseT)
        print("7. Lusha hpan ni         :",Products)
        print("8. Hpu dik htum manu     :",priceMax)
        print("9. Hkyem sa dik htum manu:",priceMin)
        print("10. Matut mahkai         :",bcontact)
        print("11. Seng a lam           :",BDescrib)
        uChoice = input(":|")
        if re.search("\d",uChoice):
            if uChoice == '1':
                BtypeID, Btype = getBtype()
            elif uChoice == '2':
                Bname = (input("> Seng mying gaw hpa nga rai? Nnga yang seng madu a mying bang ya rit. \n:|")).lower()
            elif uChoice == '3' or uChoice == '4':
                bcity,bcountry = GetCityCountry(uInid)
            elif uChoice == '5':
                OpenT = input("> Seng hpaw hpang ai ten hkying kade kaw rai? \n:|")
            elif uChoice == '6':
                CloseT = input("> Seng pat ten hkying kade kaw rai? \n:|")
            elif uChoice == '7':
                Products =  GetproductsL() 
            elif uChoice == '8':
                priceMax = input("> Seng kaw na manu hpu dik htum lusha gaw gade dang re rai? \n:|")
            elif uChoice == '9':
                priceMin = input("> Seng kaw na manu hkyem sa dik htum lusha gaw gade dang re rai? \n:|")
            elif uChoice == '10':
                bcontact = input("> Seng de matut mahkai na matu phone(sh)social app account hpe ka bang da ya rit. \n:|")
            elif uChoice == '11':
                BDescrib = input("> Seng na lam hpe manam ni chye hkra kadun dawk sang lang dan rit. \n:|")
        else: 
            uChoice = uChoice.lower()
            if re.search(r"nrai",uChoice)and(re.search(r"nrai\W",uChoice)):
                break
            elif re.search(r"\Wum\W",uChoice) or re.search(r"\Wrai\W",uChoice) or re.search(r"um",uChoice) or (re.search(r"rai",uChoice)and(re.search(r"rai\W",uChoice))):
                RofPrice = priceMin + "-" + priceMax
                database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
                conn = create_connection(database)
                cur = conn.cursor()
                executeStr =  '"'+ Bname + '",' + str(BtypeID) + ',"' + OpenT + '","' + CloseT + '","'+ bcity + '","' + bcountry  + '","' + Products + '","'  + bcontact + '","'+ BDescrib + '","'+ Bowner +'","' + RofPrice +'");'
                cur.execute('INSERT INTO Business(Bname,Btype,OpenTime,CloseTime,placeCity,placeCountry,\
                products,BContant,BusinessDescrib,Owner,priceRange)VALUES('+executeStr)
                conn.commit()
                break
        
    
def keywordsShift(n,wD,keyW):
    for wrdpl in wD:
        if n+1 < len(keyW):
            if keyW[n+1] == wrdpl[4]:
                Nwrd = keyW[n] + ' ' + wrdpl[4] #two words one meaning
                wD = LoadWDt(Nwrd)
                keyW[n] = Nwrd
                for toshift in range(n+1,len(keyW)-1):
                    keyW[toshift] = keyW[toshift+1]
                keyW.remove(keyW[len(keyW)-1])
                wD,keyW = keywordsShift(n,wD,keyW)
                break
    return wD,keyW

def KWprocess(uinTy,keywords,uInpt):
    FkwList = []
    #uInpt = uInpt.split()
    if keywords != []:
        wrd = 0
        while wrd < len(keywords):
            wrdP = LoadWDt(keywords[wrd])
            rightW = []
            wrdP,keywords = keywordsShift(wrd,wrdP,keywords)
            
            if wrdP != []:
                if wrd == 0:
                    firstKW = ['Noun','Verb','State']
                    for ll in wrdP:
                        if ll[3] in firstKW:
                            rightW.append(ll)
                    if rightW != []:
                        preFkwList = []
                        if len(rightW) > 1:
                            for rightw in rightW:
                                preFkwList1 = []
                                splitrightw = rightw[5].split(",")
                                if len(splitrightw) > 1 and splitrightw[0] != 'None':
                                    for lrightw in splitrightw:
                                        if lrightw in uInpt:
                                            preFkwList1.append(rightw[0])
                                            preFkwList1.append(rightw[1])
                                            preFkwList1.append(rightw[3])
                                            preFkwList1.append(rightw[6])
                                else:
                                    preFkwList1.append(rightw[0])
                                    preFkwList1.append(rightw[1])
                                    preFkwList1.append(rightw[3])
                                    preFkwList1.append(rightw[6])
                                preFkwList.append(preFkwList1)
                            if preFkwList == []:
                                FkwList.append([rightW[0][0],rightW[0][1],rightW[0][3],rightW[0][6]])
                            else:
                                FkwList1 = []
                                wrdP2 = LoadWDt(keywords[wrd+1])
                                savewl = []
                                for wp2 in wrdP2:
                                    if wp2[3] == 'placeRW' or wp2[3] == 'Endword':
                                        savewl = wp2
                                for l in preFkwList:
                                    if l[1] == 'nga' and l[2] == 'Verb' and uinTy == 'whQuestionWhere':
                                        FkwList1 = l
                                    elif l[1] == 'nga' and l[2] == 'Verb' and savewl != []:
                                        FkwList1 = l
                                    else:
                                        FkwList1 = l
                                FkwList.append(FkwList1)
                        else:        
                            FkwList.append([rightW[0][0],rightW[0][1],rightW[0][3],rightW[0][6]])
                    else:
                        FkwList.append([])
                else:
                    if FkwList[wrd-1] != []:
                        if FkwList[wrd-1][2] == 'Verb':
                            addToFkw = 0
                            for wrdl in wrdP:
                                if wrdl[3] == 'Verb' or wrdl[3] == 'State' or wrdl[3] == 'Vbeing' or wrdl[3] == 'Time':
                                    if addToFkw == 0:
                                        FkwList.append([wrdl[0],wrdl[1],wrdl[3],wrdl[6]])
                                        addToFkw += 1
                                else:
                                    FkwList.append([])
                        elif FkwList[wrd-1][2] == 'Noun':
                            addToFkw = 0
                            verbfirst = []
                            for prewrdP in wrdP:
                                if prewrdP[3] == 'Verb':
                                    verbfirst = [prewrdP[0],prewrdP[1],prewrdP[3],prewrdP[6]]
                                    FkwList.append(verbfirst)
                                    addToFkw += 1
                            for wrdl in wrdP:
                                if wrdl[3] == 'Verb' or wrdl[3] == 'State' or wrdl[3] == 'placeRW' or wrdl[3] == 'Noun':
                                    if addToFkw == 0:
                                        FkwList.append([wrdl[0],wrdl[1],wrdl[3],wrdl[6]])
                                        addToFkw += 1
                                else:
                                    FkwList.append([])
                        elif FkwList[wrd-1][2] == 'placeRW':
                            wrdP2 = LoadWDt(keywords[wrd])
                            addToFkw = 0
                            for wrdl in wrdP:                                
                                if wrdl[3] == 'Verb':
                                    if wrdP2 != []:
                                        for wrdl2 in wrdP2:
                                            if wrdl2[3] == 'Vbeing' or wrdl2[3] == 'Endword':
                                                if addToFkw == 0:
                                                    FkwList.append([wrdl[0],wrdl[1],wrdl[3],wrdl[6]])
                                                    addToFkw += 1
                                            else:
                                                FkwList.append([])
                            for wrdl in wrdP:
                                if wrdl[3] == 'State' or wrdl[3] == 'Noun':
                                    if addToFkw == 0:
                                        FkwList.append([wrdl[0],wrdl[1],wrdl[3],wrdl[6]])
                                        addToFkw += 1
                                else:
                                    FkwList.append([])
                        else:
                            addToFkw = 0
                            for wrdl in wrdP:
                                if wrdl[3] == 'Verb' or wrdl[3] == 'State' or wrdl[3] == 'Noun' or wrdl[3] == 'placeRW' or wrdl[3] == 'Time':
                                    if addToFkw == 0:
                                        FkwList.append([wrdl[0],wrdl[1],wrdl[3],wrdl[6]])
                                        addToFkw += 1
                                else:
                                    FkwList.append([])
                    else:
                        VerbPriority = []
                        for wrdl in wrdP:
                            if wrdl[3] == "Verb":
                                VerbPriority = [wrdl[0],wrdl[1],wrdl[3],wrdl[6]]
                        for wrdl in wrdP:
                            if wrdl[3] == 'Verb' or wrdl[3] == 'State' or wrdl[3] == 'placeRW' or wrdl[3] == 'Noun':
                                if VerbPriority != []:
                                    FkwList.append(VerbPriority)
                                    break
                                else:
                                    FkwList.append([wrdl[0],wrdl[1],wrdl[3],wrdl[6]])
                                    break
                            else:
                                FkwList.append([])
                #print("check one by one - ",FkwList)
            else:
                FkwList.append([])
                with open('UnknownWord.csv', 'a', newline='') as file:
                    fieldnames = ['UnavailableWord', 'SentenceIn']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({'UnavailableWord': keywords[wrd], 'SentenceIn': uInpt})
                #print("gasi '",keywords[wrd],"' nga hpe lachyum re nchye ai nchye ai. App Madu hpe ndai lam shana da ya na.")
            wrd += 1
    
    PFkwList = []
    for allL in FkwList:
        if allL != []:
            PFkwList.append(allL)
            
    return PFkwList

def autoRemoveW(Nang,stringIn):
    autoRemove = ['nang','ngai','nye','hpe','hte','jinghpaw','wunpawng']
    if 'nang' in stringIn:
        Nang = True
    for rmword in autoRemove:
        stringIn = re.sub(rmword,"",stringIn)
    return Nang,stringIn

def ReSearchW(wordIn):
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    moreDetail = "SELECT Bname,products,BusinessDescrib FROM Business"
    cur.execute(moreDetail)
    rows = cur.fetchall()
    getRW = []
    for row in rows:
        row = str(row)
        if re.search(wordIn,row):
            row = re.sub("[\(|\)|']","",row)
            row = row.split(', ')
            if row[0] != 'None':
                getRW.append(row)
    return getRW

def GetDeeperRespN(wrdid,m0in):
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    moreDetail = "SELECT BID,Bname FROM Business WHERE Btype == " + wrdid+ " AND " + m0in[1] + " == '" + m0in[0] + "'"
    cur.execute(moreDetail)
    rows = cur.fetchall()
    getdeeper = []
    for row in rows:
        row = str(row)
        row = re.sub("[\(|\)|']","",row)
        row = row.split(', ')
        if row[0] != 'None':
            getdeeper.append(row)
    return getdeeper

def GetDtRespN(wrdid,m0in):
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    DtforResp = "SELECT wordID, word from wordsLibrary WHERE ParentWid == " + wrdid + " AND\
    wordID != " + wrdid 
    cur.execute(DtforResp)
    rows = cur.fetchall()
    GetDtR = []
    for row in rows:
        row = str(row)
        row = re.sub("[\(|\)|']","",row)
        row = row.split(', ')
        GetDtR.append(row)
    
    GetDtR2 = []
    for eachD in GetDtR:
        moreDetail = GetDeeperRespN(eachD[0],m0in)
        for eachMD in moreDetail:
            GetDtR2.append(eachMD)
    if GetDtR2 != []:
        GetDtR = GetDtR2
    
    return GetDtR
    
def ProduceRespond(NN,sentenceType,keywords,uinputsentence,memory):
    Bnames = []
    Noun = []
    verb = []
    nickn = NN
    state = []
    place = []
    #manu = []
    time = []
    
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    GetCountry = 'SELECT DISTINCT placeCountry FROM Business'
    cur.execute(GetCountry)
    rows = cur.fetchall()
    avaicountry = []
    for row in rows:
        row = str(row)
        row = re.sub("[\(|\)|\,|']","",row)
        avaicountry.append(row)
    
    GetCountry = 'SELECT DISTINCT placeCity FROM Business'
    cur.execute(GetCountry)
    rows = cur.fetchall()
    avaicity = []
    for row in rows:
        row = str(row)
        row = re.sub("[\(|\)|\,|']","",row)
        avaicity.append(row)
    
    allBnames = 'SELECT Bname FROM Business'
    cur.execute(allBnames)
    rows = cur.fetchall()
    GetBnames = []
    for row in rows:
        row = str(row)
        row = re.sub("[\(|\)|\,|']","",row)
        GetBnames.append(row)
    
    for B in GetBnames:
        if re.search(B,uinputsentence):
            B = "SELECT Bname,OpenTime,CloseTime,placeCity,placeCountry,products,BContant,\
            BusinessDescrib,Owner,priceRange FROM Business WHERE Bname == '" + B + "'"
            cur.execute(B)
            row = cur.fetchone()
            row = str(row)
            row = re.sub("[\(|\)]","",row)
            row = re.sub("', '","',,,'",row)
            B = row.split(',,,')
            Dln = []
            for w in B:
                w = re.sub("'","",w)
                Dln.append(w)
            B = Dln
            Bnames = []
            Bnames.append(B)
            uinputsentence = re.sub(B[0],"",uinputsentence)
            sentenceType,keywords = checkInput(uinputsentence)
            keywords = KWprocess(sentenceType,keywords,uinputsentence)
            memory[1] = B
            #print("Memory",memory[1])
        else:
            if len(memory) == 1:
                memory.append([])
    if Bnames == []:
        Bnames=memory[1]
    #print("Bnames",Bnames,'and memory1',memory[1])
        
    for country in avaicountry:
        if re.search(country,uinputsentence):
            memory=[[country,"placeCountry"],[]]
            Bnames = []
    for city in avaicity:
        if re.search(city,uinputsentence):
            memory=[[city,"placeCity"],[]]
            Bnames = []
    
    for kw in keywords:
        if kw[2] == 'Noun':
            Noun.append(kw)
        elif kw[2] == 'Verb':
            verb.append(kw)
        elif kw[2] == 'placeRW':
            place.append(kw)
        elif kw[2] == 'Time':
            time.append(kw)
        elif kw[2] == 'State':
            state.append(kw)
    if sentenceType == 'Sentence':
        specialV = ['madun','tsun','chye']        
        if Noun != [] and state != [] and Bnames == []:
            savens = []
            iffood = ''
            for ns in Noun:
                if ns[3] == '40':
                    iffood = 'lusha'
                ss = ReSearchW(ns[1])
                print("\n> ",memory[0][0],"kaw gaw npu na seng ni kaw mai lu ai")
                count = 1
                for s in ss:
                    print(" ",count,".",s[0])
                    count += 1
                if ss != []:
                    savens = ss
            if savens == []:
                print("\n> ",nickn,"tsun ai",iffood,"dut ai seng",memory[0][0],"kaw nnga shi ai")
        elif (Noun != [] and verb != []):
            if Noun[0][0] == '29':
                DfR = GetDtRespN(Noun[0][0],memory[0])
                count = 1
                print('\n> ',memory[0][0],'kaw nga ai',Noun[0][1],'gaw')
                for linDfR in DfR:
                    linDfR = linDfR[1].split()
                    ClinDfR = ""
                    for WtoC in linDfR:
                        ClinDfR += WtoC.capitalize() + " "
                    print(count,".",ClinDfR)
                    count += 1
            elif Noun[0][3] == '29':
                DfR = GetDeeperRespN(Noun[0][0],memory[0])
                count = 1
                print('\n> ',memory[0][0],'kaw nga ai',Noun[0][1],'gaw')
                for linDfR in DfR:
                    linDfR = linDfR[1].split()
                    ClinDfR = ""
                    for WtoC in linDfR:
                        ClinDfR += WtoC.capitalize() + " "
                    print(count,".",ClinDfR)
                    count += 1
            elif Bnames != []:
                for ns in Noun:
                    if ns[3] == '108':
                        print('\n> ',memory[0][0],'na matut mahkai mai ai ni gaw',memory[0][6],'re')
                    if ns[3] == '40':
                        count = 1
                        print('\n> ',memory[0][0],'kaw gaw')
                        productss = memory[0][5].split(",")
                        for prol in productss:
                            print(' ',count,'.',prol)
                            count += 1
                    if ns[3] == '57':
                        print('\n> ',memory[0][0],'kaw gaw manu ni',memory[0][9],'lapran nga ai')  
            else:
                print("\n> ",nickn,"tsun ai hpe ya yang htai na matu machye nnga shi ai")
        elif (Bnames != [] and verb != []):
            for linV in verb:
                if linV[1] in specialV:
                    #DTtoPrint = []
                    for oneBn in Bnames:
                        print(" Seng Mying            :",oneBn[0])
                        print(" Seng nga ai Myo mare  :",oneBn[3])
                        print(" Seng nga ai mungdan   :",oneBn[4])
                        print(" Seng hpaw hpang ai ten:",oneBn[1])
                        print(" Seng pat ai ten       :",oneBn[2])
                        print(" Lusha hpan ni         :",oneBn[5])
                        print(" Manu ni gaw           :",oneBn[9])
                        print(" Matut mahkai          :",oneBn[6])
                        print(" Seng a lam            :",oneBn[7])
        else:
            print("\n> Laga ga hkaw hku nna grau sang lang hkra kalang bai sang lang ya rit.")
    elif sentenceType == "whQuestionWhat":
        if (Noun != [] or verb != []) and memory[1] == []:
            if Noun[0][0] == '29':
                DfR = GetDtRespN(Noun[0][0],memory[0])
                count = 1
                print('\n> ',memory[0][0],'kaw nga ai',Noun[0][1],'gaw')
                for linDfR in DfR:
                    linDfR = linDfR[1].split()
                    ClinDfR = ""
                    for WtoC in linDfR:
                        ClinDfR += WtoC.capitalize() + " "
                    print(count,".",ClinDfR)
                    count += 1
            elif Noun[0][3] == '29':
                DfR = GetDeeperRespN(Noun[0][0],memory[0])
                count = 1
                print('\n> ',memory[0][0],'kaw nga ai',Noun[0][1],'gaw')
                for linDfR in DfR:
                    linDfR = linDfR[1].split()
                    ClinDfR = ""
                    for WtoC in linDfR:
                        ClinDfR += WtoC.capitalize() + " "
                    print(count,".",ClinDfR)
                    count += 1
        elif memory[1] != []:
            for ns in Noun:
                if ns[3] == '108':
                    print('\n> ',memory[1][0],'na matut mahkai mai ai ni gaw',memory[1][6],'re')
                elif ns[3] == '40':
                    count = 1
                    print('\n> ',memory[1][0],'kaw gaw')
                    productss = memory[1][5].split(',')
                    for prol in productss:
                        print(' ',count,'.',prol)
                        count += 1
                elif ns[3] == '29' and verb == []:
                    print('\n>  Seng madu was tsun ai',memory[1][0],'gaw "',memory[1][7],'" nga tsun dan da ai')
                elif ns[3] == '57':
                    print('\n> ',memory[1][0],'kaw gaw manu ni',Bnames[9],'lapran nga ai')
            if Noun == [] and verb != []:
                count = 1
                print('> ',memory[1][0],'kaw gaw')
                productss = memory[1][5].split(',')
                for prol in productss:
                    print(' ',count,'.',prol)
                    count += 1
            
        else:
            print("> ",nickn,"san ai hpe ya yang htai na matu machye nnga shi ai. Seng madu hpe bai san da ya na.")
    elif sentenceType == "whQuestionWhen":
        if verb != [] and memory[1] != []:
            for v in verb:
                if v[1] == 'hpaw' and state != []:
                    print('\n> ',memory[1][0],'gaw',memory[1][1],'kaw na',memory[1][2],' du hpaw ai re.')
                elif v[1] == 'hpaw':
                    print('\n> ',memory[1][0],'hpaw ai gaw',memory[1][1],'kaw re.')
                elif v[1] == 'pat':
                    print('\n> ',memory[1][0],'pat ai gaw',memory[1][2],'kaw re.')
                
        else:
            print("\n> Laga ga hkaw hku nna grau sang lang hkum sup hkra kalang bai ka ya rit.")
    elif sentenceType == "HowMuch":
        if memory[1] != [] and Noun != []:
            found = False
            for ns in Noun:
                if ns[3] == '40' or ns[1] == 'manu':
                    found = True
            if found == True:
                print("\n> Manu gaw", memory[1][9],"lapran re.")
            else:
                print("\n> Laga ga hkaw hku nna grau sang lang hkum sup hkra kalang bai ka ya rit.")
        elif memory[1] == [] and Noun != []:
            for Ns in Noun:
                if Ns[0] == '29':
                    DfR = GetDtRespN(Ns[0],memory[0])
                    print("\n> ",memory[0][0],"kaw gaw",Ns[1],"ni",len(DfR),"nga ai.")
                    print(">  dai ni gaw")
                    count = 1
                    for b in DfR:
                        print(" ",count,".", b[1])
                        count += 1
                elif Ns[3] == '29':
                    DfR = GetDeeperRespN(Ns[0],memory[0])
                    print("\n> ",memory[0][0],"kaw gaw",Ns[1],"ni",len(DfR),"nga ai.")
                    print(">  dai ni gaw")
                    count = 1
                    for b in DfR:
                        print(" ",count,".", b[1])
                        count += 1
        else:
            print("\n> ",nickn,"san ai hpe ya yang htai na matu machye nnga shi ai. Seng madu hpe bai san da ya na.")
    elif sentenceType == 'whQuestionWhere':
        if memory[1] != []:
            print('\n> ',memory[1][0],'gaw',memory[1][3],',',memory[1][4],'mungdan kaw re.')
        elif Noun != [] and verb != []:
            savens = []
            iffood = ''
            for ns in Noun:
                if ns[3] == '40':
                    iffood = 'lusha'
                ss = ReSearchW(ns[1])
                print("\n> ",memory[0][0],"kaw gaw npu na seng ni kaw mai lu ai")
                count = 1
                for s in ss:
                    print(" ",count,".",s[0])
                    count += 1
                if ss != []:
                    savens = ss
            if savens == []:
                print("\n> ",nickn,"tsun ai",iffood,"dut ai seng",memory[0][0],"kaw nnga shi ai")
        elif Noun == [] and verb != []:
            for v in verb:
                if v[1] == 'sa':
                    print("\n> Dai chyawm ya yang re nchye shi ai. Seng madu hpe bai san da ya na.")
        else:
            print("> ",nickn,"san ai hpe ya yang htai na matu machye nnga shi ai")
    elif sentenceType == "whQuestionHow":
        if memory[1] != [] and Noun != []:
            for ns in Noun:
                if ns[3] == '108':
                    print('> ',Bnames[0][0],'na matut mahkai mai ai ni gaw',Bnames[0][6],'re')
        else:
            print("> ",nickn,"san ai hpe ya yang htai na matu machye nnga shi ai")
    elif sentenceType == "y/nQuestion":
        if (Noun != [] or verb != []) and Noun[0][0] == '29':
            DfR = GetDtRespN(Noun[0][0],memory[0])
            count = 1
            if DfR != []:
                print("> um nga ai")
                print('> ',memory[0][0],'kaw nga ai',Noun[0][1],'gaw')
                for linDfR in DfR:
                    linDfR = linDfR[1].split()
                    ClinDfR = ""
                    for WtoC in linDfR:
                        ClinDfR += WtoC.capitalize() + " "
                    print(count,".",ClinDfR)
                    count += 1
            else:
                print("> nnga ai")
        elif (Noun != [] or verb != []) and Noun[0][3] == '29':
            DfR = GetDeeperRespN(Noun[0][0],memory[0])
            count = 1
            if DfR != []:
                print("> um nga ai")
                print('> ',memory[0][0],'kaw nga ai',Noun[0][1],'gaw')
                for linDfR in DfR:
                    linDfR = linDfR[1].split()
                    ClinDfR = ""
                    for WtoC in linDfR:
                        ClinDfR += WtoC.capitalize() + " "
                    print(count,".",ClinDfR)
                    count += 1
            else:
                print("> nnga ai")
        elif Noun != [] and verb != []:
            savens = []
            iffood = ''
            for ns in Noun:
                if ns[3] == '40':
                    iffood = 'lusha'
                ss = ReSearchW(ns[1])
                print("> ",memory[0][0],"kaw gaw npu na seng ni kaw mai lu ai")
                count = 1
                for s in ss:
                    print(" ",count,".",s[0])
                    count += 1
                if ss != []:
                    savens = ss
            if savens == []:
                print("> ",nickn,"tsun ai",iffood,"dut ai seng",memory[0][0],"kaw nnga shi ai")
        elif memory[1] != []:
            productsss = memory[1][5].split(',')
            count = 1
            if productsss != []:
                print("> um nga ai")
                print('> ',memory[1][0],'kaw gaw')
                for prod in productsss:
                    print(count,'.',prod)
                    count += 1
            else:
                print("> nnga ai")
        else:
            print("> ",nickn,"san ai hpe ya yang htai na matu machye nnga shi ai")
                        
    return memory

def MainF(userD):
    uId = userD[0]
    #print(uId)
    DoB = userD[5]
    nickN = userD[4]
    BirthD = CheckDoB(DoB)
    Nang = False
    CurrentPlace = [userD[7],userD[8]]
    workingM = [[CurrentPlace[0],'placeCity']]
    
    if BirthD == True:
        print("> Ngwi Pyaw ai Shangai nhtoi rai u ga yaw",nickN)
        userInp = input("> San mayu ai lam hpa nga ai rai?\n: ")
    else:
        print("> Kalang bai hkrum lu ai majaw kabu ai yaw",nickN)
        userInp = input("> San mayu ai lam hpa nga ai rai?\n: ")
    userInp = userInp.lower()
    userInp = re.sub(r"[\,\.\?\<\>\"\'\!]","",userInp)
    Nang,userInp = autoRemoveW(Nang,userInp)
    while userInp != 'pat':
        try:
            if userInp == 'sengseng':
                BusinessCreate(uId)
            InTy,KeyWs = checkInput(userInp)
            KeyWs = KWprocess(InTy,KeyWs,userInp)
            workingM = ProduceRespond(nickN,InTy,KeyWs,userInp,workingM)
            Nang = False
            userInp = (input(": ")).lower()
            userInp = re.sub(r"[\,\.\?\<\>\"\'\!]","",userInp)
        except:
            print("\n> Laga ga hkaw ni hku grau sang lang hkrum sup hkra ka ya rit.")
            userInp = (input(": ")).lower()
            userInp = re.sub(r"[\,\.\?\<\>\"\'\!]","",userInp)
            Nang,userInp = autoRemoveW(Nang,userInp)
        
def main():    
    Choice = (input("> User account galaw da ai nga sai i? \n:")).lower()
    InputT,keyWs = checkInput(Choice.lower())
    if ('nga' in keyWs or 'um' in keyWs) and ('n nga' not in Choice):
        Defaultdata = LogIn()
        if Defaultdata != 'pat':
            MainF(Defaultdata)
    else:
        Defaultdata = SignUp()
        if Defaultdata != 'pat':
            MainF(Defaultdata)

if __name__ == '__main__':
    main()
    
#there are 29 functions in this Program 