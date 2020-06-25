# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 11:30:07 2020

@author: wehka
"""
import re 
import sqlite3
from sqlite3 import Error
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


def loadData(idIn):
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    Dload = 'SELECT Myubawhpan, HtinggawMying, ShingtengMying, ShagaMying, ShangaiNhtoi, \
    Buga, NgaShara,NgasharaMungdan FROM UserInfo where Userid = ' + idIn
    cur.execute(Dload)
    row = cur.fetchone()
    Dl = str(row)
    Dl = re.sub('[\(|\)|]','',Dl)
    Dl = re.sub("', '","',,,'",Dl)
    Dl = Dl.split(',,,')
    Dln = []
    for s in Dl:
        s = re.sub("'","",s)
        Dln.append(s)
    Dl = Dln
    return Dl

#answer (um re,ai) (if question askedg)
#yes/no question (i rai, re rai, ai i, re i)
# question (hpa baw, hpa nga ai rai, hpa baw rai, kun, nga kun, hpa ta)
#command (if q has asked it can be answer too)
def LoadWDt(wordIn):
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
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
    #print(LoadDtL)
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
    qw10 = 'ai'
    qw11 = 'baw'
    qw12 = 'rai'
    qw13 = 'na'
    qw14 = 'ma'
    qw15 = 'sa'
    qw16 = 'taw'
    qw17 = 're'
    qw18 = 'sai'
    qw19 = 'gade'
    #qwl = [qw1,qw2,qw3,qw4,qw5,qw6,qw7,qw8,qw9,qw10,qw11,qw12,qw13,qw14,qw15,qw16,qw17]
    Specialqwl = [qw9,qw10,qw12,qw13,qw15,qw16,qw18]
    Endword = [qw1,qw2,qw9,qw10,qw12,qw13,qw14,qw15,qw16,qw17,qw18]
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
        if qw1 in qWords1 or qw2 in qWords1: #i (sh) kun is in the sentence
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
    
    
def CheckInputM1():
    getIn1 = input(":")
    getIn = getIn1.split()
    letter1 = ['i',['ai','re','rai']]
    letter2 = ['rai',['i','re']]
    #byin = i sa byin ai rai
    letter3 = ['ai',['i','kun','rai','re']]
    qw1 = 'i'
    qw2 = 'rai'
    qw3 = 'ai'
    qw4 = 'hpa'
    qw5 = 'baw'
    qwl = [qw1,qw2,qw3,qw4,qw5]
    qwlStore = []
    LtoReturn = []
    startW =''
    pureEndW = ''
    EndAndKey = ''
    keywords = []
    listhold = []
    if letter1[0] in getIn:
        listhold.append([letter1[0],True,getIn.index(letter1[0])])
    else:
        listhold.append([letter1[0],False])
    if letter2[0] in getIn:
        listhold.append([letter2[0],True,getIn.index(letter2[0])])
    else:
        listhold.append([letter2[0],False])
    if letter3[0] in getIn:
        listhold.append([letter3[0],True,getIn.index(letter3[0])])
    else:
        listhold.append([letter3[0],False])
    print(listhold)
    for lhcheck in range(len(listhold)):
        if listhold[lhcheck][1] == False:
            listhold.remove(listhold[lhcheck])
    print(listhold)
    for lhtochange in range(len(listhold)):
        listhold[lhtochange] = listhold[lhtochange][0]
    
    
    if listhold[0][1] == True and listhold[1][1]==True:
        if listhold[0][0] in letter2[1]:
            DifferenceBetween = abs(listhold[0][2]-listhold[1][2])
            if DifferenceBetween == 1:
                pureEndW = listhold[0][0]+' '+listhold[1][0]
            else:
                EndAndKey = listhold[0][0]+"(.+)"+listhold[1][0]
                for kw in range(1,DifferenceBetween):
                    keywords.append(getIn[listhold[0][2]+kw])
        else:
            DifferenceBetween = abs(listhold[0][2]-listhold[1][2])
            if DifferenceBetween == 1:
                pureEndW = listhold[1][0]+' '+listhold[0][0]
            else:
                EndAndKey = listhold[1][0]+"(.+)"+listhold[0][0]
                for kw in range(1,DifferenceBetween):
                    keywords.append(getIn[listhold[1][2]+kw])
        if pureEndW != '':
            print(pureEndW)
        elif EndAndKey != '':
            print(EndAndKey)
            print(keywords)
        print ('yes')
    else:
        print()
    

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
            while getPwd != upwd:
                print("password njaw nga ai, kalang bai jaw hkra bang ya rit")
                print(upwd,getPwd)
                getPwd = input("Password: ")
            break
        else:
            print("username %s nga ai nnga ai"%(getUname))
    GetD = 'SELECT Userid FROM LogIn where Username = "' + getUname +'"'
    cur.execute(GetD)
    row = cur.fetchone()
    Uid = str(row)
    Uid = re.sub("[\(|\)|\,]","",Uid)
    #print(Uid)
    return loadData(Uid)

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
                            preFkwList1 = []
                            for rightw in rightW:
                                splitrightw = rightw[5].split(",")
                                if splitrightw != []:
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
                                FkwList.append([rightW[0][0],rightW[0][1],rightW[0][3]],rightW[0][6])
                            else:
                                for l in preFkwList:
                                    if l[1] == 'nga' and uinTy == 'whQuestionWhere':
                                        FkwList.append(l)
                                    else:
                                        FkwList.append(l)
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
                            for wrdl in wrdP:
                                if wrdl[3] == 'Verb' or wrdl[3] == 'State' or wrdl[3] == 'placeRW' or wrdl[3] == 'Noun':
                                    if addToFkw == 0:
                                        FkwList.append([wrdl[0],wrdl[1],wrdl[3],wrdl[6]])
                                        addToFkw += 1
                                else:
                                    FkwList.append([])
                        elif FkwList[wrd-1][2] == 'placeRW':
                            wrdP2 = LoadWDt(keywords[wrd+1])
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
                        for wrdl in wrdP:
                            if wrdl[3] == 'Verb' or wrdl[3] == 'State' or wrdl[3] == 'placeRW' or wrdl[3] == 'Noun':
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
    autoRemove = ['nang','ngai','nye','hpe','hte']
    if 'nang' in autoRemove:
        Nang = True
    for rmword in autoRemove:
        stringIn = re.sub(rmword,"",stringIn)
    return Nang,stringIn

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
    
def ProduceRespond(sentenceType,keywords,uinputsentence,memory):
    Bnames = []
    Noun = []
    verb = []
    state = []
    place = []
    manu = []
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
        if B in uinputsentence:
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
        if country in uinputsentence:
            memory[0]=[country,"placeCountry"]
    for city in avaicity:
        if city in uinputsentence:
            memory[0]=[city,"placeCity"]
    
    
    for kw in keywords:
        if kw[2] == 'Noun':
            Noun.append(kw)
        elif kw[2] == 'Verb':
            verb.append(kw)
        elif kw[2] == 'placeRW':
            place.append(kw)
        elif kw[2] == 'Time':
            time.append(kw)
    if sentenceType == 'Sentence':
        specialV = ['madun','tsun','chye']
        if Bnames != [] and verb != []:
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
        if (Noun != [] and verb != []) and Noun[0][0] == '29':
            DfR = GetDtRespN(Noun[0][0],memory[0])
            count = 1
            print(memory[0][0],'kaw nga ai',Noun[0][1],'gaw')
            for linDfR in DfR:
                linDfR = linDfR[1].split()
                ClinDfR = ""
                for WtoC in linDfR:
                    ClinDfR += WtoC.capitalize() + " "
                print(count,".",ClinDfR)
                count += 1
        elif (Noun != [] and verb != []) and Noun[0][3] == '29':
            DfR = GetDeeperRespN(Noun[0][0],memory[0])
            count = 1
            print(memory[0][0],'kaw nga ai',Noun[0][1],'gaw')
            for linDfR in DfR:
                linDfR = linDfR[1].split()
                ClinDfR = ""
                for WtoC in linDfR:
                    ClinDfR += WtoC.capitalize() + " "
                print(count,".",ClinDfR)
                count += 1
        else:
            print("Laga ga hkaw hku nna grau sang lang hkra kalang bai sang lang ya rit.")
    elif sentenceType == "whQuestionWhat":
        if (Noun != [] or verb != []) and Noun[0][0] == '29':
            print(Noun[0][0])
            DfR = GetDtRespN(Noun[0][0],memory[0])
            count = 1
            print(memory[0][0],'kaw nga ai',Noun[0][1],'gaw')
            for linDfR in DfR:
                linDfR = linDfR[1].split()
                ClinDfR = ""
                for WtoC in linDfR:
                    ClinDfR += WtoC.capitalize() + " "
                print(count,".",ClinDfR)
                count += 1
        elif (Noun != [] or verb != []) and Noun[0][3] == '29':
            DfR = GetDeeperRespN(Noun[0][0],memory[0])
            count = 1
            print(memory[0][0],'kaw nga ai',Noun[0][1],'gaw')
            for linDfR in DfR:
                linDfR = linDfR[1].split()
                ClinDfR = ""
                for WtoC in linDfR:
                    ClinDfR += WtoC.capitalize() + " "
                print(count,".",ClinDfR)
                count += 1
        elif memory[1] != []:
            print(memory[1][0],'kaw gaw')
            productsss = memory[1][5].split(',')
            count = 1
            for prod in productsss:
                print(count,'.',prod)
                count += 1
        else:
            print("Laga ga hkaw hku nna grau sang lang hkra kalang bai sang lang ya rit.")
    elif sentenceType == "whQuestionWhen":
        if verb != [] and memory[1] != []:
            for v in verb:
                if v[1] == 'hpaw':
                    print(memory[1][0],'gaw',memory[1][1],'kaw re.')
                elif v[1] == 'pat':
                    print(memory[1][0],'gaw',memory[1][2],'kaw re.')
                elif v[2] == 'sha':
                    print(memory[1][0],'gaw',memory[1][1],'kaw na',memory[1][2],' du hpaw ai re.')
        else:
            print("Laga ga hkaw hku nna grau sang lang hkra kalang bai sang lang ya rit.")
    elif sentenceType == "HowMuch":
        if memory[1] != [] and Noun != []:
            found = False
            for ns in Noun:
                if ns[3] == '40' or ns[1] == 'manu':
                    found = True
            if found == True:
                print("Manu gaw", memory[1][9],"lapran re.")
            else:
                print("Laga ga hkaw hku nna grau sang lang hkra kalang bai sang lang ya rit.")
        else:
            print("Laga ga hkaw hku nna grau sang lang hkra kalang bai sang lang ya rit.")
    elif sentenceType == 'whQuestionWhere':
        if memory[1] != []:
            print(memory[1][0],'gaw',memory[1][3],',',memory[1][4],'mungdan kaw re.')
        elif verb != []:
            for v in verb:
                if v[1] == 'sa':
                    print("Dai chyawm ya yang ye nchye shi ai. Seng madu hpe bai san da ya na.")
        else:
            print("Laga ga hkaw hku nna grau sang lang hkra kalang bai sang lang ya rit.")
    #elif sentenceType == "whQuestionWhen":
        #print('DfR',DfR)
            #####################hpawt de bai galaw na verb chye mayu, madun dan, tsun dn.....
    return memory
    
def intoapp(userD):
    DoB = userD[4]
    nickN = userD[3]
    BirthD = False#CheckDoB(DoB)
    CurrentPlace = [userD[6],userD[7]]
    address = '' #for where q
    NounsCat = []
    priceR = [] #for price
    Nang = False
    workingM = [CurrentPlace[0]]
    
    if BirthD == True:
        print("Ngwi Pyaw ai Shangai nhtoi rai u ga yaw",nickN)
        userInp = input("San mayu ai lam hpa nga ai rai?\n: ")
    else:
        print("Kalang bai hkrum lu ai majaw kabu ai yaw",nickN)
        userInp = input("San mayu ai lam hpa nga ai rai?\n: ")
    userInp = userInp.lower()
    Nang,userInp = autoRemoveW(Nang,userInp)
    #print(Nang,userInp)
    while userInp != 'pat':
        try:
            if userInp == 'SengSeng':
                BusinessCreate(uId)
            InTy,KeyWs = checkInput(userInp)
            KeyWs = KWprocess(InTy,KeyWs,userInp)
            workingM = ProduceRespond(InTy,KeyWs,userInp,workingM)
            Nang = False
        except:
            print("laga ga hkaw ni hku grau sang lang hkrum sup hkra ka ya rit.")
        userInp = (input(": ")).lower()
        Nang,userInp = autoRemoveW(Nang,userInp)
        
    #print(checkInput(userInp))
    
def getUserLocation(userid):
    database = r"D:\PYU_4yrs_courses\PYU4thYear\4Y2S_PYUIT\Senior Project\FirstTestingDB.db"
    conn = create_connection(database)
    cur = conn.cursor()
    userid = str(userid)
    print(userid)
    executeStr = 'SELECT NgaShara,NgasharaMungdan FROM UserInfo WHERE Userid == ' + userid 
    print(executeStr)
    cur.execute(executeStr)
    row = cur.fetchone()
    row = str(row)
    row = re.sub("[\(\)\']","",row)
    row = row.split(", ")
    return row

def main():
    
    wkys = intoapp(loadData('6'))
    print(wkys)
    #x = getWordType('kaw')    
    #for x in range(2):
     #   userIn = input(": ")
      #  checkInput(userIn)
    #x =getWordType('oi')
    #x = LogIn()
    #if x != []:
    #    print(x,len(x))
    
    #test = "nkaja ai"
    #zzz = re.findall("n([^a].+)\s",test)
    #zz = re.match("i \W+ rai",'ndai i jaw rai')
    #print(zzz)
if __name__ == '__main__':
    main()

#print(date1)

#Association - shat/kawsi > lusha seng, muk, >>> (verbs and adj associated with nouns )
    #shamu shamaw (v), mabyin (condition, adj), 
    
#kayword shawng na hpe shawng jet, laba na dai kw gaw lachyum langai hta grau law yang dai kw ni na cancombin ni hpe la nna
    #dai kw na hpang yep na kw wtype hpe yu na, yu yu na nga yang dai nga ai wa na wtype rai sai, 
    #nnga yang gaw dai word na type hpe check na verb/N nga yang gaw ya na kw gaw N rai sai, 
    #State nga yang V/N mai byin ai rai yang State na hpang kaw ai rai yang V, nrai yang N (eg.pyaw ai ,pyaw dik ai)
#hpa nga baw rai gasan hpe htai na matu word na description hte htai na. DataBase kaw dai tam ai w nnga yang
    #user hpe bai nhtang san na. user htai ai hpe txt kaw matsing da na, the developer dai hpe yu DB kaw bai jet na