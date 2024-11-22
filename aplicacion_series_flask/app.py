from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clave_secreta_muerte_a_javascript"

# Diccionario para almacenar usuarios con sus series
users = {}

@app.route('/')  # Página principal
def home():
    if 'logged_in' in session and session['logged_in']:  # Verificar si el usuario está autenticado
        username = session['username']

        # Obtener las series del usuario (si no tiene, inicializar listas vacías)
        user_series = users.get(username, {'watchlist': [], 'watching': [], 'watched': []})

        # Obtener las tres categorías de series
        watchlist = user_series['watchlist']
        watching = user_series['watching']
        watched = user_series['watched']

        return render_template('home.html', username=username, watchlist=watchlist,
                               watching=watching, watched=watched)

    return redirect(url_for('login'))  # Si no está autenticado, redirigir al login

@app.route('/register', methods=['GET', 'POST'])  # Ruta de registro de usuario
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users:  # Verificar si el usuario ya existe
            error = "El usuario ya está registrado. Elige otro nombre de usuario."
            return render_template('register.html', error=error)

        # Registrar nuevo usuario
        users[username] = {
            'password': password,
            'watchlist': [],
            'watching': [],
            'watched': []
        }
        return redirect(url_for('login'))  # Redirigir al login después de registro

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])  # Ruta de inicio de sesión
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username]['password'] == password:  # Validar credenciales
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))  # Redirigir al home después del login
        else:
            error = "Nombre de usuario o contraseña incorrectos."
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/add_series', methods=['GET', 'POST'])  # Página para añadir series
def add_series():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        name = request.form.get('name')
        synopsis = request.form.get('synopsis')
        rating = request.form.get('rating')
        genre = request.form.get('genre')
        release_date = request.form.get('release_date')
        episodes = request.form.get('episodes')
        duration = request.form.get('duration')
        category = request.form.get('category')

        # Verificar que los campos estén completos
        if not name or not category or not rating:
            error = "Completa todos los campos obligatorios."
            return render_template('formulario.html', error=error)

        # Añadir la serie a la categoría correspondiente
        series_entry = {
            'name': name,
            'synopsis': synopsis,
            'rating': rating,
            'genre': genre,
            'release_date': release_date,
            'episodes': episodes,
            'duration': duration
        }
        users[username][category].append(series_entry)
        return redirect(url_for('home'))  # Redirigir al home después de añadir la serie

    return render_template('formulario.html')

@app.route('/logout')  # Ruta de cierre de sesión
def logout_function():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))  # Redirigir al login tras cerrar sesión

if __name__ == '__main__':
    app.run(debug=True)

