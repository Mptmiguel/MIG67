"""
MÓDULO 6: MONITORAMENTO E AJUSTES
Sistema avançado de monitoramento contínuo e ajustes baseados em biofeedback e resultados
"""

from flask import jsonify
import json
from datetime import datetime, timedelta
import statistics
import math

class MonitoramentoAjustesModule:
    def __init__(self):
        self.indicadores_biofeedback = {
            'sono': {
                'parametros': ['duração', 'qualidade', 'latência', 'despertares'],
                'escala': '1-10',
                'frequencia': 'Diário',
                'valores_ideais': {'duracao': 7-9, 'qualidade': '>7', 'latencia': '<20min'},
                'sinais_alerta': {'qualidade': '<5', 'duracao': '<6h', 'latencia': '>45min'}
            },
            'libido': {
                'parametros': ['desejo', 'frequência', 'satisfação'],
                'escala': '1-10',
                'frequencia': 'Semanal',
                'valores_ideais': {'desejo': '>6', 'satisfacao': '>7'},
                'sinais_alerta': {'desejo': '<4', 'frequencia': 'redução >50%'}
            },
            'disposicao': {
                'parametros': ['energia_geral', 'motivacao_treino', 'humor'],
                'escala': '1-10',
                'frequencia': 'Diário',
                'valores_ideais': {'energia': '>6', 'motivacao': '>7', 'humor': '>6'},
                'sinais_alerta': {'energia': '<4', 'motivacao': '<4', 'humor': '<4'}
            },
            'recuperacao': {
                'parametros': ['dor_muscular', 'fadiga', 'rigidez_articular'],
                'escala': '1-10 (inversa)',
                'frequencia': 'Diário',
                'valores_ideais': {'dor': '<4', 'fadiga': '<4', 'rigidez': '<3'},
                'sinais_alerta': {'dor': '>7', 'fadiga': '>7', 'rigidez': '>6'}
            }
        }
        
        self.metricas_performance = {
            'forca': {
                'testes': ['1RM estimado', 'força explosiva', 'resistência força'],
                'frequencia_teste': '4-6 semanas',
                'progressao_esperada': {
                    'iniciante': '5-10%/mês',
                    'intermediario': '2-5%/mês',
                    'avançado': '1-3%/mês',
                    'atleta': '0.5-2%/mês'
                }
            },
            'composicao_corporal': {
                'medidas': ['peso', 'circunferências', 'dobras cutâneas', 'bioimpedância'],
                'frequencia_avaliacao': 'Semanal (peso) / Quinzenal (medidas)',
                'objetivos_progressao': {
                    'cutting': '-0.5 a -1kg/semana',
                    'bulking': '+0.2 a +0.5kg/semana',
                    'recomposicao': 'Estável peso, -gordura +músculo'
                }
            },
            'cardiovascular': {
                'parametros': ['FC repouso', 'FC exercício', 'recuperação FC', 'PA'],
                'frequencia': 'Diário (FC repouso) / Semanal (PA)',
                'valores_saudaveis': {
                    'fc_repouso': '60-100 bpm',
                    'pa_sistolica': '<130 mmHg',
                    'pa_diastolica': '<80 mmHg'
                }
            }
        }
        
        self.protocolos_ajuste = {
            'sobrecarga_progressiva': {
                'criterios_progressao': {
                    'forca': 'Completar todas as séries/reps com RPE <8',
                    'hipertrofia': 'RPE 7-9 na última série',
                    'resistencia': 'Capacidade de adicionar volume'
                },
                'ajustes_carga': {
                    'aumento_peso': '2.5-5% quando critérios atingidos',
                    'aumento_volume': '1-2 séries adicionais',
                    'aumento_frequencia': 'Adicionar 1 sessão semanal'
                }
            },
            'deload_protocols': {
                'indicadores': ['RPE médio >8.5', 'Queda performance >10%', 'Biofeedback ruim >5 dias'],
                'tipos_deload': {
                    'volume': 'Reduzir séries 40-60%',
                    'intensidade': 'Reduzir carga 20-40%',
                    'densidade': 'Aumentar descansos 50%',
                    'completo': 'Descanso total 3-7 dias'
                }
            }
        }
        
        self.algoritmos_ajuste = {
            'nutricao': {
                'peso_estagnado_3sem': {
                    'cutting': 'Reduzir calorias 10-15% ou aumentar cardio',
                    'bulking': 'Aumentar calorias 10-15% ou reduzir cardio'
                },
                'perda_muito_rapida': 'Aumentar calorias 5-10%',
                'ganho_muito_rapido': 'Reduzir calorias 5-10%'
            },
            'treinamento': {
                'plateau_forca': ['Deload semana', 'Mudar exercícios', 'Alterar rep ranges'],
                'plateau_hipertrofia': ['Aumentar volume', 'Técnicas intensidade', 'Frequência maior'],
                'overreaching': ['Reduzir volume 50%', 'Foco recuperação', 'Avaliação stress']
            },
            'suplementacao': {
                'performance_baixa': 'Revisar pré-treino, hidratação, eletrólitos',
                'recuperacao_lenta': 'Avaliar magnésio, ômega-3, sono',
                'libido_baixa': 'Checar zinco, vitamina D, stress'
            }
        }
    
    def processar_monitoramento(self, dados):
        """
        Processa dados de monitoramento e gera ajustes personalizados
        """
        try:
            # Validar dados obrigatórios
            if 'dados_historicos' not in dados:
                return jsonify({
                    'success': False,
                    'message': 'Dados históricos são obrigatórios para análise'
                })
            
            # Analisar tendências dos indicadores
            analise_biofeedback = self._analisar_biofeedback(dados['dados_historicos'])
            
            # Avaliar progresso das metas
            analise_progresso = self._avaliar_progresso_metas(dados)
            
            # Identificar padrões e correlações
            padroes_identificados = self._identificar_padroes(dados['dados_historicos'])
            
            # Calcular scores de performance
            scores_performance = self._calcular_scores_performance(dados)
            
            # Gerar recomendações de ajustes
            recomendacoes_ajustes = self._gerar_recomendacoes_ajustes(
                analise_biofeedback, analise_progresso, padroes_identificados
            )
            
            # Definir protocolo de monitoramento futuro
            protocolo_futuro = self._definir_protocolo_monitoramento_futuro(dados, recomendacoes_ajustes)
            
            # Gerar alertas e sinais de atenção
            alertas_sistema = self._gerar_alertas_sistema(analise_biofeedback, analise_progresso)
            
            # Calcular próximas avaliações e ajustes
            cronograma_avaliacoes = self._gerar_cronograma_avaliacoes(dados)
            
            resultado = {
                'success': True,
                'relatorio_monitoramento': {
                    'resumo_executivo': {
                        'periodo_analisado': self._calcular_periodo_analise(dados['dados_historicos']),
                        'score_geral': scores_performance['score_geral'],
                        'tendencia_progresso': analise_progresso['tendencia_geral'],
                        'necessidade_ajustes': recomendacoes_ajustes['prioridade_ajustes'],
                        'proxima_avaliacao': cronograma_avaliacoes['proxima_completa']
                    },
                    'analise_biofeedback': analise_biofeedback,
                    'progresso_metas': analise_progresso,
                    'padroes_comportamentais': padroes_identificados,
                    'scores_performance': scores_performance,
                    'recomendacoes_ajustes': recomendacoes_ajustes,
                    'protocolo_monitoramento': protocolo_futuro,
                    'alertas_sistema': alertas_sistema,
                    'cronograma_avaliacoes': cronograma_avaliacoes,
                    'dashboard_indicadores': self._gerar_dashboard_indicadores(dados)
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify(resultado)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erro no processamento do monitoramento: {str(e)}'
            })
    
    def _analisar_biofeedback(self, dados_historicos):
        """Analisa tendências dos indicadores de biofeedback"""
        analise = {}
        
        # Analisar cada categoria de biofeedback
        for categoria, config in self.indicadores_biofeedback.items():
            if categoria in dados_historicos:
                dados_categoria = dados_historicos[categoria]
                
                analise[categoria] = {
                    'media_periodo': self._calcular_media_periodo(dados_categoria),
                    'tendencia': self._calcular_tendencia(dados_categoria),
                    'variabilidade': self._calcular_variabilidade(dados_categoria),
                    'dias_fora_ideal': self._contar_dias_fora_ideal(dados_categoria, config),
                    'correlacoes': self._buscar_correlacoes_categoria(categoria, dados_historicos),
                    'status_atual': self._classificar_status_atual(dados_categoria, config),
                    'recomendacao_imediata': self._gerar_recomendacao_imediata(categoria, dados_categoria, config)
                }
        
        # Análise integrada do biofeedback
        analise['integracao_geral'] = {
            'score_biofeedback_geral': self._calcular_score_biofeedback_geral(analise),
            'areas_criticas': self._identificar_areas_criticas(analise),
            'areas_excelentes': self._identificar_areas_excelentes(analise),
            'impacto_performance': self._avaliar_impacto_performance(analise)
        }
        
        return analise
    
    def _avaliar_progresso_metas(self, dados):
        """Avalia progresso em direção às metas estabelecidas"""
        metas_originais = dados.get('metas_estabelecidas', {})
        dados_atuais = dados.get('dados_atuais', {})
        dados_historicos = dados.get('dados_historicos', {})
        
        progresso = {}
        
        # Avaliar progresso por categoria de meta
        for categoria_meta, meta_info in metas_originais.items():
            if categoria_meta in dados_atuais:
                progresso[categoria_meta] = {
                    'meta_inicial': meta_info,
                    'valor_atual': dados_atuais[categoria_meta],
                    'progresso_percentual': self._calcular_progresso_percentual(meta_info, dados_atuais[categoria_meta]),
                    'velocidade_progresso': self._calcular_velocidade_progresso(categoria_meta, dados_historicos),
                    'projecao_meta': self._projetar_atingimento_meta(meta_info, dados_historicos),
                    'ajustes_necessarios': self._avaliar_necessidade_ajustes_meta(meta_info, dados_historicos),
                    'probabilidade_sucesso': self._calcular_probabilidade_sucesso(meta_info, dados_historicos)
                }
        
        # Análise geral do progresso
        progresso['analise_geral'] = {
            'tendencia_geral': self._determinar_tendencia_geral_progresso(progresso),
            'metas_no_prazo': self._contar_metas_no_prazo(progresso),
            'metas_atrasadas': self._contar_metas_atrasadas(progresso),
            'intervencoes_recomendadas': self._recomendar_intervencoes_progresso(progresso)
        }
        
        return progresso
    
    def _identificar_padroes(self, dados_historicos):
        """Identifica padrões comportamentais e correlações"""
        padroes = {
            'padroes_temporais': {},
            'correlacoes_significativas': {},
            'ciclos_identificados': {},
            'fatores_influenciadores': {}
        }
        
        # Padrões temporais (dias da semana, períodos do mês)
        padroes['padroes_temporais'] = {
            'melhor_dia_semana': self._identificar_melhor_dia_semana(dados_historicos),
            'pior_dia_semana': self._identificar_pior_dia_semana(dados_historicos),
            'padroes_mensais': self._identificar_padroes_mensais(dados_historicos),
            'sazonalidade': self._identificar_sazonalidade(dados_historicos)
        }
        
        # Correlações entre diferentes métricas
        padroes['correlacoes_significativas'] = {
            'sono_performance': self._calcular_correlacao_sono_performance(dados_historicos),
            'stress_recuperacao': self._calcular_correlacao_stress_recuperacao(dados_historicos),
            'nutricao_energia': self._calcular_correlacao_nutricao_energia(dados_historicos),
            'treino_biofeedback': self._calcular_correlacao_treino_biofeedback(dados_historicos)
        }
        
        # Ciclos e oscilações
        padroes['ciclos_identificados'] = {
            'ciclos_performance': self._identificar_ciclos_performance(dados_historicos),
            'oscilacoes_peso': self._analisar_oscilacoes_peso(dados_historicos),
            'padroes_recuperacao': self._identificar_padroes_recuperacao(dados_historicos)
        }
        
        return padroes
    
    def _calcular_scores_performance(self, dados):
        """Calcula scores de performance por área"""
        dados_atuais = dados.get('dados_atuais', {})
        dados_historicos = dados.get('dados_historicos', {})
        
        scores = {}
        
        # Score de Biofeedback (0-100)
        scores['biofeedback'] = self._calcular_score_biofeedback(dados_historicos)
        
        # Score de Progresso nas Metas (0-100)
        scores['progresso_metas'] = self._calcular_score_progresso_metas(dados)
        
        # Score de Consistência (0-100)
        scores['consistencia'] = self._calcular_score_consistencia(dados_historicos)
        
        # Score de Adaptação ao Treinamento (0-100)
        scores['adaptacao_treinamento'] = self._calcular_score_adaptacao_treinamento(dados_historicos)
        
        # Score de Saúde Geral (0-100)
        scores['saude_geral'] = self._calcular_score_saude_geral(dados_atuais)
        
        # Score Geral Ponderado
        scores['score_geral'] = self._calcular_score_geral_ponderado(scores)
        
        # Classificação do score
        scores['classificacao'] = self._classificar_score_geral(scores['score_geral'])
        
        return scores
    
    def _gerar_recomendacoes_ajustes(self, biofeedback, progresso, padroes):
        """Gera recomendações específicas de ajustes"""
        recomendacoes = {
            'prioridade_alta': [],
            'prioridade_media': [],
            'prioridade_baixa': [],
            'ajustes_nutricionais': [],
            'ajustes_treinamento': [],
            'ajustes_suplementacao': [],
            'ajustes_recuperacao': [],
            'ajustes_lifestyle': []
        }
        
        # Analisar biofeedback para ajustes prioritários
        for categoria, dados in biofeedback.items():
            if categoria == 'integracao_geral':
                continue
                
            if dados.get('status_atual') == 'CRÍTICO':
                recomendacoes['prioridade_alta'].append({
                    'area': categoria,
                    'problema': dados.get('recomendacao_imediata'),
                    'acao': self._definir_acao_critica(categoria, dados),
                    'prazo': '24-48 horas'
                })
            elif dados.get('status_atual') == 'ATENÇÃO':
                recomendacoes['prioridade_media'].append({
                    'area': categoria,
                    'observacao': dados.get('recomendacao_imediata'),
                    'acao': self._definir_acao_atencao(categoria, dados),
                    'prazo': '1 semana'
                })
        
        # Ajustes baseados no progresso das metas
        for meta, dados_meta in progresso.items():
            if meta == 'analise_geral':
                continue
                
            if dados_meta.get('probabilidade_sucesso', 50) < 30:
                recomendacoes['prioridade_alta'].append({
                    'area': f'Meta {meta}',
                    'problema': 'Baixa probabilidade de sucesso',
                    'acao': self._definir_acao_meta_critica(meta, dados_meta),
                    'prazo': 'Imediato'
                })
        
        # Ajustes específicos por categoria
        recomendacoes['ajustes_nutricionais'] = self._gerar_ajustes_nutricionais(biofeedback, progresso, padroes)
        recomendacoes['ajustes_treinamento'] = self._gerar_ajustes_treinamento(biofeedback, progresso, padroes)
        recomendacoes['ajustes_suplementacao'] = self._gerar_ajustes_suplementacao(biofeedback, progresso)
        recomendacoes['ajustes_recuperacao'] = self._gerar_ajustes_recuperacao(biofeedback, padroes)
        recomendacoes['ajustes_lifestyle'] = self._gerar_ajustes_lifestyle(biofeedback, padroes)
        
        # Determinar prioridade geral dos ajustes
        recomendacoes['prioridade_ajustes'] = self._determinar_prioridade_geral_ajustes(recomendacoes)
        
        return recomendacoes
    
    def _definir_protocolo_monitoramento_futuro(self, dados, recomendacoes):
        """Define protocolo de monitoramento personalizado"""
        nivel_complexidade = dados.get('nivel_experiencia', 'intermediario')
        areas_criticas = recomendacoes.get('prioridade_alta', [])
        
        protocolo = {
            'frequencia_avaliacao_completa': self._definir_frequencia_avaliacao_completa(nivel_complexidade, areas_criticas),
            'monitoramento_diario': {
                'obrigatorios': self._definir_parametros_diarios_obrigatorios(areas_criticas),
                'opcionais': self._definir_parametros_diarios_opcionais(nivel_complexidade),
                'tempo_estimado': '5-10 minutos/dia'
            },
            'monitoramento_semanal': {
                'parametros': self._definir_parametros_semanais(dados),
                'dia_recomendado': self._definir_melhor_dia_avaliacao(dados),
                'tempo_estimado': '15-30 minutos'
            },
            'monitoramento_mensal': {
                'avaliacao_completa': self._definir_avaliacao_mensal_completa(dados),
                'ajustes_protocolo': 'Baseado nos resultados mensais',
                'tempo_estimado': '60-90 minutos'
            },
            'tecnologias_sugeridas': self._sugerir_tecnologias_monitoramento(nivel_complexidade),
            'alertas_automaticos': self._definir_alertas_automaticos(areas_criticas)
        }
        
        return protocolo
    
    def _gerar_alertas_sistema(self, biofeedback, progresso):
        """Gera alertas automáticos do sistema"""
        alertas = {
            'criticos': [],
            'atencao': [],
            'informativos': [],
            'celebracao': []
        }
        
        # Alertas críticos
        for categoria, dados in biofeedback.items():
            if categoria == 'integracao_geral':
                continue
            if dados.get('status_atual') == 'CRÍTICO':
                alertas['criticos'].append({
                    'tipo': 'biofeedback_critico',
                    'categoria': categoria,
                    'mensagem': f'{categoria.title()} em nível crítico - intervenção imediata necessária',
                    'acao_requerida': dados.get('recomendacao_imediata')
                })
        
        # Alertas de atenção
        for meta, dados_meta in progresso.items():
            if meta == 'analise_geral':
                continue
            if dados_meta.get('probabilidade_sucesso', 50) < 50:
                alertas['atencao'].append({
                    'tipo': 'meta_em_risco',
                    'meta': meta,
                    'mensagem': f'Meta {meta} com baixa probabilidade de sucesso',
                    'probabilidade': f"{dados_meta.get('probabilidade_sucesso', 0):.1f}%"
                })
        
        # Alertas informativos
        alertas['informativos'] = [
            'Próxima avaliação completa em X dias',
            'Padrão identificado: melhor performance às segundas-feiras',
            'Correlação identificada: sono ruim = performance reduzida'
        ]
        
        # Celebrações (marcos atingidos)
        alertas['celebracao'] = self._identificar_marcos_celebracao(progresso)
        
        return alertas
    
    def _gerar_cronograma_avaliacoes(self, dados):
        """Gera cronograma personalizado de avaliações"""
        hoje = datetime.now()
        
        cronograma = {
            'proxima_completa': hoje + timedelta(days=28),
            'proxima_semanal': hoje + timedelta(days=7),
            'proximos_exames_laboratoriais': hoje + timedelta(days=90),
            'proxima_avaliacao_composicao_corporal': hoje + timedelta(days=14),
            'proximo_teste_performance': hoje + timedelta(days=21),
            'calendario_mensal': self._gerar_calendario_mensal_avaliacoes(dados),
            'lembretes_automaticos': {
                'biofeedback_diario': 'Todo dia às 22:00',
                'pesagem_semanal': 'Domingo pela manhã',
                'fotos_progresso': 'A cada 15 dias',
                'medidas_corporais': 'Primeiro domingo do mês'
            }
        }
        
        return cronograma
    
    def _gerar_dashboard_indicadores(self, dados):
        """Gera estrutura para dashboard de indicadores"""
        dashboard = {
            'widgets_principais': [
                {
                    'tipo': 'score_geral',
                    'titulo': 'Score Geral',
                    'valor': self._calcular_score_geral_ponderado({}),
                    'cor': self._definir_cor_score(75),
                    'tendencia': 'subindo'
                },
                {
                    'tipo': 'progresso_meta_principal',
                    'titulo': 'Meta Principal',
                    'valor': '65%',
                    'meta': 'Perder 8kg',
                    'prazo_restante': '12 semanas'
                },
                {
                    'tipo': 'biofeedback_resumo',
                    'titulo': 'Biofeedback Geral',
                    'sono': 7.5,
                    'energia': 6.2,
                    'recuperacao': 7.8,
                    'status': 'BOM'
                }
            ],
            'graficos_tendencia': [
                {
                    'tipo': 'peso_corporal',
                    'dados': 'últimas_12_semanas',
                    'meta_linha': True
                },
                {
                    'tipo': 'biofeedback_integrado',
                    'dados': 'últimas_4_semanas',
                    'areas_sombreadas': True
                },
                {
                    'tipo': 'performance_testes',
                    'dados': 'últimos_6_meses',
                    'comparativo': True
                }
            ],
            'alertas_dashboard': [
                'Sono abaixo do ideal há 3 dias',
                'Peso estagnado há 2 semanas',
                'Performance em alta - bom momento para progressão'
            ],
            'proximas_acoes': [
                'Avaliação semanal amanhã',
                'Fotos de progresso em 3 dias',
                'Ajuste nutricional recomendado'
            ]
        }
        
        return dashboard
    
    # Métodos auxiliares para cálculos específicos
    def _calcular_media_periodo(self, dados):
        """Calcula média de um período de dados"""
        if not dados or len(dados) == 0:
            return 0
        return statistics.mean(dados) if isinstance(dados[0], (int, float)) else 0
    
    def _calcular_tendencia(self, dados):
        """Calcula tendência dos dados (subindo/descendo/estável)"""
        if len(dados) < 2:
            return 'INSUFICIENTE'
        
        # Regressão linear simples
        n = len(dados)
        x = list(range(n))
        y = dados
        
        if not all(isinstance(val, (int, float)) for val in y):
            return 'DADOS_INVÁLIDOS'
        
        # Coeficiente angular
        xy_mean = sum(x[i] * y[i] for i in range(n)) / n
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        x2_mean = sum(x[i] ** 2 for i in range(n)) / n
        
        slope = (xy_mean - x_mean * y_mean) / (x2_mean - x_mean ** 2) if (x2_mean - x_mean ** 2) != 0 else 0
        
        if slope > 0.1:
            return 'SUBINDO'
        elif slope < -0.1:
            return 'DESCENDO'
        else:
            return 'ESTÁVEL'
    
    def _calcular_variabilidade(self, dados):
        """Calcula variabilidade dos dados"""
        if len(dados) < 2:
            return 0
        
        if not all(isinstance(val, (int, float)) for val in dados):
            return 0
        
        return statistics.stdev(dados)
    
    def _contar_dias_fora_ideal(self, dados, config):
        """Conta dias fora da faixa ideal"""
        valores_ideais = config.get('valores_ideais', {})
        if not valores_ideais or not dados:
            return 0
        
        # Simplificado - assumindo um parâmetro principal
        if isinstance(dados, list) and len(dados) > 0:
            return sum(1 for valor in dados if valor < 5)  # Assumindo escala 1-10
        return 0
    
    def _classificar_status_atual(self, dados, config):
        """Classifica status atual baseado nos dados"""
        if not dados:
            return 'SEM_DADOS'
        
        # Usar último valor ou média recente
        valor_atual = dados[-1] if isinstance(dados, list) else dados
        
        if isinstance(valor_atual, (int, float)):
            if valor_atual >= 7:
                return 'EXCELENTE'
            elif valor_atual >= 5:
                return 'BOM'
            elif valor_atual >= 3:
                return 'ATENÇÃO'
            else:
                return 'CRÍTICO'
        
        return 'INDEFINIDO'
    
    def _calcular_score_geral_ponderado(self, scores):
        """Calcula score geral com ponderação"""
        if not scores:
            return 75  # Valor exemplo
        
        pesos = {
            'biofeedback': 0.3,
            'progresso_metas': 0.3,
            'consistencia': 0.2,
            'adaptacao_treinamento': 0.1,
            'saude_geral': 0.1
        }
        
        score_total = sum(scores.get(key, 50) * peso for key, peso in pesos.items())
        return min(100, max(0, score_total))
    
    def _determinar_prioridade_geral_ajustes(self, recomendacoes):
        """Determina prioridade geral dos ajustes"""
        alta = len(recomendacoes.get('prioridade_alta', []))
        media = len(recomendacoes.get('prioridade_media', []))
        
        if alta > 0:
            return 'ALTA'
        elif media > 2:
            return 'MÉDIA'
        else:
            return 'BAIXA'
