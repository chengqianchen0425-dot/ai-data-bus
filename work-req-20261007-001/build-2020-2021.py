#!/usr/bin/env python3
"""Build 2020/21 pre-match standings snapshots from worldfootball round tables (live browser)."""
import json, datetime

BASE = '/home/hatch/workspace/ai-inbox/repo/work-req-20261007-001'
URL_TMPL = 'https://www.worldfootball.net/competition/co111/italy-serie-a/se36220/2020-2021/ro110161/matchday/md{}/results-and-standings/'

NAME_MAP = {
    'Inter': 'Inter', 'Atalanta': 'Atalanta', 'Genoa CFC': 'Genoa',
    'Hellas Verona': 'Verona', 'Juventus': 'Juventus', 'Spezia Calcio': 'Spezia',
    'ACF Fiorentina': 'Fiorentina', 'AC Milan': 'Milan', 'SSC Napoli': 'Napoli',
    'Cagliari Calcio': 'Cagliari', 'US Sassuolo': 'Sassuolo', 'Torino FC': 'Torino',
    'Bologna FC': 'Bologna', 'Parma Calcio 1913': 'Parma', 'Udinese Calcio': 'Udinese',
    'Benevento Calcio': 'Benevento', 'FC Crotone': 'Crotone', 'Lazio Roma': 'Lazio',
    'AS Roma': 'Roma', 'Sampdoria': 'Sampdoria',
}

# (pos, wf_name, P, W, D, L, GF, GA, Pts) per round, as displayed on worldfootball round page
TABLES = {
1: [(1,'Inter',1,1,0,0,5,2,3),(2,'Atalanta',1,1,0,0,4,1,3),(3,'Genoa CFC',1,1,0,0,4,1,3),(4,'Hellas Verona',1,1,0,0,3,0,3),(5,'Juventus',1,1,0,0,3,0,3),(6,'Spezia Calcio',1,1,0,0,2,0,3),(7,'ACF Fiorentina',1,1,0,0,1,0,3),(8,'AC Milan',1,1,0,0,2,0,3),(9,'SSC Napoli',1,1,0,0,2,0,3),(10,'Cagliari Calcio',1,0,1,0,1,1,1),(11,'US Sassuolo',1,0,1,0,1,1,1),(12,'Torino FC',1,0,0,1,0,1,0),(13,'Bologna FC',1,0,0,1,0,2,0),(14,'Parma Calcio 1913',1,0,0,1,0,2,0),(15,'Udinese Calcio',1,0,0,1,0,2,0),(16,'Benevento Calcio',1,0,0,1,2,5,0),(17,'FC Crotone',1,0,0,1,1,4,0),(18,'Lazio Roma',1,0,0,1,1,4,0),(19,'AS Roma',1,0,0,1,0,3,0),(20,'Sampdoria',1,0,0,1,0,3,0)],
2: [(1,'Atalanta',2,2,0,0,8,3,6),(2,'Inter',2,2,0,0,9,5,6),(3,'Hellas Verona',2,2,0,0,4,0,6),(4,'AC Milan',2,2,0,0,4,0,6),(5,'SSC Napoli',2,2,0,0,8,0,6),(6,'Juventus',2,1,1,0,5,2,4),(7,'US Sassuolo',2,1,1,0,5,2,4),(8,'Bologna FC',2,1,0,1,4,3,3),(9,'ACF Fiorentina',2,1,0,1,4,4,3),(10,'Lazio Roma',2,1,0,1,3,4,3),(11,'Spezia Calcio',2,1,0,1,3,4,3),(12,'Benevento Calcio',2,1,0,1,5,7,3),(13,'Genoa CFC',2,1,0,1,4,7,3),(14,'Cagliari Calcio',2,0,1,1,1,3,1),(15,'AS Roma',2,0,1,1,2,5,1),(16,'Torino FC',2,0,0,2,2,5,0),(17,'Udinese Calcio',2,0,0,2,0,3,0),(18,'Sampdoria',2,0,0,2,2,6,0),(19,'FC Crotone',2,0,0,2,1,6,0),(20,'Parma Calcio 1913',2,0,0,2,1,6,0)],
3: [(1,'Atalanta',3,3,0,0,13,5,9),(2,'AC Milan',3,3,0,0,7,0,9),(3,'US Sassuolo',3,2,1,0,9,3,7),(4,'Inter',3,2,1,0,10,6,7),(5,'Juventus',3,2,1,0,7,3,7),(6,'Hellas Verona',3,2,0,1,4,1,6),(7,'Benevento Calcio',3,2,0,1,6,7,6),(8,'SSC Napoli',3,2,0,1,9,2,6),(9,'Lazio Roma',3,1,1,1,4,5,4),(10,'AS Roma',3,1,1,1,3,5,4),(11,'Bologna FC',3,1,0,2,4,4,3),(12,'ACF Fiorentina',3,1,0,2,5,6,3),(13,'Torino FC',3,1,0,2,4,6,3),(14,'Sampdoria',3,1,0,2,4,7,3),(15,'Genoa CFC',3,1,0,2,5,9,3),(16,'Spezia Calcio',3,1,0,2,3,7,3),(17,'Parma Calcio 1913',3,1,0,2,2,6,3),(18,'Cagliari Calcio',3,0,1,2,3,8,1),(19,'Udinese Calcio',3,0,0,3,0,4,0),(20,'FC Crotone',3,0,0,3,2,10,0)],
4: [(1,'AC Milan',4,4,0,0,9,1,12),(2,'US Sassuolo',4,3,1,0,13,6,10),(3,'Atalanta',4,3,0,1,14,9,9),(4,'SSC Napoli',4,3,0,1,13,3,9),(5,'Juventus',4,2,2,0,8,4,8),(6,'Inter',4,2,1,1,11,8,7),(7,'Hellas Verona',4,2,1,1,4,1,7),(8,'AS Roma',4,2,1,1,8,7,7),(9,'Sampdoria',4,2,0,2,7,7,6),(10,'Benevento Calcio',4,2,0,2,8,12,6),(11,'ACF Fiorentina',4,1,1,2,7,8,4),(12,'Cagliari Calcio',4,1,1,2,6,10,4),(13,'Genoa CFC',4,1,1,2,5,9,4),(14,'Spezia Calcio',4,1,1,2,5,9,4),(15,'Lazio Roma',4,1,1,2,4,8,4),(16,'Bologna FC',4,1,0,3,7,8,3),(17,'Torino FC',4,1,0,3,6,9,3),(18,'Udinese Calcio',4,1,0,3,3,6,3),(19,'Parma Calcio 1913',4,1,0,3,4,9,3),(20,'FC Crotone',4,0,1,3,3,11,1)],
5: [(1,'AC Milan',5,4,1,0,12,4,13),(2,'SSC Napoli',5,4,0,1,15,4,12),(3,'US Sassuolo',5,3,2,0,16,9,11),(4,'Inter',5,3,1,1,13,8,10),(5,'Juventus',5,2,3,0,9,5,9),(6,'Atalanta',5,3,0,2,15,12,9),(7,'Sampdoria',5,3,0,2,10,8,9),(8,'Hellas Verona',5,2,2,1,5,2,8),(9,'AS Roma',5,2,2,1,11,10,8),(10,'ACF Fiorentina',5,2,1,2,10,10,7),(11,'Cagliari Calcio',5,2,1,2,10,12,7),(12,'Lazio Roma',5,2,1,2,6,9,7),(13,'Benevento Calcio',5,2,0,3,9,14,6),(14,'Spezia Calcio',5,1,2,2,7,11,5),(15,'Torino FC',5,1,1,3,9,12,4),(16,'Parma Calcio 1913',5,1,1,3,6,11,4),(17,'Genoa CFC',5,1,1,3,5,11,4),(18,'Bologna FC',5,1,0,4,8,10,3),(19,'Udinese Calcio',5,1,0,4,5,9,3),(20,'FC Crotone',5,0,1,4,5,15,1)],
6: [(1,'AC Milan',6,5,1,0,14,5,16),(2,'US Sassuolo',6,4,2,0,18,9,14),(3,'Juventus',6,3,3,0,13,6,12),(4,'Atalanta',6,4,0,2,17,13,12),(5,'SSC Napoli',6,4,0,2,15,6,12),(6,'Inter',6,3,2,1,15,10,11),(7,'Hellas Verona',6,3,2,1,8,3,11),(8,'AS Roma',6,3,2,1,13,10,11),(9,'Sampdoria',6,3,1,2,11,9,10),(10,'Lazio Roma',6,3,1,2,10,12,10),(11,'ACF Fiorentina',6,2,1,3,10,12,7),(12,'Cagliari Calcio',6,2,1,3,12,15,7),(13,'Bologna FC',6,2,0,4,11,12,6),(14,'Benevento Calcio',6,2,0,4,10,17,6),(15,'Parma Calcio 1913',6,1,2,3,8,13,5),(16,'Genoa CFC',6,1,2,3,6,12,5),(17,'Spezia Calcio',6,1,2,3,8,15,5),(18,'Torino FC',6,1,1,4,12,16,4),(19,'Udinese Calcio',6,1,0,5,6,11,3),(20,'FC Crotone',6,0,1,5,6,17,1)],
7: [(1,'AC Milan',7,5,2,0,16,7,17),(2,'US Sassuolo',7,4,3,0,18,9,15),(3,'SSC Napoli',7,5,0,2,16,6,15),(4,'AS Roma',7,4,2,1,16,11,14),(5,'Juventus',7,3,4,0,14,7,13),(6,'Atalanta',7,4,1,2,18,14,13),(7,'Inter',7,3,3,1,16,11,12),(8,'Hellas Verona',7,3,3,1,10,5,12),(9,'Lazio Roma',7,3,2,2,11,13,11),(10,'Sampdoria',7,3,1,3,11,11,10),(11,'Cagliari Calcio',7,3,1,3,14,15,10),(12,'ACF Fiorentina',7,2,2,3,10,12,8),(13,'Spezia Calcio',7,2,2,3,11,15,8),(14,'Bologna FC',7,2,0,5,11,13,6),(15,'Parma Calcio 1913',7,1,3,3,8,13,6),(16,'Benevento Calcio',7,2,0,5,10,20,6),(17,'Torino FC',7,1,2,4,12,16,5),(18,'Genoa CFC',7,1,2,4,7,15,5),(19,'Udinese Calcio',7,1,1,5,6,11,4),(20,'FC Crotone',7,0,2,5,6,17,2)],
8: [(1,'AC Milan',8,6,2,0,19,8,20),(2,'US Sassuolo',8,5,3,0,20,9,18),(3,'AS Roma',8,5,2,1,19,11,17),(4,'Juventus',8,4,4,0,16,7,16),(5,'Inter',8,4,3,1,20,13,15),(6,'SSC Napoli',8,5,0,3,17,9,15),(7,'Atalanta',8,4,2,2,18,14,14),(8,'Lazio Roma',8,4,2,2,13,13,14),(9,'Hellas Verona',8,3,3,2,10,7,12),(10,'Sampdoria',8,3,1,4,12,13,10),(11,'Cagliari Calcio',8,3,1,4,14,17,10),(12,'Bologna FC',8,3,0,5,13,14,9),(13,'Spezia Calcio',8,2,3,3,11,15,9),(14,'Benevento Calcio',8,3,0,5,11,20,9),(15,'ACF Fiorentina',8,2,2,4,10,13,8),(16,'Udinese Calcio',8,2,1,5,7,11,7),(17,'Parma Calcio 1913',8,1,3,4,8,16,6),(18,'Torino FC',8,1,2,5,14,20,5),(19,'Genoa CFC',8,1,2,5,7,16,5),(20,'FC Crotone',8,0,2,6,6,19,2)],
9: [(1,'AC Milan',9,7,2,0,21,8,23),(2,'Inter',9,5,3,1,23,13,18),(3,'US Sassuolo',9,5,3,1,20,12,18),(4,'SSC Napoli',9,6,0,3,21,9,18),(5,'Juventus',9,4,5,0,17,8,17),(6,'AS Roma',9,5,2,2,19,15,17),(7,'Hellas Verona',9,4,3,2,12,7,15),(8,'Atalanta',9,4,2,3,18,16,14),(9,'Lazio Roma',9,4,2,3,14,16,14),(10,'Bologna FC',9,4,0,5,14,14,12),(11,'Sampdoria',9,3,2,4,14,15,11),(12,'Cagliari Calcio',9,3,2,4,16,19,11),(13,'Udinese Calcio',9,3,1,5,10,12,10),(14,'Spezia Calcio',9,2,4,3,13,17,10),(15,'Benevento Calcio',9,3,1,5,12,21,10),(16,'Parma Calcio 1913',9,2,3,4,10,17,9),(17,'ACF Fiorentina',9,2,2,5,10,15,8),(18,'Torino FC',9,1,3,5,16,22,6),(19,'Genoa CFC',9,1,2,6,8,18,5),(20,'FC Crotone',9,0,2,7,6,20,2)],
10: [(1,'AC Milan',10,8,2,0,23,9,26),(2,'Inter',10,6,3,1,26,14,21),(3,'SSC Napoli',10,7,0,3,25,9,21),(4,'Juventus',10,5,5,0,19,9,20),(5,'US Sassuolo',10,5,4,1,20,12,19),(6,'AS Roma',10,5,3,2,19,15,18),(7,'Lazio Roma',10,5,2,3,16,17,17),(8,'Hellas Verona',10,4,4,2,13,8,16),(9,'Atalanta',10,4,3,3,19,17,15),(10,'Bologna FC',10,4,0,6,15,17,12),(11,'Cagliari Calcio',10,3,3,4,17,20,12),(12,'Sampdoria',10,3,2,5,15,17,11),(13,'Udinese Calcio',10,3,2,5,11,13,11),(14,'Benevento Calcio',10,3,2,5,12,21,11),(15,'Spezia Calcio',10,2,4,4,14,19,10),(16,'Parma Calcio 1913',10,2,4,4,10,17,10),(17,'ACF Fiorentina',10,2,3,5,11,16,9),(18,'Torino FC',10,1,3,6,17,24,6),(19,'Genoa CFC',10,1,3,6,9,19,6),(20,'FC Crotone',10,0,2,8,6,24,2)],
11: [(1,'AC Milan',11,8,3,0,25,11,27),(2,'Inter',11,7,3,1,29,15,24),(3,'SSC Napoli',11,8,0,3,27,10,24),(4,'Juventus',11,6,5,0,22,10,23),(5,'US Sassuolo',11,6,4,1,21,12,22),(6,'AS Roma',11,6,3,2,24,16,21),(7,'Hellas Verona',11,5,4,2,15,9,19),(8,'Atalanta',11,5,3,3,22,17,18),(9,'Lazio Roma',11,5,2,4,17,19,17),(10,'Udinese Calcio',11,4,2,5,14,15,14),(11,'Cagliari Calcio',11,3,3,5,18,23,12),(12,'Bologna FC',11,4,0,7,16,22,12),(13,'Sampdoria',11,3,2,6,16,19,11),(14,'Parma Calcio 1913',11,2,5,4,12,19,11),(15,'Benevento Calcio',11,3,2,6,12,22,11),(16,'Spezia Calcio',11,2,4,5,15,23,10),(17,'ACF Fiorentina',11,2,3,6,11,19,9),(18,'Torino FC',11,1,3,7,19,27,6),(19,'Genoa CFC',11,1,3,7,10,22,6),(20,'FC Crotone',11,1,2,8,10,25,5)],
12: [(1,'AC Milan',12,8,4,0,27,13,28),(2,'Inter',12,8,3,1,30,15,27),(3,'Juventus',12,6,6,0,23,11,24),(4,'AS Roma',12,7,3,2,27,17,24),(5,'SSC Napoli',12,8,0,4,27,11,24),(6,'US Sassuolo',12,6,5,1,22,13,23),(7,'Atalanta',12,5,4,3,23,18,19),(8,'Hellas Verona',12,5,4,3,16,11,19),(9,'Lazio Roma',12,5,3,4,18,20,18),(10,'Udinese Calcio',12,4,3,5,14,15,15),(11,'Sampdoria',12,4,2,6,18,20,14),(12,'Cagliari Calcio',12,3,4,5,18,23,13),(13,'Bologna FC',12,4,1,7,18,24,13),(14,'Parma Calcio 1913',12,2,6,4,12,19,12),(15,'Benevento Calcio',12,3,3,6,13,23,12),(16,'Spezia Calcio',12,2,5,5,17,25,11),(17,'ACF Fiorentina',12,2,4,6,12,20,10),(18,'Genoa CFC',12,1,4,7,12,24,7),(19,'Torino FC',12,1,3,8,20,30,6),(20,'FC Crotone',12,1,3,8,10,25,6)],
13: [(1,'AC Milan',13,9,4,0,29,14,31),(2,'Inter',13,9,3,1,32,16,30),(3,'Juventus',13,7,6,0,27,11,27),(4,'AS Roma',13,7,3,3,28,21,24),(5,'SSC Napoli',13,8,0,5,27,13,24),(6,'US Sassuolo',13,6,5,2,23,15,23),(7,'Atalanta',13,6,4,3,27,19,22),(8,'Lazio Roma',13,6,3,4,20,20,21),(9,'Hellas Verona',13,5,5,3,17,12,20),(10,'Sampdoria',13,5,2,6,21,21,17),(11,'Udinese Calcio',13,4,4,5,15,16,16),(12,'Benevento Calcio',13,4,3,6,15,23,15),(13,'Cagliari Calcio',13,3,5,5,19,24,14),(14,'Bologna FC',13,4,2,7,19,25,14),(15,'Parma Calcio 1913',13,2,6,5,12,23,12),(16,'ACF Fiorentina',13,2,5,6,13,21,11),(17,'Spezia Calcio',13,2,5,6,18,27,11),(18,'Torino FC',13,1,4,8,21,31,7),(19,'Genoa CFC',13,1,4,8,12,26,7),(20,'FC Crotone',13,1,3,9,11,28,6)],
14: [(1,'AC Milan',14,10,4,0,32,16,34),(2,'Inter',14,10,3,1,34,17,33),(3,'Juventus',14,7,6,1,27,14,27),(4,'AS Roma',14,8,3,3,31,23,27),(5,'US Sassuolo',14,7,5,2,26,17,26),(6,'SSC Napoli',14,8,1,5,28,14,25),(7,'Atalanta',14,6,5,3,29,21,23),(8,'Lazio Roma',14,6,3,5,22,23,21),(9,'Hellas Verona',14,5,5,4,18,14,20),(10,'Benevento Calcio',14,5,3,6,17,23,18),(11,'Sampdoria',14,5,2,7,23,24,17),(12,'Udinese Calcio',14,4,4,6,15,18,16),(13,'Bologna FC',14,4,3,7,21,27,15),(14,'ACF Fiorentina',14,3,5,6,16,21,14),(15,'Cagliari Calcio',14,3,5,6,21,27,14),(16,'Parma Calcio 1913',14,2,6,6,13,25,12),(17,'Spezia Calcio',14,2,5,7,19,29,11),(18,'Genoa CFC',14,2,4,8,14,27,10),(19,'FC Crotone',14,2,3,9,13,29,9),(20,'Torino FC',14,1,5,8,22,32,8)],
15: [(1,'AC Milan',15,11,4,0,34,16,37),(2,'Inter',15,11,3,1,40,19,36),(3,'Juventus',15,8,6,1,31,15,30),(4,'AS Roma',15,9,3,3,32,23,30),(5,'SSC Napoli',15,9,1,5,32,15,28),(6,'Atalanta',15,7,5,3,34,22,26),(7,'US Sassuolo',15,7,5,3,27,22,26),(8,'Hellas Verona',15,6,5,4,19,14,23),(9,'Lazio Roma',15,6,4,5,23,24,22),(10,'Benevento Calcio',15,5,3,7,17,25,18),(11,'Sampdoria',15,5,2,8,23,25,17),(12,'Bologna FC',15,4,4,7,21,27,16),(13,'Udinese Calcio',15,4,4,7,16,22,16),(14,'ACF Fiorentina',15,3,6,6,16,21,15),(15,'Cagliari Calcio',15,3,5,7,22,31,14),(16,'Parma Calcio 1913',15,2,6,7,13,28,12),(17,'Torino FC',15,2,5,8,25,32,11),(18,'Spezia Calcio',15,2,5,8,19,30,11),(19,'Genoa CFC',15,2,5,8,15,28,11),(20,'FC Crotone',15,2,3,10,15,35,9)],
16: [(1,'AC Milan',16,11,4,1,35,19,37),(2,'Inter',16,11,3,2,41,21,36),(3,'Juventus',16,9,6,1,34,16,33),(4,'AS Roma',16,10,3,3,35,24,33),(5,'Atalanta',16,8,5,3,37,22,29),(6,'US Sassuolo',16,8,5,3,29,23,29),(7,'SSC Napoli',16,9,1,6,33,17,28),(8,'Lazio Roma',16,7,4,5,25,25,25),(9,'Hellas Verona',16,6,6,4,20,15,24),(10,'Benevento Calcio',16,6,3,7,19,26,21),(11,'Sampdoria',16,6,2,8,25,26,20),(12,'Bologna FC',16,4,5,7,23,29,17),(13,'Udinese Calcio',16,4,5,7,18,24,17),(14,'ACF Fiorentina',16,3,6,7,17,23,15),(15,'Cagliari Calcio',16,3,5,8,23,33,14),(16,'Spezia Calcio',16,3,5,8,21,31,14),(17,'Torino FC',16,2,6,8,26,33,12),(18,'Parma Calcio 1913',16,2,6,8,13,31,12),(19,'Genoa CFC',16,2,5,9,16,30,11),(20,'FC Crotone',16,2,3,11,16,38,9)],
17: [(1,'AC Milan',17,12,4,1,37,19,40),(2,'Inter',17,11,4,2,43,23,37),(3,'Juventus',17,10,6,1,37,17,36),(4,'AS Roma',17,10,4,3,37,26,34),(5,'Atalanta',17,9,5,3,41,23,32),(6,'SSC Napoli',17,10,1,6,35,18,31),(7,'US Sassuolo',17,8,5,4,30,26,29),(8,'Lazio Roma',17,8,4,5,27,25,28),(9,'Hellas Verona',17,7,6,4,22,16,27),(10,'Benevento Calcio',17,6,3,8,20,30,21),(11,'Sampdoria',17,6,2,9,26,28,20),(12,'ACF Fiorentina',17,4,6,7,18,23,18),(13,'Udinese Calcio',17,4,5,8,19,26,17),(14,'Bologna FC',17,4,5,8,23,31,17),(15,'Spezia Calcio',17,4,5,8,23,32,17),(16,'Cagliari Calcio',17,3,5,9,23,34,14),(17,'Genoa CFC',17,3,5,9,18,30,14),(18,'Torino FC',17,2,6,9,26,35,12),(19,'Parma Calcio 1913',17,2,6,9,13,33,12),(20,'FC Crotone',17,2,3,12,17,40,9)],
18: [(1,'AC Milan',18,13,4,1,39,19,43),(2,'Inter',18,12,4,2,45,23,40),(3,'Juventus',18,10,6,2,37,19,36),(4,'AS Roma',18,10,4,4,37,29,34),(5,'SSC Napoli',18,11,1,6,41,18,34),(6,'Atalanta',18,9,6,3,41,23,33),(7,'Lazio Roma',18,9,4,5,30,25,31),(8,'US Sassuolo',18,8,6,4,31,27,30),(9,'Hellas Verona',18,7,6,5,22,17,27),(10,'Sampdoria',18,7,2,9,28,29,23),(11,'Benevento Calcio',18,6,3,9,21,34,21),(12,'Bologna FC',18,5,5,8,24,31,20),(13,'Spezia Calcio',18,4,6,8,23,32,18),(14,'ACF Fiorentina',18,4,6,8,18,29,18),(15,'Udinese Calcio',18,4,5,9,20,28,17),(16,'Genoa CFC',18,3,6,9,18,30,15),(17,'Cagliari Calcio',18,3,5,10,23,36,14),(18,'Torino FC',18,2,7,9,26,35,13),(19,'Parma Calcio 1913',18,2,7,9,14,34,13),(20,'FC Crotone',18,3,3,12,21,41,12)],
19: [(1,'AC Milan',19,13,4,2,39,22,43),(2,'Inter',19,12,5,2,45,23,41),(3,'Juventus',19,11,6,2,39,19,39),(4,'AS Roma',19,11,4,4,41,32,37),(5,'Atalanta',19,10,6,3,44,23,36),(6,'Lazio Roma',19,10,4,5,32,26,34),(7,'SSC Napoli',19,11,1,7,42,21,34),(8,'Hellas Verona',19,8,6,5,25,18,30),(9,'US Sassuolo',19,8,6,5,32,29,30),(10,'Sampdoria',19,8,2,9,30,29,26),(11,'Benevento Calcio',19,6,4,9,23,36,22),(12,'ACF Fiorentina',19,5,6,8,20,30,21),(13,'Bologna FC',19,5,5,9,24,33,20),(14,'Udinese Calcio',19,4,6,9,20,28,18),(15,'Spezia Calcio',19,4,6,9,26,36,18),(16,'Genoa CFC',19,4,6,9,19,30,18),(17,'Torino FC',19,2,8,9,28,37,14),(18,'Cagliari Calcio',19,3,5,11,23,37,14),(19,'Parma Calcio 1913',19,2,7,10,14,36,13),(20,'FC Crotone',19,3,3,13,22,43,12)],
}

ZERO = {'position': 0, 'played': 0, 'won': 0, 'drawn': 0, 'lost': 0,
        'goals_for': 0, 'goals_against': 0, 'goal_diff': 0, 'points': 0}

VERONA_ROMA_NOTE = ('R1 table reflects official 3-0 administrative award to Verona '
                    '(on-field 0-0, 2020-09-19); fixtures file records 3-0.')

def snap(round_after, wf_name):
    if round_after == 0:
        return dict(ZERO), None
    for (pos, name, p, w, d, l, gf, ga, pts) in TABLES[round_after]:
        if name == wf_name:
            s = {'position': pos, 'played': p, 'won': w, 'drawn': d,
                 'lost': l, 'goals_for': gf, 'goals_against': ga,
                 'goal_diff': gf - ga, 'points': pts}
            note = VERONA_ROMA_NOTE if NAME_MAP[name] in ('Verona', 'Roma') else None
            return s, note
    raise ValueError(f'team {wf_name} not in round {round_after} table')

def main():
    rows = json.load(open(BASE + '/req-20261007-001-rounds.json'))
    fixtures = [r for r in rows if r['season'] == '2020/21']
    assert len(fixtures) == 190, len(fixtures)
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds')
    out, unmapped = [], []
    for f in fixtures:
        rnd = f['official_round_first_cycle']
        for side, key in (('home', 'first_fixture_home'), ('away', 'first_fixture_away')):
            team = f[key]
            wf = next((w for w, m in NAME_MAP.items() if m == team), None)
            if wf is None:
                unmapped.append(team)
                continue
            s, note = snap(rnd - 1, wf)
            out.append({
                'fixture_key': f['first_fixture_key'],
                'season': '2020/21',
                'official_round_first_cycle': rnd,
                'fixture_date_iso': f['first_fixture_date_iso'],
                'side': side,
                'team': team,
                'pre_match': s,
                'field_semantics': 'explicit_round_table' if rnd > 1 else 'zeros_round1',
                'source_url': URL_TMPL.format(rnd - 1) if rnd > 1 else None,
                'source_tier': 'secondary_explicit',
                'table_semantics': ('nominal_round: postponed matches counted in original round '
                                    '(e.g. Juve-Napoli replay 2021-04-07 counted in R3; '
                                    'Genoa-Torino 2020-11-04 counted in R3)') if rnd > 1 else None,
                'notes': note,
                'retrieved_at': now,
            })
    assert not unmapped, unmapped
    assert len(out) == 380, len(out)
    r1 = [o for o in out if o['official_round_first_cycle'] == 1]
    assert len(r1) == 20 and all(o['pre_match']['played'] == 0 for o in r1)
    # R19 pre-match == table after R18: Milan 43 pts top
    r19m = [o for o in out if o['official_round_first_cycle'] == 19 and o['team'] == 'Milan']
    assert len(r19m) == 1 and r19m[0]['pre_match']['points'] == 43, r19m
    # Juve pre-R4 == table after R3: 7 pts (includes replayed 2-1 Napoli win counted in R3)
    r4j = [o for o in out if o['official_round_first_cycle'] == 4 and o['team'] == 'Juventus']
    assert len(r4j) == 1 and r4j[0]['pre_match']['points'] == 7, r4j
    json.dump(out, open(BASE + '/standings-2020-2021.json', 'w'), ensure_ascii=False, indent=1)
    print('wrote', len(out), 'snapshots')

if __name__ == '__main__':
    main()
