import re

    
def writeToLogfile(logtext):
            flogobj = open("logfile.log", "a")
            flogobj.write(logtext)
            flogobj.close()

def createOutputFile(fname):
    foutobj = open(fname,"w")
    foutobj.write("WKZ Umsatz SollHaben BuSchluessel Gegenkonto Belegfeld1 Belegfeld2 BuchungDatum Konto Kost1 Kost2 Buchungstext Kurs\n")
    foutobj.close()

def writeToOutputFile(fname,line):
    foutobj = open(fname,"a")
    foutobj.write(line["WKZ"])
    foutobj.write(" ")
    foutobj.write(str(line["Umsatz"]))
    foutobj.write(" ")
    foutobj.write(line["SollHaben"])
    foutobj.write(" "+" ")
    foutobj.write(line["Gegenkonto"])
    foutobj.write(" ")
    foutobj.write(line["Belegfeld1"])
    foutobj.write(" "+" ")
    foutobj.write(line["BuchungsDatum"])
    foutobj.write(" ")
    foutobj.write(line["Konto"])
    foutobj.write(" "+" "+" ")
    foutobj.write(line["Buchungstext"])
    foutobj.write(" "+"\n")
    foutobj.close()

def ausgabeList(fname,list):
    foutobj = open(fname+"listout.txt","w")
    for l in list:
        foutobj.write(str(l))
        foutobj.write("\n")
    foutobj.close()

def ausgabeDic(fname,dic):
    lst = dic.keys()
    foutobj = open(fname+"dicout.txt","w")
    for l in lst:
        foutobj.write(str(l)+" mit subdic: "+str(dic[l]))
        foutobj.write("\n")
    foutobj.close()

def nettoTobrutto(stkey,netto):
    return (float(float(netto.replace(",",".")))*(1+float(stkey)))

def formatDatum(date):
    return (date[0:2]+"."+date[2:4]+".20"+date[4:])

def createDataTree(zlist):
    rechl=[]
    #main dictionary rechd ordered by "RechnungsNr"
    rechd={}
    #subdictionary of rechd ordered in two gruops by lines with "Gegenkonto" and lines with "Konto", the oredering keys also are "Konto", "Gegenkonto"
    kongegkond = {"Konto":{}, "Gegenkonto":{}}
    #two subdictionarys of kongegkon ordered by the linenumbers of the source-file as keys  
    kontod={}
    gegkontod={}
    #two subdictionaries: fieldskon of kontod and fieldsgegkon of gegkond
    #both are ordered by the fieldnames used in the output-file
    fieldskond={"WKZ":[],"Umsatz":[],"SollHaben":"S",
               "BuchSchluessel":["LEER"],"Gegenkonto":[],
               "Belegfeld1":[],"Belegfeld2":["LEER"],
                "BuchungsDatum":[],"Konto":[],
                "Kost1":["LEER"],"Kost2":["LEER"],
                "Buchungstext":[],"Kurs":["LEER"],
                "QuellZeilenNr":[],"ListID":[]}

    fieldsgegkond={"WKZ":[],"Umsatz":[],"SollHaben":"S",
                  "BuchSchluessel":["LEER"],"Gegenkonto":[],
                  "Belegfeld1":[],"Belegfeld2":["LEER"],
                  "BuchungsDatum":[],"MwstSchluessel":[],
                  "Kost1":["LEER"],"Kost2":["LEER"],
                  "Buchungstext":[],"Kurs":["LEER"],
                  "QuellZeilenNr":[],"ListID":[]}

    kongegkond["Konto"] = kontod
    kongegkond["Gegenkonto"] = gegkontod
    for lis in zlist:
        rechl.extend([zlist.index(lis), lis[7]])
        if lis[7] not in rechd:
            rechd.update({lis[7]:{}})
        if lis[7] in rechd:
            if lis[8]=="1":
                kongegkond["Konto"].update({zlist.index(lis):lis[13]})

                fieldskond["WKZ"]=lis[12]
                fieldskond["Umsatz"]=nettoTobrutto(lis[4],lis[10])
                fieldskond["Gegenkonto"]=lis[0]
                fieldskond["Belegfeld1"]=lis[7]
                fieldskond["BuchungsDatum"]=formatDatum(lis[6])
                fieldskond["Konto"]=lis[9]
                fieldskond["Buchungstext"]=lis[3]
                fieldskond["QuellZeilenNr"]=lis[13]
                fieldskond["ListID"]=zlist.index(lis)

                if "Konto" in rechd[lis[7]]:
                    rechd[lis[7]]["Konto"].update({lis[13]:fieldskond})
                else:
                    rechd[lis[7]].update({"Konto":{}})
                    rechd[lis[7]]["Konto"].update({lis[13]:fieldskond})
            elif lis[8]=="2":
                kongegkond["Gegenkonto"].update({zlist.index(lis):lis[13]})

                fieldsgegkond["WKZ"]=lis[12]
                fieldsgegkond["Umsatz"]=lis[10]
                fieldsgegkond["Gegenkonto"]=lis[9]
                fieldsgegkond["Belegfeld1"]=lis[7]
                fieldsgegkond["BuchungsDatum"]=lis[6]
                fieldsgegkond["MwstSchluessel"]=[lis[4]]
                fieldsgegkond["Buchungstext"]=lis[3]
                fieldsgegkond["QuellZeilenNr"]=lis[13]
                fieldsgegkond["ListID"]=zlist.index(lis)

                if "Gegenkonto" in rechd[lis[7]]:
                    rechd[lis[7]]["Gegenkonto"].update({lis[13]:fieldsgegkond})
                else:
                    rechd[lis[7]].update({"Gegenkonto":{}})
                    rechd[lis[7]]["Gegenkonto"].update({lis[13]:fieldsgegkond})
            else:
                writeToLogfile("\n Has no konto or gegenkonto found!in line: "
                           +lis[13]+" of the source fiel\n")
        
    ausgabeList("rechkey",rechl)
    ausgabeDic("rechkeydic",rechd)
    createOutputFile("testOutPut.txt")
    for k in rechd["944547"]["Konto"]:
        writeToOutputFile("testOutPut.txt",rechd["944547"]["Konto"][k])

def GetNumbersFromBlock(stg,negativb):
    datum=stg[7:13]
    datumt=stg[13:19]
    if datum!=datumt:
        writeToLogfile("\n================"
                       +str(len(stg))
                       +" Error with Date "+str(datum)+" != "
                       +str(datumt)+"============\n")    
    rechnr=stg[39:45].strip("0")
    rechnrt=stg[60:74].strip("0")
    if rechnr!=rechnrt:
        writeToLogfile("\n================"
                       +"Error with RechnungsNummer"
                       +str(rechnr)+"!="+str(rechnrt)+"============\n")
    #pos1=39+len(rechnr)
    #pos2=pos1+9
    konto=stg[46:53].strip("0")
    gegkonto=stg[53:59].strip("0")
    pos="NULL"
    if konto!=gegkonto:
        if konto=="":
            konto=gegkonto
            pos="2"
        else:
            pos="1"
    else:
        writeToLogfile("\n================"
                       +"Error with Konto: "+str(konto)
                       +" und Gegenkonto: "+str(gegkonto)+"============\n")
    #pos2=78
    betrag=stg[74:].lstrip("0")
    if negativb:
        betrag="-"+betrag
    return [datum,rechnr,pos,konto,betrag]
    
def GetMwstNr(stg):
    leng=len(stg)
    if leng>4:
        pos2=len(stg)-3
        mw1 = stg[:pos2]
        mw2= stg[pos2:]
    else:
        mw1="NULL"
        mw2=stg
    return [mw1,mw2]
    
def GetBuchungstext(lst):
    if len(lst) == 4:
        if len(lst[2])>1:
            newlst = lst[0:2]
            newlst.append(lst[2][:2])
            newlst.append(lst[2][2:]+" "+lst[3])
        else:
            newlst = lst
            writeToLogfile("\n================"
                           +"Error with Buchungstext: "
                           +str(lst[2])+" is to short."+"============\n")
    else:
        newlst = lst
        writeToLogfile("\n================"
                       +"Error with Buchungstext: "
                       +str(lst)+" is to short."+"============\n")
    return newlst
    
def RestructureLine(nl,leng,linenum):
    if leng==8:
        #6 Dann mit MwstSchluessel und ohne Minuszeichen hinter dem Betrag
        nl1 = GetBuchungstext(nl[0:4])
        mnr = GetMwstNr(nl[4])
        print (mnr)
        s=nl[5]
        nl2 = nl[6:]
        nl1.extend(mnr)
        nl=nl1
        #print (s)
        nl1 = GetNumbersFromBlock(s,False)
        nl.extend(nl1)
        nl.extend(nl2)
        
    elif leng==6:
        #5 Dann ohne MwstSchluessel und mit Minuszeichen hinter dem Betrag
        nl1 = GetBuchungstext(nl[0:4])
        mnr = ["NULL","NULL"]
        s=nl[4]
        nl2 = nl[5:]
        nl1.extend(mnr)
        nl=nl1
        ls=s.split("-")
        if len(ls)==2:
            nl1=GetNumbersFromBlock(ls[0],True)
            nl1.append(ls[1])
        else:
            writeToLogfile("\n================"+"Error with 6 "+str(ls)+"============\n")
        nl.extend(nl1)
        nl.extend(nl2)
    elif leng==7:
        #5 Dann entweder 1.Fall: Mit Mwstschluessel aber mit Minuszeichen hinter Betrag, oder 2.Fall: Ohne MwstSchluessel aber ohne Minuszeichen hinter dem Betrag 
        nl1 = GetBuchungstext(nl[0:4])
        #mnr = "NULL"
        s=nl[4]
        if len(s)<9:
            mnr= GetMwstNr(s)
            news=nl[5]
            nl2 = nl[6:]
            nl1.extend(mnr)
            nl=nl1
            ls=news.split("-")
            if len(ls)==2:
                nl1=GetNumbersFromBlock(ls[0],True)
                nl1.append(ls[1])
                #s[0]=s[0]+"-"
            else:
                writeToLogfile("\n================"+"Error with 7 "+str(ls)+"============\n")
            nl.extend(nl1)
            nl.extend(nl2)
        else:
            mnr = ["NULL","NULL"]
            print (mnr)
            #news = nl[4]
            nl2 = nl[5:]
            nl1.extend(mnr)
            nl = nl1
            nl1=GetNumbersFromBlock(s,False)
            nl.extend(nl1)
            nl.extend(nl2)
            
    else:
        writeToLogfile(str(linenum)+".st line is not correct. The Line begins with: "
                       +str(nl)+"\n has number of groups: "+str(len(nl))+"\n")
    return nl

def updateMwst(mw,nr):
    return []

def getLineOfFile(fname,z):
    linenum = 0
    mswtBlockNr = 0
    Mwst = 0.19
    Mkont = ""
    fileobj = open(fname, "r")
    for line in fileobj:
        linenum += 1
        nl = line.split(" ")

        n=nl.count('')
        for i in range(n):
                nl.remove('')
        nl[-1]=nl[-1].strip("\n")
        nl[-1]=nl[-1].strip("\r")
        nl[-1]=nl[-1].strip("\t")
        e=nl[-1]
        llm1=len(e)
        if len(e) > 3:
            wkz=e[-1]+e[-2]+e[-3]
            nl[-1]=e.strip[wkz]
            if len(nl[-1])==(llm1-3):
                #nl[-1]=nl[-1].strip("0")
                nl.append[wkz]
            else:
                writeToLogfile("***Error: "+str(linenum)+".st line is not correct. The line ends with: "
                               +str(nl[-1])+" and "+str(wkz)+"\n")
                nl.append["NULL"]

        leng=len(nl)
        newnl=RestructureLine(nl,leng,linenum)
        e=newnl[-2]
        newnl[-2]=e.lstrip("0")
        #writeToLogfile(str(e))
        if len(newnl)==13:
            newnl.append(str(linenum))

            if newnl[4]=="NULL" and newnl[5]=="NULL" :
                newnl[0]=Mkont
                newnl[4]=Mwst
                newnl[5]=mswtBlockNr
            else:
                Mkont = newnl[9]
                if newnl[4]=="NULL":
                    mswtBlockNr+=1
                    newnl[4]=Mwst
                    newnl[5]=newnl[5]+"-"+str(mswtBlockNr)
                    pass
                else:
                    Mwst = int(newnl[4][1:])*0.01
                    mswtBlockNr +=1
                    newnl[4]=Mwst
                    newnl[5]=newnl[5]+"-"+str(mswtBlockNr)

            z.append(newnl)
        else:
            writeToLogfile("!!!Error: "+str(linenum)
                           +".st line is not correct. The Line begins with: "
                           +str(newnl)+"\n has number of groups: "+str(len(newnl))+"\n")
    fileobj.close()
                
  
    

def main():
    #fileRead("PT311013.df")
    z=[]
    #getLineOfFile("test.df",z)
    getLineOfFile("PT311013.df",z)
    
    print (z[0])
    print(z[1])
    ausgabeList("PT311013",z)
    createDataTree(z)

if __name__ == "__main__":
    main()
