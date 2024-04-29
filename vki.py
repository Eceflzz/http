boy = float(input("boyunuzu giriniz(örneğin = 1.70): "))
kilo = float(input("kilonuzu giriniz'kilogram': "))

vki = (kilo / boy ** 2)
print("vki değeriniz: ", vki)

if vki < 18.5:
    print("sağlıklı kilonuzun altındasınız.")
elif vki >= 18.5 and vki < 25:
    print("sağlıklı kilo aralığınızdasınız. ")
elif vki >= 25 and vki < 30:
    print("sağlıklı kilonuzun üzerindesiniz. ")
elif vki >= 30 and vki <34:
    print("obezite ")
else:
    print("obezite sınırları üzerindesiniz.") 