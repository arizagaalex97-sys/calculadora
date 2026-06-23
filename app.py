import streamlit as st
from funcion import*
from streamlit_option_menu import option_menu
import os
set_bg_local("imagenes/fondo-de-pantalla-negro.png")

if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "menu"

# Mostrar menú principal
if st.session_state["selected_page"] == "menu":

    st.markdown(
        """
        <h1 style='text-align:center;'>
            📚 Calculadora de Cálculo
        </h1>
        <h4 style='text-align:center;'>
            Seleccione una opción
        </h4>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🧮 Calculadora",
            use_container_width=True
        ):
            st.session_state["selected_page"] = "Calculadora"
            st.rerun()

    with col2:
        if st.button(
            "📈 Gráficas 3D",
            use_container_width=True
        ):
            st.session_state["selected_page"] = "Graficas 3d"
            st.rerun()
        st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("imagenes/images.png", width=250)

    with col2:
        st.markdown("""
        ## Bienvenido

        Esta aplicación permite resolver problemas de cálculo diferencial e integral.

        ### Funciones disponibles
        - Límites
        - Regla de L'Hôpital
        - Integración por partes
        - Gráficas 2D
        - Gráficas 3D
        """)

    st.markdown("---")

    st.markdown("### Ejemplos")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.latex(r"\lim_{x\to0}\frac{\sin(x)}{x}")

    with col2:
        st.latex(r"\int x e^x\,dx")

    with col3:
        st.latex(r"f(x,y)=x^2+y^2")

    st.stop()

    st.stop()
st.title("CALCULADORA")

selected = st.session_state["selected_page"]
st.session_state["selected_page"] = selected
if selected == 'Calculadora': 
  if "opcion_actual" not in st.session_state:
        st.session_state["opcion_actual"] = "Limites"
  opcion = option_menu(None, ["Limites", "L Hopital", "Integracion por partes"], 
  icons=["bi bi-calculator", "bi bi-arrow-down-right","bi bi-card-checklist"], menu_icon="cast", default_index=0, orientation="horizontal") 
  opcion 
#Limites 
  if opcion == "Limites": 
    st.subheader("Calculadora de limites✌") 
    func_input = st.text_input("Ingrese la Funcion f(x): ", "sin(x)/x")
    valor=st.text_input("Tiende a: ","x") 
    dir_lim=st.selectbox("Direccion: ",["ambos","+","-"])
    if requiere_3d(func_input):
        st.info(
        "📈 La expresión contiene la variable 'y'. "
        "Se recomienda utilizar el módulo de Gráficas 3D."
         )
        st.success("📈 abra el graficador 3d")
        if st.button("🚀 Ir a Graficas 3D"):
    
          st.session_state["ultima_funcion"] = func_input
          st.session_state["selected_page"] = 'Graficas 3d'

          st.rerun()
    if st.button("Calcular"): 
      x = sp.symbols('x') 
      try:
       f = validar_funcion(func_input)
      except ValueError as e:
       st.error(f"❌ {e}")
       st.stop()
      val_num = float(valor) 
      st.write("### Procedimiento paso a paso") 
      st.latex(rf"\lim_{{x \to {val_num}}} {sp.latex(f)}")
      st.write("Sustituyendo el valor en la función:") 
      evaluacion = f.subs(x, val_num) 
      st.latex(rf"f({val_num}) = {sp.latex(evaluacion)}")
      resultado = sp.limit(f, x, val_num)
      st.write("Resultado final:") 
      st.latex(rf"\lim_{{x \to {val_num}}} {sp.latex(f)} = {sp.latex(resultado)}") 
      pasos = [
        f"Función: {func_input}",
        f"x tiende a {valor}",
        f"Sustitución: f({valor}) = {evaluacion}"
        ]
      generar_pdf("limite.pdf",
         "Calculadora de Limites",
       pasos,
       str(resultado),
       "grafica.png"
)
    if st.button("Graficar"):
      st.subheader("Visualizacion")
      figura = graficar_funcion(func_input)
      figura.savefig("grafica.png",
      bbox_inches="tight" )
      st.pyplot(figura)
      with open("limite.pdf", "rb") as archivo:

       st.download_button(
        "📄 Descargar PDF",
        archivo,
        file_name="limite.pdf",
        mime="application/pdf"
      )

#Lhopital
  if opcion == "L Hopital":
    st.subheader("Regla de L Hopital")
    num=st.text_input("Numerador f(x); ", "sin(x)")
    st.session_state["ultima_funcion"] = num
    den_input = st.text_input("Denominador g(x) (opcional): ", "x")
    den = den_input if den_input.strip() != "" else "1"
    val_input = st.text_input("Tiende a (número o 'infinito'): ", "0")
    if requiere_3d(num):
        st.info(
        "📈 Se detectó la variable 'y'. "
        "Para visualizar correctamente la función use Gráficas 3D."
        )
        st.success("📈 abra el graficador 3d")
         
        if st.button("🚀 Abrir Graficadora 3D"):
    
          st.session_state["ultima_funcion"] = num
          st.session_state["selected_page"] = 'Graficas 3d'

          st.rerun()
    
    if st.button("Aplicar L Hopital"):
      x = sp.symbols('x')
      try:
        f = validar_funcion(num)
        g = validar_funcion(den)
        if val_input.lower() == 'infinito':
            val_num = sp.oo
        else:
            val_num = float(val_input)
      except ValueError as e:
        st.error(f"❌ {e}")
        st.stop()
      st.write("Veririficacion de condiciones")
        #Validacion :v
      lim_num = sp.limit(f, x, val_num)
      lim_den = sp.limit(g, x, val_num)
        #procedimiento de la verificacion
      st.latex(rf"\lim_{{x \to {val_input}}} f(x) = {sp.latex(lim_num)}")
      st.latex(rf"\lim_{{x \to {val_input}}} g(x) = {sp.latex(lim_den)}")
        #verificacion de ideterminaciones
      
      if es_indeterminado(lim_num):
        st.success("Se ha confirmado una indeterminacion")
        
        
        #Proceso
        f_p,g_p,res=aplicar_lhopital(num,den,val_num)
        st.write("Procedimiento paso a paso: ")
        #Exprecion original
        st.latex(rf"\lim_{{x \to {val}}} \frac{{{sp.latex(f)}}}{{{sp.latex(g)}}}")
        st.write("Aplicamos la regla de L Hopital: ")
        #Mostramos las derivadas
        st.latex(rf"\frac{{f'(x)}}{{g'(x)}} = \frac{{{sp.latex(f_p)}}}{{{sp.latex(g_p)}}}")
        #Mostramos el resultado final 
        st.write("Resultado:")
        st.latex(rf"\lim_{{x \to {val}}} \frac{{{sp.latex(f_p)}}}{{{sp.latex(g_p)}}} = {sp.latex(res)}")
      
      
        pasos = [
          f"Numerador: {num}",
          f"Denominador: {den}",
          f"Limite numerador: {lim_num}",
          f"Limite denominador: {lim_den}",
          f"Derivada numerador: {f_p}",
          f"Derivada denominador: {g_p}",
          f"Resultado final: {res}"
          ]
        generar_pdf(
           "lhopital.pdf",
           "Regla de L'Hopital",
           pasos,
           str(res)
            )


      else:
           st.warning("El limite no resulta en 0/0. puede que la regla de l hopital no se aplique correctamente")   

    if st.button("Graficar Funciones"):
       try:
          validar_funcion(num)
          validar_funcion(den)
          st.subheader("Visualización")
          col1, col2 = st.columns(2)
          with col1:
            st.write("f(x)")
            figura_f = graficar_funcion(num)
            figura_f.savefig(
               "grafica_lhopital_f.png",
                bbox_inches="tight"
                )
            st.pyplot(figura_f)

          with col2:
            st.write("g(x)")
            figura_g = graficar_funcion(den)
            figura_g.savefig(
              "grafica_lhopital_g.png",
               bbox_inches="tight"
                )
            st.pyplot(figura_g)

       except ValueError as e:
          st.error(f"❌ {e}")  
    if os.path.exists("lhopital.pdf"):
    
     with open("lhopital.pdf", "rb") as archivo:

        st.download_button(
            "📄 Descargar PDF",
            archivo,
            file_name="lhopital.pdf",
            mime="application/pdf"
        )   
#integracioj por partes
  if opcion == "Integracion por partes":
    st.subheader("Integracion por Partes")   
    u_input = st.text_input("Ingresa u: ", "x")
    st.session_state["ultima_funcion"] = u_input
    dv_input = st.text_input("Ingresa dv: ", "exp(x)")
    if requiere_3d(u_input):
        st.info(
        "📈 Se detectó una función de dos variables. "
        "Puede visualizarla mejor en el módulo de Gráficas 3D."
        
        )
        st.success("📈 abra el graficador 3d")
        
        if st.button("🚀 Abrir Graficadora 3D"):

          st.session_state["ultima_funcion"] = u_input
          st.session_state["selected_page"] = 'Graficas 3d'

          st.rerun()
    
    
    if st.button("Calcular"):
        try:
         validar_funcion(u_input)
         validar_funcion(dv_input)

        except ValueError as e:
         st.error(f"❌ {e}")
         st.stop()
        u,dv,du,v,res=integrar_por_partes(u_input, dv_input)
        st.write("### Procedimiento")
        #mostrar la formula 
        st.write("Identificación de componentes:")
        st.latex(rf"u = {sp.latex(u)}, \quad dv = {sp.latex(dv)} dx")
        #mostrar la derivada
        st.write("Derivando $u$ e integrando $dv$:")
        st.latex(rf"du = {sp.latex(du)} dx, \quad v = {sp.latex(v)}")
        #aplicar la formula
        st.write("3. Aplicando la fórmula $\\int u \\, dv = uv - \\int v \\, du$:")
        st.latex(rf"\int {sp.latex(u)} \cdot {sp.latex(dv)} dx = ({sp.latex(u)})({sp.latex(v)}) - \int ({sp.latex(v)})({sp.latex(du)}) dx")
        #resultado final
        st.write("### Resultado final:")
        st.latex(rf"= {sp.latex(res)} + C") 
        pasos = [
         f"u = {u}",
         f"dv = {dv}",
         f"du = {du}",
         f"v = {v}",
         f"Resultado = {res}"
         ]
        generar_pdf(
         "integracion.pdf",
         "Integracion por Partes",
        pasos,
        str(res)
         )     
    if st.button("Graficar Componentes"):
      try:
        validar_funcion(u_input)
        validar_funcion(dv_input)
        st.subheader("Visualización")
        col1, col2 = st.columns(2)
        with col1:
            st.write("u(x)")
            figura_u = graficar_funcion(u_input)
            figura_u.savefig(
                "grafica_u.png",
                bbox_inches="tight"
            )
            st.pyplot(figura_u)
        with col2:
            st.write("dv(x)")
            figura_dv = graficar_funcion(dv_input)
            figura_dv.savefig(
                "grafica_dv.png",
                bbox_inches="tight"
            )
            st.pyplot(figura_dv)
      except ValueError as e:

        st.error(f"❌ {e}")
    if os.path.exists("integracion.pdf"):
      with open("integracion.pdf", "rb") as archivo:

        st.download_button(
            "📄 Descargar PDF",
            archivo,
            file_name="integracion.pdf",
            mime="application/pdf"
      )        
  if st.button("⬅ Regresar al menú principal"):
    st.session_state["selected_page"] = "menu"
    st.rerun()
          
if selected=='Graficas 3d': 
    
    st.subheader("📈 Graficador 3D")

    funcion_3d = st.text_input(
        "Función f(x,y):",
        value=st.session_state.get(
            "ultima_funcion",
            "x**2 + y**2"
        )
    )

    if st.button("Graficar 3D"):

        try:
            figura = graficar_3d(funcion_3d)
            st.pyplot(figura)

        except Exception as e:
            st.error(f"❌ {e}")
    if st.button("⬅ Regresar al menú principal"):
       st.session_state["selected_page"] = "menu"
       st.rerun()
      