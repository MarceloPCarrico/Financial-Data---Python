import matplotlib.pyplot as plt
import pandas as pd

# Importar tabela
df = pd.read_csv('financial.csv', sep=";")

# Limpar dados duplicados e nulos
df_clean = df.dropna().drop_duplicates()
df_clean = df_clean.rename(columns=lambda x: x.strip())

# Converter valores para floats uma vez que estão concatenados e não somados
df_clean["Gross Sales"] = df_clean['Gross Sales'].str.replace(',', '').astype(float)
df_clean["Profit"] = df_clean['Profit'].str.replace(',', '').astype(float)

# Adicionar uma coluna fictícia de mês para exemplo
df_clean['Month'] = pd.to_datetime(df_clean['Date']).dt.month_name()

# Criar uma figura para subplots
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(18, 12))
plt.subplots_adjust(hspace=0.8)  # Ajustar espaçamento vertical

# 1 Gráfico - Vendas por Ano 
axs[0, 0].pie(df_clean.groupby('Year')['Gross Sales'].sum(), labels=df_clean['Year'].unique(), autopct='%1.1f%%', startangle=90)
axs[0, 0].set_title('Vendas por Ano')

# 2 Gráfico - Vendas por Ano e Mês
vendas_por_ano_mes = df_clean.groupby(['Year', 'Month'])['Gross Sales'].sum().unstack()
vendas_por_ano_mes.plot(kind='bar', stacked=True, colormap='viridis', ax=axs[0, 1], rot=30)  # Ajusta a rotação dos rótulos
axs[0, 1].set_title('Vendas por Ano e Mês')

# 3 Gráfico - Lucro por Ano
lucro_por_ano = df_clean.groupby('Year')['Profit'].sum()
lucro_por_ano.plot(kind='bar', color='lightgreen', edgecolor='black', ax=axs[0, 2], rot=30)
axs[0, 2].set_title('Lucro por Ano')

# Adicionar mais espaço entre as linhas de gráficos
plt.subplots_adjust(hspace=0.5)

# 4 Gráfico - Top 5 Gross Sales por Cliente
top_vendas_cliente = df_clean.groupby('Segment')['Gross Sales'].sum().sort_values(ascending=False).head(5)
top_vendas_cliente.plot(kind='bar', color='skyblue', edgecolor='black', ax=axs[1, 0], rot=30)
axs[1, 0].set_title('Top 5 Gross Sales por Cliente')

# 5 Gráfico - Top 5 Produtos por Lucro
top_lucro_produto = df_clean.groupby('Product')['Profit'].sum().sort_values(ascending=False).head(5)
top_lucro_produto.plot(kind='bar', color='lightgreen', edgecolor='black', ax=axs[1, 1], rot=30)
axs[1, 1].set_title('Top 5 Produtos por Lucro')

# Remover os eixos não utilizados
axs[1, 2].axis('off')

# Ajustar o layout da figura
plt.tight_layout()
plt.show()
