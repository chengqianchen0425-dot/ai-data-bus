#!/usr/bin/env python3
"""Build 2018/19 pre-match standings snapshots from worldfootball round tables (live browser)."""
import json, datetime

BASE = '/home/hatch/workspace/ai-inbox/repo/work-req-20261007-001'
URL_TMPL = 'https://www.worldfootball.net/competition/co111/italy-serie-a/se28594/2018-2019/ro92446/matchday/md{}/results-and-standings/'

NAME_MAP = {
    'Atalanta': 'Atalanta', 'Empoli FC': 'Empoli', 'Juventus': 'Juventus',
    'AC Milan': 'Milan', 'SSC Napoli': 'Napoli', 'AS Roma': 'Roma',
    'SPAL 2013 Ferrara': 'Spal', 'US Sassuolo': 'Sassuolo',
    'Udinese Calcio': 'Udinese', 'Sampdoria': 'Sampdoria',
    'Parma Calcio 1913': 'Parma', 'ACF Fiorentina': 'Fiorentina',
    'Genoa CFC': 'Genoa', 'Lazio Roma': 'Lazio', 'Bologna FC': 'Bologna',
    'Inter': 'Inter', 'Torino FC': 'Torino', 'Frosinone Calcio': 'Frosinone',
    'Cagliari Calcio': 'Cagliari', 'Chievo Verona': 'Chievo',
}

# (pos, wf_name, P, W, D, L, GF, GA, Pts) per round, as displayed on worldfootball round page
TABLES = {
1: [(1,'Atalanta',1,1,0,0,4,0,3),(2,'Empoli FC',1,1,0,0,2,0,3),(3,'Juventus',1,1,0,0,3,2,3),(4,'AC Milan',1,1,0,0,2,1,3),(4,'SSC Napoli',1,1,0,0,2,1,3),(6,'AS Roma',1,1,0,0,1,0,3),(6,'SPAL 2013 Ferrara',1,1,0,0,1,0,3),(6,'US Sassuolo',1,1,0,0,1,0,3),(9,'Udinese Calcio',1,0,1,0,2,2,1),(10,'Sampdoria',1,0,1,0,1,1,1),(11,'Parma Calcio 1913',1,0,1,0,2,2,1),(12,'ACF Fiorentina',1,0,1,0,1,1,1),(13,'Genoa CFC',1,0,0,1,1,2,0),(13,'Lazio Roma',1,0,0,1,1,2,0),(15,'Bologna FC',1,0,0,1,0,1,0),(15,'Inter',1,0,0,1,0,1,0),(15,'Torino FC',1,0,0,1,0,1,0),(18,'Frosinone Calcio',1,0,0,1,0,4,0),(19,'Cagliari Calcio',1,0,0,1,0,2,0),(20,'Chievo Verona',1,0,0,1,2,3,-3)],
2: [(1,'Juventus',2,2,0,0,5,2,6),(2,'SSC Napoli',2,2,0,0,5,3,6),(3,'SPAL 2013 Ferrara',2,2,0,0,2,0,6),(4,'Atalanta',2,1,1,0,7,3,4),(5,'AS Roma',2,1,1,0,4,3,4),(6,'Udinese Calcio',2,1,1,0,3,2,4),(6,'US Sassuolo',2,1,1,0,3,2,4),(8,'ACF Fiorentina',2,1,1,0,7,2,4),(9,'Empoli FC',2,1,0,1,3,2,3),(10,'AC Milan',2,1,0,1,4,4,3),(11,'Genoa CFC',2,1,0,1,3,3,3),(12,'Inter',2,0,1,1,2,3,1),(12,'Torino FC',2,0,1,1,2,3,1),(14,'Sampdoria',2,0,1,1,1,2,1),(15,'Bologna FC',2,0,1,1,0,1,1),(16,'Frosinone Calcio',2,0,1,1,0,4,1),(17,'Parma Calcio 1913',2,0,1,1,2,3,1),(18,'Cagliari Calcio',2,0,1,1,2,4,1),(19,'Lazio Roma',2,0,0,2,1,4,0),(20,'Chievo Verona',2,0,0,2,3,9,-3)],
3: [(1,'Juventus',3,3,0,0,7,3,9),(2,'US Sassuolo',3,2,1,0,8,5,7),(3,'ACF Fiorentina',3,2,1,0,8,2,7),(4,'AC Milan',3,2,0,1,6,5,6),(5,'SPAL 2013 Ferrara',3,2,0,1,2,1,6),(6,'SSC Napoli',3,2,0,1,5,6,6),(7,'Atalanta',3,1,1,1,7,4,4),(8,'Inter',3,1,1,1,5,3,4),(9,'Sampdoria',3,1,1,1,4,2,4),(10,'Empoli FC',3,1,1,1,3,2,4),(11,'AS Roma',3,1,1,1,5,5,4),(12,'Torino FC',3,1,1,1,3,3,4),(12,'Udinese Calcio',3,1,1,1,3,3,4),(14,'Cagliari Calcio',3,1,1,1,3,4,4),(15,'Genoa CFC',3,1,0,2,6,8,3),(16,'Lazio Roma',3,1,0,2,2,4,3),(17,'Bologna FC',3,0,1,2,0,4,1),(18,'Frosinone Calcio',3,0,1,2,0,5,1),(19,'Parma Calcio 1913',3,0,1,2,3,5,1),(20,'Chievo Verona',3,0,1,2,3,9,-2)],
4: [(1,'Juventus',4,4,0,0,9,4,12),(2,'SPAL 2013 Ferrara',4,3,0,1,4,1,9),(3,'SSC Napoli',4,3,0,1,6,6,9),(4,'Sampdoria',4,2,1,1,9,2,7),(5,'US Sassuolo',4,2,1,1,9,7,7),(6,'AC Milan',4,2,1,1,7,6,7),(7,'ACF Fiorentina',4,2,1,1,8,3,7),(8,'Genoa CFC',4,2,0,2,7,8,6),(9,'Lazio Roma',4,2,0,2,3,4,6),(10,'AS Roma',4,1,2,1,7,7,5),(11,'Torino FC',4,1,2,1,4,4,5),(11,'Udinese Calcio',4,1,2,1,4,4,5),(13,'Cagliari Calcio',4,1,2,1,4,5,5),(14,'Atalanta',4,1,1,2,7,6,4),(15,'Inter',4,1,1,2,5,4,4),(16,'Empoli FC',4,1,1,2,3,3,4),(17,'Parma Calcio 1913',4,1,1,2,4,5,4),(18,'Bologna FC',4,0,1,3,0,5,1),(19,'Frosinone Calcio',4,0,1,3,0,10,1),(20,'Chievo Verona',4,0,2,2,5,11,-1)],
5: [(1,'Juventus',5,5,0,0,11,4,15),(2,'SSC Napoli',5,4,0,1,9,7,12),(3,'US Sassuolo',5,3,1,1,12,8,10),(4,'ACF Fiorentina',5,3,1,1,11,3,10),(5,'Lazio Roma',5,3,0,2,7,5,9),(6,'SPAL 2013 Ferrara',5,3,0,2,4,4,9),(7,'Udinese Calcio',5,2,2,1,6,4,8),(8,'AC Milan',5,2,2,1,9,8,8),(9,'Sampdoria',5,2,1,2,9,3,7),(10,'Inter',5,2,1,2,6,4,7),(11,'Parma Calcio 1913',5,2,1,2,6,5,7),(12,'Genoa CFC',5,2,0,3,8,12,6),(13,'Atalanta',5,1,2,2,9,8,5),(14,'AS Roma',5,1,2,2,7,9,5),(15,'Torino FC',5,1,2,2,5,7,5),(16,'Cagliari Calcio',5,1,2,2,4,7,5),(17,'Empoli FC',5,1,1,3,4,6,4),(18,'Bologna FC',5,1,1,3,2,5,4),(19,'Frosinone Calcio',5,0,1,4,0,12,1),(20,'Chievo Verona',5,0,2,3,5,13,-1)],
6: [(1,'Juventus',6,6,0,0,13,4,18),(2,'SSC Napoli',6,5,0,1,12,7,15),(3,'US Sassuolo',6,4,1,1,14,8,13),(4,'Lazio Roma',6,4,0,2,9,6,12),(5,'Inter',6,3,1,2,8,5,10),(6,'ACF Fiorentina',6,3,1,2,12,5,10),(7,'AC Milan',6,2,3,1,10,9,9),(8,'Genoa CFC',6,3,0,3,10,12,9),(9,'SPAL 2013 Ferrara',6,3,0,3,4,6,9),(10,'Sampdoria',6,2,2,2,9,3,8),(11,'AS Roma',6,2,2,2,11,9,8),(12,'Udinese Calcio',6,2,2,2,7,6,8),(13,'Parma Calcio 1913',6,2,1,3,6,8,7),(14,'Atalanta',6,1,3,2,9,8,6),(15,'Torino FC',6,1,3,2,5,7,6),(16,'Cagliari Calcio',6,1,3,2,4,7,6),(17,'Empoli FC',6,1,2,3,5,7,5),(18,'Bologna FC',6,1,1,4,2,7,4),(19,'Frosinone Calcio',6,0,1,5,0,16,1),(20,'Chievo Verona',6,0,2,4,5,15,-1)],
7: [(1,'Juventus',7,7,0,0,16,5,21),(2,'SSC Napoli',7,5,0,2,13,10,15),(3,'Inter',7,4,1,2,10,5,13),(4,'US Sassuolo',7,4,1,2,15,12,13),(5,'ACF Fiorentina',7,4,1,2,14,5,13),(6,'AC Milan',7,3,3,1,14,10,12),(7,'Lazio Roma',7,4,0,3,10,9,12),(8,'Genoa CFC',7,4,0,3,12,13,12),(9,'Sampdoria',7,3,2,2,11,4,11),(10,'AS Roma',7,3,2,2,14,10,11),(11,'Parma Calcio 1913',7,3,1,3,7,8,10),(12,'Torino FC',7,2,3,2,6,7,9),(13,'SPAL 2013 Ferrara',7,3,0,4,5,8,9),(14,'Udinese Calcio',7,2,2,3,8,8,8),(15,'Bologna FC',7,2,1,4,4,8,7),(16,'Atalanta',7,1,3,3,9,10,6),(17,'Cagliari Calcio',7,1,3,3,4,9,6),(18,'Empoli FC',7,1,2,4,5,8,5),(19,'Frosinone Calcio',7,0,1,6,1,18,1),(20,'Chievo Verona',7,0,2,5,5,16,-1)],
8: [(1,'Juventus',8,8,0,0,18,5,24),(2,'SSC Napoli',8,6,0,2,15,10,18),(3,'Inter',8,5,1,2,12,6,16),(4,'AC Milan',8,4,3,1,17,11,15),(5,'Lazio Roma',8,5,0,3,11,9,15),(6,'Sampdoria',8,4,2,2,12,4,14),(7,'AS Roma',8,4,2,2,16,10,14),(8,'US Sassuolo',8,4,1,3,15,14,13),(9,'Parma Calcio 1913',8,4,1,3,10,9,13),(10,'ACF Fiorentina',8,4,1,3,14,6,13),(11,'Torino FC',8,3,3,2,9,9,12),(12,'Genoa CFC',8,4,0,4,13,16,12),(13,'SPAL 2013 Ferrara',8,3,0,5,6,10,9),(14,'Cagliari Calcio',8,2,3,3,6,9,9),(15,'Udinese Calcio',8,2,2,4,8,10,8),(16,'Bologna FC',8,2,1,5,4,10,7),(17,'Atalanta',8,1,3,4,9,11,6),(18,'Empoli FC',8,1,2,5,5,10,5),(19,'Frosinone Calcio',8,0,1,7,3,21,1),(20,'Chievo Verona',8,0,2,6,6,19,-1)],
9: [(1,'Juventus',9,8,1,0,19,6,25),(2,'SSC Napoli',9,7,0,2,18,10,21),(3,'Inter',9,6,1,2,13,6,19),(4,'Lazio Roma',9,6,0,3,13,9,18),(5,'Sampdoria',9,4,3,2,12,4,15),(6,'AC Milan',9,4,3,2,17,12,15),(7,'AS Roma',9,4,2,3,16,12,14),(8,'US Sassuolo',9,4,2,3,15,14,14),(9,'ACF Fiorentina',9,4,2,3,15,7,14),(10,'Torino FC',9,3,4,2,11,11,13),(11,'Genoa CFC',9,4,1,4,14,17,13),(12,'Parma Calcio 1913',9,4,1,4,10,11,13),(13,'SPAL 2013 Ferrara',9,4,0,5,8,10,12),(14,'Cagliari Calcio',9,2,4,3,7,10,10),(15,'Atalanta',9,2,3,4,14,12,9),(16,'Udinese Calcio',9,2,2,5,8,13,8),(17,'Bologna FC',9,2,2,5,6,12,8),(18,'Empoli FC',9,1,3,5,8,13,6),(19,'Frosinone Calcio',9,0,2,7,6,24,2),(20,'Chievo Verona',9,0,2,7,7,24,-1)],
10: [(1,'Juventus',10,9,1,0,21,7,28),(2,'Inter',10,7,1,2,16,6,22),(3,'SSC Napoli',10,7,1,2,19,11,22),(4,'AC Milan',10,5,3,2,20,14,18),(5,'Lazio Roma',10,6,0,4,13,12,18),(6,'Sampdoria',10,4,3,3,14,7,15),(7,'AS Roma',10,4,3,3,17,13,15),(8,'US Sassuolo',10,4,3,3,17,16,15),(9,'ACF Fiorentina',10,4,3,3,16,8,15),(10,'Torino FC',10,3,5,2,12,12,14),(11,'Genoa CFC',10,4,2,4,16,19,14),(12,'Parma Calcio 1913',10,4,1,5,10,14,13),(13,'Cagliari Calcio',10,3,4,3,9,11,13),(14,'Atalanta',10,3,3,4,17,12,12),(15,'SPAL 2013 Ferrara',10,4,0,6,8,13,12),(16,'Udinese Calcio',10,2,3,5,10,15,9),(17,'Bologna FC',10,2,3,5,8,14,9),(18,'Empoli FC',10,1,3,6,9,15,6),(19,'Frosinone Calcio',10,1,2,7,9,24,5),(20,'Chievo Verona',10,0,2,8,8,26,-1)],
11: [(1,'Juventus',11,10,1,0,24,8,31),(2,'Inter',11,8,1,2,21,6,25),(3,'SSC Napoli',11,8,1,2,24,12,25),(4,'AC Milan',11,6,3,2,21,14,21),(5,'Lazio Roma',11,7,0,4,17,13,21),(6,'US Sassuolo',11,5,3,3,19,16,18),(7,'Torino FC',11,4,5,2,16,13,17),(8,'AS Roma',11,4,4,3,18,14,16),(9,'ACF Fiorentina',11,4,4,3,17,9,16),(10,'Atalanta',11,4,3,4,19,13,15),(11,'Sampdoria',11,4,3,4,15,11,15),(12,'Genoa CFC',11,4,2,5,16,24,14),(13,'Parma Calcio 1913',11,4,2,5,10,14,14),(14,'Cagliari Calcio',11,3,4,4,10,14,13),(15,'SPAL 2013 Ferrara',11,4,0,7,9,17,12),(16,'Udinese Calcio',11,2,3,6,10,16,9),(17,'Bologna FC',11,2,3,6,9,16,9),(18,'Empoli FC',11,1,3,7,10,20,6),(19,'Frosinone Calcio',11,1,3,7,9,24,6),(20,'Chievo Verona',11,0,2,9,8,28,-1)],
12: [(1,'Juventus',12,11,1,0,26,8,34),(2,'SSC Napoli',12,9,1,2,26,13,28),(3,'Inter',12,8,1,3,22,10,25),(4,'Lazio Roma',12,7,1,4,18,14,22),(5,'AC Milan',12,6,3,3,21,16,21),(6,'AS Roma',12,5,4,3,22,15,19),(7,'US Sassuolo',12,5,4,3,20,17,19),(8,'Atalanta',12,5,3,4,23,14,18),(9,'Torino FC',12,4,5,3,17,15,17),(10,'Parma Calcio 1913',12,5,2,5,12,15,17),(11,'ACF Fiorentina',12,4,5,3,18,10,17),(12,'Sampdoria',12,4,3,5,16,15,15),(13,'Genoa CFC',12,4,2,6,17,26,14),(14,'Cagliari Calcio',12,3,5,4,12,16,14),(15,'SPAL 2013 Ferrara',12,4,1,7,11,19,13),(16,'Bologna FC',12,2,4,6,11,18,10),(17,'Udinese Calcio',12,2,3,7,11,18,9),(18,'Empoli FC',12,2,3,7,12,21,9),(19,'Frosinone Calcio',12,1,4,7,10,25,7),(20,'Chievo Verona',12,0,3,9,10,30,0)],
13: [(1,'Juventus',13,12,1,0,28,8,37),(2,'SSC Napoli',13,9,2,2,26,13,29),(3,'Inter',13,9,1,3,25,10,28),(4,'Lazio Roma',13,7,2,4,19,15,23),(5,'AC Milan',13,6,4,3,22,17,22),(6,'Parma Calcio 1913',13,6,2,5,14,16,20),(7,'AS Roma',13,5,4,4,22,16,19),(8,'US Sassuolo',13,5,4,4,21,19,19),(9,'Atalanta',13,5,3,5,25,17,18),(10,'Torino FC',13,4,6,3,17,15,18),(11,'ACF Fiorentina',13,4,6,3,18,10,18),(12,'Sampdoria',13,4,4,5,17,16,16),(13,'Genoa CFC',13,4,3,6,18,27,15),(14,'Cagliari Calcio',13,3,6,4,12,16,15),(15,'SPAL 2013 Ferrara',13,4,1,8,11,21,13),(16,'Udinese Calcio',13,3,3,7,12,18,12),(17,'Empoli FC',13,3,3,7,15,23,12),(18,'Bologna FC',13,2,5,6,11,18,11),(19,'Frosinone Calcio',13,1,4,8,10,28,7),(20,'Chievo Verona',13,0,4,9,10,30,1)],
14: [(1,'Juventus',14,13,1,0,31,8,40),(2,'SSC Napoli',14,10,2,2,28,14,32),(3,'Inter',14,9,2,3,27,12,29),(4,'AC Milan',14,7,4,3,24,18,25),(5,'Lazio Roma',14,7,3,4,20,16,24),(6,'Torino FC',14,5,6,3,19,16,21),(7,'AS Roma',14,5,5,4,24,18,20),(8,'US Sassuolo',14,5,5,4,21,19,20),(9,'Parma Calcio 1913',14,6,2,6,15,18,20),(10,'Sampdoria',14,5,4,5,21,17,19),(11,'Atalanta',14,5,3,6,26,19,18),(12,'ACF Fiorentina',14,4,6,4,18,13,18),(13,'Cagliari Calcio',14,3,7,4,13,17,16),(14,'Genoa CFC',14,4,3,7,19,29,15),(15,'SPAL 2013 Ferrara',14,4,2,8,13,23,14),(16,'Udinese Calcio',14,3,4,7,12,18,13),(17,'Empoli FC',14,3,4,7,17,25,13),(18,'Bologna FC',14,2,5,7,12,22,11),(19,'Frosinone Calcio',14,1,5,8,11,29,8),(20,'Chievo Verona',14,0,5,9,11,31,2)],
15: [(1,'Juventus',15,14,1,0,32,8,43),(2,'SSC Napoli',15,11,2,2,32,14,35),(3,'Inter',15,9,2,4,27,13,29),(4,'AC Milan',15,7,5,3,24,18,26),(5,'Lazio Roma',15,7,4,4,22,18,25),(6,'Torino FC',15,5,7,3,19,16,22),(7,'Atalanta',15,6,3,6,29,20,21),(8,'AS Roma',15,5,6,4,26,20,21),(9,'US Sassuolo',15,5,6,4,24,22,21),(10,'Parma Calcio 1913',15,6,3,6,16,19,21),(11,'Sampdoria',15,5,5,5,23,19,20),(12,'ACF Fiorentina',15,4,7,4,21,16,19),(13,'Cagliari Calcio',15,3,8,4,15,19,17),(14,'Empoli FC',15,4,4,7,19,26,16),(15,'Genoa CFC',15,4,4,7,20,30,16),(16,'SPAL 2013 Ferrara',15,4,3,8,14,24,15),(17,'Udinese Calcio',15,3,4,8,13,21,13),(18,'Bologna FC',15,2,5,8,13,24,11),(19,'Frosinone Calcio',15,1,5,9,11,33,8),(20,'Chievo Verona',15,0,6,9,12,32,3)],
16: [(1,'Juventus',16,15,1,0,33,8,46),(2,'SSC Napoli',16,12,2,2,33,14,38),(3,'Inter',16,10,2,4,28,13,32),(4,'AC Milan',16,7,6,3,24,18,27),(5,'Lazio Roma',16,7,4,5,22,19,25),(6,'Atalanta',16,7,3,6,30,20,24),(7,'AS Roma',16,6,6,4,29,22,24),(8,'US Sassuolo',16,6,6,4,26,22,24),(9,'Sampdoria',16,6,5,5,25,19,23),(10,'Torino FC',16,5,7,4,19,17,22),(11,'ACF Fiorentina',16,5,7,4,24,17,22),(12,'Parma Calcio 1913',16,6,3,7,16,21,21),(13,'Cagliari Calcio',16,3,8,5,15,20,17),(14,'Empoli FC',16,4,4,8,20,29,16),(15,'SPAL 2013 Ferrara',16,4,4,8,14,24,16),(16,'Genoa CFC',16,4,4,8,22,33,16),(17,'Udinese Calcio',16,3,4,9,13,22,13),(18,'Bologna FC',16,2,6,8,13,24,12),(19,'Frosinone Calcio',16,1,5,10,11,35,8),(20,'Chievo Verona',16,0,7,9,12,32,4)],
17: [(1,'Juventus',17,16,1,0,34,8,49),(2,'SSC Napoli',17,13,2,2,34,14,41),(3,'Inter',17,10,3,4,29,14,33),(4,'Lazio Roma',17,8,4,5,25,20,28),(5,'AC Milan',17,7,6,4,24,19,27),(6,'Sampdoria',17,7,5,5,29,21,26),(7,'US Sassuolo',17,6,7,4,27,23,25),(8,'ACF Fiorentina',17,6,7,4,25,17,25),(9,'Atalanta',17,7,3,7,31,23,24),(10,'AS Roma',17,6,6,5,29,23,24),(11,'Torino FC',17,5,8,4,20,18,23),(12,'Parma Calcio 1913',17,6,4,7,16,21,22),(13,'Genoa CFC',17,5,4,8,25,34,19),(14,'Cagliari Calcio',17,3,8,6,16,23,17),(15,'Empoli FC',17,4,4,9,22,33,16),(16,'SPAL 2013 Ferrara',17,4,4,9,14,25,16),(17,'Udinese Calcio',17,3,5,9,14,23,14),(18,'Bologna FC',17,2,7,8,13,24,13),(19,'Frosinone Calcio',17,1,6,10,12,36,9),(20,'Chievo Verona',17,0,8,9,13,33,5)],
18: [(1,'Juventus',18,16,2,0,36,10,50),(2,'SSC Napoli',18,13,2,3,34,15,41),(3,'Inter',18,11,3,4,30,14,36),(4,'Lazio Roma',18,9,4,5,27,20,31),(5,'Sampdoria',18,8,5,5,31,21,29),(6,'AC Milan',18,7,7,4,24,19,28),(7,'AS Roma',18,7,6,5,32,24,27),(8,'Torino FC',18,6,8,4,23,18,26),(9,'Atalanta',18,7,4,7,33,25,25),(10,'US Sassuolo',18,6,7,5,28,26,25),(11,'Parma Calcio 1913',18,7,4,7,17,21,25),(12,'ACF Fiorentina',18,6,7,5,25,18,25),(13,'Cagliari Calcio',18,4,8,6,17,23,20),(14,'Genoa CFC',18,5,4,9,25,35,19),(15,'SPAL 2013 Ferrara',18,4,5,9,14,25,17),(16,'Empoli FC',18,4,4,10,22,36,16),(17,'Udinese Calcio',18,3,6,9,14,23,15),(18,'Bologna FC',18,2,7,9,13,26,13),(19,'Frosinone Calcio',18,1,7,10,12,36,10),(20,'Chievo Verona',18,0,8,10,13,35,5)],
19: [(1,'Juventus',19,17,2,0,38,11,53),(2,'SSC Napoli',19,14,2,3,37,17,44),(3,'Inter',19,12,3,4,31,14,39),(4,'Lazio Roma',19,9,5,5,28,21,32),(5,'AC Milan',19,8,7,4,26,20,31),(6,'AS Roma',19,8,6,5,34,24,30),(7,'Sampdoria',19,8,5,6,32,23,29),(8,'Atalanta',19,8,4,7,39,27,28),(9,'Torino FC',19,6,9,4,24,19,27),(10,'ACF Fiorentina',19,6,8,5,25,18,26),(11,'US Sassuolo',19,6,7,6,30,32,25),(12,'Parma Calcio 1913',19,7,4,8,17,23,25),(13,'Genoa CFC',19,5,5,9,25,35,20),(14,'Cagliari Calcio',19,4,8,7,17,25,20),(15,'Udinese Calcio',19,4,6,9,16,23,18),(16,'SPAL 2013 Ferrara',19,4,5,10,15,27,17),(17,'Empoli FC',19,4,4,11,22,37,16),(18,'Bologna FC',19,2,7,10,15,29,13),(19,'Frosinone Calcio',19,1,7,11,12,37,10),(20,'Chievo Verona',19,1,8,10,14,35,8)],
}

ZERO = {'position': 0, 'played': 0, 'won': 0, 'drawn': 0, 'lost': 0,
        'goals_for': 0, 'goals_against': 0, 'goal_diff': 0, 'points': 0}

def snap(round_after, wf_name):
    if round_after == 0:
        return dict(ZERO)
    for (pos, name, p, w, d, l, gf, ga, pts) in TABLES[round_after]:
        if name == wf_name:
            return {'position': pos, 'played': p, 'won': w, 'drawn': d,
                    'lost': l, 'goals_for': gf, 'goals_against': ga,
                    'goal_diff': gf - ga, 'points': pts}
    raise ValueError(f'team {wf_name} not in round {round_after} table')

def main():
    rows = json.load(open(BASE + '/req-20261007-001-rounds.json'))
    fixtures = [r for r in rows if r['season'] == '2018/19']
    assert len(fixtures) == 190, len(fixtures)
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='seconds')
    out = []
    unmapped = []
    for f in fixtures:
        rnd = f['official_round_first_cycle']
        for side, key in (('home', 'first_fixture_home'), ('away', 'first_fixture_away')):
            team = f[key]
            wf = next((w for w, m in NAME_MAP.items() if m == team), None)
            if wf is None:
                unmapped.append(team)
                continue
            s = snap(rnd - 1, wf)
            out.append({
                'fixture_key': f['first_fixture_key'],
                'season': '2018/19',
                'official_round_first_cycle': rnd,
                'fixture_date_iso': f['first_fixture_date_iso'],
                'side': side,
                'team': team,
                'pre_match': s,
                'field_semantics': 'explicit_round_table' if rnd > 1 else 'zeros_round1',
                'source_url': URL_TMPL.format(rnd - 1) if rnd > 1 else None,
                'source_tier': 'secondary_explicit',
                'notes': 'Chievo points include -3pt deduction (worldfootball footnote)' if team == 'Chievo' and rnd > 1 else None,
                'retrieved_at': now,
            })
    assert not unmapped, unmapped
    assert len(out) == 380, len(out)
    # sanity: round-1 snapshots all zero
    r1 = [o for o in out if o['official_round_first_cycle'] == 1]
    assert len(r1) == 20 and all(o['pre_match']['played'] == 0 for o in r1)
    # sanity: round-19 pre-match == table after round 18 (Juventus 50 pts)
    r19j = [o for o in out if o['official_round_first_cycle'] == 19 and o['team'] == 'Juventus']
    assert len(r19j) == 1 and r19j[0]['pre_match']['points'] == 50, r19j
    json.dump(out, open(BASE + '/standings-2018-2019.json', 'w'), ensure_ascii=False, indent=1)
    print('wrote', len(out), 'snapshots')

if __name__ == '__main__':
    main()
