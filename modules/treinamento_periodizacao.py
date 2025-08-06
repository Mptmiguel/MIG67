"""
MÓDULO 5: TREINAMENTO E PERIODIZAÇÃO
Sistema avançado de prescrição de treinamento e periodização para alta performance
"""

from flask import jsonify
import json
from datetime import datetime, timedelta
import math

class TreinamentoPeriodizacaoModule:
    def __init__(self):
        self.sistemas_energia = {
            'fosfocreatina': {'duracao_max': 15, 'recuperacao': 180, 'intensidade': 95},
            'glicoliase_anaerobica': {'duracao_max': 120, 'recuperacao': 240, 'intensidade': 85},
            'metabolismo_aerobio': {'duracao_min': 120, 'recuperacao': 60, 'intensidade': 65}
        }
        
        self.metodologias_treinamento = {
            'linear': {
                'descricao': 'Progressão gradual em volume/intensidade',
                'duracao_tipica': '12-16 semanas',
                'indicacao': 'Iniciantes a intermediários',
                'vantagens': ['Simples', 'Previsível', 'Baixo risco lesão'],
                'desvantagens': ['Adaptação limitada', 'Platôs frequentes']
            },
            'ondulatorio': {
                'descricao': 'Variação sistemática de volume/intensidade',
                'duracao_tipica': '8-12 semanas',
                'indicacao': 'Intermediários a avançados',
                'vantagens': ['Evita adaptação', 'Versatilidade', 'Recuperação otimizada'],
                'desvantagens': ['Complexidade', 'Maior planejamento']
            },
            'conjugado': {
                'descricao': 'Treinamento simultâneo de múltiplas qualidades',
                'duracao_tipica': '4-8 semanas',
                'indicacao': 'Avançados e atletas',
                'vantagens': ['Desenvolvimento integral', 'Transferência específica'],
                'desvantagens': ['Alta demanda', 'Risco de overtraining']
            },
            'dup': {
                'descricao': 'Periodização Ondulatória Diária',
                'duracao_tipica': '6-10 semanas',
                'indicacao': 'Atletas experientes',
                'vantagens': ['Variação constante', 'Adaptações múltiplas'],
                'desvantagens': ['Complexidade extrema', 'Difícil progressão']
            }
        }
        
        self.divisoes_treino = {
            'full_body': {
                'frequencia': '3-4x/semana',
                'indicacao': 'Iniciantes, cutting extremo',
                'volume_sessao': 'Moderado',
                'exercicios_sessao': '6-10',
                'vantagens': ['Alta frequência', 'Simples', 'Flexível'],
                'desvantagens': ['Limitação de volume', 'Fadiga acumulada']
            },
            'upper_lower': {
                'frequencia': '4-6x/semana',
                'indicacao': 'Intermediários',
                'volume_sessao': 'Moderado-Alto',
                'exercicios_sessao': '8-12',
                'vantagens': ['Equilíbrio', 'Recuperação adequada', 'Versatilidade'],
                'desvantagens': ['Pode ser genérico', 'Menos especialização']
            },
            'push_pull_legs': {
                'frequencia': '6x/semana (2x cada)',
                'indicacao': 'Intermediários a avançados',
                'volume_sessao': 'Alto',
                'exercicios_sessao': '6-9 por grupo',
                'vantagens': ['Alto volume', 'Especialização', 'Sinergia muscular'],
                'desvantagens': ['Demanda tempo', 'Pode ser repetitivo']
            },
            'bro_split': {
                'frequencia': '5-6x/semana',
                'indicacao': 'Avançados, foco hipertrofia',
                'volume_sessao': 'Muito Alto',
                'exercicios_sessao': '4-8 por grupo',
                'vantagens': ['Volume extremo', 'Especialização máxima'],
                'desvantagens': ['Baixa frequência', 'Menos funcional']
            }
        }
        
        self.tecnicas_intensidade = {
            'drop_sets': {
                'execucao': 'Redução imediata de carga ao atingir falha',
                'reducao_carga': '20-30%',
                'series_extras': '1-3',
                'indicacao': 'Hipertrofia, final do treino',
                'frequencia_max': '1-2x/semana por grupo muscular'
            },
            'rest_pause': {
                'execucao': 'Pausa de 10-15s após falha, continuidade',
                'pausas': '2-3',
                'indicacao': 'Hipertrofia, exercícios isolados',
                'frequencia_max': '1-2x/semana por grupo muscular'
            },
            'cluster_sets': {
                'execucao': 'Pausas intra-séries para manter intensidade',
                'pausa_intra': '15-30s',
                'indicacao': 'Força, potência',
                'beneficio': 'Manutenção da qualidade técnica'
            },
            'fst7': {
                'execucao': '7 séries finais com 30s descanso',
                'carga': '65-75% 1RM',
                'indicacao': 'Hipertrofia, exercícios isolados',
                'frequencia_max': '1x/semana por grupo muscular'
            },
            'mechanical_drop_sets': {
                'execucao': 'Mudança de exercício (mais fácil) na falha',
                'progressao': 'Difícil → Intermediário → Fácil',
                'exemplo': 'Inclinado → Reto → Declinado',
                'indicacao': 'Hipertrofia avançada'
            },
            'pre_exaustao': {
                'execucao': 'Isolado até fadiga + Composto imediatamente',
                'objetivo': 'Pré-fadiga do músculo alvo',
                'exemplo': 'Crucifixo + Supino',
                'indicacao': 'Hipertrofia, quebra de platôs'
            }
        }
        
        self.parametros_treinamento = {
            'forca_maxima': {
                'intensidade': '85-100% 1RM',
                'series': '3-6',
                'repeticoes': '1-5',
                'descanso': '3-5 minutos',
                'frequencia_semanal': '2-3x',
                'exercicios': 'Compostos, específicos',
                'volume_semanal': '10-20 séries/grupo muscular'
            },
            'hipertrofia': {
                'intensidade': '65-85% 1RM',
                'series': '3-5',
                'repeticoes': '6-12',
                'descanso': '1-3 minutos',
                'frequencia_semanal': '2-3x',
                'exercicios': 'Compostos + isolados',
                'volume_semanal': '12-20+ séries/grupo muscular'
            },
            'forca_resistencia': {
                'intensidade': '50-70% 1RM',
                'series': '3-4',
                'repeticoes': '12-20+',
                'descanso': '30s-2 minutos',
                'frequencia_semanal': '3-4x',
                'exercicios': 'Variados',
                'volume_semanal': '15-25+ séries/grupo muscular'
            },
            'potencia': {
                'intensidade': '30-60% 1RM (velocidade máxima)',
                'series': '3-6',
                'repeticoes': '1-6',
                'descanso': '2-5 minutos',
                'frequencia_semanal': '2-4x',
                'exercicios': 'Explosivos, pliométricos',
                'volume_semanal': '6-15 séries'
            }
        }
        
        self.exercicios_base = {
            'compostos_principais': {
                'agachamento': {
                    'grupos_primarios': ['Quadríceps', 'Glúteos'],
                    'grupos_secundarios': ['Core', 'Panturrilhas'],
                    'variações': ['Back squat', 'Front squat', 'Bulgarian', 'Pistol'],
                    'progressoes': ['Peso corporal', 'Goblet', 'Barra', 'Avançadas']
                },
                'levantamento_terra': {
                    'grupos_primarios': ['Posterior coxa', 'Glúteos', 'Lombar'],
                    'grupos_secundarios': ['Trapézio', 'Latíssimo', 'Core'],
                    'variações': ['Convencional', 'Sumo', 'Romeno', 'Stiff'],
                    'progressoes': ['Deficit', 'Paused', 'Chains', 'Bands']
                },
                'supino': {
                    'grupos_primarios': ['Peitoral', 'Tríceps', 'Deltoide anterior'],
                    'grupos_secundarios': ['Core', 'Serrátil'],
                    'variações': ['Reto', 'Inclinado', 'Declinado', 'Halteres'],
                    'progressoes': ['Paused', 'Tempo', 'Chains', '1 1/4 reps']
                },
                'desenvolvimento': {
                    'grupos_primarios': ['Deltoides', 'Tríceps'],
                    'grupos_secundarios': ['Trapézio', 'Core'],
                    'variações': ['Militar', 'Push press', 'Halteres', 'Arnold'],
                    'progressoes': ['Sentado', 'Em pé', 'Behind neck', 'Single arm']
                }
            },
            'auxiliares_importantes': {
                'remada': ['Curvada', 'T-bar', 'Cavalinho', 'Unilateral'],
                'barra_fixa': ['Pronada', 'Supinada', 'Neutra', 'L-sit'],
                'paralelas': ['Mergulho', 'Dips', 'Ring dips', 'Weighted'],
                'farmers_walk': ['Tradicional', 'Unilateral', 'Overhead', 'Mixed']
            }
        }
        
    def gerar_plano_treino(self, dados):
        """
        Gera plano de treinamento personalizado e periodização
        """
        try:
            # Validar dados obrigatórios
            campos_obrigatorios = ['objetivo', 'nivel_experiencia', 'frequencia_semanal', 'tempo_disponivel']
            for campo in campos_obrigatorios:
                if campo not in dados:
                    return jsonify({
                        'success': False,
                        'message': f'Campo obrigatório não preenchido: {campo}'
                    })
            
            # Analisar perfil de treinamento
            perfil_treinamento = self._analisar_perfil_treinamento(dados)
            
            # Definir metodologia de periodização
            metodologia = self._definir_metodologia_periodizacao(dados, perfil_treinamento)
            
            # Selecionar divisão de treino
            divisao_treino = self._selecionar_divisao_treino(dados, perfil_treinamento)
            
            # Prescrever parâmetros de treinamento
            parametros = self._prescrever_parametros_treinamento(dados, perfil_treinamento)
            
            # Gerar macrociclo (12-16 semanas)
            macrociclo = self._gerar_macrociclo(dados, metodologia, parametros)
            
            # Gerar mesociclos (4 semanas cada)
            mesociclos = self._gerar_mesociclos(dados, macrociclo, parametros)
            
            # Gerar microciclos (semana típica)
            microciclos = self._gerar_microciclos(dados, divisao_treino, parametros)
            
            # Prescrever exercícios específicos
            prescricao_exercicios = self._prescrever_exercicios(dados, divisao_treino, parametros)
            
            # Definir progressões
            progressoes = self._definir_progressoes(dados, parametros)
            
            # Protocolos de recuperação
            recuperacao = self._definir_protocolos_recuperacao(dados, perfil_treinamento)
            
            # Monitoramento de carga
            monitoramento = self._definir_monitoramento_carga(dados, metodologia)
            
            resultado = {
                'success': True,
                'plano_treinamento': {
                    'resumo_executivo': {
                        'objetivo_principal': dados['objetivo'],
                        'metodologia': metodologia['tipo'],
                        'divisao_treino': divisao_treino['tipo'],
                        'frequencia_semanal': dados['frequencia_semanal'],
                        'duracao_macrociclo': f"{macrociclo['duracao_semanas']} semanas",
                        'nivel_complexidade': perfil_treinamento['nivel_complexidade']
                    },
                    'perfil_treinamento': perfil_treinamento,
                    'metodologia_periodizacao': metodologia,
                    'divisao_treino': divisao_treino,
                    'parametros_treinamento': parametros,
                    'macrociclo': macrociclo,
                    'mesociclos': mesociclos,
                    'microciclos_exemplo': microciclos,
                    'prescricao_exercicios': prescricao_exercicios,
                    'progressoes': progressoes,
                    'protocolos_recuperacao': recuperacao,
                    'monitoramento_carga': monitoramento
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify(resultado)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erro ao gerar plano de treinamento: {str(e)}'
            })
    
    def _analisar_perfil_treinamento(self, dados):
        """Analisa perfil específico para prescrição de treinamento"""
        nivel = dados.get('nivel_experiencia', 'iniciante').lower()
        objetivo = dados.get('objetivo', '').lower()
        limitacoes = dados.get('limitacoes_fisicas', [])
        tempo_disponivel = dados.get('tempo_disponivel', 60)  # minutos por sessão
        
        # Classificar nível de complexidade
        if nivel == 'iniciante':
            complexidade = 'BÁSICA'
            capacidade_volume = 1.0
        elif nivel == 'intermediario':
            complexidade = 'MODERADA'
            capacidade_volume = 1.3
        elif nivel == 'avancado':
            complexidade = 'ALTA'
            capacidade_volume = 1.6
        else:  # atleta
            complexidade = 'EXTREMA'
            capacidade_volume = 2.0
        
        # Analisar limitações e adaptações necessárias
        adaptacoes = []
        if 'lombar' in ' '.join(limitacoes).lower():
            adaptacoes.append('Evitar flexão lombar excessiva')
            adaptacoes.append('Priorizar estabilização do core')
        
        if 'joelho' in ' '.join(limitacoes).lower():
            adaptacoes.append('Amplitude controlada em agachamentos')
            adaptacoes.append('Enfatizar fortalecimento do quadríceps')
        
        if 'ombro' in ' '.join(limitacoes).lower():
            adaptacoes.append('Evitar movimentos overhead agressivos')
            adaptacoes.append('Priorizar mobilidade escapular')
        
        # Calcular volume semanal recomendado
        volume_base = {
            'iniciante': 10,
            'intermediario': 16,
            'avancado': 22,
            'atleta': 28
        }.get(nivel, 10)
        
        volume_semanal = int(volume_base * capacidade_volume)
        
        return {
            'nivel_experiencia': nivel,
            'nivel_complexidade': complexidade,
            'capacidade_volume': capacidade_volume,
            'volume_semanal_recomendado': f'{volume_semanal} séries/grupo muscular',
            'adaptacoes_necessarias': adaptacoes,
            'tempo_sessao': tempo_disponivel,
            'limitacoes_identificadas': limitacoes,
            'prioridades_treinamento': self._definir_prioridades_treinamento(objetivo, limitacoes)
        }
    
    def _definir_prioridades_treinamento(self, objetivo, limitacoes):
        """Define prioridades específicas de treinamento"""
        prioridades = []
        
        if 'hipertrofia' in objetivo:
            prioridades.extend(['Volume alto', 'Tensão mecânica', 'Stress metabólico'])
        elif 'forca' in objetivo:
            prioridades.extend(['Intensidade alta', 'Especificidade', 'Técnica perfeita'])
        elif 'emagrecimento' in objetivo:
            prioridades.extend(['Densidade', 'HIIT', 'Preservação massa magra'])
        elif 'performance' in objetivo:
            prioridades.extend(['Potência', 'Coordenação', 'Transferência esportiva'])
        
        # Prioridades baseadas em limitações
        if limitacoes:
            prioridades.insert(0, 'Reabilitação/Prevenção')
            prioridades.insert(1, 'Mobilidade e estabilidade')
        
        return prioridades
    
    def _definir_metodologia_periodizacao(self, dados, perfil):
        """Define metodologia de periodização mais adequada"""
        nivel = perfil['nivel_experiencia']
        objetivo = dados.get('objetivo', '').lower()
        tempo_disponivel = dados.get('tempo_disponivel_total', 12)  # semanas
        
        if nivel == 'iniciante':
            metodologia = 'linear'
        elif nivel == 'intermediario':
            if 'hipertrofia' in objetivo:
                metodologia = 'ondulatorio'
            else:
                metodologia = 'linear'
        elif nivel == 'avancado':
            if tempo_disponivel <= 8:
                metodologia = 'conjugado'
            else:
                metodologia = 'ondulatorio'
        else:  # atleta
            if 'competicao' in objetivo:
                metodologia = 'conjugado'
            else:
                metodologia = 'dup'
        
        metodologia_info = self.metodologias_treinamento[metodologia].copy()
        metodologia_info['tipo'] = metodologia
        
        # Personalizar baseado no objetivo
        if 'forca' in objetivo:
            metodologia_info['fases'] = self._definir_fases_forca(metodologia)
        elif 'hipertrofia' in objetivo:
            metodologia_info['fases'] = self._definir_fases_hipertrofia(metodologia)
        elif 'performance' in objetivo:
            metodologia_info['fases'] = self._definir_fases_performance(metodologia)
        
        return metodologia_info
    
    def _definir_fases_forca(self, metodologia):
        """Define fases específicas para desenvolvimento de força"""
        if metodologia == 'linear':
            return {
                'anatomica': {'semanas': '1-4', 'foco': 'Adaptação anatômica', 'intensidade': '60-70%'},
                'hipertrofia': {'semanas': '5-8', 'foco': 'Hipertrofia funcional', 'intensidade': '70-80%'},
                'forca_maxima': {'semanas': '9-12', 'foco': 'Força máxima', 'intensidade': '80-95%'},
                'pico': {'semanas': '13-14', 'foco': 'Pico de força', 'intensidade': '90-100%'}
            }
        elif metodologia == 'ondulatorio':
            return {
                'bloco_1': {'semanas': '1-4', 'foco': 'Volume alto', 'variacao': 'Força-Hipertrofia'},
                'bloco_2': {'semanas': '5-8', 'foco': 'Intensidade moderada', 'variacao': 'Força-Potência'},
                'bloco_3': {'semanas': '9-12', 'foco': 'Intensidade alta', 'variacao': 'Força máxima'}
            }
        
        return {}
    
    def _selecionar_divisao_treino(self, dados, perfil):
        """Seleciona divisão de treino mais adequada"""
        freq_semanal = dados.get('frequencia_semanal', 3)
        nivel = perfil['nivel_experiencia']
        objetivo = dados.get('objetivo', '').lower()
        tempo_sessao = perfil['tempo_sessao']
        
        # Lógica de seleção baseada na frequência e nível
        if freq_semanal <= 3:
            divisao_escolhida = 'full_body'
        elif freq_semanal == 4:
            divisao_escolhida = 'upper_lower'
        elif freq_semanal == 5:
            if nivel in ['avancado', 'atleta'] and 'hipertrofia' in objetivo:
                divisao_escolhida = 'bro_split'
            else:
                divisao_escolhida = 'upper_lower'
        elif freq_semanal >= 6:
            if nivel in ['intermediario', 'avancado', 'atleta']:
                divisao_escolhida = 'push_pull_legs'
            else:
                divisao_escolhida = 'upper_lower'
        
        divisao_info = self.divisoes_treino[divisao_escolhida].copy()
        divisao_info['tipo'] = divisao_escolhida
        
        # Personalizar divisão baseada no objetivo
        if divisao_escolhida == 'push_pull_legs':
            divisao_info['distribuicao'] = {
                'push': ['Peito', 'Ombros', 'Tríceps'],
                'pull': ['Costas', 'Bíceps', 'Posterior de coxa'],
                'legs': ['Quadríceps', 'Glúteos', 'Panturrilhas']
            }
        elif divisao_escolhida == 'upper_lower':
            divisao_info['distribuicao'] = {
                'upper': ['Peito', 'Costas', 'Ombros', 'Bíceps', 'Tríceps'],
                'lower': ['Quadríceps', 'Posterior coxa', 'Glúteos', 'Panturrilhas']
            }
        
        return divisao_info
    
    def _prescrever_parametros_treinamento(self, dados, perfil):
        """Prescreve parâmetros específicos de treinamento"""
        objetivo = dados.get('objetivo', '').lower()
        nivel = perfil['nivel_experiencia']
        
        # Determinar objetivo primário de treinamento
        if 'forca' in objetivo:
            objetivo_primario = 'forca_maxima'
        elif 'hipertrofia' in objetivo or 'massa' in objetivo:
            objetivo_primario = 'hipertrofia'
        elif 'resistencia' in objetivo or 'emagrecimento' in objetivo:
            objetivo_primario = 'forca_resistencia'
        elif 'potencia' in objetivo or 'explosao' in objetivo:
            objetivo_primario = 'potencia'
        else:
            objetivo_primario = 'hipertrofia'  # default
        
        parametros_base = self.parametros_treinamento[objetivo_primario].copy()
        
        # Personalizar baseado no nível
        if nivel == 'iniciante':
            parametros_base['series'] = '2-3'
            parametros_base['volume_semanal'] = parametros_base['volume_semanal'].replace('20', '15')
        elif nivel in ['avancado', 'atleta']:
            if 'hipertrofia' in objetivo:
                parametros_base['volume_semanal'] = '16-25 séries/grupo muscular'
        
        # Definir parâmetros específicos por fase
        parametros_base['progressao'] = self._definir_progressao_parametros(objetivo_primario, nivel)
        parametros_base['tecnicas_intensidade'] = self._selecionar_tecnicas_intensidade(objetivo_primario, nivel)
        
        return {
            'objetivo_primario': objetivo_primario,
            'parametros_base': parametros_base,
            'adaptacoes_nivel': f'Adaptado para {nivel}',
            'volume_progressivo': True
        }
    
    def _selecionar_tecnicas_intensidade(self, objetivo, nivel):
        """Seleciona técnicas de intensidade apropriadas"""
        if nivel == 'iniciante':
            return ['Foco na técnica básica']
        
        tecnicas = []
        
        if objetivo == 'hipertrofia':
            if nivel == 'intermediario':
                tecnicas.extend(['drop_sets', 'rest_pause'])
            elif nivel in ['avancado', 'atleta']:
                tecnicas.extend(['drop_sets', 'rest_pause', 'fst7', 'pre_exaustao'])
        
        elif objetivo == 'forca_maxima':
            if nivel in ['intermediario', 'avancado', 'atleta']:
                tecnicas.extend(['cluster_sets', 'pause_reps'])
        
        elif objetivo == 'potencia':
            tecnicas.extend(['cluster_sets', 'contrast_training'])
        
        # Adicionar detalhes das técnicas selecionadas
        tecnicas_detalhadas = []
        for tecnica in tecnicas:
            if tecnica in self.tecnicas_intensidade:
                info = self.tecnicas_intensidade[tecnica].copy()
                info['nome'] = tecnica
                tecnicas_detalhadas.append(info)
        
        return tecnicas_detalhadas
    
    def _gerar_macrociclo(self, dados, metodologia, parametros):
        """Gera estrutura do macrociclo"""
        duracao_total = dados.get('tempo_disponivel_total', 12)
        objetivo = dados.get('objetivo', '').lower()
        
        # Determinar fases do macrociclo
        if 'competicao' in dados.get('data_competicao', ''):
            fases = self._gerar_macrociclo_competitivo(duracao_total)
        else:
            fases = self._gerar_macrociclo_geral(duracao_total, objetivo)
        
        return {
            'duracao_semanas': duracao_total,
            'metodologia': metodologia['tipo'],
            'fases': fases,
            'periodizacao_volume': self._calcular_periodizacao_volume(fases),
            'periodizacao_intensidade': self._calcular_periodizacao_intensidade(fases),
            'deload_weeks': self._definir_semanas_deload(duracao_total)
        }
    
    def _gerar_macrociclo_geral(self, duracao, objetivo):
        """Gera fases para macrociclo geral"""
        if duracao <= 8:
            return {
                'preparatoria': {'semanas': f'1-{duracao//2}', 'foco': 'Volume e adaptação'},
                'especifica': {'semanas': f'{duracao//2+1}-{duracao-1}', 'foco': 'Intensidade específica'},
                'pico': {'semanas': f'{duracao}', 'foco': 'Pico de performance'}
            }
        elif duracao <= 16:
            return {
                'adaptacao_anatomica': {'semanas': '1-4', 'foco': 'Adaptação estrutural'},
                'desenvolvimento': {'semanas': '5-10', 'foco': 'Desenvolvimento das qualidades'},
                'intensificacao': {'semanas': '11-14', 'foco': 'Intensificação específica'},
                'pico_tapering': {'semanas': '15-16', 'foco': 'Pico e recuperação'}
            }
        else:
            return {
                'preparacao_geral': {'semanas': '1-6', 'foco': 'Base aeróbia e força geral'},
                'preparacao_especifica': {'semanas': '7-12', 'foco': 'Desenvolvimento específico'},
                'pre_competitiva': {'semanas': '13-18', 'foco': 'Intensidade específica'},
                'competitiva': {'semanas': '19-20', 'foco': 'Manutenção e pico'}
            }
    
    def _gerar_mesociclos(self, dados, macrociclo, parametros):
        """Gera estrutura dos mesociclos (4 semanas cada)"""
        mesociclos = []
        semana_atual = 1
        
        for fase_nome, fase_info in macrociclo['fases'].items():
            # Extrair número de semanas da fase
            if '-' in fase_info['semanas']:
                inicio, fim = map(int, fase_info['semanas'].split('-'))
                duracao_fase = fim - inicio + 1
            else:
                duracao_fase = 1
            
            # Criar mesociclos de 4 semanas (ou menos se a fase for menor)
            while duracao_fase > 0:
                duracao_mesociclo = min(4, duracao_fase)
                
                mesociclo = {
                    'nome': f'Mesociclo {len(mesociclos) + 1}',
                    'fase_macrociclo': fase_nome,
                    'semanas': f'{semana_atual}-{semana_atual + duracao_mesociclo - 1}',
                    'duracao': f'{duracao_mesociclo} semanas',
                    'foco_principal': fase_info['foco'],
                    'progressao': self._definir_progressao_mesociclo(fase_nome, parametros),
                    'volume_relativo': self._calcular_volume_mesociclo(fase_nome),
                    'intensidade_relativa': self._calcular_intensidade_mesociclo(fase_nome)
                }
                
                # Determinar se há semana de deload
                if duracao_mesociclo == 4:
                    mesociclo['deload_semana'] = semana_atual + 3
                    mesociclo['estrutura'] = 'Carga-Carga-Carga-Deload'
                else:
                    mesociclo['estrutura'] = 'Progressão linear'
                
                mesociclos.append(mesociclo)
                semana_atual += duracao_mesociclo
                duracao_fase -= duracao_mesociclo
        
        return mesociclos
    
    def _gerar_microciclos(self, dados, divisao_treino, parametros):
        """Gera estrutura dos microciclos (semana típica)"""
        freq_semanal = dados.get('frequencia_semanal', 3)
        divisao_tipo = divisao_treino['tipo']
        
        microciclos = {
            'estrutura_semanal': self._definir_estrutura_semanal(freq_semanal, divisao_tipo),
            'distribuicao_volume': self._distribuir_volume_semanal(divisao_tipo, freq_semanal),
            'progressao_semanal': self._definir_progressao_semanal(parametros),
            'exemplo_semana': self._gerar_exemplo_semana(divisao_tipo, freq_semanal)
        }
        
        return microciclos
    
    def _definir_estrutura_semanal(self, frequencia, divisao):
        """Define estrutura semanal de treinamento"""
        estruturas = {
            'full_body': {
                3: ['FB', 'Descanso', 'FB', 'Descanso', 'FB', 'Descanso', 'Descanso'],
                4: ['FB', 'Descanso', 'FB', 'Descanso', 'FB', 'Descanso', 'FB']
            },
            'upper_lower': {
                4: ['Upper', 'Lower', 'Descanso', 'Upper', 'Lower', 'Descanso', 'Descanso'],
                5: ['Upper', 'Lower', 'Descanso', 'Upper', 'Lower', 'Upper', 'Descanso'],
                6: ['Upper', 'Lower', 'Upper', 'Lower', 'Descanso', 'Upper', 'Lower']
            },
            'push_pull_legs': {
                6: ['Push', 'Pull', 'Legs', 'Push', 'Pull', 'Legs', 'Descanso']
            },
            'bro_split': {
                5: ['Peito', 'Costas', 'Pernas', 'Ombros', 'Braços', 'Descanso', 'Descanso']
            }
        }
        
        return estruturas.get(divisao, {}).get(frequencia, ['Personalizar conforme necessidade'])
    
    def _prescrever_exercicios(self, dados, divisao_treino, parametros):
        """Prescreve exercícios específicos baseados na divisão e objetivos"""
        divisao_tipo = divisao_treino['tipo']
        objetivo = parametros['objetivo_primario']
        nivel = dados.get('nivel_experiencia', 'iniciante')
        
        prescricoes = {}
        
        if divisao_tipo == 'push_pull_legs':
            prescricoes = {
                'push': self._prescrever_push(objetivo, nivel),
                'pull': self._prescrever_pull(objetivo, nivel),
                'legs': self._prescrever_legs(objetivo, nivel)
            }
        elif divisao_tipo == 'upper_lower':
            prescricoes = {
                'upper': self._prescrever_upper(objetivo, nivel),
                'lower': self._prescrever_lower(objetivo, nivel)
            }
        elif divisao_tipo == 'full_body':
            prescricoes = {
                'full_body': self._prescrever_full_body(objetivo, nivel)
            }
        
        return prescricoes
    
    def _prescrever_push(self, objetivo, nivel):
        """Prescreve exercícios para treino push"""
        exercicios = []
        
        # Exercício composto principal
        if nivel == 'iniciante':
            exercicios.append({
                'exercicio': 'Supino reto',
                'series': '3',
                'repeticoes': '8-10',
                'descanso': '90s',
                'observacoes': 'Foco na técnica'
            })
        else:
            exercicios.append({
                'exercicio': 'Supino reto/inclinado (alternar)',
                'series': '4',
                'repeticoes': '6-8',
                'descanso': '120s',
                'observacoes': 'Exercício principal'
            })
        
        # Desenvolvimento para ombros
        exercicios.append({
            'exercicio': 'Desenvolvimento com halteres',
            'series': '3-4',
            'repeticoes': '8-12',
            'descanso': '90s',
            'observacoes': 'Amplitude completa'
        })
        
        # Isolados para peito
        if nivel != 'iniciante':
            exercicios.append({
                'exercicio': 'Crucifixo inclinado',
                'series': '3',
                'repeticoes': '10-15',
                'descanso': '60s',
                'observacoes': 'Contração máxima'
            })
        
        # Tríceps
        exercicios.append({
            'exercicio': 'Tríceps testa/corda',
            'series': '3',
            'repeticoes': '10-15',
            'descanso': '60s',
            'observacoes': 'Controle excêntrico'
        })
        
        return exercicios
    
    def _definir_progressoes(self, dados, parametros):
        """Define protocolos de progressão"""
        objetivo = parametros['objetivo_primario']
        nivel = dados.get('nivel_experiencia', 'iniciante')
        
        progressoes = {
            'sobrecarga_progressiva': {
                'tipo_principal': self._definir_tipo_progressao(objetivo, nivel),
                'frequencia_progressao': self._definir_frequencia_progressao(nivel),
                'magnitude_progressao': self._definir_magnitude_progressao(objetivo),
                'criterios_progressao': self._definir_criterios_progressao(objetivo)
            },
            'periodizacao_carga': {
                'modelo': 'Linear' if nivel == 'iniciante' else 'Ondulatório',
                'progressao_semanal': self._calcular_progressao_semanal(objetivo),
                'deload_frequencia': 'A cada 4-6 semanas'
            },
            'ajustes_exercicios': {
                'progressao_movimento': self._definir_progressao_movimento(nivel),
                'variabilidade': self._definir_variabilidade_exercicios(nivel),
                'especializacao': self._definir_especializacao(objetivo)
            }
        }
        
        return progressoes
    
    def _definir_protocolos_recuperacao(self, dados, perfil):
        """Define protocolos específicos de recuperação"""
        nivel = perfil['nivel_experiencia']
        volume_treino = perfil['volume_semanal_recomendado']
        limitacoes = perfil['limitacoes_identificadas']
        
        protocolos = {
            'recuperacao_ativa': {
                'frequencia': '2-3x por semana',
                'atividades': ['Caminhada leve', 'Yoga', 'Natação recreativa'],
                'duracao': '20-40 minutos',
                'intensidade': '40-60% FCmax'
            },
            'mobilidade_flexibilidade': {
                'frequencia': 'Diária',
                'duracao': '10-20 minutos',
                'foco_areas': self._definir_foco_mobilidade(limitacoes),
                'tecnicas': ['Alongamento estático', 'Foam rolling', 'Mobilização articular']
            },
            'sono_recuperacao': {
                'horas_recomendadas': '7-9 horas/noite',
                'qualidade': 'Ambiente escuro, temperatura amena',
                'suplementacao': 'Magnésio, melatonina (se necessário)',
                'monitoramento': 'Diário de sono'
            },
            'nutricao_recuperacao': {
                'pos_treino': 'Proteína + carboidratos em 30-60min',
                'hidratacao': '35ml/kg peso corporal/dia',
                'anti_inflamatorios': 'Ômega-3, curcumina, frutas vermelhas'
            },
            'tecnicas_avancadas': self._definir_tecnicas_recuperacao_avancadas(nivel)
        }
        
        return protocolos
    
    def _definir_monitoramento_carga(self, dados, metodologia):
        """Define sistema de monitoramento de carga de treinamento"""
        nivel = dados.get('nivel_experiencia', 'iniciante')
        
        monitoramento = {
            'indicadores_objetivos': {
                'volume_semanal': 'Total de séries por grupo muscular',
                'intensidade_media': '% 1RM média das sessões',
                'tonnage': 'Volume x Intensidade (kg total movimentado)',
                'densidade': 'Volume/tempo total de treino'
            },
            'indicadores_subjetivos': {
                'rpe_sessao': 'RPE (1-10) ao final de cada sessão',
                'qualidade_sono': 'Escala 1-10 diária',
                'disposicao_treino': 'Escala 1-10 pré-treino',
                'dor_muscular': 'DOMS (1-5) 24-48h pós-treino'
            },
            'biofeedback': {
                'frequencia_cardiaca_repouso': 'Diária (ao acordar)',
                'variabilidade_fc': 'Se disponível equipamento',
                'peso_corporal': 'Diário (mesmo horário)',
                'circunferencias': 'Semanal'
            },
            'testes_performance': self._definir_testes_performance(dados),
            'ajustes_baseados_feedback': {
                'alta_fadiga': 'Reduzir volume 10-20%',
                'baixa_disposicao': 'Sessão regenerativa',
                'plateau_forca': 'Deload ou mudança exercícios',
                'overreaching': 'Redução drástica ou descanso'
            }
        }
        
        return monitoramento
    
    # Métodos auxiliares para definições específicas
    def _definir_tipo_progressao(self, objetivo, nivel):
        """Define tipo principal de progressão"""
        if objetivo == 'forca_maxima':
            return 'Aumento de carga'
        elif objetivo == 'hipertrofia':
            return 'Volume progressivo'
        elif objetivo == 'forca_resistencia':
            return 'Aumento de repetições'
        else:
            return 'Combinado'
    
    def _definir_testes_performance(self, dados):
        """Define testes de performance específicos"""
        objetivo = dados.get('objetivo', '').lower()
        
        testes = {
            'forca': ['1RM supino', '1RM agachamento', '1RM levantamento terra'],
            'resistencia': ['Teste 12 minutos Cooper', 'Máximo de flexões', 'Prancha isométrica'],
            'composicao_corporal': ['Bioimpedância', 'Circunferências', 'Fotos comparativas'],
            'mobilidade': ['FMS', 'Teste sentar-alcançar', 'Overhead squat assessment']
        }
        
        if 'forca' in objetivo:
            return testes['forca'] + testes['composicao_corporal']
        elif 'hipertrofia' in objetivo:
            return testes['composicao_corporal'] + ['Força submáxima']
        elif 'emagrecimento' in objetivo:
            return testes['resistencia'] + testes['composicao_corporal']
        else:
            return testes['composicao_corporal']
    
    def _calcular_progressao_semanal(self, objetivo):
        """Calcula progressão semanal ideal"""
        if objetivo == 'forca_maxima':
            return '2.5-5% aumento carga/semana'
        elif objetivo == 'hipertrofia':
            return '1-2 séries adicionais/semana ou 2.5% carga'
        else:
            return '1-2 repetições adicionais ou 2.5% carga'
    
    def _definir_foco_mobilidade(self, limitacoes):
        """Define foco da mobilidade baseado nas limitações"""
        focos = []
        
        if not limitacoes:
            focos = ['Ombros', 'Quadris', 'Coluna torácica', 'Tornozelos']
        else:
            for limitacao in limitacoes:
                if 'lombar' in limitacao.lower():
                    focos.extend(['Flexores do quadril', 'Isquiotibiais', 'Core'])
                elif 'joelho' in limitacao.lower():
                    focos.extend(['Quadríceps', 'IT band', 'Panturrilhas'])
                elif 'ombro' in limitacao.lower():
                    focos.extend(['Peitoral', 'Latíssimo', 'Escapulares'])
        
        return list(set(focos))  # Remove duplicatas
    
    def _definir_tecnicas_recuperacao_avancadas(self, nivel):
        """Define técnicas avançadas baseadas no nível"""
        if nivel in ['avancado', 'atleta']:
            return {
                'crioterapia': 'Banhos de gelo 10-15min pós-treino intenso',
                'contraste_termico': 'Alternância quente-frio',
                'massagem_esportiva': '1-2x por semana',
                'compressao_pneumatica': 'Se disponível',
                'sauna': '15-20min 3-4x por semana'
            }
        else:
            return {
                'banho_quente': 'Relaxamento muscular',
                'automassagem': 'Foam roller diário',
                'tecnicas_respiracao': 'Meditação/relaxamento'
            }
