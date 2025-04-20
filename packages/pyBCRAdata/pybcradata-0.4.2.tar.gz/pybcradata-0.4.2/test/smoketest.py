from pyBCRAdata import BCRAclient

client = BCRAclient()

switch = False

df_1 = client.monetary.series(id_variable=6, debug=switch)
df_2 = client.monetary.variables(debug=switch)
df_3 = client.monetary.series(id_variable=6, desde='2023-01-01', hasta='2023-01-31', limit=12, offset=2, debug=switch)

df_4 = client.currency.currencies(debug=switch)
df_5 = client.currency.rates(fecha='2023-01-17', debug=switch)
df_6 = client.currency.series(moneda='USD', fechadesde='2023-01-01', fechahasta='2023-02-01', limit=12, offset=2, debug=switch)

df_7 = client.debtors.debtors(identificacion='23409233449', debug=switch)

df_8 = client.checks.banks(debug=switch)
df_9 = client.checks.reported(codigo_entidad=11, numero_cheque=20377516, debug=switch)

df_10 = client.debtors.history(identificacion='23409233449', debug=switch)
df_11 = client.debtors.rejected(identificacion='23409233449', debug=switch)

print("DataFrame 1:")
print(df_1)
print("\nDataFrame 2:")
print(df_2)
print("\nDataFrame 3:")
print(df_3)
print("\nDataFrame 4:")
print(df_4)
print("\nDataFrame 5:")
print(df_5)
print("\nDataFrame 6:")
print(df_6)
print("\nDataFrame 7:")
print(df_7)
print("\nDataFrame 8:")
print(df_8)
print("\nDataFrame 9:")
print(df_9)
print("\nDataFrame 10:")
print(df_10)
print("\nDataFrame 11:")
print(df_11)
