def FindPilot(plane,airport):
     q="MATCH (y:plane {type:'"+plane+"', port:'"+airport+"'})-[:PILOT]->(x:pilot) RETURN x";
     with driver.session() as graphDB_Session:
          info = graphDB_Session.run(q);
          for i in info:
               print(i);
def FindAllPlanes(airport):
     q="MATCH (y:airport {name:'"+airport+"Airport'})-[:OWNED_PLANE]->(x:plane) RETURN x";
     with driver.session() as graphDB_Session:
          info = graphDB_Session.run(q);
          for i in info:
               print(i);
def FindAllPaths(AirportA,AirportB):
     q="MATCH (a:airport{name:'"+AirportA+"Airport'})-[r*..5]-(t:airport{name:'"+AirportB+"Airport'}) return DISTINCT r"
     with driver.session() as graphDB_Session:
          info = graphDB_Session.run(q);
          for i in info:
               print("---------");
               for p in i:  
                    print(p);
def ShortestPath(AirportA,AirportB):
     #q="MATCH (y:airport {name:'"+AirportA+"Airport'}), (c:airport {name:'"+AirportB+"Airport'}), path = ShortestPath((y)-[*..10]-(c)) RETURN path";
     #q="MATCH (y:airport {name:'"+AirportA+"Airport'}), (c:airport {name:'"+AirportB+"Airport'}),path=shortestpath((y)-[:CAN_TRAVEL_TO*..6]->(c)) RETURN path, REDUCE(distancekm=0, r in relationships(path) | distancekm+r.distancekm) AS totalDistance ORDER BY totalDistance ASC LIMIT 1"
     q="MATCH (c1:airport {name:'"+AirportA+"Airport'}) MATCH (c2:airport{name: '"+AirportB+"Airport'}) CALL apoc.algo.dijkstra(c1,c2,'CAN_TRAVEL_TO','distancekm') YIELD path RETURN path"
     with driver.session() as graphDB_Session:
          info = graphDB_Session.run(q);
          for i in info:
               nodes = i["path"].nodes
               for node in nodes:
                    print(node);
def FindYoungestAndOldestPilot():
     q="MATCH (n:pilot) Return max(n.age)";
     with driver.session() as graphDB_Session:
          info = graphDB_Session.run(q);
          
          for i in info:
               print("Oldest pilot's age: " + i[0]);
          q="MATCH (n:pilot) Return min(n.age)";
          info = graphDB_Session.run(q);
          for i in info:
               print("Youngest pilot's age: " + i[0]);
from neo4j import GraphDatabase
uri             = "bolt://localhost:7687"
userName        = "AirportAdmin"
password        = "Iamapilot123"

# Connect to the neo4j database server
driver = GraphDatabase.driver(uri, auth=(userName, password))
connection = driver.session()

# CQL to query all the universities present in the graph
query = "MATCH (N) detach DELETE(N)"

connection.run(query)

q = """CREATE
(Amsterdam:airport { name: 'AmsterdamAirport'}),
(Paris:airport { name: 'ParisAirport'}),
(Dallas:airport { name: 'DallasAirport'}),
(London:airport { name: 'LondonAirport'}),
(Chicago:airport { name: 'ChicagoAirport'}),
(LasVegas:airport { name: 'LasVegasAirport'}),
(LosAngeles:airport { name: 'LosAngelesAirport'}),
(Tokyo:airport { name: 'TokyoAirport'}),
(Dubai:airport { name: 'DubaiAirport'}),
(Vilnius:airport { name: 'VilniusAirport'}),
(Beijing:airport { name: 'BeijingAirport'}),
(Sydney:airport { name: 'SydneyAirport'}),

(Amsterdam)-[:CAN_TRAVEL_TO {distancekm:417}]->(Paris),
(Amsterdam)-[:CAN_TRAVEL_TO {distancekm:395}]->(London),
(Amsterdam)-[:CAN_TRAVEL_TO {distancekm:1530}]->(Vilnius),
(Amsterdam)-[:CAN_TRAVEL_TO {distancekm:5293}]->(Dubai),
(Vilnius)-[:CAN_TRAVEL_TO {distancekm:1461}]->(London),
(Vilnius)-[:CAN_TRAVEL_TO {distancekm:1458}]->(Paris),
(Vilnius)-[:CAN_TRAVEL_TO {distancekm:4088}]->(Dubai),
(Paris)-[:CAN_TRAVEL_TO {distancekm:329}]->(London),
(Dallas)-[:CAN_TRAVEL_TO {distancekm:1982}]->(LosAngeles),
(Dallas)-[:CAN_TRAVEL_TO {distancekm:7939}]->(Paris),
(Dubai)-[:CAN_TRAVEL_TO {distancekm:5460}]->(London),
(Dubai)-[:CAN_TRAVEL_TO {distancekm:5235}]->(Paris),
(Chicago)-[:CAN_TRAVEL_TO {distancekm:1289}]->(Dallas),
(Chicago)-[:CAN_TRAVEL_TO {distancekm:2430}]->(LasVegas),
(Sydney)-[:CAN_TRAVEL_TO {distancekm:7812}]->(Tokyo),
(Sydney)-[:CAN_TRAVEL_TO {distancekm:12053}]->(LosAngeles),
(Sydney)-[:CAN_TRAVEL_TO {distancekm:12036}]->(Dubai),
(Beijing)-[:CAN_TRAVEL_TO {distancekm:2089}]->(Tokyo),
(Beijing)-[:CAN_TRAVEL_TO {distancekm:8957}]->(Sydney),
(Beijing)-[:CAN_TRAVEL_TO {distancekm:5843}]->(Dubai),
(LosAngeles)-[:CAN_TRAVEL_TO {distancekm:8807}]->(Tokyo),
(LasVegas)-[:CAN_TRAVEL_TO {distancekm:8732}]->(Paris),
(LasVegas)-[:CAN_TRAVEL_TO {distancekm:380}]->(LosAngeles),


(AmsterdamA350:plane { type: 'A350', port: 'Amsterdam'}),
(AmsterdamA380:plane { type: 'A380', port: 'Amsterdam' }),
(Amsterdam747:plane { type: '747', port: 'Amsterdam'}),

(ParisA350:plane { type: 'A350', port: 'Paris'}),
(ParisA380:plane { type: 'A380', port: 'Paris'}),
(Paris747:plane { type: '747', port: 'Paris'}),

(DallasA350:plane { type: 'A350', port: 'Dallas'}),
(DallasA380:plane { type: 'A380', port: 'Dallas'}),
(Dallas747:plane { type: '747', port: 'Dallas'}),

(LondonA350:plane { type: 'A350', port: 'London'}),
(LondonA380:plane { type: 'A380', port: 'London'}),
(London747:plane { type: '747', port: 'London'}),

(ChicagoA350:plane { type: 'A350', port: 'Chicago'}),
(ChicagoA380:plane { type: 'A380', port: 'Chicago'}),
(Chicago747:plane { type: '747', port: 'Chicago'}),

(LasVegasA350:plane { type: 'A350', port: 'LasVegas'}),
(LasVegasA380:plane { type: 'A380', port: 'LasVegas'}),
(LasVegas747:plane { type: '747', port: 'LasVegas'}),

(LosAngelesA350:plane { type: 'A350', port: 'LosAngeles'}),
(LosAngelesA380:plane { type: 'A380', port: 'LosAngeles'}),
(LosAngeles747:plane { type: '747', port: 'LosAngeles'}),

(TokyoA350:plane { type: 'A350', port: 'Tokyo'}),
(TokyoA380:plane { type: 'A380', port: 'Tokyo'}),
(Tokyo747:plane { type: '747' , port: 'Tokyo'}),

(DubaiA350:plane { type: 'A350', port: 'Dubai'}),
(DubaiA380:plane { type: 'A380', port: 'Dubai'}),
(Dubai747:plane { type: '747', port: 'Dubai'}),

(VilniusA350:plane { type: 'A350', port: 'Vilnius'}),
(VilniusA380:plane { type: 'A380', port: 'Vilnius'}),
(Vilnius747:plane { type: '747', port: 'Vilnius'}),

(BeijingA350:plane { type: 'A350', port: 'Beijing'}),
(BeijingA380:plane { type: 'A380', port: 'Beijing'}),
(Beijing747:plane { type: '747', port: 'Beijing'}),

(SydneyA350:plane { type: 'A350', port: 'Sydney'}),
(SydneyA380:plane { type: 'A380', port: 'Sydney'}),
(Sydney747:plane { type: '747', port: 'Sydney'}),

(Amsterdam)-[:OWNED_PLANE]->(AmsterdamA350),
(Amsterdam)-[:OWNED_PLANE]->(AmsterdamA380),
(Amsterdam)-[:OWNED_PLANE]->(Amsterdam747),
(Vilnius)-[:OWNED_PLANE]->(VilniusA350),
(Vilnius)-[:OWNED_PLANE]->(VilniusA380),
(Vilnius)-[:OWNED_PLANE]->(Vilnius747),
(London)-[:OWNED_PLANE]->(LondonA350),
(London)-[:OWNED_PLANE]->(LondonA380),
(London)-[:OWNED_PLANE]->(London747),
(Paris)-[:OWNED_PLANE]->(ParisA350),
(Paris)-[:OWNED_PLANE]->(ParisA380),
(Paris)-[:OWNED_PLANE]->(Paris747),
(Dallas)-[:OWNED_PLANE]->(DallasA350),
(Dallas)-[:OWNED_PLANE]->(DallasA380),
(Dallas)-[:OWNED_PLANE]->(Dallas747),
(Dubai)-[:OWNED_PLANE]->(DubaiA350),
(Dubai)-[:OWNED_PLANE]->(DubaiA380),
(Dubai)-[:OWNED_PLANE]->(Dubai747),
(Chicago)-[:OWNED_PLANE]->(ChicagoA350),
(Chicago)-[:OWNED_PLANE]->(ChicagoA380),
(Chicago)-[:OWNED_PLANE]->(Chicago747),
(Sydney)-[:OWNED_PLANE]->(SydneyA350),
(Sydney)-[:OWNED_PLANE]->(SydneyA380),
(Sydney)-[:OWNED_PLANE]->(Sydney747),
(Tokyo)-[:OWNED_PLANE]->(TokyoA350),
(Tokyo)-[:OWNED_PLANE]->(TokyoA380),
(Tokyo)-[:OWNED_PLANE]->(Tokyo747),
(Beijing)-[:OWNED_PLANE]->(BeijingA350),
(Beijing)-[:OWNED_PLANE]->(BeijingA380),
(Beijing)-[:OWNED_PLANE]->(Beijing747),
(LosAngeles)-[:OWNED_PLANE]->(LosAngelesA350),
(LosAngeles)-[:OWNED_PLANE]->(LosAngelesA380),
(LosAngeles)-[:OWNED_PLANE]->(LosAngeles747),
(LasVegas)-[:OWNED_PLANE]->(LasVegasA350),
(LasVegas)-[:OWNED_PLANE]->(LasVegasA380),
(LasVegas)-[:OWNED_PLANE]->(LasVegas747),

(John:pilot { name: 'John', age: '21'}),
(Bob:pilot { name: 'Bob', age: '21'}),
(Patrick:pilot { name: 'Patrick', age: '21'}),
(Igor:pilot { name: 'Igor', age: '52'}),
(Lee:pilot { name: 'Lee', age: '24'}),
(Felix:pilot { name: 'Felix', age: '25'}),

(Vlad:pilot { name: 'Vlad', age: '21'}),
(David:pilot { name: 'David', age: '21'}),
(Tom:pilot { name: 'Tom', age: '36'}),
(Matt:pilot { name: 'Matt', age: '32'}),
(Louis:pilot { name: 'Louis', age: '31'}),
(Stephen:pilot { name: 'Stephen', age: '28'}),

(Elon:pilot { name: 'Elon', age: '27'}),
(William:pilot { name: 'William', age: '74'}),
(Mark:pilot { name: 'Mark', age: '65'}),
(Jack:pilot { name: 'Jack', age: '45'}),
(Sean:pilot { name: 'Sean', age: '68'}),
(Darius:pilot { name: 'Darius', age: '12'}),

(Paul:pilot { name: 'Paul', age: '21'}),
(Eve:pilot { name: 'Eve', age: '21'}),
(Adolf:pilot { name: 'Adolf', age: '21'}),
(Susan:pilot { name: 'Susan', age: '21'}),
(Michael:pilot { name: 'Michael', age: '21'}),
(Don:pilot { name: 'Don', age: '21'}),

(Gon:pilot { name: 'Gon', age: '21'}),
(Ron:pilot { name: 'Ron', age: '21'}),
(Harry:pilot { name: 'Harry', age: '21'}),
(Snape:pilot { name: 'Snape', age: '21'}),
(Hulk:pilot { name: 'Hulk', age: '21'}),
(Bill:pilot { name: 'Bill', age: '21'}),

(Krillin:pilot { name: 'Krillin', age: '30'}),
(Goku:pilot { name: 'Goku', age: '50'}),
(Piccolo:pilot { name: 'Piccolo', age: '45'}),
(Joshua:pilot { name: 'Joshua', age: '39'}),
(Giovani:pilot { name: 'Giovani', age: '24'}),
(Luffy:pilot { name: 'Luffy', age: '20'}),

(AmsterdamA350)-[:PILOT]->(John),
(AmsterdamA380)-[:PILOT]->(Bob),
(Amsterdam747)-[:PILOT]->(Patrick),

(ParisA350)-[:PILOT]->(Igor),
(ParisA380)-[:PILOT]->(Lee),
(Paris747)-[:PILOT]->(Felix),

(DallasA350)-[:PILOT]->(Vlad),
(DallasA380)-[:PILOT]->(David),
(Dallas747)-[:PILOT]->(Tom),

(LondonA350)-[:PILOT]->(Matt),
(LondonA380)-[:PILOT]->(Louis),
(London747)-[:PILOT]->(Stephen),

(ChicagoA350)-[:PILOT]->(Elon),
(ChicagoA380)-[:PILOT]->(William),
(Chicago747)-[:PILOT]->(Mark),

(LasVegasA350)-[:PILOT]->(Jack),
(LasVegasA380)-[:PILOT]->(Sean),
(LasVegas747)-[:PILOT]->(Darius),

(LosAngelesA350)-[:PILOT]->(Paul),
(LosAngelesA380)-[:PILOT]->(Eve),
(LosAngeles747)-[:PILOT]->(Adolf),

(TokyoA350)-[:PILOT]->(Susan),
(TokyoA380)-[:PILOT]->(Michael),
(Tokyo747)-[:PILOT]->(Don),

(DubaiA350)-[:PILOT]->(Gon),
(DubaiA380)-[:PILOT]->(Ron),
(Dubai747)-[:PILOT]->(Harry),

(VilniusA350)-[:PILOT]->(Snape),
(VilniusA380)-[:PILOT]->(Hulk),
(Vilnius747)-[:PILOT]->(Bill),

(BeijingA350)-[:PILOT]->(Krillin),
(BeijingA380)-[:PILOT]->(Goku),
(Beijing747)-[:PILOT]->(Piccolo),

(SydneyA350)-[:PILOT]->(Joshua),
(SydneyA380)-[:PILOT]->(Giovani),
(Sydney747)-[:PILOT]->(Luffy)
"""
with driver.session() as graphDB_Session:
     nodes = graphDB_Session.run(q);
while True:  
     var = input(
"""
1. Find pilot by plane and airport
2. Find all planes by airport
3. Find all paths from A to B
4. Shortest path from A to B
5. Find Youngest and Oldest pilot's age
""")
     if var == '1':
          print("PLANE TYPES:");
          print("A350 | A380 | 747");
          print("AIRPORTS AVAILABLE:");
          print("Amsterdam , Paris , Dallas , London , Chicago , LasVegas , LosAngeles , Tokyo , Dubai , Vilnius , Beijing , Sydney");
          plane = input("Enter a specific plane: ");
          airport = input("Enter a specific airport: ");
          FindPilot(plane, airport);
     elif var == '2':
          print("AIRPORTS AVAILABLE:");
          print("Amsterdam , Paris , Dallas , London , Chicago , LasVegas , LosAngeles , Tokyo , Dubai , Vilnius , Beijing , Sydney");
          airport = input("Enter an airport city: ");
          FindAllPlanes(airport);
     elif var == '3':
          print("AIRPORTS AVAILABLE:");
          print("Amsterdam , Paris , Dallas , London , Chicago , LasVegas , LosAngeles , Tokyo , Dubai , Vilnius , Beijing , Sydney");
          airportA = input("Enter starting airport: ");
          airportB = input("Enter destination airport: ");
          FindAllPaths(airportA,airportB);
     elif var == '4':
          airportA = input("Enter starting airport: ");
          airportB = input("Enter destination airport: ");
          ShortestPath(airportA,airportB);
     elif var == '5':
          FindYoungestAndOldestPilot();
     else:
          print("There is no such choice!");
     
