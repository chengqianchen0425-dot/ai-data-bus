#!/usr/bin/env python3
"""Build 2019/20 pre-match standings snapshots from worldfootball round tables (live browser).

Replaces the earlier derived version (derived_from_complete_verified_results, actual-date
ordering) with explicit nominal-round tables. Semantics: pre-match snapshot for official
round N = worldfootball table after rounds 1..N-1, postponed matches counted in their
nominal original round (site convention, consistent with 001 official rounds).
"""
import json, datetime

BASE = '/home/hatch/workspace/ai-inbox/repo/work-req-20261007-001'
URL_TMPL = 'https://www.worldfootball.net/competition/co111/italy-serie-a/se31821/2019-2020/ro100927/matchday/md{}/results-and-standings/'

NAME_MAP = {
    'Inter': 'Inter', 'Lazio Roma': 'Lazio', 'SSC Napoli': 'Napoli',
    'Atalanta': 'Atalanta', 'Torino FC': 'Torino', 'Brescia Calcio': 'Brescia',
    'Juventus': 'Juventus', 'Udinese Calcio': 'Udinese', 'AS Roma': 'Roma',
    'Genoa CFC': 'Genoa', 'Bologna FC': 'Bologna', 'Hellas Verona': 'Verona',
    'SPAL 2013 Ferrara': 'Spal', 'US Sassuolo': 'Sassuolo', 'AC Milan': 'Milan',
    'Sampdoria': 'Sampdoria', 'US Lecce': 'Lecce', 'ACF Fiorentina': 'Fiorentina',
    'Parma Calcio 1913': 'Parma', 'Cagliari Calcio': 'Cagliari',
}

# (pos, wf_name, P, W, D, L, GF, GA, Pts) per round, as displayed on worldfootball round page
TABLES = {
1: [(1,'Inter',1,1,0,0,4,0,3),(2,'Lazio Roma',1,1,0,0,3,0,3),(3,'SSC Napoli',1,1,0,0,4,3,3),(4,'Atalanta',1,1,0,0,3,2,3),(5,'Torino FC',1,1,0,0,2,1,3),(6,'Brescia Calcio',1,1,0,0,1,0,3),(7,'Juventus',1,1,0,0,1,0,3),(8,'Udinese Calcio',1,1,0,0,1,0,3),(9,'AS Roma',1,0,1,0,3,3,1),(10,'Genoa CFC',1,0,1,0,3,3,1),(11,'Bologna FC',1,0,1,0,1,1,1),(12,'Hellas Verona',1,0,1,0,1,1,1),(13,'SPAL 2013 Ferrara',1,0,0,1,2,3,0),(14,'US Sassuolo',1,0,0,1,1,2,0),(15,'AC Milan',1,0,0,1,0,1,0),(16,'Sampdoria',1,0,0,1,0,3,0),(17,'US Lecce',1,0,0,1,0,4,0),(18,'ACF Fiorentina',1,0,0,1,3,4,0),(19,'Parma Calcio 1913',1,0,0,1,0,1,0),(20,'Cagliari Calcio',1,0,0,1,0,1,0)],
2: [(1,'Inter',2,2,0,0,6,1,6),(2,'Juventus',2,2,0,0,5,3,6),(3,'Torino FC',2,2,0,0,5,3,6),(4,'Lazio Roma',2,1,1,0,4,1,4),(5,'Genoa CFC',2,1,1,0,5,4,4),(6,'Bologna FC',2,1,1,0,2,1,4),(7,'Hellas Verona',2,1,1,0,2,1,4),(8,'US Sassuolo',2,1,0,1,5,3,3),(9,'SSC Napoli',2,1,0,1,7,7,3),(10,'Atalanta',2,1,0,1,5,5,3),(11,'AC Milan',2,1,0,1,1,1,3),(12,'Brescia Calcio',2,1,0,1,1,1,3),(13,'Parma Calcio 1913',2,1,0,1,3,2,3),(14,'Udinese Calcio',2,1,0,1,2,3,3),(15,'AS Roma',2,0,2,0,4,4,2),(16,'SPAL 2013 Ferrara',2,0,0,2,2,4,0),(17,'US Lecce',2,0,0,2,0,5,0),(18,'Sampdoria',2,0,0,2,1,7,0),(19,'ACF Fiorentina',2,0,0,2,4,6,0),(20,'Cagliari Calcio',2,0,0,2,1,3,0)],
3: [(1,'Inter',3,3,0,0,7,1,9),(2,'Bologna FC',3,2,1,0,6,4,7),(3,'Juventus',3,2,1,0,5,3,7),(4,'SSC Napoli',3,2,0,1,9,7,6),(5,'Atalanta',3,2,0,1,7,6,6),(6,'Torino FC',3,2,0,1,6,5,6),(7,'AC Milan',3,2,0,1,2,1,6),(8,'AS Roma',3,1,2,0,8,6,5),(9,'Lazio Roma',3,1,1,1,5,3,4),(10,'Genoa CFC',3,1,1,1,6,6,4),(11,'Hellas Verona',3,1,1,1,2,2,4),(12,'US Sassuolo',3,1,0,2,7,7,3),(13,'Brescia Calcio',3,1,0,2,4,5,3),(14,'SPAL 2013 Ferrara',3,1,0,2,4,5,3),(15,'US Lecce',3,1,0,2,2,6,3),(16,'Parma Calcio 1913',3,1,0,2,4,5,3),(17,'Udinese Calcio',3,1,0,2,2,4,3),(18,'Cagliari Calcio',3,1,0,2,4,4,3),(19,'ACF Fiorentina',3,0,1,2,4,6,1),(20,'Sampdoria',3,0,0,3,1,9,0)],
4: [(1,'Inter',4,4,0,0,9,1,12),(2,'Juventus',4,3,1,0,7,4,10),(3,'SSC Napoli',4,3,0,1,13,8,9),(4,'AS Roma',4,2,2,0,10,7,8),(5,'Lazio Roma',4,2,1,1,7,3,7),(6,'Atalanta',4,2,1,1,9,8,7),(7,'Bologna FC',4,2,1,1,7,6,7),(8,'US Sassuolo',4,2,0,2,10,7,6),(9,'Torino FC',4,2,0,2,6,6,6),(10,'Brescia Calcio',4,2,0,2,5,5,6),(11,'AC Milan',4,2,0,2,2,3,6),(12,'Cagliari Calcio',4,2,0,2,7,5,6),(13,'Genoa CFC',4,1,1,2,7,9,4),(14,'Hellas Verona',4,1,1,2,3,4,4),(15,'SPAL 2013 Ferrara',4,1,0,3,4,8,3),(16,'US Lecce',4,1,0,3,3,10,3),(17,'Sampdoria',4,1,0,3,2,9,3),(18,'Parma Calcio 1913',4,1,0,3,4,7,3),(19,'Udinese Calcio',4,1,0,3,2,5,3),(20,'ACF Fiorentina',4,0,2,2,6,8,2)],
5: [(1,'Inter',5,5,0,0,10,1,15),(2,'Juventus',5,4,1,0,9,5,13),(3,'Atalanta',5,3,1,1,11,8,10),(4,'SSC Napoli',5,3,0,2,13,9,9),(5,'Torino FC',5,3,0,2,8,7,9),(6,'Cagliari Calcio',5,3,0,2,8,5,9),(7,'AS Roma',5,2,2,1,10,9,8),(8,'Bologna FC',5,2,2,1,7,6,8),(9,'Lazio Roma',5,2,1,2,7,4,7),(10,'US Sassuolo',5,2,0,3,10,8,6),(11,'Brescia Calcio',5,2,0,3,6,7,6),(12,'AC Milan',5,2,0,3,3,5,6),(13,'US Lecce',5,2,0,3,6,11,6),(14,'Parma Calcio 1913',5,2,0,3,5,7,6),(15,'Genoa CFC',5,1,2,2,7,9,5),(16,'Hellas Verona',5,1,2,2,3,4,5),(17,'ACF Fiorentina',5,1,2,2,8,9,5),(18,'Udinese Calcio',5,1,1,3,2,5,4),(19,'SPAL 2013 Ferrara',5,1,0,4,5,11,3),(20,'Sampdoria',5,1,0,4,3,11,3)],
6: [(1,'Inter',6,6,0,0,13,2,18),(2,'Juventus',6,5,1,0,11,5,16),(3,'Atalanta',6,4,1,1,15,9,13),(4,'SSC Napoli',6,4,0,2,15,10,12),(5,'AS Roma',6,3,2,1,11,9,11),(6,'Lazio Roma',6,3,1,2,11,4,10),(7,'Cagliari Calcio',6,3,1,2,9,6,10),(8,'Torino FC',6,3,0,3,10,10,9),(9,'Parma Calcio 1913',6,3,0,3,8,9,9),(10,'Bologna FC',6,2,2,2,7,7,8),(11,'ACF Fiorentina',6,2,2,2,11,10,8),(12,'Udinese Calcio',6,2,1,3,3,5,7),(13,'US Sassuolo',6,2,0,4,11,12,6),(14,'Brescia Calcio',6,2,0,4,7,9,6),(15,'AC Milan',6,2,0,4,4,8,6),(16,'US Lecce',6,2,0,4,6,12,6),(17,'Hellas Verona',6,1,3,2,4,5,6),(18,'Genoa CFC',6,1,2,3,7,13,5),(19,'SPAL 2013 Ferrara',6,1,0,5,5,13,3),(20,'Sampdoria',6,1,0,5,4,14,3)],
7: [(1,'Juventus',7,6,1,0,13,6,19),(2,'Inter',7,6,0,1,14,4,18),(3,'Atalanta',7,5,1,1,18,10,16),(4,'SSC Napoli',7,4,1,2,15,10,13),(5,'AS Roma',7,3,3,1,12,10,12),(6,'Lazio Roma',7,3,2,2,13,6,11),(7,'ACF Fiorentina',7,3,2,2,12,10,11),(8,'Cagliari Calcio',7,3,2,2,10,7,11),(9,'Torino FC',7,3,1,3,10,10,10),(10,'US Sassuolo',7,3,0,4,13,12,9),(11,'Bologna FC',7,2,3,2,9,9,9),(12,'AC Milan',7,3,0,4,6,9,9),(13,'Hellas Verona',7,2,3,2,6,5,9),(14,'Parma Calcio 1913',7,3,0,4,8,10,9),(15,'Udinese Calcio',7,2,1,4,3,6,7),(16,'Brescia Calcio',7,2,0,5,7,11,6),(17,'SPAL 2013 Ferrara',7,2,0,5,6,13,6),(18,'US Lecce',7,2,0,5,7,15,6),(19,'Genoa CFC',7,1,2,4,8,15,5),(20,'Sampdoria',7,1,0,6,4,16,3)],
8: [(1,'Juventus',8,7,1,0,15,7,22),(2,'Inter',8,7,0,1,18,7,21),(3,'Atalanta',8,5,2,1,21,13,17),(4,'SSC Napoli',8,5,1,2,17,10,16),(5,'Cagliari Calcio',8,4,2,2,12,7,14),(6,'AS Roma',8,3,4,1,12,10,13),(7,'Lazio Roma',8,3,3,2,16,9,12),(8,'ACF Fiorentina',8,3,3,2,12,10,12),(9,'Parma Calcio 1913',8,4,0,4,13,11,12),(10,'Torino FC',8,3,1,4,10,11,10),(11,'AC Milan',8,3,1,4,8,11,10),(12,'Udinese Calcio',8,3,1,4,4,6,10),(13,'US Sassuolo',8,3,0,5,16,16,9),(14,'Bologna FC',8,2,3,3,10,11,9),(15,'Hellas Verona',8,2,3,3,6,7,9),(16,'Brescia Calcio',8,2,1,5,7,11,7),(17,'US Lecce',8,2,1,5,9,17,7),(18,'SPAL 2013 Ferrara',8,2,0,6,6,15,6),(19,'Genoa CFC',8,1,2,5,9,20,5),(20,'Sampdoria',8,1,1,6,4,16,4)],
9: [(1,'Juventus',9,7,2,0,16,8,23),(2,'Inter',9,7,1,1,20,9,22),(3,'Atalanta',9,6,2,1,28,14,20),(4,'SSC Napoli',9,5,2,2,18,11,17),(5,'AS Roma',9,4,4,1,14,11,16),(6,'Lazio Roma',9,4,3,2,18,10,15),(7,'Cagliari Calcio',9,4,3,2,13,8,15),(8,'Parma Calcio 1913',9,4,1,4,15,13,13),(9,'US Sassuolo',9,4,0,5,17,16,12),(10,'Bologna FC',9,3,3,3,12,12,12),(11,'ACF Fiorentina',9,3,3,3,13,12,12),(12,'Torino FC',9,3,2,4,11,12,11),(13,'AC Milan',9,3,1,5,9,13,10),(14,'Udinese Calcio',9,3,1,5,5,13,10),(15,'Hellas Verona',9,2,3,4,6,8,9),(16,'US Lecce',9,2,2,5,10,18,8),(17,'Genoa CFC',9,2,2,5,12,21,8),(18,'Brescia Calcio',9,2,1,6,8,14,7),(19,'SPAL 2013 Ferrara',9,2,1,6,7,16,7),(20,'Sampdoria',9,1,1,7,5,18,4)],
10: [(1,'Juventus',10,8,2,0,18,9,26),(2,'Inter',10,8,1,1,22,10,25),(3,'Atalanta',10,6,3,1,30,16,21),(4,'AS Roma',10,5,4,1,18,11,19),(5,'Lazio Roma',10,5,3,2,22,10,18),(6,'SSC Napoli',10,5,3,2,20,13,18),(7,'Cagliari Calcio',10,5,3,2,16,10,18),(8,'ACF Fiorentina',10,4,3,3,15,13,15),(9,'AC Milan',10,4,1,5,10,13,13),(10,'Parma Calcio 1913',10,4,1,5,15,14,13),(11,'US Sassuolo',10,4,0,6,18,18,12),(12,'Bologna FC',10,3,3,4,14,15,12),(13,'Hellas Verona',10,3,3,4,7,8,12),(14,'Torino FC',10,3,2,5,11,16,11),(15,'Udinese Calcio',10,3,1,6,5,17,10),(16,'US Lecce',10,2,3,5,11,19,9),(17,'Genoa CFC',10,2,2,6,13,23,8),(18,'Brescia Calcio',10,2,1,7,9,16,7),(19,'SPAL 2013 Ferrara',10,2,1,7,7,17,7),(20,'Sampdoria',10,1,2,7,6,19,5)],
11: [(1,'Juventus',11,9,2,0,19,9,29),(2,'Inter',11,9,1,1,24,11,28),(3,'AS Roma',11,6,4,1,20,12,22),(4,'Lazio Roma',11,6,3,2,24,11,21),(5,'Atalanta',11,6,3,2,30,18,21),(6,'Cagliari Calcio',11,6,3,2,18,10,21),(7,'SSC Napoli',11,5,3,3,21,15,18),(8,'ACF Fiorentina',11,4,4,3,16,14,16),(9,'Hellas Verona',11,4,3,4,9,9,15),(10,'Parma Calcio 1913',11,4,2,5,16,15,14),(11,'US Sassuolo',11,4,1,6,20,20,13),(12,'AC Milan',11,4,1,6,11,15,13),(13,'Udinese Calcio',11,4,1,6,8,18,13),(14,'Bologna FC',11,3,3,5,15,17,12),(15,'Torino FC',11,3,2,6,11,17,11),(16,'US Lecce',11,2,4,5,13,21,10),(17,'Genoa CFC',11,2,2,7,14,26,8),(18,'Sampdoria',11,2,2,7,7,19,8),(19,'Brescia Calcio',11,2,1,8,10,18,7),(20,'SPAL 2013 Ferrara',11,2,1,8,7,18,7)],
12: [(1,'Juventus',12,10,2,0,20,9,32),(2,'Inter',12,10,1,1,26,12,31),(3,'Lazio Roma',12,7,3,2,28,13,24),(4,'Cagliari Calcio',12,7,3,2,23,12,24),(5,'Atalanta',12,6,4,2,30,18,22),(6,'AS Roma',12,6,4,2,20,14,22),(7,'SSC Napoli',12,5,4,3,21,15,19),(8,'Parma Calcio 1913',12,5,2,5,18,15,17),(9,'US Sassuolo',12,5,1,6,23,21,16),(10,'ACF Fiorentina',12,4,4,4,18,19,16),(11,'Hellas Verona',12,4,3,5,10,11,15),(12,'Torino FC',12,4,2,6,15,17,14),(13,'Udinese Calcio',12,4,2,6,8,18,14),(14,'AC Milan',12,4,1,7,11,16,13),(15,'Bologna FC',12,3,3,6,16,20,12),(16,'US Lecce',12,2,4,6,15,25,10),(17,'Genoa CFC',12,2,3,7,14,26,9),(18,'Sampdoria',12,2,3,7,7,19,9),(19,'SPAL 2013 Ferrara',12,2,2,8,7,18,8),(20,'Brescia Calcio',12,2,1,9,10,22,7)],
13: [(1,'Juventus',13,11,2,0,23,10,35),(2,'Inter',13,11,1,1,29,12,34),(3,'Lazio Roma',13,8,3,2,30,14,27),(4,'AS Roma',13,7,4,2,23,14,25),(5,'Cagliari Calcio',13,7,4,2,25,14,25),(6,'Atalanta',13,6,4,3,31,21,22),(7,'SSC Napoli',13,5,5,3,22,16,20),(8,'Hellas Verona',13,5,3,5,11,11,18),(9,'Parma Calcio 1913',13,5,3,5,20,17,18),(10,'US Sassuolo',13,5,1,7,24,23,16),(11,'ACF Fiorentina',13,4,4,5,18,20,16),(12,'Torino FC',13,4,2,7,15,20,14),(13,'AC Milan',13,4,2,7,12,17,14),(14,'Udinese Calcio',13,4,2,7,9,20,14),(15,'Bologna FC',13,3,4,6,18,22,13),(16,'Sampdoria',13,3,3,7,9,20,12),(17,'US Lecce',13,2,5,6,17,27,11),(18,'Genoa CFC',13,2,4,7,15,27,10),(19,'SPAL 2013 Ferrara',13,2,3,8,8,19,9),(20,'Brescia Calcio',13,2,1,10,10,25,7)],
14: [(1,'Inter',14,12,1,1,31,13,37),(2,'Juventus',14,11,3,0,25,12,36),(3,'Lazio Roma',14,9,3,2,33,14,30),(4,'AS Roma',14,8,4,2,26,15,28),(5,'Cagliari Calcio',14,8,4,2,29,17,28),(6,'Atalanta',14,7,4,3,34,21,25),(7,'SSC Napoli',14,5,5,4,23,18,20),(8,'Hellas Verona',14,5,3,6,12,14,18),(9,'Parma Calcio 1913',14,5,3,6,20,18,18),(10,'US Sassuolo',14,5,2,7,26,25,17),(11,'Torino FC',14,5,2,7,16,20,17),(12,'AC Milan',14,5,2,7,13,17,17),(13,'Bologna FC',14,4,4,6,20,23,16),(14,'ACF Fiorentina',14,4,4,6,18,21,16),(15,'US Lecce',14,3,5,6,18,27,14),(16,'Udinese Calcio',14,4,2,8,9,23,14),(17,'Sampdoria',14,3,3,8,12,24,12),(18,'Genoa CFC',14,2,4,8,15,28,10),(19,'SPAL 2013 Ferrara',14,2,3,9,9,21,9),(20,'Brescia Calcio',14,2,1,11,10,28,7)],
15: [(1,'Inter',15,12,2,1,31,13,38),(2,'Juventus',15,11,3,1,26,15,36),(3,'Lazio Roma',15,10,3,2,36,15,33),(4,'AS Roma',15,8,5,2,26,15,29),(5,'Cagliari Calcio',15,8,5,2,31,19,29),(6,'Atalanta',15,8,4,3,37,23,28),(7,'SSC Napoli',15,5,6,4,24,19,21),(8,'Parma Calcio 1913',15,6,3,6,21,18,21),(9,'Torino FC',15,6,2,7,18,21,20),(10,'AC Milan',15,6,2,7,16,19,20),(11,'US Sassuolo',15,5,3,7,28,27,18),(12,'Hellas Verona',15,5,3,7,14,17,18),(13,'Bologna FC',15,4,4,7,22,26,16),(14,'ACF Fiorentina',15,4,4,7,19,23,16),(15,'US Lecce',15,3,6,6,20,29,15),(16,'Udinese Calcio',15,4,3,8,10,24,15),(17,'Sampdoria',15,3,3,9,12,25,12),(18,'Genoa CFC',15,2,5,8,17,30,11),(19,'Brescia Calcio',15,3,1,11,11,28,10),(20,'SPAL 2013 Ferrara',15,2,3,10,9,22,9)],
16: [(1,'Inter',16,12,3,1,32,14,39),(2,'Juventus',16,12,3,1,29,16,39),(3,'Lazio Roma',16,11,3,2,38,16,36),(4,'AS Roma',16,9,5,2,29,16,32),(5,'Cagliari Calcio',16,8,5,3,32,21,29),(6,'Atalanta',16,8,4,4,38,25,28),(7,'Parma Calcio 1913',16,7,3,6,23,19,24),(8,'SSC Napoli',16,5,6,5,25,21,21),(9,'Torino FC',16,6,3,7,21,24,21),(10,'AC Milan',16,6,3,7,16,19,21),(11,'US Sassuolo',16,5,4,7,28,27,19),(12,'Bologna FC',16,5,4,7,24,27,19),(13,'Hellas Verona',16,5,4,7,17,20,19),(14,'ACF Fiorentina',16,4,5,7,20,24,17),(15,'US Lecce',16,3,6,7,20,32,15),(16,'Sampdoria',16,4,3,9,13,25,15),(17,'Udinese Calcio',16,4,3,9,11,27,15),(18,'Brescia Calcio',16,4,1,11,14,28,13),(19,'Genoa CFC',16,2,5,9,17,31,11),(20,'SPAL 2013 Ferrara',16,2,3,11,10,25,9)],
17: [(1,'Inter',17,13,3,1,36,14,42),(2,'Juventus',17,13,3,1,31,17,42),(3,'Lazio Roma',17,11,4,2,38,16,37),(4,'AS Roma',17,10,5,2,33,17,35),(5,'Atalanta',17,9,4,4,43,25,31),(6,'Cagliari Calcio',17,8,5,4,33,23,29),(7,'Parma Calcio 1913',17,7,4,6,24,20,25),(8,'SSC Napoli',17,6,6,5,27,22,24),(9,'Bologna FC',17,6,4,7,27,29,22),(10,'Torino FC',17,6,3,8,22,26,21),(11,'AC Milan',17,6,3,8,16,24,21),(12,'Hellas Verona',17,5,5,7,17,20,20),(13,'US Sassuolo',17,5,4,8,29,29,19),(14,'Udinese Calcio',17,5,3,9,13,28,18),(15,'ACF Fiorentina',17,4,5,8,21,28,17),(16,'US Lecce',17,3,6,8,22,35,15),(17,'Sampdoria',17,4,3,10,14,27,15),(18,'Brescia Calcio',17,4,2,11,15,29,14),(19,'SPAL 2013 Ferrara',17,3,3,11,12,26,12),(20,'Genoa CFC',17,2,5,10,17,35,11)],
18: [(1,'Inter',18,14,3,1,39,15,45),(2,'Juventus',18,14,3,1,35,17,45),(3,'Lazio Roma',18,12,4,2,40,17,40),(4,'AS Roma',18,10,5,3,33,19,35),(5,'Atalanta',18,10,4,4,48,25,34),(6,'Cagliari Calcio',18,8,5,5,33,27,29),(7,'Parma Calcio 1913',18,7,4,7,24,25,25),(8,'SSC Napoli',18,6,6,6,28,25,24),(9,'Torino FC',18,7,3,8,24,26,24),(10,'Bologna FC',18,6,5,7,28,30,23),(11,'Hellas Verona',18,6,5,7,19,20,23),(12,'AC Milan',18,6,4,8,16,24,22),(13,'Udinese Calcio',18,6,3,9,14,28,21),(14,'US Sassuolo',18,5,4,9,30,31,19),(15,'ACF Fiorentina',18,4,6,8,22,29,18),(16,'Sampdoria',18,4,4,10,14,27,16),(17,'US Lecce',18,3,6,9,22,36,15),(18,'Brescia Calcio',18,4,2,12,16,31,14),(19,'Genoa CFC',18,3,5,10,19,36,14),(20,'SPAL 2013 Ferrara',18,3,5,10,12,28,12)],
19: [(1,'Juventus',19,15,3,1,37,18,48),(2,'Inter',19,14,4,1,40,16,46),(3,'Lazio Roma',19,13,4,2,41,17,43),(4,'Atalanta',19,10,5,4,49,26,35),(5,'AS Roma',19,10,5,4,34,21,35),(6,'Cagliari Calcio',19,8,5,6,33,29,29),(7,'Parma Calcio 1913',19,8,4,7,26,25,28),(8,'Torino FC',19,8,3,8,25,26,27),(9,'Hellas Verona',19,7,5,7,21,21,26),(10,'AC Milan',19,7,4,8,18,24,25),(11,'SSC Napoli',19,6,6,7,28,26,24),(12,'Udinese Calcio',19,7,3,9,17,28,24),(13,'Bologna FC',19,6,5,8,28,31,23),(14,'ACF Fiorentina',19,5,6,8,23,29,21),(15,'US Sassuolo',19,5,4,10,30,34,19),(16,'Sampdoria',19,5,4,10,19,28,19),(17,'US Lecce',19,3,6,10,22,38,15),(18,'Genoa CFC',19,3,5,11,20,38,14),(19,'Brescia Calcio',19,4,2,13,17,36,14),(20,'SPAL 2013 Ferrara',19,3,3,13,12,29,12)],
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
    fixtures = [r for r in rows if r['season'] == '2019/20']
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
            out.append({
                'fixture_key': f['first_fixture_key'],
                'season': '2019/20',
                'official_round_first_cycle': rnd,
                'fixture_date_iso': f['first_fixture_date_iso'],
                'side': side,
                'team': team,
                'pre_match': snap(rnd - 1, wf),
                'field_semantics': 'explicit_round_table' if rnd > 1 else 'zeros_round1',
                'source_url': URL_TMPL.format(rnd - 1) if rnd > 1 else None,
                'source_tier': 'secondary_explicit',
                'table_semantics': ('nominal_round: postponed matches counted in original round '
                                    '(site convention)') if rnd > 1 else None,
                'retrieved_at': now,
            })
    assert not unmapped, unmapped
    assert len(out) == 380, len(out)
    r1 = [o for o in out if o['official_round_first_cycle'] == 1]
    assert len(r1) == 20 and all(o['pre_match']['played'] == 0 for o in r1)
    # cross-check: pre-R19 = table after R18: Juventus 45 (2nd), Lazio 40
    r19j = [o for o in out if o['official_round_first_cycle'] == 19 and o['team'] == 'Juventus']
    assert len(r19j) == 1 and r19j[0]['pre_match']['points'] == 45, r19j
    r19l = [o for o in out if o['official_round_first_cycle'] == 19 and o['team'] == 'Lazio']
    assert len(r19l) == 1 and r19l[0]['pre_match']['points'] == 40, r19l
    json.dump(out, open(BASE + '/standings-2019-2020.json', 'w'), ensure_ascii=False, indent=1)
    print('wrote', len(out), 'snapshots (explicit, replaced derived version)')

if __name__ == '__main__':
    main()
