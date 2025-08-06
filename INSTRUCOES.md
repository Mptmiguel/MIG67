# 🚀 INSTRUÇÕES DE USO - 1Rep Pro

## ⚡ Início Rápido

### 1. Instalação e Configuração
```bash
# Clone ou acesse o diretório do projeto
cd /caminho/para/1rep-pro

# Crie um ambiente virtual
python3 -m venv venv

# Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências básicas
pip install flask flask-sqlalchemy flask-login flask-wtf

# Para instalação completa (opcional)
pip install -r requirements.txt
```

### 2. Executar a Aplicação
```bash
# Versão simplificada (recomendada para testes)
python app_simple.py

# Versão completa (requer todas as dependências)
python app.py
```

### 3. Acessar o Sistema
- **URL**: http://localhost:5000
- **Usuário de teste**: admin
- **Senha de teste**: 123456

## 📋 Funcionalidades Disponíveis

### ✅ Implementado e Testado
- ✅ Sistema de autenticação (login/registro)
- ✅ Dashboard diferenciado para Coach e Cliente
- ✅ Interface responsiva e profissional
- ✅ Sistema modular com 6 módulos especializados
- ✅ Banco de dados SQLite funcional
- ✅ Templates HTML avançados
- ✅ Estrutura completa de backend Flask

### 🚧 Em Desenvolvimento (Estrutura Criada)
- 🚧 Módulo 1: Avaliação completa do perfil do cliente
- 🚧 Módulo 2: Análise hematológica avançada
- 🚧 Módulo 3: Nutrição estratégica personalizada
- 🚧 Módulo 4: Prescrição de suplementos e ergogênicos
- 🚧 Módulo 5: Treinamento e periodização científica
- 🚧 Módulo 6: Monitoramento inteligente e ajustes

## 🎯 Como Usar

### Para Coaches/Profissionais:
1. **Faça login** com as credenciais de teste
2. **Dashboard Coach** - Visualize métricas gerais
3. **Adicione clientes** usando o botão "Novo Cliente"
4. **Acesse os módulos** através do menu lateral
5. **Monitore progresso** através do dashboard

### Para Clientes/Atletas:
1. **Registre-se** como "Cliente/Atleta"
2. **Faça login** com suas credenciais
3. **Dashboard Cliente** - Acompanhe seu progresso pessoal
4. **Visualize planos** criados pelo seu coach

## 🔧 Customização

### Alterando Configurações
```python
# Em app_simple.py ou app.py
app.config['SECRET_KEY'] = 'sua-chave-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sua-string-conexao'
```

### Adicionando Novos Módulos
```python
@app.route('/modulo7')
@login_required
def modulo7():
    return render_template('modulos/modulo7.html')
```

### Personalizando Interface
- Templates estão em `/templates/`
- CSS customizado em `/templates/base.html`
- Componentes Bootstrap 5 disponíveis

## 📊 Estrutura dos Módulos

### Módulo 1: Perfil do Cliente
- **Arquivo**: `modules/perfil_cliente.py`
- **Função**: Avaliação antropométrica completa
- **Features**: Anamnese, testes físicos, histórico médico

### Módulo 2: Avaliação Hematológica  
- **Arquivo**: `modules/avaliacao_hematologica.py`
- **Função**: Interpretação de exames laboratoriais
- **Features**: 50+ biomarcadores, correlações, alertas

### Módulo 3: Nutrição Estratégica
- **Arquivo**: `modules/nutricao_estrategica.py`
- **Função**: Planejamento nutricional individualizado
- **Features**: Macros, timing, periodização nutricional

### Módulo 4: Suplementos & Ergogênicos
- **Arquivo**: `modules/suplementos_ergogenicos.py`
- **Função**: Prescrição técnica especializada
- **Features**: Naturais, SARMs, esteroides, TPC

### Módulo 5: Treinamento & Periodização
- **Arquivo**: `modules/treinamento_periodizacao.py`
- **Função**: Periodização científica de treinamento
- **Features**: Metodologias avançadas, técnicas de intensidade

### Módulo 6: Monitoramento & Ajustes
- **Arquivo**: `modules/monitoramento_ajustes.py`
- **Função**: Biofeedback e ajustes automáticos
- **Features**: IA integrada, alertas preditivos

## ⚠️ Notas Importantes

### Segurança
- **Desenvolvimento**: Use `app_simple.py` para testes
- **Produção**: Configure variáveis de ambiente adequadas
- **Senhas**: Sempre altere a senha padrão

### Farmacologia Esportiva
> **ATENÇÃO**: O módulo de farmacologia contém informações sobre substâncias controladas. Destina-se exclusivamente a profissionais qualificados e deve ser usado com acompanhamento médico especializado.

### Performance
- SQLite é adequado para desenvolvimento/testes
- Para produção, considere PostgreSQL
- Configure cache e otimizações conforme necessário

## 🐛 Solução de Problemas

### Erro de Dependências
```bash
# Se houver erro com requirements.txt, instale individualmente:
pip install flask flask-sqlalchemy flask-login flask-wtf
pip install pandas numpy matplotlib  # Para funcionalidades avançadas
```

### Banco de Dados
```python
# Para resetar o banco de dados:
import os
os.remove('onerepapp.db')
# Reinicie a aplicação
```

### Porta Ocupada
```python
# Altere a porta em app.py:
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📞 Suporte Técnico

### Logs e Debugging
- Mode debug habilitado por padrão
- Logs aparecem no terminal
- Erros detalhados no navegador (development)

### Estrutura de Arquivos
```
1rep-pro/
├── app.py                 # Aplicação principal completa
├── app_simple.py          # Aplicação simplificada para testes
├── requirements.txt       # Dependências Python
├── README.md             # Documentação completa
├── INSTRUCOES.md         # Este arquivo
├── modules/              # Módulos especializados
│   ├── perfil_cliente.py
│   ├── avaliacao_hematologica.py
│   ├── nutricao_estrategica.py
│   ├── suplementos_ergogenicos.py
│   ├── treinamento_periodizacao.py
│   └── monitoramento_ajustes.py
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard_coach.html
└── venv/                 # Ambiente virtual
```

## 🎉 Próximos Passos

### Desenvolvimento
1. **Implemente os módulos** conforme sua especialidade
2. **Customize a interface** para sua marca
3. **Adicione validações** específicas
4. **Integre APIs externas** se necessário

### Deploy em Produção
1. **Configure variáveis de ambiente**
2. **Use PostgreSQL** como banco
3. **Configure Gunicorn + Nginx**
4. **Implemente backups automáticos**

## 💡 Dicas de Uso

- **Sempre teste** em ambiente de desenvolvimento primeiro
- **Faça backup** do banco de dados regularmente
- **Documente modificações** que fizer
- **Mantenha atualizado** com literatura científica
- **Use com responsabilidade** as informações farmacológicas

---

**🚀 Desenvolvido para coaches que buscam excelência em consultoria esportiva!**
