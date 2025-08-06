from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onerepapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelos simplificados
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_coach = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    objetivo_primario = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        
        if user and check_password_hash(user.password_hash, data['password']):
            login_user(user)
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        else:
            return jsonify({'success': False, 'message': 'Usuário ou senha inválidos'})
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        # Verificar se usuário já existe
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'message': 'Usuário já existe'})
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': 'Email já cadastrado'})
        
        # Criar novo usuário
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            is_coach=data.get('is_coach', False)
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Usuário criado com sucesso'})
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_coach:
        clientes = Cliente.query.filter_by(coach_id=current_user.id).all()
        return render_template('dashboard_coach.html', clientes=clientes)
    else:
        return render_template('dashboard_client.html')

# Rotas dos módulos (simplificadas)
@app.route('/modulo1')
@login_required
def modulo1():
    return "<h1>Módulo 1: Perfil do Cliente</h1><p>Módulo em desenvolvimento...</p>"

@app.route('/modulo2')
@login_required
def modulo2():
    return "<h1>Módulo 2: Avaliação Hematológica</h1><p>Módulo em desenvolvimento...</p>"

@app.route('/modulo3')
@login_required
def modulo3():
    return "<h1>Módulo 3: Nutrição Estratégica</h1><p>Módulo em desenvolvimento...</p>"

@app.route('/modulo4')
@login_required
def modulo4():
    return "<h1>Módulo 4: Suplementos & Ergogênicos</h1><p>Módulo em desenvolvimento...</p>"

@app.route('/modulo5')
@login_required
def modulo5():
    return "<h1>Módulo 5: Treinamento & Periodização</h1><p>Módulo em desenvolvimento...</p>"

@app.route('/modulo6')
@login_required
def modulo6():
    return "<h1>Módulo 6: Monitoramento & Ajustes</h1><p>Módulo em desenvolvimento...</p>"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Criar usuário admin se não existir
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@1reppro.com',
                password_hash=generate_password_hash('123456'),
                is_coach=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Usuário admin criado! Login: admin / Senha: 123456")
    
    print("🚀 1Rep Pro iniciado com sucesso!")
    print("📱 Acesse: http://localhost:5000")
    print("👤 Login de teste: admin / 123456")
    app.run(debug=True, host='0.0.0.0', port=5000)
