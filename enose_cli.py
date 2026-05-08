em_execucao = False

def ajuda():
    print('Comandos disponíveis...')
    print('  testar               verifica a conexão com os dispositivos')
    print('  configurar exp       modifica parametros da experiência, nome de sensores, pesquisador')
    print('  configurar tempo     define os parâmetros de tempo e fluxo de ar para o ciclo da experiência')
    print('  iniciar #            executa o cliclo da experiência # vezes')
    print('  parar                interrompe a execução da experiência')
    print('  abrir tabela         após concluída a experiência, abre a tabela de resultados')
    print('  abrir json           após concluída a experiência, abre arquivo JSON de resultados')
    print('  sair                 interrompe a execução da experiência e fecha esta linha de comando')
    print('')

def testar():
    pass

def configurar_exp():
    pass

def configurar_tempos():
    pass

def iniciar():
    pass

def parar():
    pass


def main():
    print("e-Nose CLI, v0.1")
    print("Use um dos comandos: 'ajuda', 'testar', 'configurar', 'iniciar', 'parar', 'abrir', 'sair")
    while True:
        op = input("> ").lower().strip().split(" ")
        cmd = op[0]
        
        if cmd in {'ajuda', 'testar', 'configurar', 'iniciar', 'parar', 'sair'}:
            if cmd == 'ajuda':
                ajuda()
                continue
            
            elif cmd == 'testar':
                print("Iniciando testes de dispositivos...")
                continue
                #testar()
            
            elif cmd == 'configurar':
                if len(op) == 1 or not op[1] in {'exp', 'tempos'}:
                    print('Parametro pendente ou desconhecido: o que você deseja configurar?')
                    print('Formas de uso:')
                    print('  configurar exp       modifica parametros da experiência, nome de sensores, pesquisador')
                    print('  configurar tempo     define os parâmetros de tempo e fluxo de ar para o ciclo da experiência')
                    continue

                elif op[1] == 'exp':
                    print("Configurando metadados experimentais")
                    #configurar_exp()
                    continue

                elif op[1] == 'tempos':
                    print("Configurando macro ciclo de tempos e fluxo de ar")
                    #configurar_tempos()
                    continue
                
            
            elif cmd == 'iniciar':
                if len(op) == 1:
                    print('Parametro pendente: indicar a quantidade de vezes que ciclo deve se repetir')
                    print('Exemplo:')
                    print(' iniciar 4')
                    continue

                elif len(op) == 2:
                    loop = None
                    try: loops = int(op[1])
                    except ValueError:
                        print("O parametro fornecido não é numérico...")
                        continue
                    #replicar parametros de tempo aqui...

                else:
                    print("Comando inadequado, digite 'ajuda' para ver as opções.")
                    continue


            elif cmd == 'parar':
                if len(op) == 1:
                    print('Parando o experimento...')
                    #Lógica de interrupção
                    continue


            elif cmd == 'abrir':
                if em_execucao:
                    print("Não é possível abrir arquivos de dados com experiência em andamento...")
                    continue
                
                if len(op) == 1 or not op[1] in {'tabela', 'json'}:
                    print('Parametro pendente ou desconhecido: o que você deseja configurar?')
                    print('Formas de uso:')
                    print('  abrir tabela         após concluída a experiência, abre a tabela de resultados')
                    print('  abrir json           após concluída a experiência, abre arquivo JSON de resultados')                    
                    continue

                elif op[1] == 'exp':
                    print("Configurando metadados experimentais")
                    #configurar_exp()
                    continue

                elif op[1] == 'tempos':
                    print("Configurando macro ciclo de tempos e fluxo de ar")
                    #configurar_tempos()
                    continue


            elif cmd == 'sair':
                if len(op) == 1:
                    print('Parando o experimento... e fechando linha de comando...')
                    #Lógica de interrupção
                    break


        print("Comando desconhecido, digite 'ajuda' para ver as opções.")




    




if __name__ == '__main__':
    main()