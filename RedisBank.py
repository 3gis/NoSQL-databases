import redis

def GetMoney (to,much):
     d.hincrby(to,"Balance",int(much));
     d.execute();
     print("Pavyko!");
def Transferm(fromm):
     d.watch(fromm);
     if int(r.hget(fromm,"Balance")) >= 40:
          d.multi();
          d.hincrby(fromm, "Balance", -40);
          d.hincrby(r.srandmember("Saskaitos"),"Balance",10);
          d.hincrby(r.srandmember("Saskaitos"),"Balance",10);
          d.hincrby(r.srandmember("Saskaitos"),"Balance",10);
          d.hincrby(r.srandmember("Saskaitos"),"Balance",10);
          d.execute();
          print("Pervedimas sekmingas!");
     else:
          print("Pervedimas nepavyko");
          d.unwatch;
    
def Transfer(fromm,to,much):
     d.watch(fromm);
     if int(r.hget(fromm,"Balance"))-much >= 0 and much > 0:
          d.multi();
          d.hincrby(fromm, "Balance", much*(-1));
          d.hincrby(to,"Balance",much);
          d.execute();
     else:
          print("Pervedimas nepavyko! Bandykite is naujo");
          d.unwatch;
    
def FindKey(fromm,what,iss,ans):
    x=0;
    answer = "-1";
    while x < int(r.scard(fromm)):
        if str(r.hget(what+str(x),iss)) == "b'"+str(ans)+"'":
            answer = what+str(x);
        x+=1;
    return answer;

def Login(key):
     print("Sveiki, " + vardas + "!");
     while key !=-1:
          print("1. Saskaitos sukurimas");
          print("2. Saskaitu perziurejimas");
          print("3. Pinigu pervedimas");
          print("4. Pinigu atidavimas");
          print("5. Gauti paskola");
          val = input("Pasirinkite operacija:");
          if val == '1':
            saskaitoskey = "SaskaitosKEY"+str(r.scard("Saskaitos"));
            user = {"Saskaita":"LT"+str(int(r.scard("Saskaitos")*100)),"UserKey":key,"Balance":0};
            d.hmset(saskaitoskey,user);
            d.sadd("Saskaitos",saskaitoskey);
            d.execute();
            print("Saskaita sukurta: " + str(r.hget(saskaitoskey,"Saskaita")) + " Balansas: " + str(r.hget(saskaitoskey,"Balance")) + " euru!");
          elif val =='2':
            x=0;
            while x < int(r.scard("Saskaitos")):
                if str(r.hget("SaskaitosKEY"+str(x),"UserKey"))=="b'"+str(key)+"'":
                    print(str(r.hmget("SaskaitosKEY"+str(x),"Saskaita","Balance")));
                x+=1;
          elif val =='3':
            sask = input("Iveskite jusu saskaitos numeri is kurios norite pervesti (PVZ: LT001): ");
            tran = input("Iveskite saskaitos numeri, kuriam norite pervesti: ");
            suma = input("Iveskite pervedimo suma: ");
            x=0;
            while x < int(r.scard("Saskaitos")):
                if str(r.hget("SaskaitosKEY"+str(x),"Saskaita"))=="b'"+str(sask)+"'":
                    if int(r.hget("SaskaitosKEY"+str(x),"Balance")) >= int(suma):
                        h = input("Patvirtinkite (Y/N): " + sask + " -> " + tran + " (" + suma + "):");
                        if h == 'Y' or h == 'y':
                           if FindKey("Saskaitos","SaskaitosKEY","Saskaita",tran) !="-1":
                               Transfer("SaskaitosKEY"+str(x),FindKey("Saskaitos","SaskaitosKEY","Saskaita",tran),int(suma));
                           else:
                               print("Saskaitos, kuriai norejote siusti, nera!");
                               Login(key);
                        else:
                            print("Transakcija atsaukiama..");
                            Login(key);
                    else:
                        print("Saskaitoje nera tiek pinigu! Atsaukiama...");
                        Login(key);
                x+=1;
          elif val =='4':
               h = input("Ar tikrai norite isdalinti 10 euru 4 bet kokiom saskaitom? (Y/N) ");
               if h == 'Y' or h == 'y':
                    h = input("Pasirinkite savo saskaita(pvz LT001): ");
                    L = FindKey("Saskaitos","SaskaitosKEY","Saskaita",h);
                    if L !="-1":
                         if str(r.hget(L,"UserKey")) == "b'"+str(key)+"'":
                              Transferm(L);
                         else:
                              print("Saskaita nepriklauso jums! Atsaukiama..");
                              Login(key);
                    else:
                         print("Tokios saskaitos nera! Atsaukiama..");
                         Login(key);
               else:
                    print("Atsaukiama..");
                    Login(key);
          elif val == '5':
               h = input("I kokia saskaita norite prideti pinigu? ");
               much = input("Kiek norite gauti prisideti pinigu? ");
               L = FindKey("Saskaitos","SaskaitosKEY","Saskaita",h);
               GetMoney(L,much);    
          else:
            print("Tokio pasirinkimo nera! Bandykite dar karta!");
'



r = redis.Redis(host='localhost',port = 6379,db=0);
d = r.pipeline(transaction = True);
if (str(r.get("NumberOfAccounts"))=="None"):
    print("Sukurta");
    d.set("NumberOfAccounts",0);
    d.execute();
else:
    print();
key = -1;
while key == -1:
     print("1. Registracija");
     print("2. Prisijungimas");
     toggle = True;
     val = input("Pasirinkite: ");
     lul = {0,1,2};
     if val =='1':
          print("----Registracija----");
          vardas = input("Iveskite vartotojo varda: ");
          passw = input("Iveskite slaptazodi: ");#FindKey("Saskaitos","SaskaitosKEY","Saskaita",h);
          x = 0;
          while x < r.scard("AccountList"):
               if("b'"+vardas+"'" == str(r.hget(x,"User"))):
                    print("Toks vartotojo vardas jau egzistuoja! Atsaukiama..");
                    toggle = False;  
               x+=1;
          if(toggle == True): 
               user = {"User":vardas,"Password":passw};
               d.hmset(int(r.scard("AccountList")),user);
               d.incr("NumberOfAccounts");
               d.sadd("AccountList",(int(r.scard("AccountList"))));
               d.execute();
               print("----Vartotojas sukurtas!----")
     elif val =='2':
        print("----Prisijungimas----");
        vardas = input("Iveskite vartotojo varda: ");
        passw = input("Iveskite slaptazodi: ");
        x=0;
        while x < int(r.get("NumberOfAccounts")):
            if str(r.hget(x,"User"))=="b'"+vardas+"'" and str(r.hget(x,"Password"))=="b'"+passw+"'":
                key = x;
                print("Prisijungete kaip ID: " + str(key));
                toggle = False;
                Login(key);
                break;
            x+=1;
        if toggle == True:
            print("Klaidingas vartotojo vardas arba slaptazodis!");
     elif val =='3':
        x=0;
        while x < int(r.get("NumberOfAccounts")):
            print(r.hgetall(x));
            x+=1;
     else:
        print("Nera tokio pasirinkimo! Bandykite dar karta!")


