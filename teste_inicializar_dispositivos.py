import subprocess
import os

os.system('cls')

print("* Iniciando teste em Arduino...\nVerifique se sensores estão sendo selecionados...")
print(subprocess.getoutput("python teste_arduino.py"))

print("* Iniciando teste em LCR...")
print(subprocess.getoutput("python teste_lcr.py"))

print("* Iniciando teste nas unidades MASS FLOW...")
print(subprocess.getoutput("python teste_mass_flow.py"))

