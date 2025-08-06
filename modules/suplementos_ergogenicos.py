"""
MÓDULO 4: PRESCRIÇÃO DE SUPLEMENTOS E ERGOGÊNICOS
Sistema de prescrição individualizada de suplementos, farmacologia esportiva e substâncias ergogênicas
"""

from flask import jsonify
import json
from datetime import datetime, timedelta

class SuplementosErgogenicosModule:
    def __init__(self):
        self.suplementos_naturais = {
            'creatina': {
                'dosagem': '3-5g/dia',
                'timing': 'Qualquer horário (consistência)',
                'duracao': 'Uso contínuo',
                'evidencia': 'A+',
                'mecanismo': 'Aumenta fosfocreatina muscular',
                'beneficios': ['Força', 'Potência', 'Volume muscular', 'Recuperação'],
                'efeitos_colaterais': 'Mínimos (retenção hídrica)',
                'contraindicacoes': 'Disfunção renal severa',
                'interacoes': 'Nenhuma significativa'
            },
            'beta_alanina': {
                'dosagem': '3-5g/dia dividida em doses',
                'timing': 'Com refeições (reduzir parestesia)',
                'duracao': '4-6 semanas para saturação',
                'evidencia': 'A',
                'mecanismo': 'Aumenta carnosina muscular',
                'beneficios': ['Resistência muscular', 'Reduz fadiga em exercícios 1-4min'],
                'efeitos_colaterais': 'Formigamento (parestesia)',
                'contraindicacoes': 'Nenhuma conhecida',
                'interacoes': 'Potencializa com bicarbonato de sódio'
            },
            'cafeina': {
                'dosagem': '3-6mg/kg peso corporal',
                'timing': '30-45min pré-treino',
                'duracao': 'Uso intermitente (evitar tolerância)',
                'evidencia': 'A+',
                'mecanismo': 'Antagonista adenosina, estimula SNC',
                'beneficios': ['Energia', 'Foco', 'Resistência', 'Termogênese'],
                'efeitos_colaterais': 'Insônia, ansiedade, taquicardia',
                'contraindicacoes': 'Hipertensão descontrolada, arritmias',
                'interacoes': 'Potencializa com L-teanina'
            },
            'citrulina': {
                'dosagem': '6-8g/dia',
                'timing': '30-60min pré-treino',
                'duracao': 'Uso contínuo',
                'evidencia': 'B+',
                'mecanismo': 'Precursor de arginina, aumenta NO',
                'beneficios': ['Pump muscular', 'Resistência', 'Recuperação'],
                'efeitos_colaterais': 'Mínimos',
                'contraindicacoes': 'Nenhuma conhecida',
                'interacoes': 'Sinérgico com arginina'
            }
        }
        
        self.suplementacao_avancada = {
            'nootropicos': {
                'alpha_gpc': {
                    'dosagem': '300-600mg/dia',
                    'mecanismo': 'Precursor de acetilcolina',
                    'beneficios': ['Foco', 'Conexão mente-músculo', 'Força'],
                    'timing': 'Pré-treino'
                },
                'rhodiola_rosea': {
                    'dosagem': '200-400mg/dia',
                    'mecanismo': 'Adaptógeno, reduz cortisol',
                    'beneficios': ['Reduz fadiga', 'Melhora humor', 'Adaptação ao stress'],
                    'timing': 'Manhã, estômago vazio'
                },
                'bacopa_monnieri': {
                    'dosagem': '300-600mg/dia',
                    'mecanismo': 'Neuroproteção, melhora cognição',
                    'beneficios': ['Memória', 'Reduz ansiedade', 'Neuroplasticidade'],
                    'timing': 'Com refeições'
                }
            },
            'adaptogenos': {
                'ashwagandha': {
                    'dosagem': '300-500mg/dia',
                    'mecanismo': 'Reduz cortisol, modula sistema nervoso',
                    'beneficios': ['Reduz stress', 'Melhora testosterona', 'Qualidade do sono'],
                    'timing': 'Noite ou manhã'
                },
                'ginseng_siberiano': {
                    'dosagem': '400-800mg/dia',
                    'mecanismo': 'Adaptógeno, melhora resistência ao stress',
                    'beneficios': ['Energia', 'Resistência', 'Função imune'],
                    'timing': 'Manhã'
                }
            }
        }
        
        self.farmacos_ergogenicos = {
            'esteroides_anabolizantes': {
                'testosterona_enantato': {
                    'classificacao': 'Testosterona de depósito',
                    'meia_vida': '4-5 dias',
                    'dosagem_iniciante': '300-500mg/semana',
                    'dosagem_avancado': '500-750mg/semana',
                    'frequencia': '2x por semana',
                    'duracao_ciclo': '12-16 semanas',
                    'aromatizacao': 'Alta',
                    'hepatotoxicidade': 'Baixa',
                    'efeitos_positivos': ['Ganho de massa muscular', 'Força', 'Recuperação'],
                    'efeitos_colaterais': ['Ginecomastia', 'Retenção hídrica', 'Acne'],
                    'monitoramento': ['Hemograma', 'Perfil lipídico', 'Função hepática', 'Estradiol']
                },
                'masteron': {
                    'classificacao': 'Diidrotestosterona derivado',
                    'meia_vida': '2-3 dias',
                    'dosagem': '300-600mg/semana',
                    'frequencia': 'EOD ou diário',
                    'duracao_ciclo': '8-12 semanas',
                    'aromatizacao': 'Nenhuma',
                    'hepatotoxicidade': 'Baixa',
                    'efeitos_positivos': ['Definição muscular', 'Dureza', 'Anti-estrogênico'],
                    'efeitos_colaterais': ['Queda de cabelo', 'Acne', 'Agressividade'],
                    'uso_tipico': 'Cutting/Pré-contest'
                },
                'boldenona': {
                    'classificacao': 'Testosterona modificada',
                    'meia_vida': '14 dias',
                    'dosagem': '400-800mg/semana',
                    'frequencia': '1-2x por semana',
                    'duracao_ciclo': '16-20 semanas',
                    'aromatizacao': 'Moderada',
                    'hepatotoxicidade': 'Baixa',
                    'efeitos_positivos': ['Ganho de massa magra', 'Vascularização', 'Apetite'],
                    'efeitos_colaterais': ['Ansiedade', 'Alterações hematológicas'],
                    'caracteristicas': 'Ganhos lentos mas duradouros'
                }
            },
            'peptideos': {
                'bpc_157': {
                    'classificacao': 'Peptídeo reparador',
                    'dosagem': '250-500mcg/dia',
                    'administracao': 'Subcutânea',
                    'frequencia': '1-2x dia',
                    'duracao': '4-8 semanas',
                    'beneficios': ['Cicatrização', 'Reparação tendões', 'Proteção gastrointestinal'],
                    'local_aplicacao': 'Próximo à lesão ou abdome',
                    'armazenamento': 'Refrigerado'
                },
                'tb_500': {
                    'classificacao': 'Fragmento de timosina beta-4',
                    'dosagem': '2-5mg/semana',
                    'administracao': 'Subcutânea ou intramuscular',
                    'frequencia': '2x por semana',
                    'duracao': '4-8 semanas',
                    'beneficios': ['Cicatrização', 'Mobilidade', 'Redução inflamação'],
                    'sinergismo': 'Potencializa com BPC-157'
                }
            },
            'sarms': {
                'ostarine': {
                    'nome_quimico': 'MK-2866',
                    'classificacao': 'SARM não-esteroidal',
                    'dosagem_masculino': '20-30mg/dia',
                    'dosagem_feminino': '10-15mg/dia',
                    'duracao': '6-8 semanas',
                    'meia_vida': '24 horas',
                    'supressao': 'Leve-moderada',
                    'beneficios': ['Preservação massa magra', 'Recuperação'],
                    'uso_tipico': 'Cutting ou bridge'
                },
                'rad_140': {
                    'nome_quimico': 'Testolone',
                    'classificacao': 'SARM potente',
                    'dosagem': '10-20mg/dia',
                    'duracao': '6-8 semanas',
                    'meia_vida': '20 horas',
                    'supressao': 'Moderada-alta',
                    'beneficios': ['Força', 'Massa muscular', 'Performance'],
                    'observacoes': 'Requer TPC'
                }
            }
        }
        
        self.protocolos_tpc = {
            'tpc_basica': {
                'indicacao': 'Ciclos leves (SARMS, testosterona baixa dose)',
                'duracao': '4 semanas',
                'protocolo': {
                    'tamoxifeno': '20mg/dia',
                    'clomid': '50mg/dia (primeira semana), 25mg/dia (3 semanas)'
                }
            },
            'tpc_moderada': {
                'indicacao': 'Ciclos moderados (testosterona média dose)',
                'duracao': '4-6 semanas',
                'protocolo': {
                    'tamoxifeno': '40mg/dia (1 semana), 20mg/dia (3-5 semanas)',
                    'clomid': '100mg/dia (1 semana), 50mg/dia (3-5 semanas)',
                    'hcg': '1000-1500 UI 2x/semana (2 semanas antes do SERM)'
                }
            },
            'tpc_avancada': {
                'indicacao': 'Ciclos longos/potentes, múltiplas substâncias',
                'duracao': '6-8 semanas',
                'protocolo': {
                    'hcg': '2000-3000 UI 2x/semana (2-3 semanas)',
                    'tamoxifeno': '40mg/dia (2 semanas), 20mg/dia (4-6 semanas)',
                    'clomid': '100mg/dia (2 semanas), 50mg/dia (4-6 semanas)',
                    'suporte_adicional': ['Vitamina D', 'Zinco', 'Magnésio', 'DAA']
                }
            }
        }
        
        self.protetores = {
            'hepaticos': {
                'tudca': {'dosagem': '250-500mg/dia', 'uso': 'Com esteroides 17-alpha-alkylados'},
                'milk_thistle': {'dosagem': '200-400mg/dia', 'uso': 'Proteção hepática geral'},
                'nac': {'dosagem': '600-1200mg/dia', 'uso': 'Antioxidante hepático'}
            },
            'cardiovasculares': {
                'cardarine': {'dosagem': '10-20mg/dia', 'uso': 'Melhora perfil lipídico'},
                'omega_3': {'dosagem': '2-4g/dia', 'uso': 'Anti-inflamatório cardiovascular'},
                'coq10': {'dosagem': '100-200mg/dia', 'uso': 'Função mitocondrial cardíaca'}
            },
            'renais': {
                'cranberry': {'dosagem': '500mg/dia', 'uso': 'Proteção urinária'},
                'astaxantina': {'dosagem': '4-8mg/dia', 'uso': 'Antioxidante renal'}
            }
        }
    
    def prescrever_suplementos(self, dados):
        """
        Prescreve suplementos e ergogênicos baseado no perfil e objetivos
        """
        try:
            # Validar dados obrigatórios
            campos_obrigatorios = ['objetivo', 'nivel_experiencia', 'peso', 'idade']
            for campo in campos_obrigatorios:
                if campo not in dados:
                    return jsonify({
                        'success': False,
                        'message': f'Campo obrigatório não preenchido: {campo}'
                    })
            
            # Classificar nível de intervenção
            nivel_intervencao = self._classificar_nivel_intervencao(dados)
            
            # Prescrição de suplementos naturais
            suplementos_naturais = self._prescrever_suplementos_naturais(dados)
            
            # Suplementação avançada
            suplementacao_avancada = self._prescrever_suplementacao_avancada(dados, nivel_intervencao)
            
            # Farmacologia esportiva (se aplicável)
            farmacologia = self._avaliar_farmacologia_esportiva(dados, nivel_intervencao)
            
            # Protocolos de proteção
            protocolos_protecao = self._definir_protocolos_protecao(dados, farmacologia)
            
            # Monitoramento e segurança
            monitoramento = self._definir_protocolo_monitoramento(dados, farmacologia)
            
            # Cronograma de implementação
            cronograma = self._gerar_cronograma_implementacao(dados, suplementos_naturais, farmacologia)
            
            resultado = {
                'success': True,
                'prescricao_completa': {
                    'nivel_intervencao': nivel_intervencao,
                    'suplementos_naturais': suplementos_naturais,
                    'suplementacao_avancada': suplementacao_avancada,
                    'farmacologia_esportiva': farmacologia,
                    'protocolos_protecao': protocolos_protecao,
                    'monitoramento_seguranca': monitoramento,
                    'cronograma_implementacao': cronograma,
                    'custo_estimado': self._calcular_custo_estimado(suplementos_naturais, farmacologia),
                    'alertas_seguranca': self._gerar_alertas_seguranca(dados, farmacologia)
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify(resultado)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erro na prescrição de suplementos: {str(e)}'
            })
    
    def _classificar_nivel_intervencao(self, dados):
        """Classifica o nível de intervenção baseado no perfil"""
        nivel_experiencia = dados.get('nivel_experiencia', 'iniciante').lower()
        objetivo = dados.get('objetivo', '').lower()
        historico_farmacos = dados.get('historico_farmacologico', {})
        idade = dados.get('idade', 25)
        
        score = 0
        
        # Experiência
        if 'iniciante' in nivel_experiencia:
            score += 1
        elif 'intermediario' in nivel_experiencia:
            score += 2
        elif 'avancado' in nivel_experiencia:
            score += 3
        elif 'atleta' in nivel_experiencia:
            score += 4
        
        # Objetivo
        if 'performance' in objetivo or 'competicao' in objetivo:
            score += 2
        elif 'hipertrofia' in objetivo:
            score += 1
        
        # Histórico farmacológico
        if historico_farmacos.get('uso_anterior_esteroides'):
            score += 2
        if historico_farmacos.get('uso_sarms'):
            score += 1
        
        # Idade
        if idade >= 30:
            score += 1
        
        if score <= 2:
            return 'CONSERVADOR'
        elif score <= 4:
            return 'MODERADO'
        elif score <= 6:
            return 'AGRESSIVO'
        else:
            return 'EXTREMO'
    
    def _prescrever_suplementos_naturais(self, dados):
        """Prescreve suplementos naturais baseados no perfil"""
        objetivo = dados.get('objetivo', '').lower()
        peso = dados.get('peso', 70)
        prescricao = {}
        
        # Suplementos base para todos
        prescricao['base'] = {
            'creatina': {
                **self.suplementos_naturais['creatina'],
                'dosagem_personalizada': f'{max(3, peso * 0.05):.1f}g/dia',
                'prioridade': 'ALTA'
            },
            'whey_protein': {
                'dosagem': f'{peso * 0.5:.0f}g/dia',
                'timing': 'Pós-treino e entre refeições',
                'justificativa': 'Suporte à síntese proteica',
                'prioridade': 'ALTA'
            }
        }
        
        # Suplementos para performance
        prescricao['performance'] = {
            'cafeina': {
                **self.suplementos_naturais['cafeina'],
                'dosagem_personalizada': f'{peso * 4:.0f}mg pré-treino',
                'prioridade': 'MÉDIA'
            },
            'beta_alanina': {
                **self.suplementos_naturais['beta_alanina'],
                'prioridade': 'MÉDIA' if 'forca' in objetivo or 'resistencia' in objetivo else 'BAIXA'
            }
        }
        
        # Suplementos específicos por objetivo
        if 'cutting' in objetivo or 'emagrecimento' in objetivo:
            prescricao['cutting'] = {
                'l_carnitina': {
                    'dosagem': '2-3g/dia',
                    'timing': 'Pré-treino',
                    'duracao': 'Durante o cutting',
                    'beneficio': 'Otimização da oxidação de gorduras',
                    'prioridade': 'MÉDIA'
                },
                'cla': {
                    'dosagem': '3-6g/dia',
                    'timing': 'Com refeições',
                    'duracao': '8-12 semanas',
                    'beneficio': 'Preservação massa magra',
                    'prioridade': 'BAIXA'
                }
            }
        
        elif 'bulking' in objetivo or 'hipertrofia' in objetivo:
            prescricao['bulking'] = {
                'citrulina': {
                    **self.suplementos_naturais['citrulina'],
                    'prioridade': 'MÉDIA'
                },
                'hmb': {
                    'dosagem': '3g/dia dividida em doses',
                    'timing': 'Com refeições',
                    'duracao': 'Fases de alto volume',
                    'beneficio': 'Anti-catabólico',
                    'prioridade': 'BAIXA'
                }
            }
        
        # Suporte geral
        prescricao['suporte'] = {
            'multivitaminico': {
                'dosagem': '1 dose/dia',
                'timing': 'Café da manhã',
                'justificativa': 'Cobertura micronutrientes',
                'prioridade': 'ALTA'
            },
            'omega_3': {
                'dosagem': '2-3g EPA+DHA/dia',
                'timing': 'Com refeições',
                'beneficio': 'Anti-inflamatório, saúde cardiovascular',
                'prioridade': 'ALTA'
            },
            'vitamina_d': {
                'dosagem': '2000-4000 UI/dia',
                'timing': 'Manhã',
                'justificativa': 'Otimização hormonal, função imune',
                'prioridade': 'ALTA'
            }
        }
        
        return prescricao
    
    def _prescrever_suplementacao_avancada(self, dados, nivel_intervencao):
        """Prescreve suplementação avançada baseada no nível"""
        if nivel_intervencao in ['CONSERVADOR']:
            return {
                'recomendacao': 'Focar em suplementos naturais básicos',
                'justificativa': 'Nível de experiência requer base sólida primeiro'
            }
        
        prescricao = {}
        objetivo = dados.get('objetivo', '').lower()
        
        # Nootrópicos para foco e performance mental
        if nivel_intervencao in ['MODERADO', 'AGRESSIVO', 'EXTREMO']:
            prescricao['nootropicos'] = {
                'alpha_gpc': {
                    **self.suplementacao_avancada['nootropicos']['alpha_gpc'],
                    'justificativa': 'Melhora conexão mente-músculo',
                    'prioridade': 'MÉDIA'
                }
            }
            
            if 'stress' in dados.get('fatores_limitantes', []):
                prescricao['adaptogenos'] = {
                    'ashwagandha': {
                        **self.suplementacao_avancada['adaptogenos']['ashwagandha'],
                        'justificativa': 'Redução cortisol, melhora recuperação',
                        'prioridade': 'ALTA'
                    }
                }
        
        return prescricao
    
    def _avaliar_farmacologia_esportiva(self, dados, nivel_intervencao):
        """Avalia necessidade e adequação de farmacologia esportiva"""
        if nivel_intervencao == 'CONSERVADOR':
            return {
                'recomendacao': 'Não recomendado',
                'justificativa': 'Nível de experiência insuficiente',
                'alternativas': 'Otimizar treinamento, nutrição e suplementação natural'
            }
        
        idade = dados.get('idade', 25)
        objetivo = dados.get('objetivo', '').lower()
        historico = dados.get('historico_farmacologico', {})
        exames = dados.get('exames_hormonais', {})
        
        avaliacao = {
            'elegibilidade': self._avaliar_elegibilidade_farmacologica(dados),
            'recomendacoes_por_nivel': {},
            'protocolos_sugeridos': {},
            'contraindicacoes': [],
            'pre_requisitos': []
        }
        
        if avaliacao['elegibilidade']['elegivel']:
            if nivel_intervencao == 'MODERADO':
                avaliacao['recomendacoes_por_nivel'] = self._protocolos_nivel_moderado(dados)
            elif nivel_intervencao == 'AGRESSIVO':
                avaliacao['recomendacoes_por_nivel'] = self._protocolos_nivel_agressivo(dados)
            elif nivel_intervencao == 'EXTREMO':
                avaliacao['recomendacoes_por_nivel'] = self._protocolos_nivel_extremo(dados)
        
        return avaliacao
    
    def _avaliar_elegibilidade_farmacologica(self, dados):
        """Avalia elegibilidade para uso de farmacologia esportiva"""
        idade = dados.get('idade', 25)
        exames = dados.get('exames_hormonais', {})
        historico_medico = dados.get('historico_medico', [])
        
        contraindicacoes_absolutas = [
            'doença cardíaca',
            'disfunção hepática severa',
            'câncer de próstata',
            'hiperplasia prostática severa'
        ]
        
        contraindicacoes_relativas = [
            'hipertensão não controlada',
            'dislipidemia severa',
            'apneia do sono não tratada'
        ]
        
        # Verificar contraindicações
        tem_contraindicacao_absoluta = any(
            contra.lower() in ' '.join(historico_medico).lower() 
            for contra in contraindicacoes_absolutas
        )
        
        if tem_contraindicacao_absoluta:
            return {
                'elegivel': False,
                'motivo': 'Contraindicação médica absoluta',
                'recomendacao': 'Consulta médica obrigatória'
            }
        
        # Verificar idade mínima
        if idade < 21:
            return {
                'elegivel': False,
                'motivo': 'Idade inferior a 21 anos',
                'recomendacao': 'Aguardar maturação do eixo hormonal'
            }
        
        # Verificar exames hormonais
        testosterona = exames.get('testosterona_total', 500)
        if testosterona < 300:
            return {
                'elegivel': True,
                'motivo': 'Hipogonadismo - indicação médica',
                'tipo_recomendado': 'TRT (Terapia de Reposição)'
            }
        
        return {
            'elegivel': True,
            'motivo': 'Perfil adequado para uso responsável',
            'observacoes': 'Necessário acompanhamento médico rigoroso'
        }
    
    def _protocolos_nivel_moderado(self, dados):
        """Protocolos para nível moderado"""
        return {
            'primeiro_ciclo': {
                'duracao': '12 semanas',
                'substancias': {
                    'testosterona_enantato': {
                        'dosagem': '300-400mg/semana',
                        'frequencia': '2x por semana',
                        'justificativa': 'Base segura para primeiro ciclo'
                    }
                },
                'suporte': {
                    'anastrozol': '0.5mg E3D (se necessário)',
                    'hcg': '250 UI 2x/semana (últimas 4 semanas)'
                },
                'tpc': self.protocolos_tpc['tpc_moderada']
            },
            'sarms_alternativo': {
                'duracao': '8 semanas',
                'substancia': 'Ostarine 20mg/dia',
                'justificativa': 'Alternativa mais conservadora',
                'tpc': self.protocolos_tpc['tpc_basica']
            }
        }
    
    def _protocolos_nivel_agressivo(self, dados):
        """Protocolos para nível agressivo"""
        objetivo = dados.get('objetivo', '').lower()
        
        protocolos = {
            'ciclo_bulking': {
                'duracao': '16 semanas',
                'substancias': {
                    'testosterona_enantato': '500mg/semana',
                    'boldenona': '400mg/semana',
                    'dbol_kickstart': '30mg/dia (4 primeiras semanas)'
                },
                'suporte': {
                    'anastrozol': '0.5mg EOD',
                    'tudca': '500mg/dia',
                    'hcg': '500 UI 2x/semana'
                },
                'tpc': self.protocolos_tpc['tpc_avancada']
            },
            'ciclo_cutting': {
                'duracao': '12 semanas',
                'substancias': {
                    'testosterona_propionato': '100mg EOD',
                    'masteron': '100mg EOD',
                    'anavar': '50mg/dia (últimas 6 semanas)'
                },
                'suporte': {
                    'cardarine': '20mg/dia',
                    'n2guard': '7 caps/dia'
                },
                'tpc': self.protocolos_tpc['tpc_moderada']
            }
        }
        
        return protocolos.get('ciclo_bulking' if 'bulking' in objetivo else 'ciclo_cutting')
    
    def _protocolos_nivel_extremo(self, dados):
        """Protocolos para nível extremo (atletas competitivos)"""
        return {
            'protocolo_competicao': {
                'observacao': 'Protocolos extremos requerem supervisão médica especializada',
                'pre_requisitos': [
                    'Acompanhamento médico especializado',
                    'Exames laboratoriais mensais',
                    'ECG e ecocardiograma',
                    'Monitoramento pressórico contínuo'
                ],
                'exemplo_off_season': {
                    'testosterona': '750-1000mg/semana',
                    'nandrolona': '400-600mg/semana',
                    'gh': '4-6 UI/dia',
                    'insulina': 'Protocolo específico pós-treino'
                },
                'pre_contest': {
                    'testosterona_propionato': '100mg EOD',
                    'masteron': '100mg EOD',
                    'trembolona_acetato': '75mg EOD',
                    'winstrol': '50mg/dia',
                    'clenbuterol': 'Protocolo piramidal'
                }
            }
        }
    
    def _definir_protocolos_protecao(self, dados, farmacologia):
        """Define protocolos de proteção baseados na farmacologia prescrita"""
        if not farmacologia.get('elegibilidade', {}).get('elegivel'):
            return {'observacao': 'Não aplicável - sem uso de farmacologia'}
        
        protocolos = {
            'hepaticos': [],
            'cardiovasculares': [],
            'renais': [],
            'hormonais': []
        }
        
        # Proteção hepática
        if any('17-alpha' in str(protocolo) for protocolo in farmacologia.get('protocolos_sugeridos', {}).values()):
            protocolos['hepaticos'] = [
                {
                    'substancia': 'TUDCA',
                    'dosagem': '500mg/dia',
                    'timing': 'Com esteroides orais',
                    'duracao': 'Durante todo o ciclo'
                },
                {
                    'substancia': 'NAC',
                    'dosagem': '1200mg/dia',
                    'timing': 'Contínuo',
                    'justificativa': 'Antioxidante hepático'
                }
            ]
        
        # Proteção cardiovascular
        protocolos['cardiovasculares'] = [
            {
                'substancia': 'Cardarine',
                'dosagem': '20mg/dia',
                'timing': 'Manhã',
                'beneficio': 'Melhora perfil lipídico'
            },
            {
                'substancia': 'Citrus Bergamot',
                'dosagem': '500mg/dia',
                'timing': 'Com refeições',
                'beneficio': 'Controle colesterol'
            }
        ]
        
        # Suporte hormonal
        protocolos['hormonais'] = [
            {
                'substancia': 'HCG',
                'dosagem': '250-500 UI 2x/semana',
                'timing': 'Durante todo o ciclo',
                'justificativa': 'Manutenção função testicular'
            }
        ]
        
        return protocolos
    
    def _definir_protocolo_monitoramento(self, dados, farmacologia):
        """Define protocolo de monitoramento e segurança"""
        if not farmacologia.get('elegibilidade', {}).get('elegivel'):
            return {
                'frequencia_exames': 'A cada 3-6 meses (protocolo padrão)',
                'parametros': ['Hemograma', 'Perfil lipídico', 'Função hepática', 'Hormônios']
            }
        
        return {
            'pre_ciclo': {
                'obrigatorios': [
                    'Hemograma completo',
                    'Perfil lipídico completo',
                    'Função hepática (AST, ALT, GGT, bilirrubinas)',
                    'Função renal (creatinina, ureia)',
                    'Painel hormonal completo',
                    'PSA (homens >35 anos)',
                    'ECG',
                    'Pressão arterial'
                ],
                'prazo': '2 semanas antes do início'
            },
            'durante_ciclo': {
                'frequencia': 'A cada 4-6 semanas',
                'parametros_prioritarios': [
                    'Hemograma',
                    'Função hepática',
                    'Perfil lipídico',
                    'Estradiol',
                    'Pressão arterial semanal'
                ],
                'sinais_alerta': [
                    'AST/ALT >3x valor normal',
                    'Hematócrito >50%',
                    'PA >140/90 mmHg persistente',
                    'Sintomas cardiovasculares'
                ]
            },
            'pos_ciclo': {
                'frequencia': '4, 8 e 12 semanas após TPC',
                'objetivo': 'Avaliar recuperação hormonal',
                'parametros': [
                    'Testosterona total e livre',
                    'LH e FSH',
                    'Função hepática',
                    'Perfil lipídico'
                ]
            },
            'biofeedback_diario': [
                'Pressão arterial',
                'Qualidade do sono',
                'Libido',
                'Disposição geral',
                'Sintomas adversos'
            ]
        }
    
    def _gerar_cronograma_implementacao(self, dados, suplementos, farmacologia):
        """Gera cronograma de implementação faseada"""
        cronograma = {
            'fase1_base': {
                'duracao': '4-6 semanas',
                'objetivo': 'Estabelecer base nutricional e suplementar',
                'implementar': [
                    'Multivitamínico',
                    'Ômega 3',
                    'Vitamina D',
                    'Whey protein',
                    'Creatina'
                ]
            },
            'fase2_performance': {
                'duracao': '2-4 semanas',
                'objetivo': 'Adicionar suplementos de performance',
                'implementar': [
                    'Cafeína pré-treino',
                    'Beta-alanina',
                    'Citrulina'
                ]
            }
        }
        
        if farmacologia.get('elegibilidade', {}).get('elegivel'):
            cronograma['fase3_farmacologia'] = {
                'duracao': 'Conforme protocolo específico',
                'pre_requisitos': [
                    'Exames pré-ciclo normais',
                    'Acompanhamento médico confirmado',
                    'Protocolo de proteção definido'
                ],
                'implementar': 'Conforme prescrição específica'
            }
        
        return cronograma
    
    def _calcular_custo_estimado(self, suplementos, farmacologia):
        """Calcula custo estimado mensal"""
        custos = {
            'suplementos_basicos': 'R$ 300-500/mês',
            'suplementos_performance': 'R$ 200-400/mês',
            'suplementacao_avancada': 'R$ 400-800/mês',
            'farmacologia_nivel_moderado': 'R$ 800-1500/mês',
            'farmacologia_nivel_agressivo': 'R$ 1500-3000/mês',
            'exames_monitoramento': 'R$ 500-1000/ciclo'
        }
        
        return custos
    
    def _gerar_alertas_seguranca(self, dados, farmacologia):
        """Gera alertas de segurança específicos"""
        alertas = [
            'Todos os suplementos devem ser de marcas confiáveis e testadas',
            'Dosagens devem ser respeitadas rigorosamente',
            'Monitoramento médico é obrigatório para farmacologia esportiva',
            'Interromper uso em caso de efeitos adversos significativos'
        ]
        
        if farmacologia.get('elegibilidade', {}).get('elegivel'):
            alertas.extend([
                'FARMACOLOGIA ESPORTIVA: Uso sob total responsabilidade do usuário',
                'Acompanhamento médico especializado é obrigatório',
                'Exames laboratoriais regulares são essenciais',
                'TPC adequada é fundamental para recuperação hormonal',
                'Uso recreativo ou sem supervisão pode causar danos permanentes'
            ])
        
        return alertas
