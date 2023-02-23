from flask import Flask
from flask import request
from flask import render_template
import forms 
from flask_wtf.csrf import CSRFProtect
from collections import Counter
from flask import make_response
from flask import flash




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

@app.route('/', methods=['GET', 'POST'])
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
    reg_traductor=forms.TraductorForm(request.form)
    datos=list()
    if request.method=='POST' and reg_traductor.validate():
        datos.append(reg_traductor.txtEspanol.data)
        datos.append(reg_traductor.txtIngles.data)
        f=open('Traductor.txt', 'a')
        f.write(str(datos[0])+"\n")
        f.write(str(datos[1])+"\n")
            
    return render_template("Traductor.html", form=reg_traductor, datos=datos)

# Resultado TRADUCTOR
@app.route("/TraductorR", methods=["GET","POST"])
def traductorR():
    if request.method=='POST':
        selTrad= (request.form.get("btnTraductor"))

        if(selTrad=="1"):
            s="La traduccion al español es: "
            return render_template("Traductor.html",s=s)

        elif(selTrad=="2"):
            s="La traduccion al ingles es: "
            return render_template("Traductor.html",s=s)

            
    return render_template("Traductor.html",s=s)



if __name__=="__main__":
    csrf.init_app(app)
    app.run(debug=True,port=3000)