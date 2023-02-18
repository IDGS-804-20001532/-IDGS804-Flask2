from flask import Flask
from flask import request
from flask import render_template
import forms 
from flask_wtf.csrf import CSRFProtect
from collections import Counter



app=Flask(__name__)
app.config['SECRET_KEY']="esta es una clave encriptada"
csrf = CSRFProtect()

@app.route("/formprueba")
def formprueba():
    return render_template("formprueba.html")

@app.route("/Alumnos", methods=["GET","POST"])
def alumnos():
    reg_alumn=forms.UserForm(request.form)
    if request.method=='POST':
        print(reg_alumn.matricula.data)
        print(reg_alumn.nombre.data)
    return render_template("Alumnos2.html",  form = reg_alumn)

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


if __name__=="__main__":
    csrf.init_app(app)
    app.run(debug=True,port=3000)