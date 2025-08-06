"""
MÓDULO 3: NUTRIÇÃO ESTRATÉGICA
Sistema de planejamento nutricional individualizado para alta performance
"""

from flask import jsonify
import json
from datetime import datetime
import math

class NutricaoEstrategicaModule:
    def __init__(self):
        self.equacoes_tmb = {
            'mifflin_st_jeor': {
                'masculino': lambda peso, altura, idade: (10 * peso) + (6.25 * altura) - (5 * idade) + 5,
                'feminino': lambda peso, altura, idade: (10 * peso) + (6.25 * altura) - (5 * idade) - 161
            },
            'katch_mcardle': lambda massa_magra: 370 + (21.6 * massa_magra),
            'cunningham': lambda massa_magra: 500 + (22 * massa_magra)
        }
        
        self.fatores_atividade = {
            'sedentario': 1.2,
            'levemente_ativo': 1.375,
            'moderadamente_ativo': 1.55,
            'muito_ativo': 1.725,
            'extremamente_ativo': 1.9,
            'atleta_profissional': 2.2
        }
        
        self.macros_por_objetivo = {
            'cutting': {
                'proteina': {'min': 2.2, 'max': 3.1},  # g/kg
                'gordura': {'min': 0.8, 'max': 1.2},   # g/kg
                'carboidrato_resto': True
            },
            'bulking': {
                'proteina': {'min': 1.8, 'max': 2.5},  # g/kg
                'gordura': {'min': 1.0, 'max': 1.5},   # g/kg
                'carboidrato_resto': True
            },
            'manutencao': {
                'proteina': {'min': 1.6, 'max': 2.2},  # g/kg
                'gordura': {'min': 1.0, 'max': 1.3},   # g/kg
                'carboidrato_resto': True
            },
            'performance': {
                'proteina': {'min': 1.8, 'max': 2.3},  # g/kg
                'gordura': {'min': 1.2, 'max': 1.8},   # g/kg
                'carboidrato': {'min': 5.0, 'max': 8.0}  # g/kg
            }
        }
        
        self.alimentos_database = {
            'proteinas_magras': {
                'frango_peito': {'proteina': 23, 'gordura': 1.2, 'carboidrato': 0, 'calorias': 100},
                'tilapia': {'proteina': 20, 'gordura': 1.7, 'carboidrato': 0, 'calorias': 96},
                'ovo_inteiro': {'proteina': 6, 'gordura': 5, 'carboidrato': 0.6, 'calorias': 70},
                'clara_ovo': {'proteina': 3.6, 'gordura': 0, 'carboidrato': 0.2, 'calorias': 17},
                'whey_protein': {'proteina': 24, 'gordura': 1, 'carboidrato': 3, 'calorias': 120}
            },
            'carboidratos_complexos': {
                'aveia': {'proteina': 13.2, 'gordura': 6.5, 'carboidrato': 67, 'calorias': 389},
                'batata_doce': {'proteina': 2, 'gordura': 0.1, 'carboidrato': 20, 'calorias': 86},
                'arroz_integral': {'proteina': 7.9, 'gordura': 2.9, 'carboidrato': 77.2, 'calorias': 370},
                'quinoa': {'proteina': 14.1, 'gordura': 6.1, 'carboidrato': 64.2, 'calorias': 368}
            },
            'gorduras_saudaveis': {
                'oleo_coco': {'proteina': 0, 'gordura': 100, 'carboidrato': 0, 'calorias': 862},
                'abacate': {'proteina': 2, 'gordura': 14.7, 'carboidrato': 8.5, 'calorias': 160},
                'amêndoas': {'proteina': 21.2, 'gordura': 49.9, 'carboidrato': 21.6, 'calorias': 579},
                'azeite_oliva': {'proteina': 0, 'gordura': 100, 'carboidrato': 0, 'calorias': 884}
            }
        }
    
    def gerar_plano_alimentar(self, dados):
        """
        Gera plano alimentar personalizado baseado no perfil e objetivos
        """
        try:
            # Validar dados obrigatórios
            campos_obrigatorios = ['peso', 'altura', 'idade', 'sexo', 'objetivo', 'nivel_atividade']
            for campo in campos_obrigatorios:
                if campo not in dados:
                    return jsonify({
                        'success': False,
                        'message': f'Campo obrigatório não preenchido: {campo}'
                    })
            
            # Calcular necessidades calóricas
            necessidades_caloricas = self._calcular_necessidades_caloricas(dados)
            
            # Calcular distribuição de macronutrientes
            distribuicao_macros = self._calcular_distribuicao_macros(dados, necessidades_caloricas)
            
            # Gerar estratégias nutricionais específicas
            estrategias = self._definir_estrategias_nutricionais(dados)
            
            # Gerar plano de refeições
            plano_refeicoes = self._gerar_plano_refeicoes(dados, distribuicao_macros)
            
            # Timing nutricional
            timing_nutricional = self._definir_timing_nutricional(dados)
            
            # Periodização nutricional
            periodizacao = self._gerar_periodizacao_nutricional(dados)
            
            # Suplementação nutricional básica
            suplementacao_nutricional = self._sugerir_suplementacao_nutricional(dados, distribuicao_macros)
            
            resultado = {
                'success': True,
                'plano_nutricional': {
                    'resumo_executivo': {
                        'calorias_totais': necessidades_caloricas['total'],
                        'deficit_superavit': necessidades_caloricas.get('deficit_superavit', 0),
                        'distribuicao_macros': distribuicao_macros,
                        'estrategia_principal': estrategias['estrategia_principal'],
                        'numero_refeicoes': dados.get('numero_refeicoes', 5)
                    },
                    'calculos_detalhados': necessidades_caloricas,
                    'macronutrientes': distribuicao_macros,
                    'estrategias_nutricionais': estrategias,
                    'plano_refeicoes': plano_refeicoes,
                    'timing_nutricional': timing_nutricional,
                    'periodizacao': periodizacao,
                    'suplementacao_nutricional': suplementacao_nutricional,
                    'monitoramento': self._definir_protocolo_monitoramento(dados)
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify(resultado)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erro ao gerar plano alimentar: {str(e)}'
            })
    
    def _calcular_necessidades_caloricas(self, dados):
        """Calcula necessidades calóricas usando múltiplas equações"""
        peso = dados['peso']
        altura = dados['altura'] * 100  # converter para cm
        idade = dados['idade']
        sexo = dados['sexo'].lower()
        nivel_atividade = dados['nivel_atividade']
        objetivo = dados['objetivo'].lower()
        percentual_gordura = dados.get('percentual_gordura')
        
        # TMB usando Mifflin-St Jeor (padrão)
        tmb_mifflin = self.equacoes_tmb['mifflin_st_jeor'][sexo](peso, altura, idade)
        
        # TMB usando Katch-McArdle se tiver % gordura
        tmb_katch = None
        if percentual_gordura:
            massa_magra = peso * (1 - percentual_gordura / 100)
            tmb_katch = self.equacoes_tmb['katch_mcardle'](massa_magra)
        
        # Escolher TMB mais apropriada
        tmb_final = tmb_katch if (tmb_katch and percentual_gordura < 15) else tmb_mifflin
        
        # GET (Gasto Energético Total)
        fator_atividade = self.fatores_atividade.get(nivel_atividade, 1.55)
        get = tmb_final * fator_atividade
        
        # Ajustar baseado no objetivo
        ajuste_calorico = self._calcular_ajuste_por_objetivo(objetivo, dados)
        calorias_alvo = get + ajuste_calorico
        
        return {
            'tmb_mifflin': round(tmb_mifflin),
            'tmb_katch': round(tmb_katch) if tmb_katch else None,
            'tmb_utilizada': round(tmb_final),
            'fator_atividade': fator_atividade,
            'get': round(get),
            'ajuste_objetivo': ajuste_calorico,
            'total': round(calorias_alvo),
            'deficit_superavit': ajuste_calorico
        }
    
    def _calcular_ajuste_por_objetivo(self, objetivo, dados):
        """Calcula ajuste calórico baseado no objetivo"""
        peso = dados['peso']
        
        if 'cutting' in objetivo or 'emagrecimento' in objetivo:
            # Déficit de 300-500 kcal ou 20-25% do GET
            return -min(500, peso * 7)  # ~7 kcal/kg para déficit moderado
        elif 'bulking' in objetivo or 'hipertrofia' in objetivo:
            # Superávit de 200-400 kcal
            return min(400, peso * 5)  # ~5 kcal/kg para superávit conservador
        elif 'recomposicao' in objetivo:
            # Manutenção ou déficit muito leve
            return -min(200, peso * 2)
        else:
            return 0  # manutenção
    
    def _calcular_distribuicao_macros(self, dados, necessidades_caloricas):
        """Calcula distribuição de macronutrientes"""
        peso = dados['peso']
        objetivo = dados['objetivo'].lower()
        calorias_totais = necessidades_caloricas['total']
        
        # Definir objetivo nutricional
        obj_key = 'cutting' if 'cutting' in objetivo or 'emagrecimento' in objetivo else \
                  'bulking' if 'bulking' in objetivo or 'hipertrofia' in objetivo else \
                  'performance' if 'performance' in objetivo else 'manutencao'
        
        macros_ref = self.macros_por_objetivo[obj_key]
        
        # Calcular proteína
        proteina_g = peso * macros_ref['proteina']['max']
        proteina_kcal = proteina_g * 4
        
        # Calcular gordura
        gordura_g = peso * macros_ref['gordura']['max']
        gordura_kcal = gordura_g * 9
        
        # Calcular carboidrato (resto das calorias)
        carboidrato_kcal = calorias_totais - proteina_kcal - gordura_kcal
        carboidrato_g = carboidrato_kcal / 4
        
        # Ajustar se carboidrato ficar muito baixo
        if carboidrato_g < peso * 2 and obj_key != 'cutting':
            carboidrato_g = peso * 3
            carboidrato_kcal = carboidrato_g * 4
            # Reajustar gordura
            gordura_kcal = calorias_totais - proteina_kcal - carboidrato_kcal
            gordura_g = gordura_kcal / 9
        
        return {
            'calorias_totais': round(calorias_totais),
            'proteina': {
                'gramas': round(proteina_g, 1),
                'calorias': round(proteina_kcal),
                'percentual': round((proteina_kcal / calorias_totais) * 100, 1),
                'g_por_kg': round(proteina_g / peso, 1)
            },
            'carboidrato': {
                'gramas': round(carboidrato_g, 1),
                'calorias': round(carboidrato_kcal),
                'percentual': round((carboidrato_kcal / calorias_totais) * 100, 1),
                'g_por_kg': round(carboidrato_g / peso, 1)
            },
            'gordura': {
                'gramas': round(gordura_g, 1),
                'calorias': round(gordura_kcal),
                'percentual': round((gordura_kcal / calorias_totais) * 100, 1),
                'g_por_kg': round(gordura_g / peso, 1)
            }
        }
    
    def _definir_estrategias_nutricionais(self, dados):
        """Define estratégias nutricionais específicas"""
        objetivo = dados['objetivo'].lower()
        nivel_atividade = dados['nivel_atividade']
        
        estrategias = {
            'estrategia_principal': '',
            'ciclagem_carboidratos': False,
            'jejum_intermitente': False,
            'cetogenica_ciclica': False,
            'refeeds': False,
            'detalhes': {}
        }
        
        if 'cutting' in objetivo or 'emagrecimento' in objetivo:
            estrategias['estrategia_principal'] = 'Déficit Calórico Sustentável'
            
            # Ciclagem de carboidratos para cutting
            if nivel_atividade in ['muito_ativo', 'extremamente_ativo', 'atleta_profissional']:
                estrategias['ciclagem_carboidratos'] = True
                estrategias['detalhes']['ciclagem'] = {
                    'dias_baixo_carbo': '4-5 dias (treino membros pequenos)',
                    'dias_medio_carbo': '1-2 dias (treino membros grandes)',
                    'dias_alto_carbo': '1 dia (refeed)',
                    'distribuicao_semanal': 'B-B-M-B-A-B-M'
                }
            
            # Jejum intermitente como ferramenta
            estrategias['jejum_intermitente'] = True
            estrategias['detalhes']['jejum'] = {
                'protocolo': '16:8 ou 18:6',
                'beneficios': 'Facilita aderência ao déficit calórico',
                'horario_alimentacao': '12h-20h (exemplo)'
            }
            
            # Refeeds periódicos
            estrategias['refeeds'] = True
            estrategias['detalhes']['refeeds'] = {
                'frequencia': 'A cada 7-14 dias',
                'duracao': '1-2 dias',
                'objetivo': 'Reset hormonal e psicológico'
            }
        
        elif 'bulking' in objetivo or 'hipertrofia' in objetivo:
            estrategias['estrategia_principal'] = 'Superávit Calórico Controlado'
            estrategias['detalhes']['bulking'] = {
                'tipo': 'Lean Bulk',
                'ganho_peso_semanal': '0.25-0.5kg',
                'monitoramento': 'Medidas corporais semanais'
            }
        
        elif 'performance' in objetivo:
            estrategias['estrategia_principal'] = 'Periodização Nutricional'
            estrategias['detalhes']['periodizacao'] = {
                'pre_treino': 'Alto carboidrato 2-3h antes',
                'pos_treino': 'Janela anabólica 30min',
                'dia_competicao': 'Carb loading específico'
            }
        
        return estrategias
    
    def _gerar_plano_refeicoes(self, dados, distribuicao_macros):
        """Gera plano de refeições detalhado"""
        numero_refeicoes = dados.get('numero_refeicoes', 5)
        objetivo = dados['objetivo'].lower()
        
        # Distribuição de macros por refeição
        distribuicao_refeicoes = self._calcular_distribuicao_por_refeicao(
            distribuicao_macros, numero_refeicoes, objetivo
        )
        
        # Sugestões de alimentos por refeição
        refeicoes = {}
        
        for refeicao, macros in distribuicao_refeicoes.items():
            refeicoes[refeicao] = {
                'macronutrientes': macros,
                'sugestoes_alimentos': self._sugerir_alimentos_refeicao(refeicao, macros, objetivo),
                'timing': self._definir_timing_refeicao(refeicao, numero_refeicoes),
                'observacoes': self._gerar_observacoes_refeicao(refeicao, objetivo)
            }
        
        return refeicoes
    
    def _calcular_distribuicao_por_refeicao(self, distribuicao_macros, numero_refeicoes, objetivo):
        """Calcula distribuição de macros por refeição"""
        distribuicao = {}
        
        if numero_refeicoes == 5:
            # Distribuição padrão para 5 refeições
            refeicoes_base = ['cafe_manha', 'lanche_manha', 'almoco', 'pre_treino', 'pos_treino', 'jantar', 'ceia']
            
            # Percentuais por refeição
            percentuais = {
                'cafe_manha': 0.20,
                'lanche_manha': 0.10,
                'almoco': 0.25,
                'pre_treino': 0.15,
                'pos_treino': 0.15,
                'jantar': 0.20,
                'ceia': 0.10
            }
            
            # Ajustar proteína para distribuição uniforme
            proteina_por_refeicao = distribuicao_macros['proteina']['gramas'] / numero_refeicoes
            
            for refeicao, percentual in list(percentuais.items())[:numero_refeicoes]:
                distribuicao[refeicao] = {
                    'calorias': round(distribuicao_macros['calorias_totais'] * percentual),
                    'proteina': round(proteina_por_refeicao, 1),
                    'carboidrato': round(distribuicao_macros['carboidrato']['gramas'] * percentual, 1),
                    'gordura': round(distribuicao_macros['gordura']['gramas'] * percentual, 1)
                }
        
        return distribuicao
    
    def _sugerir_alimentos_refeicao(self, refeicao, macros, objetivo):
        """Sugere alimentos específicos para cada refeição"""
        sugestoes = {
            'proteinas': [],
            'carboidratos': [],
            'gorduras': [],
            'exemplo_refeicao': ''
        }
        
        if refeicao == 'cafe_manha':
            sugestoes['proteinas'] = ['Ovos inteiros', 'Clara de ovos', 'Whey protein', 'Iogurte grego']
            sugestoes['carboidratos'] = ['Aveia', 'Frutas', 'Pão integral', 'Tapioca']
            sugestoes['gorduras'] = ['Abacate', 'Oleaginosas', 'Azeite', 'Pasta de amendoim']
            sugestoes['exemplo_refeicao'] = f'3 ovos inteiros + 50g aveia + 1/2 abacate'
        
        elif refeicao == 'pre_treino':
            sugestoes['proteinas'] = ['Whey protein', 'BCAA']
            sugestoes['carboidratos'] = ['Banana', 'Aveia', 'Dextrose', 'Batata doce']
            sugestoes['gorduras'] = ['MCT oil (mínimo)']
            sugestoes['exemplo_refeicao'] = f'1 banana + 30g whey protein + 30g aveia'
        
        elif refeicao == 'pos_treino':
            sugestoes['proteinas'] = ['Whey protein', 'Albumina']
            sugestoes['carboidratos'] = ['Dextrose', 'Maltodextrina', 'Banana', 'Arroz branco']
            sugestoes['gorduras'] = ['Evitar por 1-2h pós-treino']
            sugestoes['exemplo_refeicao'] = f'40g whey + 30g dextrose + 1 banana'
        
        elif refeicao in ['almoco', 'jantar']:
            sugestoes['proteinas'] = ['Frango', 'Peixe', 'Carne vermelha magra', 'Ovos']
            sugestoes['carboidratos'] = ['Arroz integral', 'Batata doce', 'Quinoa', 'Legumes']
            sugestoes['gorduras'] = ['Azeite', 'Abacate', 'Oleaginosas']
            sugestoes['exemplo_refeicao'] = f'150g frango + 100g batata doce + salada + azeite'
        
        elif refeicao == 'ceia':
            sugestoes['proteinas'] = ['Caseína', 'Iogurte grego', 'Cottage', 'Ovos']
            sugestoes['carboidratos'] = ['Aveia', 'Frutas vermelhas (mínimo se cutting)']
            sugestoes['gorduras'] = ['Oleaginosas', 'Pasta de amendoim']
            sugestoes['exemplo_refeicao'] = f'30g caseína + 10 amêndoas'
        
        return sugestoes
    
    def _definir_timing_nutricional(self, dados):
        """Define timing nutricional otimizado"""
        objetivo = dados['objetivo'].lower()
        horario_treino = dados.get('horario_treino', 'manha')
        
        timing = {
            'pre_treino': {},
            'pos_treino': {},
            'durante_treino': {},
            'observacoes_gerais': []
        }
        
        # Pre-treino (2-3h antes)
        timing['pre_treino'] = {
            'tempo_antes': '2-3 horas',
            'macros_foco': 'Carboidratos complexos + proteína',
            'evitar': 'Gorduras em excesso, fibras',
            'exemplo': 'Aveia + whey protein + banana',
            'hidratacao': '500-600ml água'
        }
        
        # Pre-treino imediato (30-60min antes)
        timing['pre_treino_imediato'] = {
            'tempo_antes': '30-60 minutos',
            'macros_foco': 'Carboidratos simples + aminoácidos',
            'exemplo': 'Banana + BCAA ou whey',
            'hidratacao': '200-300ml água'
        }
        
        # Durante o treino
        if dados.get('duracao_treino', 60) > 90:
            timing['durante_treino'] = {
                'necessario': True,
                'opcoes': 'BCAA + carboidratos simples',
                'quantidade': '15-30g carboidratos/hora',
                'hidratacao': '150-250ml a cada 15-20min'
            }
        else:
            timing['durante_treino'] = {
                'necessario': False,
                'hidratacao': 'Água suficiente'
            }
        
        # Pós-treino
        timing['pos_treino'] = {
            'janela_anabolica': '30-60 minutos',
            'proteina': '25-40g whey protein',
            'carboidratos': '0.5-1g/kg peso corporal',
            'ratio_carbo_proteina': '3:1 a 4:1',
            'exemplo': '40g whey + 30g dextrose + banana',
            'hidratacao': 'Repor 150% do perdido no suor'
        }
        
        return timing
    
    def _gerar_periodizacao_nutricional(self, dados):
        """Gera periodização nutricional por fases"""
        objetivo = dados['objetivo'].lower()
        
        periodizacao = {
            'tipo_periodizacao': '',
            'fases': {},
            'transicoes': {},
            'monitoramento': {}
        }
        
        if 'cutting' in objetivo:
            periodizacao['tipo_periodizacao'] = 'Cutting Periodizado'
            periodizacao['fases'] = {
                'fase1_adaptacao': {
                    'duracao': '2-3 semanas',
                    'deficit': '300-400 kcal',
                    'cardio': 'Moderado',
                    'objetivo': 'Adaptação metabólica'
                },
                'fase2_progressao': {
                    'duracao': '4-6 semanas',
                    'deficit': '400-500 kcal',
                    'cardio': 'Intensificado',
                    'objetivo': 'Perda de gordura acelerada'
                },
                'fase3_finalizacao': {
                    'duracao': '2-4 semanas',
                    'deficit': '500-600 kcal',
                    'cardio': 'Máximo tolerável',
                    'objetivo': 'Definição final'
                }
            }
        
        elif 'bulking' in objetivo:
            periodizacao['tipo_periodizacao'] = 'Bulking Controlado'
            periodizacao['fases'] = {
                'fase1_ganho': {
                    'duracao': '8-12 semanas',
                    'superavit': '300-400 kcal',
                    'objetivo': 'Ganho de massa magra'
                },
                'fase2_mini_cut': {
                    'duracao': '2-4 semanas',
                    'deficit': '300-400 kcal',
                    'objetivo': 'Controle da gordura corporal'
                }
            }
        
        return periodizacao
    
    def _sugerir_suplementacao_nutricional(self, dados, distribuicao_macros):
        """Sugere suplementação nutricional básica"""
        objetivo = dados['objetivo'].lower()
        
        suplementacao = {
            'essenciais': [],
            'performance': [],
            'objetivo_especifico': [],
            'timing': {}
        }
        
        # Suplementos essenciais
        if distribuicao_macros['proteina']['gramas'] > 150:
            suplementacao['essenciais'].append({
                'suplemento': 'Whey Protein',
                'dosagem': '25-40g',
                'timing': 'Pós-treino e entre refeições',
                'justificativa': 'Facilitar atingir meta proteica'
            })
        
        suplementacao['essenciais'].extend([
            {
                'suplemento': 'Multivitamínico',
                'dosagem': '1 dose/dia',
                'timing': 'Café da manhã',
                'justificativa': 'Cobertura de micronutrientes'
            },
            {
                'suplemento': 'Ômega 3',
                'dosagem': '2-3g EPA+DHA',
                'timing': 'Com refeições',
                'justificativa': 'Anti-inflamatório e saúde cardiovascular'
            }
        ])
        
        # Suplementos para performance
        suplementacao['performance'].extend([
            {
                'suplemento': 'Creatina',
                'dosagem': '3-5g/dia',
                'timing': 'Qualquer horário',
                'justificativa': 'Força e volume muscular'
            },
            {
                'suplemento': 'Cafeína',
                'dosagem': '200-400mg',
                'timing': '30-45min pré-treino',
                'justificativa': 'Energia e foco'
            }
        ])
        
        # Específico por objetivo
        if 'cutting' in objetivo:
            suplementacao['objetivo_especifico'].extend([
                {
                    'suplemento': 'L-Carnitina',
                    'dosagem': '2-3g/dia',
                    'timing': 'Pré-treino',
                    'justificativa': 'Otimização da oxidação de gorduras'
                },
                {
                    'suplemento': 'CLA',
                    'dosagem': '3-6g/dia',
                    'timing': 'Com refeições',
                    'justificativa': 'Preservação de massa magra'
                }
            ])
        
        return suplementacao
    
    def _definir_protocolo_monitoramento(self, dados):
        """Define protocolo de monitoramento nutricional"""
        return {
            'frequencia_pesagem': 'Diária (mesmo horário, jejum)',
            'medidas_corporais': 'Semanal',
            'fotos_progresso': 'Semanal (mesma iluminação/posição)',
            'bioimpedancia': 'Quinzenal',
            'ajustes_caloricos': {
                'frequencia': 'A cada 7-14 dias',
                'criterios': 'Baseado na média de peso semanal',
                'magnitude': '±10-15% das calorias atuais'
            },
            'sinais_alerta': [
                'Perda de peso >1kg/semana (cutting)',
                'Ganho de peso >0.5kg/semana (bulking)',
                'Fadiga excessiva',
                'Perda de força significativa',
                'Alterações de humor'
            ]
        }
    
    def _definir_timing_refeicao(self, refeicao, numero_refeicoes):
        """Define horários sugeridos para cada refeição"""
        horarios = {
            5: {
                'cafe_manha': '07:00',
                'lanche_manha': '10:00',
                'almoco': '13:00',
                'pre_treino': '16:00',
                'pos_treino': '18:00',
                'jantar': '20:00',
                'ceia': '22:00'
            }
        }
        
        return horarios.get(numero_refeicoes, {}).get(refeicao, 'A definir')
    
    def _gerar_observacoes_refeicao(self, refeicao, objetivo):
        """Gera observações específicas por refeição"""
        observacoes = []
        
        if refeicao == 'cafe_manha':
            observacoes.append('Primeira refeição quebra o jejum noturno')
            observacoes.append('Importante para estabelecer ritmo metabólico')
        
        elif refeicao == 'pre_treino':
            observacoes.append('Evitar gorduras em excesso')
            observacoes.append('Priorizar digestibilidade')
        
        elif refeicao == 'pos_treino':
            observacoes.append('Janela anabólica - prioridade máxima')
            observacoes.append('Carboidratos de alto índice glicêmico são bem-vindos')
        
        elif refeicao == 'ceia':
            if 'cutting' in objetivo:
                observacoes.append('Priorizar proteínas de lenta absorção')
                observacoes.append('Minimizar carboidratos')
            else:
                observacoes.append('Pode incluir carboidratos de baixo IG')
        
        return observacoes
