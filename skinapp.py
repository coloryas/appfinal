import pandas as pd
import streamlit as st

# Cargamos los datos desde el archivo CSV.
data = pd.read_csv('basedatos.csv')

# Limpiamos los nombres de las columnas del DataFrame.
data.columns = data.columns.str.strip()
data.columns = data.columns.str.lower()

# Espacio para comparar productos seleccionados
if "productos_seleccionados" not in st.session_state:
    st.session_state["productos_seleccionados"] = []

st.title("Explorador de Productos")

# Filtros interactivos
st.sidebar.header("Filtros")
marca = st.sidebar.selectbox("Seleccionar marca", options=["Todos"] + data["marca"].dropna().unique().tolist())
tipo_piel = st.sidebar.selectbox("Seleccionar tipo de piel", options=["Todos"] + data["tipo de piel"].dropna().unique().tolist())
aplicacion = st.sidebar.selectbox("Seleccionar aplicación", options=["Todos"] + data["aplicación"].dropna().unique().tolist())
libre_crueldad = st.sidebar.selectbox("¿Libre de crueldad?", options=["Todos", "Si", "No"])
rango_precio = st.sidebar.slider(
    "Seleccionar rango de precio", 
    min_value=0, 
    max_value=int(data["precio"].str.extract(r'(\d+)', expand=False).astype(float).max()), 
    value=(0, 1000)
)

# Filtrar productos según selección
productos_filtrados = data.copy()

if marca != "Todos":
    productos_filtrados = productos_filtrados[productos_filtrados["marca"] == marca]
if tipo_piel != "Todos":
    productos_filtrados = productos_filtrados[productos_filtrados["tipo de piel"] == tipo_piel]
if aplicacion != "Todos":
    productos_filtrados = productos_filtrados[productos_filtrados["aplicación"] == aplicacion]
if libre_crueldad != "Todos":
    productos_filtrados = productos_filtrados[productos_filtrados["libre de crueldad"] == libre_crueldad]
productos_filtrados["precio_num"] = productos_filtrados["precio"].str.extract(r'(\d+)', expand=False).astype(float)
productos_filtrados = productos_filtrados[
    (productos_filtrados["precio_num"] >= rango_precio[0]) & 
    (productos_filtrados["precio_num"] <= rango_precio[1])
]

# Mostrar productos filtrados
st.header("Productos filtrados")
if not productos_filtrados.empty:
    for index, row in productos_filtrados.iterrows():
        st.subheader(row["nombre del producto"])
        st.write(f"**Marca:** {row['marca']}")
        st.write(f"**Producto:** {row['producto']}")
        st.write(f"**Precio:** {row['precio']}")
        st.write(f"**Tipo de piel:** {row['tipo de piel']}")
        st.write(f"**Aplicación:** {row['aplicación']}")
        st.write(f"**Efecto a largo plazo:** {row['efecto a largo plazo']}")
        st.write(f"**Libre de crueldad:** {row['libre de crueldad']}")  # Nueva información añadida
        st.write(f"[Comprar aquí]({row['enlaces']})")
        
        # Botón para seleccionar producto para comparar
        if st.button(f"Seleccionar {row['nombre del producto']} para comparar", key=f"select_{index}"):
            if row["nombre del producto"] not in st.session_state["productos_seleccionados"]:
                st.session_state["productos_seleccionados"].append(row["nombre del producto"])
                st.success(f"{row['nombre del producto']} añadido para comparar.")
else:
    st.warning("No se encontraron productos con los filtros seleccionados.")

st.write("---")

# Mostrar productos seleccionados para comparar
st.header("Comparar productos seleccionados")
if st.session_state["productos_seleccionados"]:
    seleccionados = data[data["nombre del producto"].isin(st.session_state["productos_seleccionados"])]
    st.write(seleccionados[["nombre del producto", "precio", "tipo de piel", "efecto a largo plazo", "libre de crueldad"]])
    if st.button("Limpiar selección"):
        st.session_state["productos_seleccionados"] = []
else:
    st.info("No hay productos seleccionados para comparar.")
