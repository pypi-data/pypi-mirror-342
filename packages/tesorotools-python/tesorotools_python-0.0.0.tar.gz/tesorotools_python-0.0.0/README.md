# Especificación de un documento

## Generar los *assets* de un semanal (fase de transición)
1. Poner en la carpeta [debug](debug) el archivo [flash.feather](debug/flash.feather) generado por el *script* `generar_semanal.py` de `dev2`. Será necesario cambiar a la rama `semanal` con un `git switch semanal`. Recordar revertir este cambio.
2. `python -m tesorotools.convert`
3. `python -m tesorotools.main`

## Plantilla

- Debe ser un archivo `.yaml`
- Si no se especifica nada, el programa buscará un archivo llamado `template.yaml` en la carpeta desde donde se esté ejecutando. En caso de no encontrarlo, lanzará un error.

### Headline
*Opcional*. Consta de dos entradas, también *opcionales* `title` y `comment`.

#### Ejemplo
```yaml
headline:
  title: Apertura
  comment: El precio del chocolate con almendras se dispara
```

Se renderizará en el estilo `Title` o `Título` del documento base de word proporcionado.

### Introduction
*Opcional*. Consta de dos entradas, también *opcionales* `date` y `hour`.

- `date`: Fecha en formato `AAAA-MM-DD`, con o sin comillas.
- `hour`: Hora en formato `HH:MM`, **siempre** entre comillas.

#### Ejemplo
```yaml
introduction:
  date: 2025-01-31
  hour: "15:30"
```

La fecha se renderizará en el estilo `Subtitle` o `Subtítulo` del documento base de word proporcionado.

# Descripción de la estructura y el funcionamiento

## Funcionamiento
- Se *leen* las plantillas del documento.
- Una vez leídas sabemos:
  - Qué es lo que hay que descargar, de dónde y con qué fechas.
  - Qué es lo que hay que calcular a partir de lo descargado y cómo.
- Descarga *missing*
  - Debe haber una opción *debug*, así como opción de no descargar y tomar directamente de nuestra bbdd.
- Cálculo o *prerrenderizado*: se generan las imágenes de los gráficos así como los archivos necesarios para renderizar las tablas en su formato final.
- *Renderizado* final.

## Sistema de lectura de archivos `.yaml`
El informe a generar se describe mediante unas *plantillas*, que en la práctica son archivos `.yaml`, con lo que es importante entender cómo el programa procede a la lectura de los mismos.

Todo archivo `.yaml` debe leerse a través de la función `utils.config.read_config`. Esta toma como parámetros el path al fichero a leer y un *cargador*. Siempre que se vaya a leer una *plantilla*, este cargador debe ser `utils.config.CustomLoader`, en caso contrario, puede dejarse en blanco.

En el proceso de lectura, el documento completo se representa como un objeto de tipo `MappingNode` y este es el parámetro `node` en la función `construct_mapping`.

Cada `MappingNode` contiene un atributo `value`, que en una lista de tuplas `(key_node, value_node)`

Dentro de un documento `.yaml` sencillo como
```yaml
clave1: "valor1"
```

La lista `value` solo tiene una tupla en su interior, donde:
- La clave o `key_node` es de tipo `ScalarNode` con tag `tag:yaml.org,2002:str` *implícito* y valor `clave1`.
- El valor o `value_node` también es de tipo `ScalarNode` con valor `valor1`.

En casos más complejos como
```yaml
clave2: !offset_table
  subclave: "subvalor"
``` 

De nuevo, la lista `value` solo contendrá una tupla en su interior, donde:
- La clave es un `ScalarNode` con valor `clave2`
- El valor es un `MappingNode` con *tag* personalizado `!offset_table`. Su valor a su vez en una lista de tuplas bla bla bla (se ve la recursividad)

## Informes
- Un *informe* (*Report*) es una **clase** que contiene un diccionario de *contenidos* (*Content*)
- Un *cotenido* (*Content*) es un **protocolo** que permite consultar y modificar su *nivel de anidamiento* así como construirse a partir de un archivo `.yaml`.
- Un informe puede *rederizarse* a un documento word a partir de una **plantilla**. Sencillamente, renderizará todos sus componentes uno por uno.