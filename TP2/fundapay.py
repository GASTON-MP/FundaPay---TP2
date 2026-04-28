"""
Logica, interfaz e interaccion FundaPay
"""

import TP2.constantes as constantes
import TP2.auxiliares as auxiliares


def crear_cuenta(dict_cuentas: dict[dict]):
    """
    Registra un nombre_apellido y un DNI, evalua que sea una cuenta inexistente.
    Se crea un diccionario con toda la informacion de la cuenta
    y se guarda en el diccionario de todas las cuentas.

    PRE-COINDICIONES:
    -Recibe el diccionario de todas las cuentas.
    """
    nombre_apellido = auxiliares.validar_nombre_apellido()
    if nombre_apellido is None:
        return
    dni = auxiliares.validar_dni()
    if dni is None:
        return
    if dni in dict_cuentas:
        print(
            constantes.MSG_CUENTA_EXISTE.format(
                nombre=dict_cuentas[dni]["nombre_apellido"]
            )
        )
        return

    # Creo una nueva cuenta
    nueva_cuenta = {
        "nombre_apellido": nombre_apellido,
        "DNI": dni,
        "saldo": 0,
        "interes": 0,
        "prestamos": [],
        "transferencias": [],
    }

    # Guardo la cuenta
    dict_cuentas[dni] = nueva_cuenta
    print(constantes.MSG_CUENTA_CREADA)


def ingresar_dinero(dict_cuentas: dict[dict]):
    """
    Pide al usuario un dni despues pide un monto y se agrega el monto al saldo.
    El saldo se agrega como informacion al diccionario

    PRE-COINDICIONES:
    -Recibe el diccionario de todas las cuentas.
    """
    saldo = 0
    dni = auxiliares.validar_dni()
    if dni is None:
        return

    if dni not in dict_cuentas:
        print(constantes.MSG_NO_EXISTE_CUENTA)
        return

    # Sumo el monto al saldo
    monto = auxiliares.validar_monto()

    if monto is None:
        return

    saldo += monto
    dict_cuentas[dni]["saldo"] += saldo
    print(
        constantes.MSG_INGRESO_ACREDITADO.format(
            monto=monto, nombre=dict_cuentas[dni]["nombre_apellido"]
        )
    )


def transferir_dinero(dict_cuentas: dict[dict]):
    """
    Pide un dni para la cuenta origen y otro para la cuenta destino.
    Despues pide un monto para hacer la transferencia de la cuenta origen a la destino,
    si el saldo esta disponible se realiza la transferencia.

    Despues se realiza un registro de todas las transferencias
    y se guardan en una lista dentro del diccionario de cuentas.

    PRE-COINDICIONES:
    -Recibe el diccionario de todas las cuentas.
    """
    dni_origen = auxiliares.validar_dni_transferencia("Ingrese DNI origen: ")

    if dni_origen is None:
        return

    if dni_origen not in dict_cuentas:
        print(constantes.MSG_NO_EXISTE_CUENTA)
        return

    dni_destino = auxiliares.validar_dni_transferencia("Ingrese DNI destino: ")

    if dni_destino is None:
        return

    if dni_destino not in dict_cuentas:
        print(constantes.MSG_NO_EXISTE_CUENTA)
        return

    monto = auxiliares.validar_monto()

    if monto is None:
        return

    saldo_cuenta_origen = dict_cuentas[dni_origen]["saldo"]

    if saldo_cuenta_origen >= monto:
        dict_cuentas[dni_origen]["saldo"] = saldo_cuenta_origen - monto
        dict_cuentas[dni_destino]["saldo"] += monto
        print(
            constantes.MSG_TRANSFERENCIA_EXITOSA.format(
                monto=monto,
                nombre_origen=dict_cuentas[dni_origen]["nombre_apellido"],
                nombre_destino=dict_cuentas[dni_destino]["nombre_apellido"],
            )
        )

        # registro de tranferencias

        registro_recibido = {
            "tipo": "recibido",
            "monto": monto,
            "nombre": dict_cuentas[dni_origen]["nombre_apellido"],
            "dni": dni_origen,
        }

        registro_enviado = {
            "tipo": "enviado",
            "monto": monto,
            "nombre": dict_cuentas[dni_destino]["nombre_apellido"],
            "dni": dni_destino,
        }

        dict_cuentas[dni_origen]["transferencias"].append(registro_enviado)
        dict_cuentas[dni_destino]["transferencias"].append(registro_recibido)

    else:
        print(constantes.MSG_MONTO_NO_DISPONIBLE)
        return


def otorgar_prestamo(dict_cuentas: dict[dict]):
    """
    Pide un DNI, un interes y un monto.
    El monto lo suma al saldo y el interes tambien.
    Calcula el 20% del balance del prestamo y calcula la tasa de interes del balance.
    Crea un diccionario con toda la informacion del prestamo
    y la agrega a una lista dentro del diccionario de cuentas.

    PRE-COINDICIONES:
    -Recibe el diccionario de todas las cuentas.
    """
    dni = auxiliares.validar_dni()

    if dni is None:
        return

    if dni not in dict_cuentas:
        print(constantes.MSG_NO_EXISTE_CUENTA)
        return

    tasa_interes = auxiliares.validar_interes()
    if tasa_interes is None:
        return

    balance = auxiliares.validar_monto()

    if balance is None:
        return

    dict_cuentas[dni]["saldo"] += balance
    dict_cuentas[dni]["interes"] += tasa_interes
    print(
        constantes.MSG_PRESTAMO_CREADO.format(
            nombre=dict_cuentas[dni]["nombre_apellido"],
            balance=dict_cuentas[dni]["saldo"],
        )
    )

    # Calculo impuesto y interes respecto del balance
    impuesto = (((100 + 20) * balance) // 100) - balance
    interes = (((100 + tasa_interes) * balance) // 100) - balance
    total_pendiente = balance + impuesto + interes

    # Informacion del prestamo
    nuevo_prestamo = {
        "id_prestamo": len(dict_cuentas[dni]["prestamos"]) + 1,
        "monto_total": total_pendiente,
        "tasa_interes": tasa_interes,
        "total_pendiente": total_pendiente,
        "impuesto": impuesto,
        "total_impuesto": impuesto,
        "intereses": interes,
        "total_intereses": interes,
        "capital": balance,
        "total_capital": balance,
        "total_pagado_impuestos": 0,
        "total_pagado_intereses": 0,
        "total_pagado_capital": 0,
    }
    dict_cuentas[dni]["prestamos"].append(nuevo_prestamo)


def validaciones_seleccion_prestamo(dict_cuentas: dict[dict]):
    """
    La funcion valida el dni ingresado si no otorgo un prestamo vuelve al menu.
    Imprime cada prestamo y su informacion.
    Pide al usuario que elija un prestamo para hacer los pagos.

    PRE-COINDICIONES:
    -Recibe el diccionario de todas las cuentas.

    POST-COINDICIONES:
    Devuelve:
    -DNI
    -Prestamo
    """
    dni = auxiliares.validar_dni()

    if dni is None:
        return None

    if dni not in dict_cuentas:
        print(constantes.MSG_NO_EXISTE_CUENTA)
        return None

    if dict_cuentas[dni]["prestamos"] == []:
        print(constantes.MSG_PRESTAMO_NO_ACTIVO)
        return None

    print(constantes.SALDO_DISPONIBLE_TEMPLATE.format(monto=dict_cuentas[dni]["saldo"]))
    print(constantes.PRESTAMOS_PENDIENTES)

    # imprimo cada prestamo y su informacion
    auxiliares.imprimir_prestamos(dict_cuentas[dni]["prestamos"])

    # elijo el id del prestamo
    prestamo = auxiliares.seleccionar_id_prestamo(dict_cuentas[dni]["prestamos"])

    if prestamo is None:
        return None

    return dni, prestamo


def pagar_prestamo(dict_cuentas: dict[dict]):
    """
    La funcion pide un monto a abonar,
    si el saldo es suficiente se realizan los pagos de manera:

    -Primero se pagan los impuestos pendientes
    -Despues se pagan los intereses pendientes
    -Por ultimo se paga el capital

    PRE-COINDICIONES:
    -Recibe el diccionario de todas las cuentas.
    """
    validaciones = validaciones_seleccion_prestamo(dict_cuentas)

    if validaciones is None:
        return

    dni, prestamo = validaciones

    monto_abonar = auxiliares.validar_monto_prestamos()

    if monto_abonar is None:
        return

    if monto_abonar > dict_cuentas[dni]["saldo"]:
        print(constantes.MSG_SALDO_INSUFICIENTE)
        return

    monto_inicial = monto_abonar

    # pago impuesto
    (
        monto_abonar,
        prestamo["impuesto"],
        prestamo["total_pagado_impuestos"],
    ) = auxiliares.pago_componente(
        monto_abonar,
        prestamo["impuesto"],
        prestamo["total_pagado_impuestos"],
    )

    # pago intereses
    if monto_abonar > 0:
        (
            monto_abonar,
            prestamo["intereses"],
            prestamo["total_pagado_intereses"],
        ) = auxiliares.pago_componente(
            monto_abonar,
            prestamo["intereses"],
            prestamo["total_pagado_intereses"],
        )

    # pago capital
    if monto_abonar > 0:
        (
            monto_abonar,
            prestamo["capital"],
            prestamo["total_pagado_capital"],
        ) = auxiliares.pago_componente(
            monto_abonar,
            prestamo["capital"],
            prestamo["total_pagado_capital"],
        )

    # actualizo el total pendiente
    prestamo["total_pendiente"] = (
        prestamo["impuesto"] + prestamo["intereses"] + prestamo["capital"]
    )

    # resto el monto del sueldo
    monto_pagado = monto_inicial - monto_abonar
    dict_cuentas[dni]["saldo"] -= monto_pagado

    print(constantes.MSG_PRESTAMO_PAGADO)
    return


def ver_resumen(dict_cuentas: dict[dict]):
    """
    Pide un DNI y accede a la lista de transferencias de ese DNI.
    Para cada transferencia dentro de la lista la imprime de atras para adelante.
    Imprime solamente las ultimos 5 movimientos e imprime todos los prestamos.

    PRE-COINDICIONES:
    -Recibe el diccionario de todas las cuentas.
    """
    dni = auxiliares.validar_dni()

    if dni is None:
        return

    if dni not in dict_cuentas:
        print(constantes.MSG_NO_EXISTE_CUENTA)
        return

    print(
        constantes.RESUMEN_TEMPLATE.format(
            nombre=dict_cuentas[dni]["nombre_apellido"],
            saldo=dict_cuentas[dni]["saldo"],
        )
    )

    # Accedo a la lista de transferencias
    for transferencia in dict_cuentas[dni]["transferencias"][-5:][::-1]:
        if transferencia["tipo"] == "recibido":
            print(
                constantes.TRANSFERENCIA_ENTRANTE_TEMPLATE.format(
                    monto=transferencia["monto"],
                    nombre=transferencia["nombre"],
                    dni=transferencia["dni"],
                )
            )

        else:
            print(
                constantes.TRANSFERENCIA_SALIENTE_TEMPLATE.format(
                    monto=transferencia["monto"],
                    nombre=transferencia["nombre"],
                    dni=transferencia["dni"],
                )
            )

    print(constantes.PRESTAMOS_PENDIENTES)

    # Imprimo cada prestamo y su informacion
    auxiliares.imprimir_prestamos(dict_cuentas[dni]["prestamos"])


def main():
    """
    Crea la variable dict_cuentas que va a ser el diccionario de todas las cuentas.
    Pide una opcion del menu.
    Depende lo que ingrese el usuario quiera hacer, se llama a la funcion correspondiente.
    Cuando el usuario quiera elija la opcion salir se termina el programa.
    """
    dict_cuentas = {}
    opciones = {
        "1": crear_cuenta,
        "2": ingresar_dinero,
        "3": transferir_dinero,
        "4": otorgar_prestamo,
        "5": pagar_prestamo,
        "6": ver_resumen,
    }

    while True:
        opcion = input(
            "1) Crear cuenta \n"
            "2) Ingresar dinero\n"
            "3) Transferir dinero\n"
            "4) Otorgar prestamo\n"
            "5) Pagar prestamo\n"
            "6) Ver resumen\n"
            "7) Salir\n"
            ">>> "
        )

        if opcion == "7":
            print(constantes.MSG_FIN)
            return

        if opcion in opciones:
            opciones[opcion](dict_cuentas)

        else:
            print(constantes.MSG_INPUT_INVALIDO)


if __name__ == "__main__":
    main()
