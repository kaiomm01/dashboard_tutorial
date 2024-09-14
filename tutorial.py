from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel('Vendas.xlsx')

# Aqui o gráfico é criado
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

opcoes = list(df['ID Loja'].unique())
# Essas "opções" vão ser usadas no botão interativo
# para ilustrar como estão a venda de cada uma das lojas
opcoes.append('Todas as Lojas')

app.layout = html.Div(children=[
# Observe que o comando acima é uma lista
# O que implica, dessa forma, de que, como em uma lista,
# iremos colocar ',' após cada comando, como se cada
# comando fosse um item
    html.H1(children='Faturamento das lojas'),
    # H1 faz referência ao título

    html.H2(children = 'Gráfico com o faturamento de todos os produtos separados por loja'),
    # H2 faz referência a um subtítulo

    html.Div(children='''
        Obs: Esse gráfico mostra a quantidade de produtos vendidos, não o faturamento
    '''),
    # Div faz referência a um texto meno
    
    dcc.Dropdown(opcoes, value = 'Todas as Lojas', id = 'lista_lojas'),
    # Esse comando serve para configurar o botão interativo
    # "value" representa o valor padrão que irá aparecer
    #no botão. Este value é o mesmo que será 
    # posteriormente usado no callback
    #"id" é o nome que nós demos ao botão


    dcc.Graph(
        id='grafico_quantidade_vendas',
        figure=fig
    )
])

@app.callback(
    # O callback precisa, necessariamente de um Input e
    # de um Output. Observe que ambas foram importadas 
    # no código lá em cima

    Output('grafico_quantidade_vendas', 'figure'),
    # O Output representa o que iremos alterar, sempre se 
    # referenciando ao id. Dessa forma, se quisermos
    # alterar o gráfico, o primeiro parâmetro seria
    # o id "gráfico_quantidade_vendas", enquanto o
    # segundo parâmetro seria figure. Se formos alterar
    # um texto, por exemplo, faríamos
    # html.Div(id = 'texto', children = 'qualquer')
    # Onde o primeiro parầmetro seria o id "texto" e o
    # segundo seria "qualquer"

    Input('lista_lojas', 'value')
    # O Input representa o que queremos alterar, que nesse
    # caso é o botão lá em cima, o qual nós demos o id
    # 'lista_lojas'
)
def update_output(value):
    # única condição a ser respeitada aqui é que a ser
    # recebido é o segundo parãmetro do Input

    if value == 'Todas as Lojas':
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada = df.loc[df['ID Loja'] == value, :]
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")


    return fig

if __name__ == '__main__':
    app.run_server(debug=True)