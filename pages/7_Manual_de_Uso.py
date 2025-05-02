import streamlit as st

st.set_page_config(page_title="Manual de Uso", layout="wide")

st.title("📘 Manual de Uso de Dashboards – Dark Kitchen")

st.markdown("""

---

### 1. 📈 **Dashboard de Tráfico**
**Objetivo:** Monitorear el comportamiento del cliente desde que ve la tienda hasta que realiza una orden, únicamente para Uber Eats.

**Filtros disponibles:**  
- Por tienda o marca  
- Por rango de fechas

**Secciones clave:**  
- Impresiones (veces que se muestra la tienda)  
- Vistas de producto  
- Órdenes generadas  
- Tasa de conversión

**Uso recomendado:** Detectar si una marca tiene buena visibilidad pero baja conversión, lo que indica posibles problemas de precios, imágenes o descripciones.

---

### 2. 📊 **Comparador de Métricas (Ventas, Pauta, Órdenes)**
**Objetivo:** Comparar el rendimiento de ventas, pauta y pedidos por tienda o plataforma.

**Filtros disponibles:**  
- Por marca  
- Por plataforma (Uber, Didi, Rappi)  
- Por rango de fechas

**Secciones clave:**  
- Ventas ($)  
- Inversión en pauta ($)  
- Órdenes (#)  
- ROAS

**Uso recomendado:** Evaluar el impacto de la pauta. Reasignar presupuesto según el retorno de inversión.

---

### 3. 😡 **Dashboard de Quejas**
**Objetivo:** Visualizar los comentarios negativos y calificaciones por semana en Uber y Didi.

**Filtros disponibles:**  
- Por plataforma  
- Por semana

**Secciones clave:**  
- Texto de las quejas  
- Número total de quejas  
- Calificación promedio

**Uso recomendado:** Leer comentarios para detectar patrones repetitivos y aplicar mejoras operativas.

---

### 4. 📦 **Dashboard de Inventario (Uso de Ingredientes)**
**Objetivo:** Ver el consumo total de ingredientes, no inventario en tiempo real.

**Filtros disponibles:**  
- Solo por ingrediente  
- Por rango de fechas

**Secciones clave:**  
- Cantidad consumida (gramos, ml, piezas, según el ingrediente)  
- Porcentaje del total  
- Tendencias semanales

**Uso recomendado:** Planear compras y evaluar si un ingrediente debe mantenerse en el menú.

---

### 5. 🛒 **Dashboard de Ventas x Producto**
**Objetivo:** Analizar el desglose de ventas por producto, incluyendo unidades, ingresos y márgenes.

**Filtros disponibles:**  
- No hay filtro por tienda o marca

**Secciones clave:**  
- Producto  
- Unidades vendidas  
- Ventas totales ($)  
- Margen bruto  
- Ordenamiento por unidades, ingresos o margen

**Uso recomendado:** Detectar productos estrella, ajustar precios o eliminar productos con baja rentabilidad.

---

### 📥 Carga de Datos – Tráfico & Conversión (Solo Uber Eats)

Sigue estos pasos cuidadosamente para subir correctamente los datos al dashboard:

#### ✅ Paso 1: Descargar la información desde Uber Eats Manager

1. Ingresa a [https://restaurant.uber.com](https://restaurant.uber.com) con tus credenciales.
2. En el menú lateral, haz clic en **Operaciones**.
3. Selecciona la tienda correspondiente y define el **rango de fechas**.
4. Desliza hacia abajo hasta encontrar las secciones de **Tráfico**.
5. Descarga **uno por uno** los datos de cada marca

---

#### ✅ Paso 2: Unifica la información en un solo archivo Excel

1. Abre un nuevo archivo en Excel.
2. Copia la información descargada y forma una **tabla con el siguiente formato exacto (nombres y orden obligatorios):**

"marca | semana | fecha_inicio | fecha_fin | trafico | vieron_menu | agregaron_articulos | pedidos_realizados | conversion"

3. **Formato de fechas obligatorio:**  
   - Las columnas `fecha_inicio` y `fecha_fin` deben estar en formato `YYYY-MM-DD` (ejemplo: 2025-04-21).

4. Llena manualmente los campos `marca` y `semana`.

---

#### ✅ Paso 3: Guardar el archivo

- Guarda el archivo como **Libro de Excel (.xlsx)**.
- Usa este nombre exactamente:  
  ➤ `Semana##_Trafico` (Ejemplo: `Semana18_Trafico.xlsx`)

---

#### ✅ Paso 4: Subir el archivo al dashboard

1. Entra al dashboard y ve a la página de **Subir Datos**.
2. Ubica el apartado **Tráfico**.
3. Haz clic en **"Browse Files"** (Buscar archivo).
4. Selecciona el archivo que acabas de crear.
5. Haz clic en **"Abrir"**, luego presiona el botón **"Subir Trafico&Conversion"**.
6. Si todo es correcto, aparecerá una **ventana verde de éxito**.

---

#### ⚠️ Errores comunes a evitar:

- ❌ El archivo **no se cargará** si las columnas están mal escritas, fuera de orden o con nombres diferentes.
- ❌ El formato de fecha debe ser exactamente `YYYY-MM-DD`.
- ❌ No modifiques el botón ni cambies el nombre de archivo especificado.

---


### 📥 Carga de Datos – Bitácora de Cambios

Sigue estos pasos cuidadosamente para subir correctamente los cambios semanales registrados por el área comercial:

#### ✅ Paso 1: Solicitar la bitácora

- Contacta al **encargado de asuntos comerciales** y pídele la **bitácora de cambios** correspondiente a la última semana.

---

#### ✅ Paso 2: Crear el archivo en Excel

1. Abre un archivo nuevo de Excel.
2. Crea una tabla **(sin formato de tabla de Excel)** con exactamente las siguientes columnas, en este orden:

"fecha | semana | plataforma | marca | accion"


3. Llena los datos proporcionados por el área comercial.
4. **Formato obligatorio de fecha:**  
   - La columna `fecha` debe estar en formato `YYYY-MM-DD` (ejemplo: 2025-04-21).

---

#### ✅ Paso 3: Guardar el archivo

- Guarda el archivo como **Libro de Excel (.xlsx)**.
- Asigna el nombre exacto siguiente:  
  ➤ `Semana##_Bitacora` (Ejemplo: `Semana18_Bitacora.xlsx`)

---

#### ✅ Paso 4: Subir el archivo al dashboard

1. Entra al dashboard y ve a la página de **Subir Datos**.
2. Ubica el apartado **Bitácora**.
3. Haz clic en el botón **"Browse files"** (Buscar archivos).
4. Selecciona el archivo que acabas de crear.
5. Haz clic en **"Abrir"** y luego en el botón **"Subir Bitacora"**.
6. Si todo está correcto, aparecerá una **ventana verde indicando registro exitoso**.

---

#### ⚠️ Errores comunes a evitar:

- ❌ El archivo **no se cargará** si los nombres de columna están mal escritos o en otro orden.
- ❌ El formato de fecha debe ser exactamente `YYYY-MM-DD`.
- ❌ No utilices el formato de tabla de Excel (solo tabla sencilla sin formato).

---

Después de subir el archivo exitosamente, regresa al **Dashboard de Tráfico**. La información de la bitácora deberá aparecer ya reflejada en los registros.

---

## 📥 Carga de Datos – Dashboard Metrics (Salud de la Marca)

Este módulo permite cargar las métricas clave semanales para cada marca y plataforma. Sigue los pasos con precisión para evitar errores en la carga:

---

#### ✅ Paso 1: Llenar el archivo de **Salud de la Marca**

- Completa primero tu análisis interno con base en los datos de ventas, pauta y órdenes por marca.
- Calcula también el **ticket promedio** si aplica.

---

#### ✅ Paso 2: Crear el archivo en Excel

1. Abre un nuevo archivo de Excel.
2. Crea una tabla con exactamente las siguientes columnas y en este orden:

---

"marca | plataforma | semana | tipo | valor"

- En la columna **tipo** se deben usar solo estos valores:  
  ➤ `ventas`, `pauta`, `ordenes`, `ticket_promedio`  
  (Es obligatorio escribirlos **tal cual**, sin errores ni variaciones)

3. Ingresa los valores correspondientes por marca y plataforma.

---

#### ✅ Paso 3: Guardar el archivo

- Guarda el archivo como **Libro de Excel (.xlsx)**.
- Asigna el nombre exacto:  
  ➤ `Semana##_SDLM` (Ejemplo: `Semana18_SDLM.xlsx`)

---

#### ✅ Paso 4: Subir el archivo al dashboard

1. Entra al dashboard y ve a la página **Subir Datos**.
2. Dirígete al apartado **Dashboard Metrics**.
3. Haz clic en **"Browse files"**.
4. Selecciona tu archivo `Semana##_SDLM.xlsx`.
5. Haz clic en **"Abrir"** y luego en **"Subir Dashboard Metrics"**.
6. Si todo está correcto, aparecerá un **recuadro verde indicando éxito**.

---

#### 🔄 Paso 5: Verifica los datos en el Dashboard Comparador

- Una vez subido el archivo con éxito, regresa al dashboard llamado **"Comparador"**.
- Ahí verás reflejados los nuevos datos cargados y confirmados en la base.

---

#### ⚠️ Errores comunes a evitar:

- ❌ El archivo no se procesará si los valores en la columna `tipo` no coinciden exactamente con los permitidos.
- ❌ El orden de columnas debe ser exactamente el especificado.
- ❌ No modifiques el nombre del archivo, debe seguir el formato `Semana##_SDLM`.

---

### 📥 Carga de Datos – Retención de Usuarios (User Retention)

Esta sección permite cargar los datos semanales de retención de usuarios por plataforma. Asegúrate de seguir cada paso correctamente para que la carga funcione sin errores.

---

#### ✅ Paso 1: Llenar el apartado de **Retención de Usuarios** en Salud de la Marca

- Recopila los datos de usuarios **nuevos**, **frecuentes** y el cálculo de **retención** desde el análisis interno.
- Organiza la información por marca y plataforma.

---

#### ✅ Paso 2: Crear el archivo en Excel

1. Abre un nuevo archivo de Excel.
2. Crea una tabla con las siguientes columnas, en este orden exacto:

"marca | plataforma | semana | pedidos | nuevos | frecuentes | retencion"

- Plataforma debe ser: `uber`, `didi` o `rappi`.

3. Llena los datos correspondientes por marca y semana.

---

#### ✅ Paso 3: Guardar el archivo

- Guarda el archivo como **Libro de Excel (.xlsx)**.
- Nómbralo así exactamente:  
  ➤ `Semana##_Retencion` (Ejemplo: `Semana18_Retencion.xlsx`)

---

#### ✅ Paso 4: Subir el archivo al dashboard

1. Entra al dashboard y ve a la sección **Subir Datos**.
2. Dirígete al apartado **User Retention**.
3. Haz clic en el botón **"Browse files"**.
4. Selecciona tu archivo `Semana##_Retencion.xlsx`.
5. Haz clic en **"Abrir"** y luego en **"Subir Retención"**.
6. Si todo está correcto, aparecerá un **recuadro verde indicando éxito**.

---

#### 🔄 Paso 5: Verifica los datos en el Dashboard Comparador

- Después de subir el archivo, ve al dashboard **"Comparador"**.
- Ahí verás reflejada la información nueva de retención de usuarios, actualizada y cargada en la base.

---

#### ⚠️ Errores comunes a evitar:

- ❌ Si la columna `plataforma` no tiene los valores exactos (`uber`, `didi`, `rappi`), la carga fallará.
- ❌ No cambies el nombre de las columnas ni el orden.
- ❌ El nombre del archivo debe ser exactamente `Semana##_Retencion`.

---


### 📥 Carga de Datos – Quejas por Órdenes (Uber Eats)

Este módulo permite cargar las quejas específicas ligadas a pedidos en Uber Eats. Es más detallado y requiere varios pasos, por lo que se recomienda hacerlo con cuidado.

---

#### ✅ Paso 1: Descargar los reportes desde Uber Eats Manager

1. Entra a [https://restaurant.uber.com](https://restaurant.uber.com) con tus credenciales.
2. Dirígete al apartado **Reportes**.
3. Genera dos reportes nuevos:
   - **Historial de pedidos**
     - Selecciona **todas las tiendas**.
     - Define el rango de fechas deseado.
     - Descarga el archivo en Excel.
   - **Reseñas de clientes**
     - Usa el **mismo rango de fechas**.
     - Descarga también en Excel.

---

#### ✅ Paso 2: Preparar el archivo combinado

1. Abre ambos archivos en Excel.
2. Crea una **nueva hoja** llamada:  
   ➤ `Semana##_QuejasUber` (Ejemplo: `Semana18_QuejasUber`)
3. En esa hoja, crea una tabla con exactamente los siguientes nombres y orden de columnas:

orden_id | fecha | hora | turno | marca | plataforma | tiene_queja | categoria | motivo_queja | comentario

4. Usa fórmulas de Excel (ej. `BUSCARV`, `XLOOKUP`, etc.) para:
   - Detectar si una orden del historial tiene una queja en el archivo de reseñas.
   - Extraer **categoría**, **motivo de la queja** y **comentario**.
   - Completa el campo `tiene_queja` como `sí` o `no`.

---

#### ✅ Paso 3: Guardar el archivo

- Guarda el archivo como **Libro de Excel (.xlsx)**.
- Asegúrate de mantener la hoja con el nombre `Semana##_QuejasUber`.

---

#### ✅ Paso 4: Subir el archivo al dashboard

1. Entra al dashboard y ve a la sección **Subir Datos**.
2. Dirígete al apartado **Quejas Órdenes**.
3. Haz clic en **"Browse files"**.
4. Selecciona el archivo que contiene la hoja `Semana##_QuejasUber`.
5. Haz clic en **"Abrir"** y luego en **"Subir Quejas"**.
6. Si todo está correcto, verás un **recuadro verde indicando éxito**.

---

#### 🔄 Paso 5: Verifica los datos en el Dashboard de Quejas

- Ve al dashboard **"Quejas"**.
- Revisa que los datos nuevos ya estén cargados y visibles en la tabla y gráficas.

Repetir proceso para DIDI
---

#### ⚠️ Errores comunes a evitar:

- ❌ No respetar el nombre y orden exacto de las columnas.
- ❌ No nombrar correctamente la hoja como `Semana##_QuejasUber`.
- ❌ No completar correctamente los campos de quejas (usando fórmulas de Excel).

---

📲 **¿Tienes dudas?**
- Puedes mandar mensaje de WhatsApp al **322 139 6141**.
- O consultar directamente la **tabla `quejas_ordenes`** en la base de datos SQL para ver el formato requerido.

---

### 📥 Carga de Datos – Inventario (Uso de Ingredientes)

Este módulo permite cargar el uso de ingredientes descargado desde Toteat, específicamente del apartado de carnes. Sigue los pasos exactamente para evitar errores en el proceso.

---

#### ✅ Paso 1: Descargar el archivo desde Toteat

1. Entra a [https://toteat.com](https://toteat.com) con tus credenciales.
2. Dirígete al apartado **Stock Control** y entra a **Ingredientes y Recetas**.
3. En la parte de filtros:
   - En **“Ingrediente”**, selecciona la categoría **CARNE**.
   - Elige el **rango de fechas** deseado.
4. Marca la opción **“Sin Formato (Activar si desea Exportar a Excel)”**.
5. Haz clic en el botón de descarga rojo con flecha hacia abajo que dice **“.xls”**.

---

#### ✅ Paso 2: Formatear el archivo

1. Abre el archivo descargado en Excel.
2. Agrega **dos columnas nuevas al inicio**:
   - `fecha_inicio`  
   - `fecha_final`
3. Llena esas columnas con las fechas exactas del rango seleccionado.
   - **Formato obligatorio:** `YYYY-MM-DD` (ejemplo: 2025-05-01)

4. Verifica que el orden y nombre de columnas sea exactamente el siguiente:

fecha_inicio | fecha_final | codigo | ingrediente | cantidad | medida | costo

---

#### ✅ Paso 3: Guardar el archivo

- Guarda el archivo como **Libro de Excel (.xlsx)**.
- Nómbralo exactamente así:  
  ➤ `Semana##_Inventario` (Ejemplo: `Semana18_Inventario.xlsx`)

---

#### ✅ Paso 4: Subir el archivo al dashboard

1. Ve a la página **Subir Datos** en el dashboard.
2. Dirígete al apartado **Inventario**.
3. Haz clic en **"Browse files"**.
4. Selecciona tu archivo `Semana##_Inventario.xlsx`.
5. Haz clic en **"Abrir"** y luego en **"Subir Inventario"**.
6. Si todo está correcto, verás una **ventana verde confirmando el éxito**.

---

#### 🔄 Paso 5: Verifica los datos en el Dashboard de Inventario

- Regresa al dashboard **“Inventario”**.
- Ahí podrás ver reflejados los datos nuevos de uso de ingredientes actualizados.

---

#### ⚠️ Errores comunes a evitar:

- ❌ No agregar `fecha_inicio` y `fecha_final` al inicio del archivo.
- ❌ Fechas en formato incorrecto (deben ser `YYYY-MM-DD`).
- ❌ Nombres y orden de columnas mal escritos.

---

### 📥 Carga de Datos – Ventas x Producto

Este módulo permite cargar los datos de ventas por producto descargados desde Toteat. El formato y orden de columnas es obligatorio para que la carga funcione correctamente.

---

#### ✅ Paso 1: Descargar el reporte desde Toteat

1. Entra a [https://toteat.com](https://toteat.com) con tus credenciales.
2. Dirígete al apartado **Reportes**.
3. Selecciona el **rango de fechas** que deseas analizar.
4. Ubica la tabla llamada **Ventas x Producto**.
5. Haz clic en el botón **“Sumar productos y extras”**.
6. Activa la opción **“Sin Formato”**.
7. Descarga el archivo en formato **`.xls`** (botón rojo con flecha hacia abajo).

---

#### ✅ Paso 2: Formatear el archivo

1. Abre el archivo descargado en Excel.
2. Agrega **dos columnas al inicio** con los siguientes nombres:
   - `fecha_inicio`  
   - `fecha_final`

3. Llena esas columnas con las fechas del rango seleccionado.
   - **Formato obligatorio:** `YYYY-MM-DD`

4. Reordena y nombra las columnas del archivo en este orden exacto:

fecha_inicio | fecha_final | id | producto | cantidad | valor_venta | descuentos | costos

---

#### ✅ Paso 3: Guardar el archivo

- Guarda el archivo como **Libro de Excel (.xlsx)**.
- Asigna el siguiente nombre exacto:  
  ➤ `Semana##_VentasxProducto` (Ejemplo: `Semana18_VentasxProducto.xlsx`)

---

#### ✅ Paso 4: Subir el archivo al dashboard

1. Ve al dashboard y entra a la sección **Subir Datos**.
2. Dirígete al apartado **Ventas x Producto**.
3. Haz clic en **"Browse files"**.
4. Selecciona tu archivo `Semana##_VentasxProducto.xlsx`.
5. Haz clic en **"Abrir"** y luego en **"Subir Ventas x Producto"**.
6. Si el registro fue exitoso, verás una **ventana verde de confirmación**.

---

#### 🔄 Paso 5: Verifica los datos en el Dashboard de Ventas x Producto

- Ve al dashboard **"Ventas x Producto"**.
- Verifica que los datos nuevos ya estén reflejados y visibles.

---

#### ⚠️ Errores comunes a evitar:

- ❌ No agregar correctamente las columnas `fecha_inicio` y `fecha_final`.
- ❌ Usar formato de fecha distinto a `YYYY-MM-DD`.
- ❌ No respetar el orden y nombres exactos de las columnas.

---


""")






