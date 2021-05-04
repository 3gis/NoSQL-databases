def AddPatient(Name, Group, Disease):
     collection = db["Patient"];  
     post = {"Name": Name, "Bloodgroup": Group, "Disease": Disease};
     collection.insert_one(post);
     print("Added successfully");
def AddDonor(Name, Group, Address, Phone):
     collection = db["Donor"]
     post = {"Name":Name,"Bloodgroup":Group,"Contactdetails":{"Address":Address,"Phonenumber":Phone}};
     collection.insert_one(post);
     print("Donor added successfully");
def AddBloodHistory(Group,Litres,DonorID):
     collection = db["BloodHistory"]
     post = {"Bloodgroup":Group,"Litres":Litres, "Donor":DonorID}
     collection.insert_one(post);
     print("Added Successfully!")
def GetDonors(args):
     collection = db["Donor"]
     Donors = collection.find(args, {"_id":0});
     for Donor in Donors:
          print(Donor);
          print(" ");
def AggregateBloodHistory(args):
     collection = db["BloodHistory"]
     members = collection.aggregate([
          {"$match":{"Bloodgroup": args } },
          {"$group": { "_id": "$Bloodgroup", "total": {"$sum": "$Litres" } } }
           ])
     for member in members:
          print(member)
def mapReduceBloodHistory():
    collection = db["BloodHistory"]
    mapf = Code("function(){emit(this.Bloodgroup, this.Litres);}")
    reduce = Code("function(key, values){return Array.sum(values);}")
    mapp = collection.map_reduce(mapf,reduce,"results");

    for i in mapp.find():
         print(i);
         
from pymongo import MongoClient
from bson.son import SON
from bson.code import Code
client = MongoClient();
db = client["BloodBankDatabase"];
#AggregateBloodHistory();
#AddBloodHistory("A","0.5");
#AddBloodHistory("A","1.5");
#AddBloodHistory("A","2.5");
#GetDonors({"Contact details.Address":"Street 25"});
while True:
     print("==========MENU===========");
     print("1.Add patient")
     print("2.Add donor")
     print("3.Add blood donation")
     print("4.Donors' contact list")
     print("5.Blood type donations")
     print("6.Blood type donations (Map-Reduce)");
     var = input("Pasirinkimas: ");
     if var == '1':
          Name = input("Patient First name and Last name: ")
          Group = input("Patient Blood type: ")
          Disease = input("Patient disease: ")
          collection = db["Patient"];
          member = collection.find_one({"Name": Name});
          if member is None:
               AddPatient(Name, Group, Disease);
          else:
               print("This patient is already in database!");
     elif var == '2':
          Name = input("Donor First name and Last name: ")
          Group = input("Donor Blood type: ")
          Address = input("Donor address: ")
          Phone = input("Donor phone number: ")
          collection = db["Donor"];
          member = collection.find_one({"Name": Name});
          if member is None:
               AddDonor(Name, Group, Address, Phone);
          else:
               print("This donor is already in database!");
     elif var == '3':
          Name = input("Enter donor's name and last name: ");
          #Group = input("Donated blood group: ")
          Litres = input("Donated amount: ")
          collection = db["Donor"]
          member = collection.find_one({"Name":Name});
          if member is None:
               print("Donor doesn't exist in the database!")
          else:
               Group = member["Bloodgroup"];
               AddBloodHistory(Group, float(Litres), member["_id"]);
     elif var == '4':
          collection = db["Donor"];
          cursor = collection.find( {}, {"Name":1,"Contactdetails":1, "_id":0});
          for cur in cursor:
               print(cur);
          #GetDonors({});
     elif var == '5':
          btype = input("Enter the blood type: ");
          AggregateBloodHistory(btype);
     elif var == '6':
          mapReduceBloodHistory();
     else:
          print("Tokio pasirinkimo nera!")



