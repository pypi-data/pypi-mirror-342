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

## Informes
- Un *informe* (*Report*) es una **clase** que contiene un diccionario de *contenidos* (*Content*)
- Un *cotenido* (*Content*) es un **protocolo** que permite consultar y modificar su *nivel de anidamiento* así como construirse a partir de un archivo `.yaml`.
- Un informe puede *rederizarse* a un documento word a partir de una **plantilla**. Sencillamente, renderizará todos sus componentes uno por uno.