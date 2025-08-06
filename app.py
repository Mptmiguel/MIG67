from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import json
from modules import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onerepapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Criar pasta de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Importar módulos
from modules.perfil_cliente import PerfilClienteModule
from modules.avaliacao_hematologica import AvaliacaoHematologicaModule
from modules.nutricao_estrategica import NutricaoEstrategicaModule
from modules.suplementos_ergogenicos import SuplementosErgogenicosModule
from modules.treinamento_periodizacao import TreinamentoPeriodizacaoModule
from modules.monitoramento_ajustes import MonitoramentoAjustesModule

# Modelos do banco de dados
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
    data_nascimento = db.Column(db.Date)
    sexo = db.Column(db.String(10))
    altura = db.Column(db.Float)
    peso = db.Column(db.Float)
    percentual_gordura = db.Column(db.Float)
    nivel_treino = db.Column(db.String(20))
    objetivo_primario = db.Column(db.String(100))
    objetivo_secundario = db.Column(db.String(100))
    historico_medico = db.Column(db.Text)
    historico_farmacologico = db.Column(db.Text)
    qualidade_sono = db.Column(db.Integer)
    nivel_estresse = db.Column(db.Integer)
    dados_adicionais = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotas principais
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

# Rotas dos módulos
@app.route('/modulo1')
@login_required
def modulo1():
    return render_template('modulos/modulo1_perfil.html')

@app.route('/modulo2')
@login_required
def modulo2():
    return render_template('modulos/modulo2_hematologia.html')

@app.route('/modulo3')
@login_required
def modulo3():
    return render_template('modulos/modulo3_nutricao.html')

@app.route('/modulo4')
@login_required
def modulo4():
    return render_template('modulos/modulo4_suplementos.html')

@app.route('/modulo5')
@login_required
def modulo5():
    return render_template('modulos/modulo5_treinamento.html')

@app.route('/modulo6')
@login_required
def modulo6():
    return render_template('modulos/modulo6_monitoramento.html')

# APIs dos módulos
@app.route('/api/perfil', methods=['POST'])
@login_required
def api_perfil():
    perfil_module = PerfilClienteModule()
    return perfil_module.processar_perfil(request.get_json())

@app.route('/api/hematologia', methods=['POST'])
@login_required
def api_hematologia():
    hematologia_module = AvaliacaoHematologicaModule()
    return hematologia_module.analisar_exames(request.get_json())

@app.route('/api/nutricao', methods=['POST'])
@login_required
def api_nutricao():
    nutricao_module = NutricaoEstrategicaModule()
    return nutricao_module.gerar_plano_alimentar(request.get_json())

@app.route('/api/suplementos', methods=['POST'])
@login_required
def api_suplementos():
    suplementos_module = SuplementosErgogenicosModule()
    return suplementos_module.prescrever_suplementos(request.get_json())

@app.route('/api/treinamento', methods=['POST'])
@login_required
def api_treinamento():
    treinamento_module = TreinamentoPeriodizacaoModule()
    return treinamento_module.gerar_plano_treino(request.get_json())

@app.route('/api/monitoramento', methods=['POST'])
@login_required
def api_monitoramento():
    monitoramento_module = MonitoramentoAjustesModule()
    return monitoramento_module.processar_monitoramento(request.get_json())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
