charts1 = ['a', 'b', 'c', 'd', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'p', 'o', 'q', 'r', 's', 't', 'u', 'v','x', 'y', 'z']
charts2 = ['!', '#', '?', '%','$', '&', '/', '(','[','{', ')',']','}','¿']
charts3 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def generar_contrasena(cedula):
    Digitos_finales = cedula[-3:]

    Caracter1 = charts1[int(Digitos_finales[0])] 
    Caracter2 = charts1[int(Digitos_finales[0]) // 2] 
    Caracter3 = charts1[int(Digitos_finales[0]) + (int(Digitos_finales[0]) // 2)] 
    Caracter4 = charts2[int(Digitos_finales[1]) // 2] 
    Caracter5 = charts3[int(Digitos_finales[2]) - int(Digitos_finales[0])] 
    Suma = int(Digitos_finales[0]) + int(Digitos_finales[1]) + int(Digitos_finales[2])

    if Suma > 9:
        Caracter6 = charts1[int(str(Suma)[0])] 
        Caracter7 = charts2[int(str(Suma)[1])] 
    else: 
        Caracter6 = charts2[int(str(Suma)[0])] 
        Caracter7 = charts2[int(Digitos_finales[2]) // 2]

    octavo_caracter = charts3[int(cedula[0])]

    password = Caracter1 + Caracter2 + Caracter3 + Caracter4 + Caracter5 + Caracter6 + Caracter7 + octavo_caracter

    return password