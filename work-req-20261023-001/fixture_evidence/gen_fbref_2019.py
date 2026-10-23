# Generator for FBref 2019 Copa Libertadores schedule transcription.
# Every row below was transcribed from the browser.open text layer of
# https://fbref.com/en/comps/14/2019/schedule/2019-Copa-Libertadores-Scores-and-Fixtures
# read 2026-10-23 (UTC+8). The Score column was dropped entirely.
# Tuple: (match_date, kickoff_local, home, away, venue, stage, wk, leg)
# leg: "first"/"second" only when Notes explicitly say Leg 1/2; else None.
URL = "https://fbref.com/en/comps/14/2019/schedule/2019-Copa-Libertadores-Scores-and-Fixtures"
RETRIEVED = "2026-10-23T21:26:14+08:00"
ROWS = [
 # First qualifying stage (6)
 ("2019-01-22", "18:30 (15:30)", "Delfín ec", "py Club Nacional", "Estadio Jocay", "First qualifying stage", None, "first"),
 ("2019-01-23", "19:30 (15:30)", "Bolívar bo", "uy Defensor", "Estadio Hernando Siles", "First qualifying stage", None, "first"),
 ("2019-01-23", "19:30 (15:30)", "Dep. La Guaira ve", "pe Real Garcilaso", "Estadio Nacional Brígido Iriarte", "First qualifying stage", None, "first"),
 ("2019-01-29", "18:30 (15:30)", "Real Garcilaso pe", "ve Dep. La Guaira", "Estadio Túpac Amaru", "First qualifying stage", None, "second"),
 ("2019-01-30", "18:15 (13:15)", "Club Nacional py", "ec Delfín", "Estadio Arsenio Erico", "First qualifying stage", None, "second"),
 ("2019-01-30", "20:30 (15:30)", "Defensor uy", "bo Bolívar", "Estadio Luis Franzini", "First qualifying stage", None, "second"),
 # Second qualifying stage (16)
 ("2019-02-05", "18:15 (13:15)", "Danubio uy", "br Atlético Mineiro", "Estadio Jardines del Hipódromo", "Second qualifying stage", None, "first"),
 ("2019-02-05", "18:30 (15:30)", "Melgar pe", "cl Univ. de Chile", "Estadio Mariano Melgar", "Second qualifying stage", None, "first"),
 ("2019-02-05", "19:30 (15:30)", "The Strongest bo", "py Libertad", "Estadio Hernando Siles", "Second qualifying stage", None, "first"),
 ("2019-02-06", "16:15 (13:15)", "Delfín ec", "ve Caracas", "Estadio Jocay", "Second qualifying stage", None, "first"),
 ("2019-02-06", "18:15 (13:15)", "Defensor uy", "ec Barcelona", "Estadio Luis Franzini", "Second qualifying stage", None, "first"),
 ("2019-02-06", "20:30 (15:30)", "Talleres–C ar", "br São Paulo", "Estadio Mario Alberto Kempes", "Second qualifying stage", None, "first"),
 ("2019-02-06", "20:30 (15:30)", "Palestino cl", "co Ind. Medellín", "Estadio Municipal de La Cisterna", "Second qualifying stage", None, "first"),
 ("2019-02-07", "19:30 (15:30)", "Dep. La Guaira ve", "co Atlético Nacional", "Estadio Olímpico", "Second qualifying stage", None, "first"),
 ("2019-02-12", "18:30 (15:30)", "Barcelona ec", "uy Defensor", "Estadio Monumental Isidro Romero Carbo", "Second qualifying stage", None, "second"),
 ("2019-02-12", "18:30 (15:30)", "Ind. Medellín co", "cl Palestino", "Estadio Atanasio Girardot", "Second qualifying stage", None, "second"),
 ("2019-02-12", "19:15 (13:15)", "Atlético Mineiro br", "uy Danubio", "Estádio Raimundo Sampaio", "Second qualifying stage", None, "second"),
 ("2019-02-13", "18:15 (13:15)", "Univ. de Chile cl", "pe Melgar", "Estadio Nacional Julio Martínez Prádanos", "Second qualifying stage", None, "second"),
 ("2019-02-13", "18:15 (13:15)", "Libertad py", "bo The Strongest", "Estadio Dr. Nicolás Leoz", "Second qualifying stage", None, "second"),
 ("2019-02-13", "19:30 (15:30)", "Caracas ve", "ec Delfín", "Estadio Olímpico", "Second qualifying stage", None, "second"),
 ("2019-02-13", "21:30 (15:30)", "São Paulo br", "ar Talleres–C", "Estádio do Morumbi", "Second qualifying stage", None, "second"),
 ("2019-02-14", "18:30 (15:30)", "Atlético Nacional co", "ve Dep. La Guaira", "Estadio Atanasio Girardot", "Second qualifying stage", None, "second"),
 # Third qualifying stage (8)
 ("2019-02-19", "19:30 (16:30)", "Melgar pe", "ve Caracas", "Estadio de la Universidad Nacional San A...", "Third qualifying stage", None, "first"),
 ("2019-02-20", "19:15 (14:15)", "Talleres–C ar", "cl Palestino", "Estadio Mario Alberto Kempes", "Third qualifying stage", None, "first"),
 ("2019-02-20", "21:30 (16:30)", "Defensor uy", "br Atlético Mineiro", "Estadio Luis Franzini", "Third qualifying stage", None, "first"),
 ("2019-02-21", "21:30 (16:30)", "Libertad py", "co Atlético Nacional", "Estadio Dr. Nicolás Leoz", "Third qualifying stage", None, "first"),
 ("2019-02-26", "20:30 (16:30)", "Caracas ve", "pe Melgar", "Estadio Olímpico", "Third qualifying stage", None, "second"),
 ("2019-02-27", "19:15 (14:15)", "Palestino cl", "ar Talleres–C", "Estadio San Carlos de Apoquindo", "Third qualifying stage", None, "second"),
 ("2019-02-27", "21:30 (16:30)", "Atlético Mineiro br", "uy Defensor", "Estádio Raimundo Sampaio", "Third qualifying stage", None, "second"),
 ("2019-02-28", "19:30 (16:30)", "Atlético Nacional co", "py Libertad", "Estadio Atanasio Girardot", "Third qualifying stage", None, "second"),
 # Group stage Wk 1 (16)
 ("2019-03-05", "17:15 (14:15)", "Melgar pe", "ar CA San Lorenzo", "Estadio de la Universidad Nacional San A...", "Group stage", 1, None),
 ("2019-03-05", "18:15 (14:15)", "San José bo", "br Flamengo", "Estadio Jesús Bermúdez", "Group stage", 1, None),
 ("2019-03-05", "19:15 (14:15)", "Godoy Cruz ar", "py Olimpia", "Estadio Malvinas Argentinas", "Group stage", 1, None),
 ("2019-03-05", "19:30 (16:30)", "Deportes Tolima co", "br Athletico–PR", "Estadio Manuel Murillo Toro", "Group stage", 1, None),
 ("2019-03-05", "20:30 (16:30)", "Wilstermann bo", "ar Boca Juniors", "Estadio Félix Capriles", "Group stage", 1, None),
 ("2019-03-05", "21:30 (16:30)", "Libertad py", "cl U. Católica", "Estadio Dr. Nicolás Leoz", "Group stage", 1, None),
 ("2019-03-06", "19:15 (14:15)", "Palestino cl", "br Internacional", "Estadio San Carlos de Apoquindo", "Group stage", 1, None),
 ("2019-03-06", "19:15 (14:15)", "Atlético Mineiro br", "py Cerro Porteño", "Estádio Raimundo Sampaio", "Group stage", 1, None),
 ("2019-03-06", "19:15 (14:15)", "U Concepción cl", "pe Sporting Cristal", "Estadio Municipal Alcaldesa Ester Roa Re...", "Group stage", 1, None),
 ("2019-03-06", "19:30 (16:30)", "Junior co", "br Palmeiras", "Estadio Metropolitano Roberto Meléndez", "Group stage", 1, None),
 ("2019-03-06", "19:30 (16:30)", "Alianza Lima pe", "ar River Plate", "Estadio Alejandro Villanueva", "Group stage", 1, None),
 ("2019-03-06", "20:30 (16:30)", "Zamora ve", "uy Nacional", "Estadio Rafael Agustín Tovar", "Group stage", 1, None),
 ("2019-03-06", "21:30 (16:30)", "Rosario Central ar", "br Grêmio", "Estadio Dr. Lisandro de la Torre", "Group stage", 1, None),
 ("2019-03-07", "19:00 (14:00)", "Huracán ar", "br Cruzeiro", "Estadio Tomás Adolfo Ducó", "Group stage", 1, None),
 ("2019-03-07", "19:00 (16:00)", "LDU Quito ec", "uy Peñarol", "Estadio de Liga Deportiva Universitaria", "Group stage", 1, None),
 ("2019-03-08", "15:00 (11:00)", "Deportivo Lara ve", "ec Emelec", "Estadio Metropolitano de Fútbol de Lara", "Group stage", 1, None),
 # Group stage Wk 2 (16)
 ("2019-03-12", "19:15 (15:15)", "Palmeiras br", "pe Melgar", "Allianz Parque", "Group stage", 2, None),
 ("2019-03-12", "19:15 (15:15)", "Olimpia py", "cl U Concepción", "Estadio Defensores del Chaco", "Group stage", 2, None),
 ("2019-03-12", "19:15 (15:15)", "Boca Juniors ar", "co Deportes Tolima", "Estadio Alberto José Armando", "Group stage", 2, None),
 ("2019-03-12", "19:30 (17:30)", "Sporting Cristal pe", "ar Godoy Cruz", "Estadio Nacional", "Group stage", 2, None),
 ("2019-03-12", "21:30 (17:30)", "Nacional uy", "br Atlético Mineiro", "Estadio Gran Parque Central", "Group stage", 2, None),
 ("2019-03-12", "21:30 (17:30)", "Grêmio br", "py Libertad", "Arena do Grêmio", "Group stage", 2, None),
 ("2019-03-13", "19:15 (15:15)", "CA San Lorenzo ar", "co Junior", "Estadio Pedro Bidegaín", "Group stage", 2, None),
 ("2019-03-13", "19:15 (15:15)", "Cerro Porteño py", "ve Zamora", "Estadio General Pablo Rojas", "Group stage", 2, None),
 ("2019-03-13", "21:30 (17:30)", "Internacional br", "pe Alianza Lima", "Estádio José Pinheiro Borba", "Group stage", 2, None),
 ("2019-03-13", "21:30 (17:30)", "Flamengo br", "ec LDU Quito", "Estadio Jornalista Mário Filho", "Group stage", 2, None),
 ("2019-03-13", "21:30 (17:30)", "U. Católica cl", "ar Rosario Central", "Estadio San Carlos de Apoquindo", "Group stage", 2, None),
 ("2019-03-13", "21:30 (17:30)", "River Plate ar", "cl Palestino", "Estadio Monumental Antonio Vespucio Libe...", "Group stage", 2, None),
 ("2019-03-14", "19:00 (15:00)", "Peñarol uy", "bo San José", "Estadio Campeón del Siglo", "Group stage", 2, None),
 ("2019-03-14", "21:00 (17:00)", "Athletico–PR br", "bo Wilstermann", "Estádio Joaquim Américo Guimarães", "Group stage", 2, None),
 ("2019-03-14", "21:00 (19:00)", "Emelec ec", "ar Huracán", "Estadio Banco del Pacífico", "Group stage", 2, None),
 ("2019-03-27", "21:30 (17:30)", "Cruzeiro br", "ve Deportivo Lara", "Estádio Governador Magalhães Pinto", "Group stage", 2, None),
 # Group stage Wk 3 (16)
 ("2019-04-02", "18:15 (15:15)", "San José bo", "ec LDU Quito", "Estadio Jesús Bermúdez", "Group stage", 3, None),
 ("2019-04-02", "18:15 (15:15)", "Cerro Porteño py", "uy Nacional", "Estadio General Pablo Rojas", "Group stage", 3, None),
 ("2019-04-02", "19:15 (15:15)", "CA San Lorenzo ar", "br Palmeiras", "Estadio Pedro Bidegaín", "Group stage", 3, None),
 ("2019-04-02", "19:30 (17:30)", "Melgar pe", "co Junior", "Estadio de la Universidad Nacional San A...", "Group stage", 3, None),
 ("2019-04-02", "21:30 (17:30)", "Palestino cl", "pe Alianza Lima", "Estadio San Carlos de Apoquindo", "Group stage", 3, None),
 ("2019-04-02", "21:30 (17:30)", "Athletico–PR br", "ar Boca Juniors", "Estádio Joaquim Américo Guimarães", "Group stage", 3, None),
 ("2019-04-03", "19:15 (15:15)", "Internacional br", "ar River Plate", "Estádio José Pinheiro Borba", "Group stage", 3, None),
 ("2019-04-03", "19:15 (15:15)", "Atlético Mineiro br", "ve Zamora", "Estádio Raimundo Sampaio", "Group stage", 3, None),
 ("2019-04-03", "19:15 (15:15)", "U Concepción cl", "ar Godoy Cruz", "Estadio Municipal Alcaldesa Ester Roa Re...", "Group stage", 3, None),
 ("2019-04-03", "19:30 (17:30)", "Deportes Tolima co", "bo Wilstermann", "Estadio Manuel Murillo Toro", "Group stage", 3, None),
 ("2019-04-03", "19:30 (17:30)", "Emelec ec", "br Cruzeiro", "Estadio Banco del Pacífico", "Group stage", 3, None),
 ("2019-04-03", "20:30 (17:30)", "Deportivo Lara ve", "ar Huracán", "Estadio Metropolitano de Fútbol de Lara", "Group stage", 3, None),
 ("2019-04-03", "21:30 (17:30)", "Flamengo br", "uy Peñarol", "Estadio Jornalista Mário Filho", "Group stage", 3, None),
 ("2019-04-04", "19:00 (15:00)", "U. Católica cl", "br Grêmio", "Estadio San Carlos de Apoquindo", "Group stage", 3, None),
 ("2019-04-04", "20:00 (17:00)", "Libertad py", "ar Rosario Central", "Estadio Dr. Nicolás Leoz", "Group stage", 3, None),
 ("2019-04-04", "21:00 (19:00)", "Sporting Cristal pe", "py Olimpia", "Estadio Nacional", "Group stage", 3, None),
 # Group stage Wk 4 (16)
 ("2019-04-09", "18:15 (15:15)", "Olimpia py", "ar Godoy Cruz", "Estadio Manuel Ferreira", "Group stage", 4, None),
 ("2019-04-09", "19:15 (15:15)", "Athletico–PR br", "co Deportes Tolima", "Estádio Joaquim Américo Guimarães", "Group stage", 4, None),
 ("2019-04-09", "21:30 (17:30)", "CA San Lorenzo ar", "pe Melgar", "Estadio Pedro Bidegaín", "Group stage", 4, None),
 ("2019-04-09", "21:30 (17:30)", "Peñarol uy", "ec LDU Quito", "Estadio Campeón del Siglo", "Group stage", 4, None),
 ("2019-04-09", "21:30 (17:30)", "Internacional br", "cl Palestino", "Estádio José Pinheiro Borba", "Group stage", 4, None),
 ("2019-04-10", "17:15 (15:15)", "Sporting Cristal pe", "cl U Concepción", "Estadio Alberto Gallardo", "Group stage", 4, None),
 ("2019-04-10", "18:15 (15:15)", "Cerro Porteño py", "br Atlético Mineiro", "Estadio General Pablo Rojas", "Group stage", 4, None),
 ("2019-04-10", "19:15 (15:15)", "Nacional uy", "ve Zamora", "Estadio Gran Parque Central", "Group stage", 4, None),
 ("2019-04-10", "19:15 (15:15)", "Cruzeiro br", "ar Huracán", "Estádio Governador Magalhães Pinto", "Group stage", 4, None),
 ("2019-04-10", "20:30 (17:30)", "U. Católica cl", "py Libertad", "Estadio San Carlos de Apoquindo", "Group stage", 4, None),
 ("2019-04-10", "21:30 (17:30)", "Boca Juniors ar", "bo Wilstermann", "Estadio Alberto José Armando", "Group stage", 4, None),
 ("2019-04-10", "21:30 (17:30)", "Grêmio br", "ar Rosario Central", "Arena do Grêmio", "Group stage", 4, None),
 ("2019-04-10", "21:30 (17:30)", "Palmeiras br", "co Junior", "Allianz Parque", "Group stage", 4, None),
 ("2019-04-11", "19:00 (15:00)", "River Plate ar", "pe Alianza Lima", "Estadio Monumental Antonio Vespucio Libe...", "Group stage", 4, None),
 ("2019-04-11", "21:00 (17:00)", "Flamengo br", "bo San José", "Estadio Jornalista Mário Filho", "Group stage", 4, None),
 ("2019-04-11", "21:00 (19:00)", "Emelec ec", "ve Deportivo Lara", "Estadio Banco del Pacífico", "Group stage", 4, None),
 # Group stage Wk 5 (16)
 ("2019-04-23", "16:00 (13:00)", "Deportivo Lara ve", "br Cruzeiro", "Estadio Metropolitano de Fútbol de Lara", "Group stage", 5, None),
 ("2019-04-23", "18:15 (15:15)", "Libertad py", "br Grêmio", "Estadio Dr. Nicolás Leoz", "Group stage", 5, None),
 ("2019-04-23", "18:15 (15:15)", "U Concepción cl", "py Olimpia", "Estadio Municipal Alcaldesa Ester Roa Re...", "Group stage", 5, None),
 ("2019-04-23", "19:15 (15:15)", "Huracán ar", "ec Emelec", "Estadio Tomás Adolfo Ducó", "Group stage", 5, None),
 ("2019-04-23", "21:30 (17:30)", "Godoy Cruz ar", "pe Sporting Cristal", "Estadio Malvinas Argentinas", "Group stage", 5, None),
 ("2019-04-23", "21:30 (17:30)", "Atlético Mineiro br", "uy Nacional", "Estádio Raimundo Sampaio", "Group stage", 5, None),
 ("2019-04-24", "18:15 (15:15)", "Palestino cl", "ar River Plate", "Estadio Municipal de La Cisterna", "Group stage", 5, None),
 ("2019-04-24", "18:15 (15:15)", "Rosario Central ar", "cl U. Católica", "El Gigante de Arroyito", "Group stage", 5, None),
 ("2019-04-24", "18:15 (15:15)", "Wilstermann bo", "br Athletico–PR", "Estadio Félix Capriles", "Group stage", 5, None),
 ("2019-04-24", "19:30 (17:30)", "Alianza Lima pe", "br Internacional", "Estadio Alejandro Villanueva", "Group stage", 5, None),
 ("2019-04-24", "19:30 (17:30)", "Deportes Tolima co", "ar Boca Juniors", "Estadio Manuel Murillo Toro", "Group stage", 5, None),
 ("2019-04-24", "20:30 (17:30)", "San José bo", "uy Peñarol", "Estadio Jesús Bermúdez", "Group stage", 5, None),
 ("2019-04-25", "01:30 (17:30)", "LDU Quito ec", "br Flamengo", "Estádio Municipal de Figueira de Castelo...", "Group stage", 5, None),
 ("2019-04-25", "16:00 (13:00)", "Zamora ve", "py Cerro Porteño", "Estadio Rafael Agustín Tovar", "Group stage", 5, None),
 ("2019-04-25", "19:00 (17:00)", "Junior co", "ar CA San Lorenzo", "Estadio Metropolitano Roberto Meléndez", "Group stage", 5, None),
 ("2019-04-25", "21:00 (19:00)", "Melgar pe", "br Palmeiras", "Estadio de la Universidad Nacional San A...", "Group stage", 5, None),
 # Group stage Wk 6 (16)
 ("2019-05-07", "18:15 (15:15)", "Zamora ve", "br Atlético Mineiro", "Estadio Rafael Agustín Tovar", "Group stage", 6, None),
 ("2019-05-07", "19:15 (15:15)", "Nacional uy", "py Cerro Porteño", "Estadio Gran Parque Central", "Group stage", 6, None),
 ("2019-05-07", "19:30 (17:30)", "Alianza Lima pe", "cl Palestino", "Estadio Alejandro Villanueva", "Group stage", 6, None),
 ("2019-05-07", "21:30 (17:30)", "River Plate ar", "br Internacional", "Estadio Monumental Antonio Vespucio Libe...", "Group stage", 6, None),
 ("2019-05-08", "19:15 (15:15)", "Grêmio br", "cl U. Católica", "Arena do Grêmio", "Group stage", 6, None),
 ("2019-05-08", "19:15 (15:15)", "Cruzeiro br", "ec Emelec", "Estádio Governador Magalhães Pinto", "Group stage", 6, None),
 ("2019-05-08", "19:15 (15:15)", "Huracán ar", "ve Deportivo Lara", "Estadio Tomás Adolfo Ducó", "Group stage", 6, None),
 ("2019-05-08", "19:15 (15:15)", "Rosario Central ar", "py Libertad", "Estadio Dr. Lisandro de la Torre", "Group stage", 6, None),
 ("2019-05-08", "19:30 (17:30)", "Junior co", "pe Melgar", "Estadio Metropolitano Roberto Meléndez", "Group stage", 6, None),
 ("2019-05-08", "20:30 (17:30)", "LDU Quito ec", "bo San José", "Estadio Polideportivo Misael Delgado", "Group stage", 6, None),
 ("2019-05-08", "21:30 (17:30)", "Peñarol uy", "br Flamengo", "Estadio Campeón del Siglo", "Group stage", 6, None),
 ("2019-05-08", "21:30 (17:30)", "Palmeiras br", "ar CA San Lorenzo", "Allianz Parque", "Group stage", 6, None),
 ("2019-05-09", "18:15 (15:15)", "Olimpia py", "pe Sporting Cristal", "Estadio Manuel Ferreira", "Group stage", 6, None),
 ("2019-05-09", "19:15 (15:15)", "Godoy Cruz ar", "cl U Concepción", "Estadio Malvinas Argentinas", "Group stage", 6, None),
 ("2019-05-09", "20:30 (17:30)", "Wilstermann bo", "co Deportes Tolima", "Estadio Félix Capriles", "Group stage", 6, None),
 ("2019-05-09", "21:30 (17:30)", "Boca Juniors ar", "br Athletico–PR", "Estadio Alberto José Armando", "Group stage", 6, None),
 # Round of 16 (16)
 ("2019-07-23", "19:15 (15:15)", "River Plate ar", "br Cruzeiro", "Estadio Monumental Antonio Vespucio Libe...", "Round of 16", None, "first"),
 ("2019-07-23", "19:30 (17:30)", "LDU Quito ec", "py Olimpia", "Estadio de Liga Deportiva Universitaria", "Round of 16", None, "first"),
 ("2019-07-23", "21:30 (17:30)", "Godoy Cruz ar", "br Palmeiras", "Estadio Malvinas Argentinas", "Round of 16", None, "first"),
 ("2019-07-24", "19:15 (15:15)", "Nacional uy", "br Internacional", "Estadio Gran Parque Central", "Round of 16", None, "first"),
 ("2019-07-24", "19:15 (15:15)", "CA San Lorenzo ar", "py Cerro Porteño", "Estadio Pedro Bidegaín", "Round of 16", None, "first"),
 ("2019-07-24", "19:30 (17:30)", "Emelec ec", "br Flamengo", "Estadio Banco del Pacífico", "Round of 16", None, "first"),
 ("2019-07-24", "21:30 (17:30)", "Athletico–PR br", "ar Boca Juniors", "Estádio Joaquim Américo Guimarães", "Round of 16", None, "first"),
 ("2019-07-25", "21:30 (17:30)", "Grêmio br", "py Libertad", "Arena do Grêmio", "Round of 16", None, "first"),
 ("2019-07-30", "19:15 (15:15)", "Cruzeiro br", "ar River Plate", "Estádio Governador Magalhães Pinto", "Round of 16", None, "second"),
 ("2019-07-30", "20:30 (17:30)", "Olimpia py", "ec LDU Quito", "Estadio Defensores del Chaco", "Round of 16", None, "second"),
 ("2019-07-30", "21:30 (17:30)", "Palmeiras br", "ar Godoy Cruz", "Allianz Parque", "Round of 16", None, "second"),
 ("2019-07-31", "18:15 (15:15)", "Cerro Porteño py", "ar CA San Lorenzo", "Estadio General Pablo Rojas", "Round of 16", None, "second"),
 ("2019-07-31", "19:15 (15:15)", "Internacional br", "uy Nacional", "Estádio José Pinheiro Borba", "Round of 16", None, "second"),
 ("2019-07-31", "21:30 (17:30)", "Flamengo br", "ec Emelec", "Estadio Jornalista Mário Filho", "Round of 16", None, "second"),
 ("2019-07-31", "21:30 (17:30)", "Boca Juniors ar", "br Athletico–PR", "Estadio Alberto José Armando", "Round of 16", None, "second"),
 ("2019-08-01", "20:30 (17:30)", "Libertad py", "br Grêmio", "Estadio Defensores del Chaco", "Round of 16", None, "second"),
 # Quarter-finals (8)
 ("2019-08-20", "21:30 (17:30)", "Grêmio br", "br Palmeiras", "Arena do Grêmio", "Quarter-finals", None, "first"),
 ("2019-08-21", "17:15 (15:15)", "LDU Quito ec", "ar Boca Juniors", "Estadio de Liga Deportiva Universitaria", "Quarter-finals", None, "first"),
 ("2019-08-21", "21:30 (17:30)", "Flamengo br", "br Internacional", "Estadio Jornalista Mário Filho", "Quarter-finals", None, "first"),
 ("2019-08-22", "19:15 (15:15)", "River Plate ar", "py Cerro Porteño", "Estadio Monumental Antonio Vespucio Libe...", "Quarter-finals", None, "first"),
 ("2019-08-27", "21:30 (17:30)", "Palmeiras br", "br Grêmio", "Allianz Parque", "Quarter-finals", None, "second"),
 ("2019-08-28", "19:15 (15:15)", "Boca Juniors ar", "ec LDU Quito", "Estadio Alberto José Armando", "Quarter-finals", None, "second"),
 ("2019-08-28", "21:30 (17:30)", "Internacional br", "br Flamengo", "Estádio José Pinheiro Borba", "Quarter-finals", None, "second"),
 ("2019-08-29", "18:15 (15:15)", "Cerro Porteño py", "ar River Plate", "Estadio General Pablo Rojas", "Quarter-finals", None, "second"),
 # Semi-finals (4)
 ("2019-10-01", "21:30 (17:30)", "River Plate ar", "ar Boca Juniors", "Estadio Monumental Antonio Vespucio Libe...", "Semi-finals", None, "first"),
 ("2019-10-02", "21:30 (17:30)", "Grêmio br", "br Flamengo", "Arena do Grêmio", "Semi-finals", None, "first"),
 ("2019-10-22", "21:30 (17:30)", "Boca Juniors ar", "ar River Plate", "Estadio Alberto José Armando", "Semi-finals", None, "second"),
 ("2019-10-23", "21:30 (17:30)", "Flamengo br", "br Grêmio", "Estadio Jornalista Mário Filho", "Semi-finals", None, "second"),
 # Final (1)
 ("2019-11-23", "15:00 (12:00)", "Flamengo br", "ar River Plate", "Estadio Monumental (Neutral Site)", "Final", None, None),
]

import json, os
from collections import Counter

assert len(ROWS) == 155, len(ROWS)
keys = [(d, t, h, a) for d, t, h, a, v, s, w, l in ROWS]
assert len(set(keys)) == 155, "duplicate unique key inside transcription"
assert not any("..." not in v and False for v in [r[4] for r in ROWS])

out_path = os.path.expanduser("~/workspace/ai-inbox/work-req-20261023-001/fbref_2019_textlayer.jsonl")
with open(out_path, "w", encoding="utf-8") as f:
    for d, t, h, a, v, s, w, l in ROWS:
        trunc = v.endswith("...")
        rec = {
            "season_year": 2019,
            "home": h,
            "away": a,
            "match_date": d,
            "kickoff_local": t,
            "source_timezone_text": None,
            "official_stage": s,
            "official_round": w,
            "venue_or_stadium": v,
            "venue_truncated": trunc,
            "city": None,
            "country": None,
            "group_id": None,
            "tie_id": None,
            "source_fixture_id": None,
            "leg": l,
            "source_url": URL,
            "final_url": URL,
            "retrieved_at": RETRIEVED,
            "field_locator": "schedule table columns Round|Wk|Day|Date|Time|Home|Away|Venue|Notes",
            "source_sha256": None,
            "source_sha256_note": "browser text layer only, no bytes downloaded; hash not fabricated",
            "status": "partial" if trunc else "complete",
            "source_id": "SRC-FBREF-TEXTLAYER",
        }
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

print("rows:", len(ROWS))
print("by stage:", dict(Counter(s for *_, s, w, l in [(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]) for r in ROWS])))
print("by stage (proper):", Counter(r[5] for r in ROWS))
print("truncated:", sum(1 for r in ROWS if r[4].endswith("...")))
print("partial:", sum(1 for r in ROWS if r[4].endswith("...")))
print("leg first/second/null:", Counter(r[7] for r in ROWS))
