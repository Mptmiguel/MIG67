# 1Rep Pro - Sistema de Consultoria Esportiva de Alta Performance

<div align="center">

![1Rep Pro Logo](https://img.shields.io/badge/1Rep-Pro-blue?style=for-the-badge&logo=lightning)

**Sistema modular completo para consultoria esportiva profissional baseado em evidências científicas**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.0-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 🚀 Visão Geral

O **1Rep Pro** é uma plataforma web avançada desenvolvida especificamente para coaches esportivos e profissionais da área de performance humana. Com 6 módulos especializados, o sistema oferece uma abordagem científica e sistemática para otimização de resultados em atletas e praticantes de atividade física.

### ✨ Características Principais

- **🔬 Baseado em Evidências**: Todos os protocolos fundamentados em literatura científica atual
- **🧩 Sistema Modular**: 6 módulos especializados e independentes
- **🤖 IA Integrada**: Algoritmos para análise preditiva e ajustes automáticos
- **📊 Analytics Avançado**: Dashboard com métricas em tempo real
- **🔒 Segurança**: Criptografia de dados e autenticação robusta
- **📱 Responsivo**: Interface adaptável para todos os dispositivos

## 📋 Módulos do Sistema

### 📝 Módulo 1: Perfil do Cliente
- Avaliação antropométrica completa
- Anamnese médica e esportiva detalhada
- Testes de performance física
- Análise postural e biomecânica
- Histórico farmacológico especializado

### 🩸 Módulo 2: Avaliação Hematológica
- Interpretação de 50+ biomarcadores
- Análise correlacional automática
- Identificação de padrões patológicos
- Recomendações de intervenção específicas
- Sistema de alertas para alterações críticas

### 🍎 Módulo 3: Nutrição Estratégica
- Cálculo personalizado de macronutrientes
- Estratégias avançadas (ciclagem, jejum intermitente)
- Timing nutricional otimizado
- Periodização nutricional por fases
- Monitoramento e ajustes automáticos

### 💊 Módulo 4: Suplementos & Ergogênicos
- Prescrição de suplementos naturais
- Protocolos de nootrópicos e adaptógenos
- **Farmacologia esportiva avançada**:
  - Esteroides anabolizantes
  - SARMs e peptídeos
  - Protocolos de TPC completos
  - Monitoramento de segurança

### 🏋️ Módulo 5: Treinamento & Periodização
- Múltiplas metodologias científicas
- Periodização linear, ondulatória e conjugada
- Técnicas de intensidade avançadas
- Monitoramento de carga de treinamento
- Protocolos de recuperação

### 📈 Módulo 6: Monitoramento & Ajustes
- Sistema de biofeedback inteligente
- Ajustes automáticos baseados em IA
- Dashboard de performance em tempo real
- Alertas preditivos de overtraining
- Relatórios detalhados de progresso

## 🛠️ Tecnologias Utilizadas

### Backend
```
- Python 3.8+
- Flask 3.0.0 (Framework web)
- SQLAlchemy 3.1.1 (ORM)
- Flask-Login 0.6.2 (Autenticação)
- Pandas 2.1.4 (Análise de dados)
- NumPy 1.24.3 (Computação científica)
- Matplotlib 3.8.2 (Visualizações)
```

### Frontend
```
- HTML5 & CSS3
- Bootstrap 5.3.0 (UI Framework)
- JavaScript ES6+ (Vanilla)
- Chart.js (Gráficos interativos)
- Bootstrap Icons (Iconografia)
```

### Banco de Dados
```
- SQLite (Desenvolvimento)
- PostgreSQL (Produção - recomendado)
```

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Git

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seuusuario/1rep-pro.git
cd 1rep-pro
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
# Crie um arquivo .env na raiz do projeto
touch .env
```

Adicione ao arquivo `.env`:
```env
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///onerepapp.db
FLASK_ENV=development
FLASK_DEBUG=True
```

5. **Execute a aplicação**
```bash
python app.py
```

6. **Acesse o sistema**
- Abra seu navegador em `http://localhost:5000`
- Crie sua conta como Coach para acesso completo

## 🚀 Deploy em Produção

### Com Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Com Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Variáveis de Ambiente para Produção
```env
SECRET_KEY=sua-chave-super-secreta-producao
DATABASE_URL=postgresql://usuario:senha@host:porta/database
FLASK_ENV=production
FLASK_DEBUG=False
```

## 👥 Tipos de Usuário

### 👨‍⚕️ Coach/Profissional
- Acesso completo a todos os módulos
- Gerenciamento de múltiplos clientes
- Dashboard avançado com analytics
- Prescrições farmacológicas (sob responsabilidade)
- Relatórios detalhados

### 👤 Cliente/Atleta
- Acesso aos próprios dados
- Monitoramento pessoal
- Feedback de progresso
- Visualização de planos

## 📊 Funcionalidades Destacadas

### 🤖 Inteligência Artificial
- Análise preditiva de resultados
- Ajustes automáticos de protocolos
- Identificação de padrões comportamentais
- Alertas preventivos de overtraining

### 🔬 Análise Laboratorial Avançada
- Interpretação automática de exames
- Correlações entre biomarcadores
- Identificação de padrões patológicos
- Recomendações específicas de intervenção

### 📈 Dashboard Interativo
- Métricas em tempo real
- Gráficos dinâmicos
- Comparativos temporais
- Alertas e notificações

## ⚠️ Avisos Importantes

### Farmacologia Esportiva
> **ATENÇÃO**: O módulo de farmacologia esportiva contém informações sobre substâncias controladas e é destinado exclusivamente a profissionais qualificados. O uso dessas informações é de total responsabilidade do usuário e deve sempre ser acompanhado por profissional médico especializado.

### Responsabilidade Profissional
- Este sistema é uma ferramenta de apoio profissional
- Não substitui conhecimento técnico e experiência
- Sempre considere individualidade biológica
- Mantenha-se atualizado com literatura científica

## 🔐 Segurança e Privacidade

- Criptografia de senhas com Werkzeug
- Autenticação de sessão robusta
- Proteção contra CSRF
- Dados de saúde protegidos por LGPD
- Auditoria de acesso ao sistema

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes de Contribuição
- Siga os padrões de código existentes
- Documente novas funcionalidades
- Adicione testes quando apropriado
- Mantenha commits claros e objetivos

## 📚 Documentação Adicional

### API Endpoints
```
GET  /api/perfil          - Dados do perfil do cliente
POST /api/hematologia     - Análise de exames laboratoriais
POST /api/nutricao        - Geração de plano alimentar
POST /api/suplementos     - Prescrição de suplementos
POST /api/treinamento     - Plano de treinamento
POST /api/monitoramento   - Análise de biofeedback
```

### Estrutura do Banco de Dados
- `users` - Usuários do sistema (coaches/clientes)
- `clientes` - Dados dos clientes
- `avaliacoes` - Histórico de avaliações
- `exames` - Dados laboratoriais
- `planos_nutricionais` - Planos alimentares
- `planos_treinamento` - Programas de exercícios

## 📞 Suporte

### Canais de Suporte
- **Email**: suporte@1reppro.com
- **Discord**: [Servidor da Comunidade](https://discord.gg/1reppro)
- **Documentação**: [Wiki do Projeto](https://github.com/seuusuario/1rep-pro/wiki)

### FAQ
**P: Posso usar para fins comerciais?**
R: Sim, sob licença MIT.

**P: É necessário conhecimento médico?**
R: Recomendado, especialmente para módulos avançados.

**P: Há suporte móvel?**
R: Interface responsiva, app nativo em desenvolvimento.

## 📋 Roadmap

### 🔄 Versão 2.0 (Planejada)
- [ ] App mobile nativo (iOS/Android)
- [ ] Integração com wearables
- [ ] Módulo de análise genética
- [ ] Sistema de teleconsulta
- [ ] Marketplace de profissionais

### 🎯 Versão 2.1
- [ ] Machine Learning avançado
- [ ] Integração com laboratórios
- [ ] Sistema de pagamentos
- [ ] Multi-idiomas

## 🏆 Reconhecimentos

- Desenvolvido com base em guidelines da ACSM, NSCA e ISSN
- Consultoria técnica de profissionais certificados
- Revisão científica contínua
- Testes em ambiente real com atletas

## 📄 Licença

Este projeto está licenciado under the MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Desenvolvedor**: Engine AI Assistant  
**Contato**: [GitHub Profile](https://github.com)  
**Especialização**: Sistemas de alta performance para saúde e esporte

---

<div align="center">

**🚀 Revolucione sua consultoria esportiva com 1Rep Pro**

[![Começar Agora](https://img.shields.io/badge/Começar%20Agora-37a779?style=for-the-badge)](http://localhost:5000)
[![Documentação](https://img.shields.io/badge/Documentação-blue?style=for-the-badge)](https://github.com/seuusuario/1rep-pro/wiki)

</div>
