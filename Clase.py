class Administratori:
    def __init__(self,ID_Adm,Nume,Prenume,email,parola,isAdmin):
        self.ID_Adm = ID_Adm
        self.Nume = Nume
        self.Prenume = Prenume
        self.email = email
        self.parola = parola
        self.isAdmin = isAdmin
    
    def __init__(self,Nume,Prenume, email, parola, isAdmin):
        self.Nume = Nume
        self.Prenume = Prenume
        self.email = email
        self.parola = parola
        self.isAdmin = isAdmin
        
class Categorii:
    def __init__(self,ID_Categ,Descriere,Cote_Categ,ID_Adm):
        self.ID_Categ = ID_Categ
        self.Descriere = Descriere
        self.Cote_Categ = Cote_Categ
        self.ID_Adm = ID_Adm
        
class Cheltuieli:
    def __init__(self,ID_Chelt,Data_Chelt,Den_Chelt,Val_Chelt,Cote_Chelt,ID_Categ):
        self.ID_Chelt = ID_Chelt
        self.Data_Chelt = Data_Chelt
        self.Den_Chelt = Den_Chelt
        self.Val_Chelt = Val_Chelt
        self.Cote_Chelt = Cote_Chelt
        self.ID_Categ = ID_Categ

class Rezultate:
    def __init__(self,ID_Rez,Den_Rez,Val_Rez,Cote_Dif,ID_Adm):
        self.ID_Rez = ID_Rez
        self.Den_Rez = Den_Rez
        self.Val_Rez = Val_Rez
        self.Cote_Dif = Cote_Dif
        self.ID_Adm = ID_Adm


import mysql.connector


def IsLoginValid(email, password):
    mydb = mysql.connector.connect(
        host= "DESKTOP-U937194",
        user="DanFkt",
        password= "Anda1Iulia2#",
        database="BugetulTau"
    )
    myCursor = mydb.cursor()
    sql = "Select Nume, Prenume, isAdmin From Administratori Where email = '" + email + "' and parola = '" + password + "'"
    myCursor.execute(sql)
    myResult = myCursor.fetchall()
    
    loginOK = False
    user = None
    for x in myResult:
        loginOK = True
        user = Administratori(x[0],x[1],email, password, x[2])
        if loginOK:
            break
    
    myCursor.close()
    return user

def insertVenitTinta(venit, tinta, procent_tinta,categorii,procent_categorii,valoare_categorii,cheltuieli):
    mydb = mysql.connector.connect(
        host= "DESKTOP-U937194",
        user="DanFkt",
        password= "Anda1Iulia2#",
        database="BugetulTau"
    )
    myCursor = mydb.cursor()
    sql = "Insert Into Categorii(<coloana_venit>, <coloana_tinta>, <coloana_procent_tinta>,<categorii>,<procent_categorii>,<valoare_categorii>,<cheltuieli>)) values (%s,%s, %s,%s,%s,%s,%s)'"
    values = (venit, tinta, procent_tinta,categorii,procent_categorii,valoare_categorii,cheltuieli)
    myCursor.execute(sql, values)
    mydb.commit()
    myCursor.close()

def get_table_column_names(tableName):
    mydb = mysql.connector.connect(
        host= "DESKTOP-U937194",
        user="DanFkt",
        password= "Anda1Iulia2#",
        database="BugetulTau"
    )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE " +
                     "TABLE_SCHEMA = 'BugetulTau' AND TABLE_NAME = '" + 
                     tableName + "' and Extra <> 'auto_increment' Order By Column_Name Asc")

    myresult = mycursor.fetchall()

    result = []
    for x in myresult:
        result.append(x[0])

    mycursor.close()

    return result

def insert_data(fileName,tableName):
    
    mydb = mysql.connector.connect(
    host= "DESKTOP-U937194",
    user="DanFkt",
    password= "Anda1Iulia2#",
    database="BugetulTau"
    )
    mycursor = mydb.cursor()
    file = open(fileName, 'r')

    #colNames: IDSpecializare, Descriere --    
    colNames = get_table_column_names(tableName)
    
    lines = file.readlines()
    for line in lines:
        query = "Insert Into " + tableName + "(" #Insert Into Administratori (
        i = 0
        strCols = ''
        for colName in colNames:
            strCols += colName + ","    #Insert Into Administratori (ID_Adm,Nume,Prenume, email,parola,isAdmin
            i += 1
        #remove last comma 
        strCols = strCols[:-1] #Insert Into Administatori (ID_Adm,Nume,Prenume, email,parola,isAdmin
        query += strCols + ") values (" #Insert Into Administatori (ID_Adm,Nume,Prenume, email,parola,isAdmin) values ("
        
        for j in range(0,i):
            query += "%s," #Insert Into Administatori (ID_Adm,Nume,Prenume, email,parola,isAdmin) values ("%s,%s,%s,%s,%s,%s
        #remova last comma
        query = query[:-1] #Insert Into Administatori (ID_Adm,Nume,Prenume, email,parola,isAdmin) values ("%s,%s,%s,%s,%s,%s
        
        query += ")" #Insert Into Administatori (ID_Adm,Nume,Prenume, email,parola,isAdmin) values ("%s,%s,%s,%s,%s,%s)
        print(query)
        values = line.split(",")
        mycursor.execute(query, values)
        mydb.commit()

    mycursor.close()

def populate_tables():
    insert_data("C:\\Temp\\Python\\BugetulTauApp\\static\\files\\Administratori.txt","Administratori")
    insert_data("C:\\Temp\\Python\\BugetulTauApp\\static\\files\\Categorii.txt","Categorii")
    insert_data("C:\\Temp\\Python\\BugetulTauApp\\static\\files\\Cheltuieli.txt","Cheltuieli")
    insert_data("C:\\Temp\\Python\\BugetulTauApp\\static\\files\\Rezultate.txt","Rezultate")
    

def generate_report():
    mydb = mysql.connector.connect(
    host= "DESKTOP-U937194",
    user="DanFkt",
    password= "Anda1Iulia2#",
    database="BugetulTau"
    )
    mycursor = mydb.cursor()

    query = """Select S.NrMatricol,
                S.Nume,
                S.Prenume,
                S.An,
                SP.Descriere as DenumireSpecializare,
                S.Grupa,
                M.Denumire as Materie,
                P.Nume,
                P.Prenume,
                C.Denumire as CatedraProfesor
            From
                studenti S Inner Join Specializari SP on S.IDSpecializare = SP.IDSpecializare
                Inner Join Materii M on M.IDSpecializare = SP.IDSpecializare
                Inner Join Profesori P on M.IDMaterie = P.IDMaterie
                Inner Join Catedre C on P.IDCatedra = C.IDCatedra"""

    mycursor.execute(query)
    myresult = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return myresult

def write_data(file, results, forHtml):
    f = open(file,"w")
    if forHtml:
        f.writelines("Nume Student  Prenume Student An  Specializare    Grupa   Materie Nume Profesor   Prenume Profesor    Catedra Profesor\n")
    for result in results:
        strLine = str(result)
        if forHtml:
            strLine = strLine.replace("(","").replace(")","")
            #f.writelines(strLine)
        #else:
            #f.writelines(strLine)
        strLines = strLine.split(",")
        for word in strLines:
            word = word.replace("\n","").replace("'","") + "    "
            f.write(word)
        f.writelines("\n")
    f.close()

def process_data(filename):
    #populate_tables()
    report = generate_report()
    filename = "C:\\Users\\Dan\\OneDrive\\Desktop\\Python course\\Celia\\Curs 21\\FacultateApp\\static\\files\\" + filename
    write_data(filename, report, True)
    return filename   
    