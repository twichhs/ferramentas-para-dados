def validar_cep(valor):

    cep = str(valor)
    cep = cep.replace("-","").replace(".","").replace(" ","")


    if len(cep) == 8 and cep.isdigit():
        return True
    else:
        return False 