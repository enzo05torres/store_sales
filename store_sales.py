# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%
df = pd.read_csv('Data.csv')

# %%
df.head(10)

# %%
df.shape

# %%
df.describe()

# %%
df.info()

# %%
df = df.drop(columns=["store_id"])

# %%
item_column = df['item']
df = df.drop(columns=['item'])
df.columns = pd.to_datetime(df.columns, format='%Y/%m')
df = df.sort_index(axis=1)
df.columns = df.columns.strftime('%Y/%m')
df['item'] = item_column

# %%
df["item"].value_counts()

# %%
vd_mes = df.drop('item', axis=1).sum()
plt.figure(figsize=(10,6))
sns.lineplot(x=vd_mes.index, y=vd_mes.values,
            linewidth=2, marker='o'
)
plt.grid(True)
plt.title('Total de Vendas por Mês')
plt.xlabel('Meses')
plt.ylabel('Total de Vendas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
ocorr_item = df['item'].value_counts().reset_index()
ocorr_item.columns = ['item', 'ocorrencias']
plt.figure(figsize=(10, 6))
sns.barplot(x='item', y='ocorrencias', data=ocorr_item, palette="viridis")
plt.title('Número de Ocorrências por Item')
plt.ylabel('Ocorrências')
plt.xlabel('Item')
plt.xticks(rotation=45) 
plt.show()

# %%
vend_item = df.groupby('item').sum().sum(axis=1).reset_index()
vend_item.columns = ['item', 'total_vendas']
plt.figure(figsize=(10, 6))
sns.barplot(x='item', y='total_vendas', data=vend_item, palette="viridis")
plt.title('Total de Vendas por Item')
plt.ylabel('Total de Vendas')
plt.xlabel('Item')
plt.xticks(rotation=45)
plt.show()

# %%
monthly_sales = df.groupby('item').sum().T
monthly_sales.plot(kind='bar', figsize=(12, 8), width=0.9)
plt.title('Total de Vendas por Item em Cada Mês')
plt.xlabel('Meses')
plt.ylabel('Total de Vendas')
plt.xticks(rotation=45)
plt.legend(title='Item')
plt.tight_layout()
plt.show()

# %%
monthly_counts = df.groupby('item').count().T
monthly_counts.plot(kind='bar', figsize=(12, 8), width=0.9)
plt.title('Número de Vendas por Item em Cada Mês')
plt.xlabel('Meses')
plt.ylabel('Número de Vendas')
plt.xticks(rotation=45)
plt.legend(title='Item')
plt.tight_layout()
plt.show()

# %%
ocorrencias_por_item = df['item'].value_counts().reset_index()
ocorrencias_por_item.columns = ['item', 'ocorrencias']

plt.figure(figsize=(10, 6))
sns.barplot(x='item', y='ocorrencias', data=ocorrencias_por_item, palette="viridis")
plt.title('Número de Ocorrências por Item')
plt.ylabel('Ocorrências')
plt.xlabel('Item')
plt.xticks(rotation=45) 
plt.show()

# %%
df2 = pd.melt(df, id_vars=['item'], var_name='data', value_name='price')
df2['data'] = pd.to_datetime(df2['data'], format='%Y/%m')

# %%
plt.figure(figsize=(12, 8))
sns.lineplot(data=df2, x='data', y='price', hue='item')
plt.xticks(rotation=45)
plt.show()

# %%
df2.set_index('data', inplace=True)
df2 = df2.groupby('data')['price'].sum()
df_cum = df2.cumsum()

# %%
df_melted = df.melt(id_vars=['item'], var_name='Month', value_name='Sales')
df_melted['Month'] = pd.to_datetime(df_melted['Month'], format='%Y/%m')

monthly_sales = df_melted.groupby('Month')['Sales'].sum()

monthly_growth_rate = monthly_sales.pct_change() * 100

plt.figure(figsize=(10, 6))

plt.plot(monthly_sales.index, monthly_growth_rate, 
marker='o', linestyle='--', color='b', label='Crescimento Mensal (%)')
plt.axhline(0, color='black', linestyle='-', lw=1)  

plt.title('Crescimento Percentual de Vendas entre os Meses')
plt.xlabel('Mês')
plt.ylabel('Crescimento (%)')
plt.grid(True)
plt.legend()

plt.show()

print("Taxa de Crescimento Mensal (%)")
print(monthly_growth_rate)

# %%

items_sold = df_melted.groupby('Month')['item'].count() 

ticket_medio = monthly_sales / items_sold

plt.figure(figsize=(10, 6))

plt.plot(ticket_medio.index, ticket_medio, marker='o', 
linestyle='-', color='green', label='Ticket Médio')
plt.title('Evolução do Ticket Médio por Mês')
plt.xlabel('Mês')
plt.ylabel('Ticket Médio (Valor Médio por Item)')
plt.grid(True)
plt.legend()

plt.show()

print("Ticket Médio por Mês:")
print(ticket_medio)

# %%
