"""
MÓDULO 1: PERFIL DO CLIENTE
Sistema de avaliação inicial e cadastro completo do cliente
"""

from flask import jsonify
import json
from datetime import datetime, date
import pandas as pd

class PerfilClienteModule:
    def __init__(self):
        self.formulario_base = {
            'dados_pessoais': {
                'idade': None,
                'sexo': None,
                'altura': None,
                'peso': None,
                'percentual_gordura': None
            },
            'historico_treinamento': {
                'tempo_experiencia': None,
                'modalidades_praticadas': [],
                'nivel_atual': None,  # iniciante/intermediário/avançado/atleta
                'lesoes_anteriores': [],
                'limitacoes_fisicas': []
            },
            'objetivos': {
                'objetivo_primario': None,
                'objetivo_secundario': None,
                'prazo_meta': None,
                'motivacao_principal': None
            },
            'historico_medico': {
                'doencas_cronicas': [],
                'medicamentos_uso': [],
                'cirurgias_anteriores': [],
                'alergias_restricoes': []
            },
            'historico_farmacologico': {
                'uso_anterior_esteroides': False,
                'ciclos_realizados': [],
                'uso_sarms': False,
                'uso_hormonio_crescimento': False,
                'uso_peptideos': False,
                'tpc_realizadas': []
            },
            'estilo_vida': {
                'qualidade_sono': None,  # 1-10
                'horas_sono_media': None,
                'nivel_estresse': None,  # 1-10
                'ocupacao_profissional': None,
                'tabagismo': False,
                'etilismo': False,
                'frequencia_exercicios_atual': None
            },
            'composicao_corporal': {
                'metodo_avaliacao': None,  # bioimpedância/dobras/dexa
                'percentual_gordura': None,
                'massa_muscular': None,
                'massa_ossea': None,
                'agua_corporal': None,
                'circunferencias': {
                    'braco': None,
                    'antebraco': None,
                    'peito': None,
                    'cintura': None,
                    'quadril': None,
                    'coxa': None,
                    'panturrilha': None
                }
            },
            'avaliacao_fisica': {
                'postural': {
                    'escoliose': False,
                    'hipercifose': False,
                    'hiperlordose': False,
                    'rotacao_interna_ombros': False,
                    'anteriorização_cabeca': False
                },
                'mobilidade': {
                    'ombro': None,  # limitada/normal/boa
                    'quadril': None,
                    'tornozelo': None,
                    'coluna_toracica': None,
                    'coluna_lombar': None
                },
                'testes_forca': {
                    'supino_1rm': None,
                    'agachamento_1rm': None,
                    'levantamento_terra_1rm': None,
                    'desenvolvimento_1rm': None
                },
                'testes_resistencia': {
                    'vo2_max': None,
                    'frequencia_cardiaca_repouso': None,
                    'frequencia_cardiaca_maxima': None,
                    'pressao_arterial': None
                }
            }
        }
    
    def processar_perfil(self, dados):
        """
        Processa os dados do perfil do cliente e gera análise inicial
        """
        try:
            # Validar dados obrigatórios
            campos_obrigatorios = ['idade', 'sexo', 'altura', 'peso', 'objetivo_primario']
            for campo in campos_obrigatorios:
                if campo not in dados or not dados[campo]:
                    return jsonify({
                        'success': False,
                        'message': f'Campo obrigatório não preenchido: {campo}'
                    })
            
            # Calcular IMC
            imc = self._calcular_imc(dados['peso'], dados['altura'])
            
            # Determinar categoria de risco metabólico
            categoria_risco = self._avaliar_risco_metabolico(dados)
            
            # Análise de perfil para treinamento
            perfil_treinamento = self._analisar_perfil_treinamento(dados)
            
            # Recomendações iniciais
            recomendacoes = self._gerar_recomendacoes_iniciais(dados)
            
            # Exames recomendados
            exames_recomendados = self._sugerir_exames_complementares(dados)
            
            resultado = {
                'success': True,
                'analise': {
                    'imc': {
                        'valor': round(imc, 2),
                        'classificacao': self._classificar_imc(imc)
                    },
                    'categoria_risco': categoria_risco,
                    'perfil_treinamento': perfil_treinamento,
                    'recomendacoes_iniciais': recomendacoes,
                    'exames_complementares': exames_recomendados,
                    'prioridades_avaliacao': self._definir_prioridades_avaliacao(dados)
                },
                'dados_processados': dados,
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify(resultado)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erro ao processar perfil: {str(e)}'
            })
    
    def _calcular_imc(self, peso, altura):
        """Calcula o Índice de Massa Corporal"""
        return peso / (altura ** 2)
    
    def _classificar_imc(self, imc):
        """Classifica o IMC segundo padrões WHO"""
        if imc < 18.5:
            return "Abaixo do peso"
        elif imc < 25:
            return "Peso normal"
        elif imc < 30:
            return "Sobrepeso"
        elif imc < 35:
            return "Obesidade Grau I"
        elif imc < 40:
            return "Obesidade Grau II"
        else:
            return "Obesidade Grau III"
    
    def _avaliar_risco_metabolico(self, dados):
        """Avalia risco metabólico baseado em fatores de risco"""
        fatores_risco = 0
        
        # Idade
        idade = dados.get('idade', 0)
        if (dados.get('sexo') == 'masculino' and idade > 45) or \
           (dados.get('sexo') == 'feminino' and idade > 55):
            fatores_risco += 1
        
        # IMC
        imc = self._calcular_imc(dados.get('peso', 0), dados.get('altura', 1))
        if imc >= 30:
            fatores_risco += 2
        elif imc >= 25:
            fatores_risco += 1
        
        # Histórico familiar/médico
        if dados.get('historico_medico', {}).get('doencas_cronicas'):
            fatores_risco += 1
        
        # Sedentarismo
        if dados.get('estilo_vida', {}).get('frequencia_exercicios_atual', 0) < 2:
            fatores_risco += 1
        
        # Tabagismo
        if dados.get('estilo_vida', {}).get('tabagismo', False):
            fatores_risco += 2
        
        if fatores_risco == 0:
            return "Baixo risco"
        elif fatores_risco <= 2:
            return "Risco moderado"
        else:
            return "Alto risco"
    
    def _analisar_perfil_treinamento(self, dados):
        """Analisa perfil específico para prescrição de treinamento"""
        nivel = dados.get('nivel_atual', 'iniciante').lower()
        
        perfil = {
            'classificacao': nivel,
            'volume_semanal_recomendado': self._calcular_volume_treino(nivel),
            'frequencia_semanal': self._calcular_frequencia_treino(nivel),
            'intensidade_inicial': self._calcular_intensidade_inicial(nivel),
            'consideracoes_especiais': []
        }
        
        # Considerações especiais baseadas no perfil
        if dados.get('historico_treinamento', {}).get('lesoes_anteriores'):
            perfil['consideracoes_especiais'].append(
                "Histórico de lesões - priorizar aquecimento e mobilidade"
            )
        
        if dados.get('estilo_vida', {}).get('nivel_estresse', 0) >= 7:
            perfil['consideracoes_especiais'].append(
                "Alto nível de estresse - modular volume/intensidade"
            )
        
        if dados.get('estilo_vida', {}).get('qualidade_sono', 0) <= 5:
            perfil['consideracoes_especiais'].append(
                "Qualidade de sono comprometida - priorizar recuperação"
            )
        
        return perfil
    
    def _calcular_volume_treino(self, nivel):
        """Calcula volume de treino baseado no nível"""
        volumes = {
            'iniciante': '8-12 séries/grupo muscular/semana',
            'intermediario': '12-18 séries/grupo muscular/semana',
            'avancado': '16-22 séries/grupo muscular/semana',
            'atleta': '20-28 séries/grupo muscular/semana'
        }
        return volumes.get(nivel, volumes['iniciante'])
    
    def _calcular_frequencia_treino(self, nivel):
        """Calcula frequência de treino baseada no nível"""
        frequencias = {
            'iniciante': '3-4x por semana',
            'intermediario': '4-5x por semana',
            'avancado': '5-6x por semana',
            'atleta': '6-7x por semana'
        }
        return frequencias.get(nivel, frequencias['iniciante'])
    
    def _calcular_intensidade_inicial(self, nivel):
        """Calcula intensidade inicial baseada no nível"""
        intensidades = {
            'iniciante': '60-70% 1RM',
            'intermediario': '70-80% 1RM',
            'avancado': '75-85% 1RM',
            'atleta': '80-95% 1RM'
        }
        return intensidades.get(nivel, intensidades['iniciante'])
    
    def _gerar_recomendacoes_iniciais(self, dados):
        """Gera recomendações iniciais baseadas no perfil"""
        recomendacoes = []
        
        # Recomendações baseadas no objetivo
        objetivo = dados.get('objetivo_primario', '').lower()
        
        if 'emagrecimento' in objetivo or 'gordura' in objetivo:
            recomendacoes.extend([
                "Priorizar déficit calórico sustentável (300-500 kcal)",
                "Incluir exercícios aeróbicos 3-4x/semana",
                "Manter alta ingestão proteica (1.6-2.2g/kg)"
            ])
        
        elif 'hipertrofia' in objetivo or 'massa' in objetivo:
            recomendacoes.extend([
                "Estabelecer superávit calórico moderado (200-400 kcal)",
                "Foco em treinamento de força com sobrecarga progressiva",
                "Garantir ingestão proteica adequada (1.8-2.5g/kg)"
            ])
        
        elif 'performance' in objetivo or 'força' in objetivo:
            recomendacoes.extend([
                "Periodização específica para modalidade",
                "Foco em exercícios compostos e específicos",
                "Monitoramento de fadiga e recuperação"
            ])
        
        # Recomendações baseadas no histórico farmacológico
        if dados.get('historico_farmacologico', {}).get('uso_anterior_esteroides'):
            recomendacoes.append(
                "Avaliação hormonal completa obrigatória antes do planejamento"
            )
        
        # Recomendações baseadas no estilo de vida
        if dados.get('estilo_vida', {}).get('qualidade_sono', 0) < 6:
            recomendacoes.append(
                "Priorizar higiene do sono - fundamental para resultados"
            )
        
        return recomendacoes
    
    def _sugerir_exames_complementares(self, dados):
        """Sugere exames complementares baseados no perfil"""
        exames_basicos = [
            "Hemograma completo",
            "Glicemia de jejum",
            "Perfil lipídico completo",
            "Função hepática (AST, ALT, GGT)",
            "Função renal (creatinina, ureia)",
            "TSH, T3, T4 livre",
            "Vitamina D",
            "Vitamina B12",
            "Ácido fólico"
        ]
        
        exames_especificos = []
        
        # Exames baseados na idade e sexo
        idade = dados.get('idade', 0)
        sexo = dados.get('sexo', '').lower()
        
        if sexo == 'masculino':
            exames_especificos.extend([
                "Testosterona total e livre",
                "LH e FSH",
                "Estradiol",
                "SHBG",
                "PSA (se >40 anos)"
            ])
        elif sexo == 'feminino':
            exames_especificos.extend([
                "Estradiol",
                "Progesterona",
                "LH e FSH",
                "Prolactina",
                "SHBG"
            ])
        
        # Exames baseados no histórico
        if dados.get('historico_farmacologico', {}).get('uso_anterior_esteroides'):
            exames_especificos.extend([
                "Painel andrógeno completo",
                "IGF-1",
                "Cortisol",
                "DHEA-S"
            ])
        
        # Exames baseados em fatores de risco
        if self._avaliar_risco_metabolico(dados) in ['Risco moderado', 'Alto risco']:
            exames_especificos.extend([
                "Hemoglobina glicada",
                "Insulina",
                "HOMA-IR",
                "PCR ultrassensível",
                "Homocisteína"
            ])
        
        return {
            'exames_basicos': exames_basicos,
            'exames_especificos': exames_especificos,
            'observacoes': [
                "Realizar exames em jejum de 12h",
                "Evitar exercícios intensos 48h antes da coleta",
                "Informar uso de medicamentos/suplementos"
            ]
        }
    
    def _definir_prioridades_avaliacao(self, dados):
        """Define prioridades na avaliação baseadas no perfil"""
        prioridades = []
        
        # Prioridade 1: Avaliação médica
        if self._avaliar_risco_metabolico(dados) == "Alto risco":
            prioridades.append({
                'nivel': 'ALTA',
                'item': 'Avaliação médica pré-participação',
                'justificativa': 'Múltiplos fatores de risco identificados'
            })
        
        # Prioridade 2: Avaliação postural/biomecânica
        if dados.get('historico_treinamento', {}).get('lesoes_anteriores'):
            prioridades.append({
                'nivel': 'ALTA',
                'item': 'Avaliação postural e biomecânica',
                'justificativa': 'Histórico de lesões prévias'
            })
        
        # Prioridade 3: Composição corporal
        objetivo = dados.get('objetivo_primario', '').lower()
        if any(word in objetivo for word in ['emagrecimento', 'gordura', 'hipertrofia']):
            prioridades.append({
                'nivel': 'MÉDIA',
                'item': 'Avaliação detalhada da composição corporal',
                'justificativa': 'Objetivo relacionado à composição corporal'
            })
        
        # Prioridade 4: Avaliação hormonal
        if dados.get('historico_farmacologico', {}).get('uso_anterior_esteroides'):
            prioridades.append({
                'nivel': 'ALTA',
                'item': 'Avaliação hormonal completa',
                'justificativa': 'Histórico de uso de esteroides anabolizantes'
            })
        
        return prioridades
