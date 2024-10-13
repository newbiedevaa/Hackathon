import os
import io
import base64
import random
import json
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, flash, session

# Leer el archivo CSV y cargarlo en un DataFrame
df = pd.read_csv('usuarios.csv')

# Configuración de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Ruta principal que muestra el formulario de login
@app.route('/')
def home():
    return render_template('login2.html')

# Ruta para manejar el login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user_record = df[(df['usuario'] == username) & (df['contraseña'] == password)]

    if not user_record.empty:
        session['username'] = username
        return redirect(url_for('stats'))
    else:
        flash("Usuario o contraseña incorrectos")
        return redirect(url_for('home'))

# Ruta para las estadísticas de gastos del usuario
@app.route('/stats')
def stats():
    return render_template('stats.html', pie_chart=get_pie_chart_base64(), income_vs_expense_chart=get_income_vs_expense_chart_base64())

@app.route('/videos', methods=['GET'])
def index():
    # Lista de IDs de videos de YouTube del canal de Banorte
    videos = [
        "2Y6p9bvwVVg?feature=shared",  # Video 1
        "FsaRh4wrGFk?feature=shared",  # Video 2
        "Cmmv-GR1o1M?feature=shared",  # Video 3
        "bu2x9yqPWiA?feature=shared",  # Video 4
        "zSMnMiF5Jrk?feature=shared",  # Video 5
    ]
    return render_template('videos.html', videos=videos)

# Ruta para subir un PDF
# Funciones para generar gráficos...

# Generar la gráfica de pastel para los gastos mensuales y devolverla en base64
def get_pie_chart_base64():
    categories = ['Alquiler', 'Comida', 'Transporte', 'Entretenimiento', 'Otros']
    values = [random.randint(10, 30) for _ in categories]

    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
    explode = (0.1, 0, 0, 0, 0)
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(values, explode=explode, labels=categories, colors=colors, 
                                      autopct='%1.1f%%', startangle=90, pctdistance=0.85)

    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)

    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(10)

    ax.set_title('Distribución de Gastos Mensuales', fontsize=16)
    ax.axis('equal')
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

# Generar la gráfica de pastel para la comparación de ingresos y egresos y devolverla en base64
def get_income_vs_expense_chart_base64():
    categories = ['Ingresos', 'Egresos']
    values = [random.randint(40, 60), random.randint(20, 40)]
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(values, labels=categories, colors=['#66b3ff', '#ff9999'], 
                                      autopct='%1.1f%%', startangle=90, pctdistance=0.85)

    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)

    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(10)

    ax.set_title('Comparación de Ingresos vs Egresos', fontsize=16)
    ax.axis('equal')
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        
        if file.filename == '':
            return 'No selected file'
        
        if file and file.filename.endswith('.pdf'):
            # Leer el archivo y convertir a Base64
            pdf_data = file.read()
            pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
        
        #pdf_base64
        
        new_user = pd.DataFrame({
            'nombre': [name],
            'correo': [email],
            'usuario': [username],
            'contraseña': [password]
        })
        global df
        df = pd.concat([df, new_user], ignore_index=True)

        df.to_csv('usuarios.csv', index=False)

        flash("Registro exitoso. Puedes iniciar sesión.")
        return redirect(url_for('home'))

    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)