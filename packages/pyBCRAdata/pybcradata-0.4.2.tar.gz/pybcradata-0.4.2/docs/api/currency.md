# Currency API

La API de divisas proporciona acceso a cotizaciones y tipos de cambio del BCRA.

## Método `currencies`

```python
client.currency.currencies(
    debug=False,
    json=False
)
```

Obtiene el catálogo maestro de divisas disponibles.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame`.

En caso de error del servidor (status_code != 200), se retornará el JSON de respuesta del servidor con el mensaje de error correspondiente.

### Ejemplos

#### Consulta básica: obtener todas las divisas disponibles

```python
df = client.currency.currencies()
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.currency.currencies(debug=True)
print(api_url)
```

## Método `rates`

```python
client.currency.rates(
    fecha=None,
    debug=False,
    json=False
)
```

Obtiene las cotizaciones de todas las divisas para una fecha específica.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `fecha` | `str` | Fecha en formato YYYY-MM-DD | No |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame`.

En caso de error del servidor (status_code != 200), se retornará el JSON de respuesta del servidor con el mensaje de error correspondiente.

### Ejemplos

#### Consulta básica: obtener cotizaciones del día

```python
df = client.currency.rates(fecha="2024-01-01")
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.currency.rates(fecha="2024-01-01", debug=True)
print(api_url)
```

## Método `series`

```python
client.currency.series(
    moneda=None,
    fechadesde=None,
    fechahasta=None,
    debug=False,
    json=False
)
```

Obtiene la serie histórica de cotizaciones para una divisa específica.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `moneda` | `str` | Código de la divisa (ej: "USD", "EUR") | Si |
| `fechadesde` | `str` | Fecha de inicio (YYYY-MM-DD) | No |
| `fechahasta` | `str` | Fecha final (YYYY-MM-DD) | No |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame`.

En caso de error del servidor (status_code != 200), se retornará el JSON de respuesta del servidor con el mensaje de error correspondiente.

### Ejemplos

#### Consulta básica: obtener serie completa

```python
df = client.currency.series(moneda="USD")
print(df.head())
```

#### Con filtros de fecha

```python
df = client.currency.series(
    moneda="USD",
    fechadesde="2023-01-01",
    fechahasta="2023-12-31"
)
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.currency.series(moneda="USD", debug=True)
print(api_url)
```

### Notas

- La validación de parámetros (tipos, formatos, etc.) es gestionada por el paquete.
- Los errores del servidor (status_code != 200) se manejan devolviendo el JSON de respuesta del servidor.
- Las fechas deben estar en formato YYYY-MM-DD.
- El código de moneda debe ser un código válido de divisa.

## Divisas Comunes

Algunas divisas comunes:

| Código | Descripción |
|--------|-------------|
| USD | Dólar Estadounidense |
| EUR | Euro |
| BRL | Real Brasileño |
| GBP | Libra Esterlina |
| JPY | Yen Japonés |


# Currency API (English Version)

The Currency API provides access to exchange rates and foreign currency quotations from the BCRA.

## Method `currencies`

```python
client.currency.currencies(
    debug=False,
    json=False
)
```

Retrieves the master catalog of available currencies.

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|-----------|
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns the data as JSON instead of a DataFrame | No |

### Return

By default, returns a `pandas.DataFrame`.

If a server error occurs (status_code != 200), the returned value will be the server's JSON response with the corresponding error message.

### Examples

#### Basic query: retrieve all available currencies

```python
df = client.currency.currencies()
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.currency.currencies(debug=True)
print(api_url)
```

## Method `rates`

```python
client.currency.rates(
    fecha=None,
    debug=False,
    json=False
)
```

Retrieves the exchange rates for all currencies on a specific date.

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|-----------|
| `fecha` | `str` | Date in YYYY-MM-DD format | No |
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns the data as JSON instead of a DataFrame | No |

### Return

By default, returns a `pandas.DataFrame`.

If a server error occurs (status_code != 200), the returned value will be the server's JSON response with the corresponding error message.

### Examples

#### Basic query: retrieve exchange rates for a specific day

```python
df = client.currency.rates(fecha="2024-01-01")
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.currency.rates(fecha="2024-01-01", debug=True)
print(api_url)
```

## Method `series`

```python
client.currency.series(
    moneda=None,
    fechadesde=None,
    fechahasta=None,
    debug=False,
    json=False
)
```

Retrieves the historical series of exchange rates for a specific currency.

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|-----------|
| `moneda` | `str` | Currency code (e.g., "USD", "EUR") | Yes |
| `fechadesde` | `str` | Start date (YYYY-MM-DD) | No |
| `fechahasta` | `str` | End date (YYYY-MM-DD) | No |
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns the data as JSON instead of a DataFrame | No |

### Return

By default, returns a `pandas.DataFrame`.

If a server error occurs (status_code != 200), the returned value will be the server's JSON response with the corresponding error message.

### Examples

#### Basic query: retrieve complete series

```python
df = client.currency.series(moneda="USD")
print(df.head())
```

#### With date filters

```python
df = client.currency.series(
    moneda="USD",
    fechadesde="2023-01-01",
    fechahasta="2023-12-31"
)
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.currency.series(moneda="USD", debug=True)
print(api_url)
```

### Notes

- Parameter validation (types, formats, etc.) is handled by the package.
- Server errors (status_code != 200) are handled by returning the server's JSON response.
- Dates must be in YYYY-MM-DD format.
- The currency code must be a valid currency identifier.

## Common Currencies

Some common currencies:

| Code | Description |
|------|-------------|
| USD | US Dollar |
| EUR | Euro |
| BRL | Brazilian Real |
| GBP | British Pound Sterling |
| JPY | Japanese Yen |
