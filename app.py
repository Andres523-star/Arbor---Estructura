import streamlit as st
from anytree import Node, PreOrderIter, find_by_attr
from anytree.exporter import UniqueDotExporter

st.set_page_config(page_title="NORTE Store", layout="wide")

NOMBRE_RAIZ = "Catálogo Principal"

# --- Armo el arbol de prueba para que la app no arranque vacia ---
def crear_arbol_ejemplo():
    raiz = Node(NOMBRE_RAIZ, tipo="categoria")

    ropa = Node("Ropa", parent=raiz, tipo="categoria")
    hombre = Node("Hombre", parent=ropa, tipo="categoria")
    mujer = Node("Mujer", parent=ropa, tipo="categoria")

    tec = Node("Tecnología", parent=raiz, tipo="categoria")
    celulares = Node("Celulares", parent=tec, tipo="categoria")
    compus = Node("Computadores", parent=tec, tipo="categoria")

    hogar = Node("Hogar", parent=raiz, tipo="categoria")
    cocina = Node("Cocina", parent=hogar, tipo="categoria")
    deco = Node("Decoración", parent=hogar, tipo="categoria")

    datos = [
        (hombre, "Camiseta Oversize Algodón", 35.0),
        (hombre, "Chaqueta Denim Clásica", 89.0),
        (hombre, "Pantalón Chino Slim", 59.0),
        (mujer, "Vestido Lino Verano", 72.0),
        (mujer, "Blusa Satinada", 45.0),
        (mujer, "Jean Mom Fit", 64.0),
        (celulares, "Smartphone Aurora X", 499.0),
        (compus, "Portátil Ultra 14", 899.0),
        (cocina, "Set de Cuchillos Chef", 58.0),
        (deco, "Lámpara de Mesa Minimal", 39.0),
    ]
    for cat_padre, nombre, precio in datos:
        Node(nombre, parent=cat_padre, tipo="producto", precio=precio)

    return raiz

if "raiz" not in st.session_state:
    st.session_state.raiz = crear_arbol_ejemplo()
if "carrito" not in st.session_state:
    st.session_state.carrito = 0

raiz = st.session_state.raiz

def todos_los_nodos():
    return list(PreOrderIter(raiz))

def lista_categorias():
    return [n for n in todos_los_nodos() if n.tipo == "categoria"]

def lista_productos():
    return [n for n in todos_los_nodos() if n.tipo == "producto"]

def nombre_existe(nombre):
    return any(n.name.lower() == nombre.lower() for n in todos_los_nodos())

def con_sangria(nombre):
    nodo = find_by_attr(raiz, nombre)
    if nodo is None:
        return nombre
    return "— " * nodo.depth + nombre

def etiqueta_nodo(nombre):
    nodo = find_by_attr(raiz, nombre)
    if nodo is not None and nodo.tipo == "producto":
        return f"{nombre} (producto)"
    return con_sangria(nombre)

def calcular_metricas():
    nodos = todos_los_nodos()
    peso = len(nodos)
    altura = raiz.height + 1
    grado = max(len(n.children) for n in nodos)
    return peso, altura, grado

def guardar_mensaje(tipo, texto):
    st.session_state.mensaje = (tipo, texto)
    st.rerun()

def agregar_al_carrito():
    st.session_state.carrito += 1
    st.toast("Producto agregado al carrito")

# --- Estilos ---
def html(texto):
    limpio = "\n".join(l.strip() for l in texto.splitlines() if l.strip())
    st.markdown(limpio, unsafe_allow_html=True)

html("""
<style>
html, body, [class*="css"], .stApp {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    background-color: #ffffff;
    color: #111111;
}
header[data-testid="stHeader"] { display: none; }
.block-container { max-width: 1200px; padding-top: 0.5rem; }

.nav { display: flex; align-items: center; justify-content: space-between;
       padding: 18px 0; border-bottom: 1px solid #e5e5e5; margin-bottom: 28px; }
.logo { font-size: 26px; font-weight: 800; letter-spacing: 6px; }
.menu a { margin: 0 18px; font-size: 13px; letter-spacing: 2px; color: #111;
          text-decoration: none; font-weight: 500; }
.iconos { display: flex; gap: 20px; align-items: center; }
.iconos svg { width: 22px; height: 22px; stroke: #111; fill: none; stroke-width: 1.7; }
.carrito { position: relative; }
.badge { position: absolute; top: -8px; right: -10px; background: #000; color: #fff;
         font-size: 10px; border-radius: 50%; width: 17px; height: 17px;
         display: flex; align-items: center; justify-content: center; }

.foto { width: 100%; border-radius: 2px; background: #f3f3f3; }
.titulo { font-size: 38px; font-weight: 700; line-height: 1.15; margin: 0 0 8px 0; }
.estrellas { color: #111; font-size: 16px; letter-spacing: 2px; }
.estrellas span { color: #777; font-size: 13px; letter-spacing: 0; margin-left: 8px; }
.precio { margin: 16px 0 22px 0; display: flex; align-items: center; gap: 12px; }
.precio-nuevo { font-size: 28px; font-weight: 700; }
.precio-viejo { font-size: 18px; color: #888; text-decoration: line-through; }
.descuento { background: #000; color: #fff; font-size: 12px; padding: 4px 9px;
             letter-spacing: 1px; }
.etiqueta { font-size: 12px; letter-spacing: 2px; font-weight: 600; margin: 18px 0 8px 0; }
.colores { display: flex; gap: 12px; }
.color { width: 30px; height: 30px; border-radius: 50%; border: 1px solid #ccc; }
.color.sel { outline: 2px solid #000; outline-offset: 3px; }
.tallas { display: flex; gap: 10px; margin-bottom: 24px; }
.talla { width: 48px; height: 48px; border: 1px solid #ccc; display: flex;
         align-items: center; justify-content: center; font-size: 14px; }
.talla.sel { background: #000; color: #fff; border-color: #000; }

div[data-testid="stButton"] button,
div[data-testid="stFormSubmitButton"] button {
    background: #000; color: #fff; border: 1px solid #000; border-radius: 0;
    height: 52px; font-size: 14px; letter-spacing: 2px; font-weight: 600;
}
div[data-testid="stButton"] button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    background: #333; color: #fff; border-color: #333;
}

.seccion { font-size: 26px; font-weight: 700; margin: 50px 0 20px 0; }
.card img { width: 100%; background: #f3f3f3; }
.card .nombre { font-size: 15px; margin-top: 10px; }
.card .p { font-size: 15px; font-weight: 700; margin-top: 2px; }
</style>
""")

html(f"""
<div class="nav">
  <div class="logo">NORTE</div>
  <div class="menu"><a>HOME</a><a>SHOP</a><a>NEW ARRIVALS</a></div>
  <div class="iconos">
    <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="16" y1="16" x2="21" y2="21"/></svg>
    <svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></svg>
    <div class="carrito">
      <svg viewBox="0 0 24 24"><path d="M5 8h14l-1.2 12H6.2L5 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>
      <div class="badge">{st.session_state.carrito}</div>
    </div>
  </div>
</div>
""")

def url_foto(nombre, ancho=600, alto=750):
    semilla = sum(ord(c) for c in nombre)
    return f"https://picsum.photos/seed/{semilla}/{ancho}/{alto}"

def pagina_tienda():
    productos = lista_productos()
    if not productos:
        st.info("Todavía no hay productos. Agrega alguno en la pestaña de administración.")
        return

    nombres = [p.name for p in productos]
    elegido = st.selectbox("Ver producto", nombres, key="prod_sel")
    prod = find_by_attr(raiz, elegido)

    precio = prod.precio
    precio_viejo = round(precio / 0.8, 2)
    resenas = 40 + len(prod.name) * 7

    col_foto, col_info = st.columns(2, gap="large")

    with col_foto:
        html(f'<img class="foto" src="{url_foto(prod.name)}">')

    with col_info:
        html(f"""
        <div class="etiqueta">{prod.parent.name.upper()}</div>
        <h1 class="titulo">{prod.name}</h1>
        <div class="estrellas">★★★★☆<span>4.5 ({resenas} reseñas)</span></div>
        <div class="precio">
            <span class="precio-nuevo">${precio:,.2f}</span>
            <span class="precio-viejo">${precio_viejo:,.2f}</span>
            <span class="descuento">-20%</span>
        </div>
        <div class="etiqueta">COLOR</div>
        <div class="colores">
            <div class="color sel" style="background:#111"></div>
            <div class="color" style="background:#e8e2d6"></div>
            <div class="color" style="background:#3b5b7a"></div>
            <div class="color" style="background:#8a3b3b"></div>
        </div>
        <div class="etiqueta">TALLA</div>
        <div class="tallas">
            <div class="talla">XS</div><div class="talla">S</div>
            <div class="talla sel">M</div><div class="talla">L</div><div class="talla">XL</div>
        </div>
        """)
        st.button("ADD TO CART", width="stretch", on_click=agregar_al_carrito)

    tab_det, tab_mat, tab_envio = st.tabs(["Details", "Materials", "Shipping"])
    with tab_det:
        st.markdown(
            f"**{prod.name}** forma parte de la categoría *{prod.parent.name}*.\n\n"
            "- Corte moderno y cómodo para uso diario\n"
            "- Costuras reforzadas\n"
            "- Disponible en varios colores y tallas\n"
            "- Se ve bien con casi todo"
        )
    with tab_mat:
        st.markdown(
            "- 100% algodón (o material similar según el producto)\n"
            "- Lavar a máquina con agua fría\n"
            "- No usar blanqueador\n"
            "- Planchar a temperatura baja"
        )
    with tab_envio:
        st.markdown(
            "- Envío estándar de 3 a 5 días hábiles\n"
            "- Cambios gratis durante 30 días\n"
            "- Envío gratis en compras grandes"
        )

    hermanos = [p for p in prod.parent.children if p.tipo == "producto" and p is not prod]
    otros = [p for p in productos if p is not prod and p not in hermanos]
    relacionados = (hermanos + otros)[:4]

    html('<div class="seccion">You May Also Like</div>')
    cols = st.columns(4, gap="medium")
    for col, rel in zip(cols, relacionados):
        with col:
            html(f"""
            <div class="card">
                <img src="{url_foto(rel.name, 400, 500)}">
                <div class="nombre">{rel.name}</div>
                <div class="p">${rel.precio:,.2f}</div>
            </div>
            """)

def pagina_admin():
    if "mensaje" in st.session_state:
        tipo, texto = st.session_state.pop("mensaje")
        if tipo == "ok":
            st.success(texto)
        else:
            st.error(texto)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("Agregar categoría")
        with st.form("form_categoria", clear_on_submit=True):
            nombre_cat = st.text_input("Nombre de la categoría")
            cat_padre = st.selectbox(
                "Categoría padre",
                [c.name for c in lista_categorias()],
                format_func=con_sangria,
            )
            enviar_cat = st.form_submit_button("AGREGAR CATEGORÍA")

        if enviar_cat:
            try:
                nombre_cat = nombre_cat.strip()
                if nombre_cat == "":
                    st.error("Escribe un nombre para la categoría.")
                elif nombre_existe(nombre_cat):
                    st.error("Esa categoría ya existe, usa otro nombre.")
                else:
                    padre = find_by_attr(raiz, cat_padre)
                    Node(nombre_cat, parent=padre, tipo="categoria")
                    guardar_mensaje("ok", f"Categoría '{nombre_cat}' agregada en '{cat_padre}'.")
            except Exception as e:
                st.error(f"No se pudo agregar la categoría: {e}")

    with col2:
        st.subheader("Agregar producto")
        with st.form("form_producto", clear_on_submit=True):
            nombre_prod = st.text_input("Nombre del producto")
            precio_prod = st.number_input("Precio", min_value=0.0, step=1.0)
            cat_destino = st.selectbox(
                "Categoría",
                [c.name for c in lista_categorias()],
                format_func=con_sangria,
            )
            enviar_prod = st.form_submit_button("AGREGAR PRODUCTO")

        if enviar_prod:
            try:
                nombre_prod = nombre_prod.strip()
                if nombre_prod == "":
                    st.error("Escribe un nombre para el producto.")
                elif precio_prod <= 0:
                    st.error("El precio debe ser mayor que cero.")
                elif nombre_existe(nombre_prod):
                    st.error("Ya existe un nodo con ese nombre, usa otro.")
                else:
                    destino = find_by_attr(raiz, cat_destino)
                    Node(nombre_prod, parent=destino, tipo="producto", precio=precio_prod)
                    guardar_mensaje("ok", f"Producto '{nombre_prod}' agregado en '{cat_destino}'.")
            except Exception as e:
                st.error(f"No se pudo agregar el producto: {e}")

    st.divider()

    st.subheader("Eliminar")
    por_borrar = st.selectbox(
        "Selecciona qué eliminar (se borra todo lo que cuelga de ahí)",
        [n.name for n in todos_los_nodos()],
        format_func=etiqueta_nodo,
    )
    if st.button("ELIMINAR"):
        try:
            nodo = find_by_attr(raiz, por_borrar)
            if nodo.is_root:
                st.error("No se puede eliminar la raíz del catálogo.")
            else:
                cantidad = len(list(PreOrderIter(nodo)))
                nodo.parent = None
                st.session_state.pop("prod_sel", None)
                guardar_mensaje("ok", f"Se eliminó '{por_borrar}' ({cantidad} nodo(s) en total).")
        except Exception as e:
            st.error(f"No se pudo eliminar: {e}")

    st.divider()

    st.subheader("Métricas del árbol")
    peso, altura, grado = calcular_metricas()
    m1, m2, m3 = st.columns(3)
    m1.metric("Peso (total de nodos)", peso)
    m2.metric("Altura (niveles)", altura)
    m3.metric("Grado (máx. hijos directos)", grado)
    st.caption("Las métricas cuentan categorías y productos, porque los productos son nodos del árbol.")

    st.subheader("Visualización")
    if st.button("VER ÁRBOL DE CATEGORÍAS"):
        try:
            def atributos(nodo):
                nombre = nodo.name.replace('"', "'")
                if nodo.tipo == "categoria":
                    return f'label="{nombre}" shape=box style=filled fillcolor="#eeeeee"'
                return f'label="{nombre}\\n${nodo.precio:,.0f}" shape=ellipse'

            dot = "\n".join(UniqueDotExporter(raiz, nodeattrfunc=atributos))
            st.graphviz_chart(dot, width="stretch")
        except Exception as e:
            st.error(f"No se pudo generar el gráfico: {e}")

tab_tienda, tab_admin = st.tabs(["Tienda", "Administrar catálogo"])
with tab_tienda:
    pagina_tienda()
with tab_admin:
    pagina_admin()