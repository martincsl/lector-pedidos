import pandas as pd
import pdfplumber
import streamlit as st

def display_pdf(uploaded_file):
    data = []
    numero_pedidos = 0
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            numero_pedidos=numero_pedidos+1
            text = page.extract_text()
            lines = text.split('\n')
            pedido_actual = {}
            subtotal = 0
            text=page.extract_text()
            subtotal=0
            pedido_actual = {}
            for row in text.split('\n'):
                if row.startswith("Sucursal:"):
                    words = row.split()
                    nombre_suc = " ".join(words[2:])
                    pedido_actual['Nombre Sucursal']=nombre_suc

                if row.startswith("Sucursal:"):
                    words = row.split()
                    codigo_suc = " ".join(words[1:2])
                    pedido_actual['Cod Sucursal']=codigo_suc    

                if row.startswith('Nro. Pedido:'):
                    pedido=row.split()[-1]
                    pedido_actual['Nro. Pedido']=pedido

                if row.startswith('Proveedor:'):
                    fecha_pedido=row.split()[-1]
                    pedido_actual['Fecha de Pedido']=fecha_pedido

                if row.startswith('Fecha Entrega:'):
                    fecha_entrega=row.split()[-1]
                    pedido_actual['Fecha de Entrega']=fecha_entrega

                if row.startswith('7842672000635'):
                    cantidad=row.split()[-4]
                    string_cantidad =  cantidad.replace(".", "").replace(",", ".", 1)
                    cantidad_int=float(string_cantidad)
                    precio=row.split()[-1]
                    string_precio = precio.replace(".", "").replace(",", ".", 1)
                    precio_float = float(string_precio) 
                    subtotal=subtotal+precio_float
                    pedido_actual['Ajo']=cantidad_int

                if row.startswith('7842672000550'):
                    cantidad=row.split()[-4]
                    string_cantidad = cantidad.replace(".", "").replace(",", ".", 1)
                    cantidad_int=float(string_cantidad)
                    precio=row.split()[-1]
                    string_precio = precio.replace(".", "").replace(",", ".", 1)
                    precio_float = float(string_precio) 
                    subtotal=subtotal+precio_float
                    pedido_actual['Ajo y Perejil']=cantidad_int

            if subtotal > 0:
                pedido_actual['Costo Total'] = subtotal

            if pedido_actual:
                data.append(pedido_actual)
                pedido_actual = {}

    orden_columnas=['Fecha de Pedido','Cod Sucursal','Nro. Pedido','Nombre Sucursal','Ajo','Ajo y Perejil','Costo Total']
    df_pedidos = pd.DataFrame(data)
    df_pedidos=df_pedidos.fillna(0)
    df_pedidos = df_pedidos.reindex(columns=orden_columnas)
    df_pedidos.to_excel('output.xlsx', sheet_name='PedidosBigie', index=False)

    return df_pedidos

with st.container(height=800):    
    st.header("El conversor chevere de Raul")
    uploaded_file = st.file_uploader("Elija el archivo .pdf de Biggie", type="pdf")
    if uploaded_file is not None:
        result=display_pdf(uploaded_file)
        with open('output.xlsx', 'rb') as file:
            st.download_button(
                label="Bajar archivo Excel",
                data=file,
                file_name="output.xlsx",
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )    
        st.write(result)


