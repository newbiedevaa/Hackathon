import os 
import matplotlib.pyplot as plt
import io
import base64
import random
import json
from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd

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
    # Obtener datos del formulario
    username = request.form['username']
    password = request.form['password']
    
    # Validar usuario y contraseña a partir del DataFrame
    user_record = df[(df['usuario'] == username) & (df['contraseña'] == password)]

    if not user_record.empty:  # Si se encuentra un registro que coincide
        session['username'] = username
        return redirect(url_for('stats'))  # Redirige a la página de estadísticas
    else:
        flash("Usuario o contraseña incorrectos")  # Mensaje de error si las credenciales no son correctas
        return redirect(url_for('home'))  # Redirigir de nuevo al login si falla

# Ruta para las estadísticas de gastos del usuario
@app.route('/stats')
def stats():
    return render_template('stats.html', pie_chart=get_pie_chart_base64(), income_vs_expense_chart=get_income_vs_expense_chart_base64())

# Generar la gráfica de pastel para los gastos mensuales y devolverla en base64
def get_pie_chart_base64():
    categories = ['Alquiler', 'Comida', 'Transporte', 'Entretenimiento', 'Otros']
    values = [random.randint(10, 30) for _ in categories]  # Generar valores aleatorios para cada categoría

    # Colores personalizados para cada segmento
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
    
    # Explosión de los segmentos para mejorar visibilidad
    explode = (0.1, 0, 0, 0, 0)  # 'Alquiler' se separará un poco

    # Crear la gráfica de pastel
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(values, explode=explode, labels=categories, colors=colors, 
                                      autopct='%1.1f%%', startangle=90, pctdistance=0.85)

    # Dibujar el círculo para mejorar la estética
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)

    # Mejorar la visualización de las etiquetas y porcentajes
    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(10)

    # Añadir título a la gráfica
    ax.set_title('Distribución de Gastos Mensuales', fontsize=16)

    # Asegurar que sea un círculo
    ax.axis('equal')  

    # Guardar la imagen en memoria como PNG
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()

    # Codificar la imagen en base64
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

# Generar la gráfica de pastel para la comparación de ingresos y egresos y devolverla en base64
def get_income_vs_expense_chart_base64():
    categories = ['Ingresos', 'Egresos']
    values = [random.randint(40, 60), random.randint(20, 40)]  # Generar valores aleatorios

    # Crear la gráfica de pastel
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(values, labels=categories, colors=['#66b3ff', '#ff9999'], 
                                      autopct='%1.1f%%', startangle=90, pctdistance=0.85)

    # Dibujar el círculo para mejorar la estética
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)

    # Mejorar la visualización de las etiquetas y porcentajes
    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(10)

    # Añadir título a la gráfica
    ax.set_title('Comparación de Ingresos vs Egresos', fontsize=16)

    # Asegurar que sea un círculo
    ax.axis('equal')  

    # Guardar la imagen en memoria como PNG
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()

    # Codificar la imagen en base64
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener los datos del formulario
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        # Crear un nuevo DataFrame con los datos del nuevo usuario
        new_user = pd.DataFrame({
            'nombre': [name],
            'correo': [email],
            'usuario': [username],
            'contraseña': [password]
        })
        # Añadir el nuevo usuario al DataFrame existente
        global df  # Asegurarte de que estás utilizando el DataFrame global
        df = pd.concat([df, new_user], ignore_index=True)

        # Guardar el DataFrame actualizado en el archivo CSV
        df.to_csv('usuarios.csv', index=False)

        flash("Registro exitoso. Puedes iniciar sesión.")  # Mensaje de éxito
        return redirect(url_for('home'))  # Redirige al login después del registro

    return render_template('register.html')  # Muestra el formulario si el método es GET

if __name__ == "__main__":
    app.run(debug=True)
    