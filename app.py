from flask import Flask
from flask import request
from flask import render_template
import forms 
from flask_wtf.csrf import CSRFProtect
from collections import Counter
from flask import make_response
from flask import flash
import math





app=Flask(__name__)
app.config['SECRET_KEY']="esta es una clave encriptada"
csrf = CSRFProtect()

@app.route("/formprueba")
def formprueba():
    return render_template("formprueba.html")

@app.route("/Alumnos", methods=["GET","POST"])
def alumnos():
    reg_alumn=forms.UserForm(request.form)
    datos=list()
    if request.method=='POST' and reg_alumn.validate():
        datos.append(reg_alumn.matricula.data)
        datos.append(reg_alumn.nombre.data)
        print(reg_alumn.matricula.data)
        print(reg_alumn.nombre.data)
    return render_template("Alumnos2.html",  form = reg_alumn, datos=datos)

@app.route('/Cajas', methods=['GET', 'POST'])
def caja():
    if request.method == 'GET':
        reg_form = forms.BoxForm()
        return render_template('cajasDinamicas.html', form=reg_form)
    else:
        reg_form = forms.BoxForm(request.form)
        return render_template('cajasDinamicas.html', form=reg_form)

# Cajas dinamicas
@app.route('/resultadoCajas', methods=['POST'])
def resultadoCajas():
    reg_form = forms.BoxForm(request.form)
    num = [int(number) for number in reg_form.num.data]
    cajasArreglo = []
    for valor in set(num):
        rep = len([num for num in num if num == valor])
        if rep > 1:
            cajasArreglo.append((valor, rep))
            
    resultadoMin=min(num)
    resultadoMax=max(num)
    resultadoPromedio=sum(num)/len(num)
    
    return render_template('resultadoCajasDinamicas.html',resultadoMin=resultadoMin,resultadoMax=resultadoMax, valores=num, resultadoPromedio=resultadoPromedio, cajasArreglo=cajasArreglo)


@app.route("/cookie", methods=['GET','POST'])
def cookie():
    reg_user=forms.LoginForm(request.form)
    response=make_response(render_template('cookie.html',form=reg_user))

    if request.method=='POST' and reg_user.validate():
        user=reg_user.username.data
        password=reg_user.password.data
        datos=user+'@'+password
        success_message='Bienvenido {}'.format(user)
        response.set_cookie('datos_usuario',datos)
        flash(success_message)
    return response




# TRADUCTOR
@app.route("/Traductor", methods=["GET","POST"])
def traductor():
    reg_traducto=forms.TraductorForm(request.form)
    datos=list()
    if request.method=='POST':
        if(reg_traducto.txtEspanol.data.lower()=="" and reg_traducto.txtIngles.data.lower()==""):
            rep="Debes ingresar el texto en español"
            return render_template("Traductor.html", form=reg_traducto, datos=datos, rep=rep)
        if(reg_traducto.txtIngles.data.lower()==""):
            rep1="Debes ingresar el texto en ingles"
            return render_template("Traductor.html", form=reg_traducto, datos=datos, rep1=rep1)
        else:
            datos.append(reg_traducto.txtEspanol.data.lower())
            datos.append(reg_traducto.txtIngles.data.lower())
            f=open('Traductor.txt', 'a')
            f.write(str(datos[0])+"\n")
            f.write(str(datos[1])+"\n")
            print(f)
            return render_template("TraductorR.html", form=reg_traducto, datos=datos)

    return render_template("Traductor.html", form=reg_traducto, datos=datos)

# Resultado TRADUCTOR
@app.route("/TraductorR", methods=["GET","POST"])
def traductorR():
    reg_traductor = forms.TraductorForm(request.form)
    if request.method=='POST':
        selTrad= (request.form.get("btnTraductor"))
        palabraT=str(reg_traductor.txtPalabra.data).lower()
        if(palabraT==""):
            ree="Debes ingresar la palabra a traducir"
            return render_template("TraductorR.html",form=reg_traductor, ree=ree)
        else:
            f=open('Traductor.txt', 'r')
            txtP = [linea.rstrip('\n') for linea in f]
            if(selTrad=="1"):
                for i in range(len(txtP)):
                    if(txtP[i-1]== (palabraT)):
                        textoE = txtP[i - 2]
                        s="La traduccion al español es: "+textoE.capitalize()
                        return render_template("TraductorR.html",s=s,form=reg_traductor)
                    else:
                        s="Lo sentimos esta palabra no fue encontrada: "+palabraT
                        return render_template("TraductorR.html",s=s,form=reg_traductor)
            elif(selTrad=="2"):
                for i in range(len(txtP)):
                    if(txtP[i-2] == palabraT):
                        textoE = txtP[i - 1]
                        s="La traduccion al ingles es: "+textoE.capitalize()
                        return render_template("TraductorR.html",s=s,form=reg_traductor)
                    else:
                        s="Lo sentimos esta palabra no fue encontrada: "+palabraT
                        return render_template("TraductorR.html",s=s,form=reg_traductor)
            else:
                r="Debes seleccionar el idioma a traducir"
                return render_template("TraductorR.html",form=reg_traductor, r=r)


    return render_template("TraductorR.html",form=reg_traductor)

def calcular_resistencia(banda1, banda2, banda3, tolerancia):

    valores = {
        "negro": 0,
        "marron": 1,
        "rojo": 2,
        "naranja": 3,
        "amarillo": 4,
        "verde": 5,
        "azul": 6,
        "violeta": 7,
        "gris": 8,
        "blanco": 9
    }
    english_names = {
        "negro": "black",
        "marron": "brown",
        "rojo": "red",
        "naranja": "orange",
        "amarillo": "yellow",
        "verde": "green",
        "azul": "blue",
        "violeta": "violet",
        "gris": "gray",
        "blanco": "white",
        "oro": "gold",
        "plata": "silver"
    }
    banda1_en = english_names[banda1]
    banda2_en = english_names[banda2]
    banda3_en = english_names[banda3]
    tolerancia_en = english_names[tolerancia]

    valor1 = valores[banda1]
    valor2 = valores[banda2]
    multiplicador = math.pow(10, valores[banda3])
    tolerancia_valor = 0.05 if tolerancia == "oro" else 0.1

    valor = (valor1 * 10 + valor2) * multiplicador
    valor_minimo = valor * (1 - tolerancia_valor)
    valor_maximo = valor * (1 + tolerancia_valor)

    return {
        "colorBanda1": banda1_en,
        "colorBanda2": banda2_en,
        "colorBanda3": banda3_en,
        "colorTolerancia": tolerancia_en,
        "banda1": banda1,
        "banda2": banda2,
        "banda3": banda3,
        "tolerancia": tolerancia,
        "valor": valor,
        "valor_minimo": valor_minimo,
        "valor_maximo": valor_maximo
    }


@app.route('/', methods=['GET'])
def index():
    form = forms.ResistenciaForm(request.form)

    with open("Resistencia.txt", "r") as f:
        valores_guardados = [line.strip().split(",") for line in f]

    resultados_guardados = []
    for valores in valores_guardados:
        if len(valores) == 4:
            resultado_guardado = calcular_resistencia(*valores)
            resultados_guardados.append(resultado_guardado)

    return render_template('resistencia.html', form=form, resultados_guardados=resultados_guardados)


@app.route('/', methods=['POST'])
def calcular():
    form =forms.ResistenciaForm(request.form)
    banda1 = request.form['banda1']
    banda2 = request.form['banda2']
    banda3 = request.form['banda3']
    tolerancia = request.form['tolerancia']

    resultado = calcular_resistencia(banda1, banda2, banda3, tolerancia)

    valores_guardados = []
    with open("Resistencia.txt", "r") as f:
        for line in f:
            valores = line.strip().split(",")
            if len(valores) == 4:
                resultado_guardado = calcular_resistencia(*valores)
                valores_guardados.append(resultado_guardado)
                print(valores_guardados)

    valores_guardados.append(resultado)

    with open("Resistencia.txt", "a") as f:
        f.write(",".join([banda1, banda2, banda3, tolerancia]) + "\n")

    return render_template('resistencia.html', resultado=resultado, form=form, valores_guardados=valores_guardados)


if __name__=="__main__":
    csrf.init_app(app)
    app.run(debug=True,port=3000)