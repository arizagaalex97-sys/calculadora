import sympy as sp
import base64
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#para descargar documentos
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet
#esto es de limites

def calcular_limite(expresion, valor, direccion='+'):
    x = sp.symbols('x')
    try:
        f = sp.sympify(expresion)
        if not f.free_symbols.issubset({x}):            
         if direccion == "ambos":
            return sp.limit(f, x, valor)
        return sp.limit(f, x, valor, dir=direccion)
    except:
        return None
def calcular_derivada(exprecion):
    x=sp.symbols('x')
    f=sp.sympify(exprecion)
    return sp.diff(f,x)
def es_indeterminado(limite):
    return (limite.is_zero) or (abs(limite).is_infinite)
 #l,Hopital
def aplicar_lhopital(num_str,den_str,valor,max_iter=3):
    x = sp.symbols('x')
    f = sp.sympify(num_str)
    g = sp.sympify(den_str)
    for i in range(max_iter):
        # 1. Verificar si el límite es 0/0 o inf/inf
        lim_f = sp.limit(f, x, valor)
        lim_g = sp.limit(g, x, valor)
        if (lim_f == 0 and lim_g == 0) or (abs(lim_f).is_infinite and abs(lim_g).is_infinite):
            # 2. Aplicar derivada
            f = sp.diff(f, x)
            g = sp.diff(g, x)
        else:
            break
    resultado = sp.limit(f / g, x, valor)
    return f, g, resultado
#Integral por partes
def integrar_por_partes(u_str, dv_str):
    x = sp.symbols('x')
    u = sp.sympify(u_str)
    dv = sp.sympify(dv_str)
    
    du = sp.diff(u,x)
    v = sp.integrate(dv, x)
    #resultado: uv - integrate(v*du)
    
    integral_parte = sp.integrate(v*du,x)
    resultado= (u*v) - integral_parte
    return u,dv,du,v,resultado
def set_bg_local(file_path):
    with open(file_path, "rb") as f:
        img_bytes = f.read()
    encoded = base64.b64encode(img_bytes).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
def graficar_funcion(expresion, rango=(-10, 10)):
    x = sp.symbols('x')
    f = sp.sympify(expresion)
    f_num = sp.lambdify(x, f, 'numpy')

    x_vals = np.linspace(rango[0], rango[1], 400)
    y_vals = f_num(x_vals)
    #parte garfica
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    ax.set_title(f"Gráfica de f(x) = {expresion}")
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    
    return fig    
def validar_funcion(expr_texto):
    x, y = sp.symbols('x y')

    permitidos = {
        'x': x,
        'y': y,
        'sin': sp.sin,
        'cos': sp.cos,
        'tan': sp.tan,
        'asin': sp.asin,
        'acos': sp.acos,
        'atan': sp.atan,
        'exp': sp.exp,
        'log': sp.log,
        'sqrt': sp.sqrt,
        'pi': sp.pi,
        'E': sp.E
    }

    try:
        expr = sp.sympify(expr_texto, locals=permitidos)

        if expr.free_symbols - {x, y}:
            raise ValueError(
                "Solo se permiten las variables x e y."
            )

        return expr

    except Exception:
        raise ValueError(
            "Expresión inválida. Use únicamente funciones matemáticas válidas."
        )
def graficar_3d(funcion):
    x, y = sp.symbols('x y')

    expr = sp.sympify(funcion)

    f = sp.lambdify((x, y), expr, "numpy")

    X = np.linspace(-5, 5, 100)
    Y = np.linspace(-5, 5, 100)

    X, Y = np.meshgrid(X, Y)
    Z = f(X, Y)

    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, Z)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    return fig
def requiere_3d(expr_texto):
    x, y = sp.symbols('x y')

    try:
        expr = sp.sympify(expr_texto)

        return y in expr.free_symbols

    except:
        return False
def generar_pdf(nombre_pdf,
                titulo,
                pasos,
                resultado,
                imagen=None):

    doc = SimpleDocTemplate(nombre_pdf)

    estilos = getSampleStyleSheet()

    elementos = []

    elementos.append(
        Paragraph(titulo, estilos["Title"])
    )

    elementos.append(Spacer(1, 12))

    elementos.append(
        Paragraph("<b>Procedimiento:</b>",
                  estilos["Heading2"])
    )

    for paso in pasos:
        elementos.append(
            Paragraph(paso, estilos["BodyText"])
        )

    elementos.append(Spacer(1, 12))

    elementos.append(
        Paragraph(
            f"<b>Resultado:</b> {resultado}",
            estilos["BodyText"]
        )
    )

    if imagen:
        elementos.append(Spacer(1, 12))
        elementos.append(
            Image(imagen, width=400, height=250)
        )

    doc.build(elementos)
