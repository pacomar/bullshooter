def parsear_tabla_html(tabla):    
    # Obtén las filas de la tabla
    filas = tabla.find_all('tr')
    
    # Obtén los encabezados de la tabla
    encabezados = [encabezado.text.strip() for encabezado in filas[0].find_all('td')]
    
    # Parsea los datos de la tabla en una lista de diccionarios
    datos = []
    for fila in filas[1:]:
        celdas = fila.find_all('td')
        fila_datos = {}
        for i, celda in enumerate(celdas):
            fila_datos[encabezados[i]] = celda.text.strip()
        datos.append(fila_datos)
    
    return encabezados, datos

def find_index(list, text_to_find):
    for i, item in enumerate(list):
        if text_to_find in item:
            return i
    return -1