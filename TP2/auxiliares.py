"""Funciones auxiliares para FundaPay"""

import TP2.constantes as constantes


def validar_input(mensaje):
    """
    Pide al usuario un ingreso y si lo ingresado es "**" devuelve None,
    sino devuelve lo que ingreso
    """
    ingreso = input(mensaje)
    if ingreso == "**":
        return None
    return ingreso


def validar_nombre_apellido():
    """
    Pide al usuario un nombre_apellido y se evalua si lo que ingreso tenga max 30 caracteres
    y sean solo letras o espacios. Sino vuelve a pedir un nombre_apellido.

    POST-COINDICIONES:
    -La funcion devuelve un nombre_apellido.
    """
    while True:
        nombre_apellido = validar_input("Ingrese nombre y apellido: ")

        if nombre_apellido is None:
            return None

        if 1 > len(nombre_apellido) or len(nombre_apellido) > 30:
            print(constantes.MSG_NOMBRE_INVALIDO)
            continue

        separados = nombre_apellido.split(" ")
        es_valido = True
        for name_surname in separados:
            if not name_surname.isalpha():
                print(constantes.MSG_NOMBRE_INVALIDO)
                es_valido = False
                break

        if es_valido:
            break

    return nombre_apellido


def validar_dni():
    """
    Pide al usuario un dni y se evalua si lo que ingreso cumpla el formato "XX.YYY.ZZZ"
    y que sean solo numeros.

    POST-COINDICIONES:
    -La funcion devuelve un DNI de la forma "XX.YYY.ZZZ".
    """
    while True:
        dni = validar_input("Ingrese DNI: ")

        if dni is None:
            return None

        if len(dni) != len("XX.YYY.ZZZ") or (dni[2] != "." or dni[6] != "."):
            print(constantes.MSG_DNI_INVALIDO)
            continue

        lista_numeros = dni.split(".")

        if (
            not lista_numeros[0].isdigit()
            or not lista_numeros[1].isdigit()
            or not lista_numeros[2].isdigit()
        ):
            print(constantes.MSG_DNI_INVALIDO)
            continue

        return dni


def validar_monto():
    """
    Pide al usuario un monto y se evalua si lo que ingreso cumpla
    que sea un numero entero mayor igual a 100.

    POST-COINDICIONES:
    -La funcion devuelve un monto.
    """
    while True:
        ingreso_monto = validar_input("Ingrese un monto: ")

        if ingreso_monto is None:
            return None

        if ingreso_monto.isdigit():
            monto = int(ingreso_monto)
            if monto >= 100:
                return monto
        print(constantes.MSG_MONTO_INVALIDO)


def validar_interes():
    """
    Pide al usuario un interes y se evalua si lo que ingreso cumpla
    que sea un numero entero mayor igual a 5.

    POST-COINDICIONES:
    -La funcion devuelve el interes.
    """
    while True:
        ingreso_interes = validar_input("Ingrese un interes: ")
        if ingreso_interes is None:
            return None

        if ingreso_interes.isdigit():
            tasa_interes = int(ingreso_interes)
            if tasa_interes >= 5:
                return tasa_interes
        print(constantes.MSG_TASA_INTERES_INVALIDA)


def imprimir_prestamos(prestamos: list[dict]):
    """
    La funcion imprime los prestamos y su informacion.

    PRE-COINDICIONES:
    -Prestamos es una lista con diccionarios
    """
    for prestamo in prestamos:
        print(
            constantes.PRESTAMO_TEMPLATE.format(
                id_prestamo=prestamo["id_prestamo"],
                monto_total=prestamo["monto_total"],
                tasa_interes=prestamo["tasa_interes"],
                total_pendiente=prestamo["total_pendiente"],
                total_impuestos=prestamo["total_impuesto"],
                total_pagado_impuestos=prestamo["total_pagado_impuestos"],
                total_intereses=prestamo["total_intereses"],
                total_pagado_intereses=prestamo["total_pagado_intereses"],
                capital_total=prestamo["total_capital"],
                total_pagado_capital=prestamo["total_pagado_capital"],
            )
        )


def seleccionar_id_prestamo(prestamos: list[dict]):
    """
    La funcion pide el id del prestamo y evalua que exista la opcion.

    PRE-COINDICIONES:
    -Prestamos es una lista con diccionarios

    POST-COINDICIONES:
    -La funcion devuelve el prestamo elegido
    """
    while True:
        opcion = validar_input("Seleccione prestamo: ")

        if opcion is None:
            return None

        for prestamo in prestamos:
            if str(prestamo["id_prestamo"]) == opcion:
                return prestamo
        print(constantes.MSG_SELECCION_INVALIDA)


def pago_componente(monto: int, componente: int, total_pagado: int):
    """
    La funcion hace el pago de los impuestos o intereses o del capital.

    PRE-COINDICIONES:
    -Monto es un numero entero
    -Componente es un numero entero
    -Total_pagado es un numero entero empieza en 0

    POST-COINDICIONES:
    La funcion devuelve:
    -Monto
    -Componente
    -Total pagado
    """
    if monto >= componente:
        monto -= componente
        total_pagado += componente
        componente = 0
    else:
        componente -= monto
        total_pagado += monto
        monto = 0

    return monto, componente, total_pagado


def validar_monto_prestamos():
    """
    La funcion valida el monto ingresado, y evalua
    que sea un numero entero mayor igual a 1.

    POST-COINDICIONES:
    -La funcion devuelve el monto a abonar
    """
    while True:
        monto = validar_input("Ingrese monto a abonar: ")

        if monto is None:
            return None

        if monto.isdigit():
            monto_abonar = int(monto)
            if monto_abonar >= 1:
                break
        print(constantes.MSG_MONTO_INVALIDO)

    return monto_abonar


def validar_dni_transferencia(mensaje: str):
    """
    Pide al usuario un dni origen o destino
    y se evalua si lo que ingreso cumpla el formato "XX.YYY.ZZZ"
    y que sean solo numeros.

    POST-COINDICIONES:
    -La funcion devuelve un DNI de la forma "XX.YYY.ZZZ".
    """
    while True:
        dni = validar_input(mensaje)

        if dni is None:
            return None

        if len(dni) != len("XX.YYY.ZZZ") or (dni[2] != "." or dni[6] != "."):
            print(constantes.MSG_DNI_INVALIDO)
            continue

        lista_numeros = dni.split(".")

        if (
            not lista_numeros[0].isdigit()
            or not lista_numeros[1].isdigit()
            or not lista_numeros[2].isdigit()
        ):
            print(constantes.MSG_DNI_INVALIDO)
            continue

        return dni
