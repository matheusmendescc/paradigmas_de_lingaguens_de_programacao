nome = input("Nome: ")
sal = float(input("Salário: "))
if sal <= 1250:
    sal += (sal*15/100)
else:
    sal += (sal*10/100)
print (f"O salário de {nome} é de: R${sal}")