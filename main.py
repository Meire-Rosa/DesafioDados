import pandas as pd

#Carrega arquivo MovtoITEM.csv para dfMovto
dfMovto = pd.read_csv('MovtoITEM.csv', delimiter=';')

#Visualiza atributos em MovtoITEM.csv
#print("dfMovto")
#print(dfMovto.info())
#print(dfMovto.head())
#print(dfMovto.dtypes)

#Altera virgulas em pontos e str em float
for i in ['quantidade', 'valor']:
    dfMovto[i] = dfMovto[i].astype(str)
    dfMovto[i] = dfMovto[i].str.replace(',', '.')
    dfMovto[i] = dfMovto[i].astype(float)

#Carrega arquivo SaldoITEM.csv para dfSaldo
dfSaldo = pd.read_csv('SaldoITEM.csv', delimiter=';')

#Visualiza atributos em SaldoITEM.csv
#print("dfSaldo")
#print(dfSaldo.info())
#print(dfSaldo.head())

#Altera virgulas em pontos e str em float
for i in ['qtd_inicio', 'valor_inicio', 'qtd_final', 'valor_final']:
    dfSaldo[i] = dfSaldo[i].astype(str)
    dfSaldo[i] = dfSaldo[i].str.replace(',', '.')
    dfSaldo[i] = dfSaldo[i].astype(float)
##
#Inicializando DataFrame saldoAtual
dfSaldoAtual = dfSaldo

#Inicializando listas para DataFrame de saída
listaItem = []
listaData = []
listaQtdEnt = []
listaValorEnt = []
listaQtdSai = []
listaValorSai = []
listaQtdSaldoInicial = []
listaQtdSaldoFinal = []
listaValorSaldoInicial = []
listaValorSaldoFinal = []

##
#Criando intervalo de datas a partir de SaldoITEM.csv
initialDate = min(dfSaldo['data_inicio'])
finalDate = max(dfSaldo['data_final'])
initialDate = initialDate.split('/')
finalDate = finalDate.split('/')

dateRange = pd.date_range(start=initialDate[2]+initialDate[1]+initialDate[0],
                          end=finalDate[2]+finalDate[1]+finalDate[0])

#Altera padrão de data para conforme SaldoITEM.csv e MovtoITEM.csv
dateBr =dateRange.strftime('%d/%m/%Y')

## Inicio looping de datas
#date = dateBr[29]  #apenas para teste inicial
#print(date)

for date in dateBr:
    #print(date)
    ## lancamentosDiario guarda movimentações diárias
    lancamentosDiario = dfMovto[dfMovto.data_lancamento == date]
    #print(lancamentosDiario)

    ## Inicio looping de itens
    #codigoItem = dfSaldo.item[0] #apenas para teste inicial
    for codigoItem in dfSaldo.item:
        #print(codigoItem)

        ## lancamentosDiarioItem guarda movimentações diárias de um item específico
        lancamentosDiarioItem = lancamentosDiario[lancamentosDiario.item == codigoItem]
        #print(lancamentosDiarioItem)

        if not lancamentosDiarioItem.empty:
            #calculo do saldo de quantidade = atual+ent-sai
            #Nesse caso, 'df.loc' recupera uma célula no DataFrame uma vez que codigoItem é único em dfSaldoAtual
            qtdAtual = dfSaldoAtual.loc[dfSaldoAtual.item == codigoItem, 'qtd_inicio']
            #Nesse caso, 'df.iloc[0]' recupera o valor na célula recuperada acima
            qtdAtual = qtdAtual.iloc[0]

            qtdEnt = sum(lancamentosDiarioItem.quantidade[lancamentosDiarioItem.tipo_movimento == 'Ent'])
            qtdSai = sum(lancamentosDiarioItem.quantidade[lancamentosDiarioItem.tipo_movimento == 'Sai'])
            qtdFinal = qtdAtual+qtdEnt-qtdSai

            #calculo do saldo de valor = atual+ent-sai
            # Nesse caso, 'df.loc' recupera uma célula no DataFrame uma vez que codigoItem é único em dfSaldoAtual
            valorAtual = dfSaldoAtual.loc[dfSaldoAtual.item == codigoItem, 'valor_inicio']
            # Nesse caso, 'df.iloc[0]' recupera o valor na célula recuperada acima
            valorAtual = valorAtual.iloc[0]

            valorEnt = sum(lancamentosDiarioItem.valor[lancamentosDiarioItem.tipo_movimento == 'Ent'])
            valorSai = sum(lancamentosDiarioItem.valor[lancamentosDiarioItem.tipo_movimento == 'Sai'])
            valorFinal = valorAtual+valorEnt-valorSai

            #Guradando informaçoes nas listas de saida
            listaItem.append(codigoItem)
            listaData.append(date)
            listaQtdEnt.append(qtdEnt)
            listaValorEnt.append(valorEnt)
            listaQtdSai.append(qtdSai)
            listaValorSai.append(valorSai)
            listaQtdSaldoInicial.append(qtdAtual)
            listaQtdSaldoFinal.append(qtdFinal)
            listaValorSaldoInicial.append(valorAtual)
            listaValorSaldoFinal.append(valorFinal)

            #Atualizando qtd e valor para próximo looping
            dfSaldoAtual.loc[dfSaldoAtual.item == codigoItem, 'qtd_inicio'] = qtdFinal
            dfSaldoAtual.loc[dfSaldoAtual.item == codigoItem, 'valor_inicio'] = valorFinal


# preparando DataFrame para saida
dataSaida = {
    'Item': listaItem,
    'Data_do_lancamento': listaData,
    'Entradas_Qtd': listaQtdEnt,
    'Entradas_Valor': listaValorEnt,
    'Saidas_Qtd': listaQtdSai,
    'Saidas_Valor': listaValorSai,
    'Saldo_Inicial_Qtd': listaQtdSaldoInicial,
    'Saldo_Inicial_Valor': listaValorSaldoInicial,
    'Saldo_Final_Qtd': listaQtdSaldoFinal,
    'Saldo_Final_Valor': listaValorSaldoFinal,
}
# creating the DataFrame
dfSaida = pd.DataFrame(dataSaida)
#print(dfSaida.info())


#Altera pontos em vígulas e float em str
for i in ['Entradas_Qtd', 'Entradas_Valor', 'Saidas_Qtd', 'Saidas_Valor', 'Saldo_Inicial_Qtd', 'Saldo_Inicial_Valor',
          'Saldo_Final_Qtd', 'Saldo_Final_Valor']:
    dfSaida[i] = dfSaida[i].astype(str)
    dfSaida[i] = dfSaida[i].str.replace('.', ',')
##

# converting to CSV file
dfSaida.to_csv("MovtoDiariaItem.csv", encoding='utf-8')