import pandas as pd
import streamlit as st
from PIL import Image
import os

# Aquí cargamos los datos desde un archivo CSV que contiene toda la información de los productos.
# Nos aseguramos de que el archivo llamado 'basedatos.csv' esté en la misma carpeta que este script.
data = pd.read_csv('basedatos.csv')

# En esta línea, limpiamos los nombres de las columnas para evitar problemas con espacios adicionales.
# Usamos el método `str.strip()` para quitar espacios al inicio y al final de los nombres de las columnas.
data.columns = data.columns.str.strip()

# Aquí convertimos los nombres de las columnas a minúsculas con `str.lower()` para trabajar con ellas de manera uniforme.
# Esto ayuda a evitar errores al escribir los nombres de las columnas en el código.
data.columns = data.columns.str.lower()

# En esta sección, creamos un espacio en la sesión para guardar los productos seleccionados para comparar.
# Usamos la variable `st.session_state` para que los datos se mantengan incluso si la página se actualiza.
if "productos_seleccionados" not in st.session_state:
    st.session_state["productos_seleccionados"] = []

# En esta línea, agregamos un título principal a la aplicacion para que el usuario sepa de qué trata.
st.title("GLOWUP Lab")

# En la barra lateral, colocamos encabezados y filtros para que los usuarios puedan buscar productos de forma personalizada.
st.sidebar.header("Filtros")

# Creamos un filtro para que los usuarios puedan seleccionar una marca de la lista.
# Usamos dropna() para asegurarnos de que no aparezcan valores nulos, y añadimos "Todos" como opción inicial.
marca = st.sidebar.selectbox("Seleccionar marca", options=["Todos"] + data["marca"].dropna().unique().tolist())

# Creamos un filtro para el tipo de piel. Esto permite a los usuarios buscar productos adecuados para sus necesidades.
tipo_piel = st.sidebar.selectbox("Seleccionar tipo de piel", options=["Todos"] + data["tipo de piel"].dropna().unique().tolist())

# Aquí añadimos un filtro para seleccionar el momento de aplicacion del producto: día, noche o ambos.
aplicacion = st.sidebar.selectbox("Seleccionar aplicacion", options=["Todos"] + data["aplicacion"].dropna().unique().tolist())


# Usamos un deslizador para que los usuarios puedan filtrar productos dentro de un rango de precios.
# Primero extraemos los valores numéricos de la columna 'precio', los convertimos a flotantes y luego definimos el rango.
rango_precio = st.sidebar.slider(
    "Seleccionar rango de precio", 
    min_value=0, 
    max_value=int(data["precio"].str.extract(r'(\d+)', expand=False).astype(float).max()), 
    value=(0, 3000)  # Valor inicial del deslizador.
)

# En esta sección, filtramos los productos según los criterios seleccionados por el usuario.
productos_filtrados = data.copy()  # Hacemos una copia del DataFrame original para mantener los datos originales intactos.

# Si el usuario selecciona una marca específica, aquí filtramos los productos para mostrar solo los que pertenecen a esa marca.
if marca != "Todos":
    productos_filtrados = productos_filtrados[productos_filtrados["marca"] == marca]

# Filtramos por tipo de piel si el usuario selecciona algo diferente a "Todos".
if tipo_piel != "Todos":
    productos_filtrados = productos_filtrados[productos_filtrados["tipo de piel"] == tipo_piel]

# Filtramos por aplicacion (día, noche o ambos) según la elección del usuario.
if aplicacion != "Todos":
    productos_filtrados = productos_filtrados[productos_filtrados["aplicacion"] == aplicacion]

# Convertimos los valores de la columna 'precio' en numéricos para poder aplicar el filtro del rango de precios.
productos_filtrados["precio_num"] = productos_filtrados["precio"].str.extract(r'(\d+)', expand=False).astype(float)

# Aplicamos el filtro del rango de precios para mostrar solo los productos dentro del rango seleccionado.
productos_filtrados = productos_filtrados[
    (productos_filtrados["precio_num"] >= rango_precio[0]) & 
    (productos_filtrados["precio_num"] <= rango_precio[1])
]

# Mostramos los productos que cumplen con los filtros seleccionados.
st.header("Productos filtrados")
if not productos_filtrados.empty:  # Verificamos si hay productos para mostrar.
    for index, row in productos_filtrados.iterrows():  # Iteramos sobre cada producto filtrado.
        # Aquí mostramos información detallada de cada producto.
        st.subheader(row["nombre del producto"])  # Nombre del producto como encabezado.
        st.write(f"**Marca:** {row['marca']}")  # Mostramos la marca.
        st.write(f"**Producto:** {row['producto']}")  # Tipo de producto, por ejemplo: limpiador, serum.
        st.write(f"**Precio:** {row['precio']}")  # Mostramos el precio del producto.
        st.write(f"**Tipo de piel:** {row['tipo de piel']}")  # Compatibilidad con el tipo de piel.
        st.write(f"**aplicacion:** {row['aplicacion']}")  # Momento del día recomendado para usarlo.
        st.write(f"**Cantidad:** {row['contenido']}")  # Cantidad del producto (por ejemplo: 200 ml).
        st.write(f"**Textura:** {row['textura']}")  # Textura del producto (ligera, media, pesada).
        st.write(f"**Vegano:** {row['vegano']}")  # Indicamos si el producto es vegano.
        st.write(f"**Libre de crueldad:** {row['libre de crueldad']}")  # Indicamos si el producto es libre de crueldad animal.
        st.write(f"**Efecto a largo plazo:** {row['efecto a largo plazo']}")  # Resultados esperados.
        st.write(f"[Comprar aquí]({row['enlaces']})")  # Agregamos un enlace para comprar el producto.

        # Mostramos la imagen del producto si desde la carpeta 'fotoscremas'.
        # Verificamos que la columna 'fotos' contenga el nombre de la imagen.
        if not pd.isna(row["fotos"]):  # Nos aseguramos de que la columna 'fotos' no esté vacía.
            image_path = os.path.join("fotoscremas", row["fotos"])  # Construimos la ruta completa de la imagen.
            if os.path.isfile(image_path):  # Verificamos si la imagen existe en la carpeta.
                st.image(image_path, caption=row["nombre del producto"], use_column_width=True)  # Mostramos la imagen.

        # Añadimos un botón para que el usuario pueda seleccionar este producto para comparar.
        if st.button(f"Seleccionar {row['nombre del producto']} para comparar", key=f"select_{index}"):
            # Verificamos si el producto ya fue seleccionado para evitar duplicados.
            if row["nombre del producto"] not in st.session_state["productos_seleccionados"]:
                st.session_state["productos_seleccionados"].append(row["nombre del producto"])  # Añadimos el producto.
                st.success(f"{row['nombre del producto']} añadido para comparar.")  # Mostramos un mensaje de confirmación.
else:
    # Si no hay productos que cumplan con los filtros, mostramos un mensaje de advertencia.
    st.warning("No se encontraron productos con los filtros seleccionados.")

st.write("---")  # Agregamos una línea divisoria para organizar visualmente las secciones.

# Mostramos los productos seleccionados para comparación.
st.header("Comparar productos seleccionados")
if st.session_state["productos_seleccionados"]:  # Verificamos si hay productos seleccionados.
    # Filtramos el DataFrame original para incluir solo los productos seleccionados.
    seleccionados = data[data["nombre del producto"].isin(st.session_state["productos_seleccionados"])]
    # Mostramos las columnas relevantes para comparar.
    st.write(seleccionados[["nombre del producto", "precio", "tipo de piel", "efecto a largo plazo"]])
    
    # Agregamos un botón para limpiar la lista de productos seleccionados.
    if st.button("Limpiar selección"):
        st.session_state["productos_seleccionados"] = []  # Limpiamos la lista.
else:
    # Si no hay productos seleccionados, mostramos un mensaje informativo.
    st.info("No hay productos seleccionados para comparar.")
