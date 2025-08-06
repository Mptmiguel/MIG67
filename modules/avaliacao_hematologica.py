"""
MÓDULO 2: AVALIAÇÃO HEMATOLÓGICA
Sistema de análise e interpretação de exames laboratoriais
"""

from flask import jsonify
import json
import re
from datetime import datetime
import pandas as pd

class AvaliacaoHematologicaModule:
    def __init__(self):
        self.valores_referencia = {
            'masculino': {
                'testosterona_total': {'min': 300, 'max': 1000, 'unidade': 'ng/dL', 'ideal_min': 500, 'ideal_max': 800},
                'testosterona_livre': {'min': 8.7, 'max': 25.1, 'unidade': 'pg/mL', 'ideal_min': 15, 'ideal_max': 22},
                'lh': {'min': 1.7, 'max': 8.6, 'unidade': 'mIU/mL', 'ideal_min': 3, 'ideal_max': 7},
                'fsh': {'min': 1.5, 'max': 12.4, 'unidade': 'mIU/mL', 'ideal_min': 2, 'ideal_max': 8},
                'estradiol': {'min': 7.6, 'max': 42.6, 'unidade': 'pg/mL', 'ideal_min': 15, 'ideal_max': 30},
                'prolactina': {'min': 4.0, 'max': 15.2, 'unidade': 'ng/mL', 'ideal_min': 5, 'ideal_max': 12},
                'shbg': {'min': 18, 'max': 54, 'unidade': 'nmol/L', 'ideal_min': 25, 'ideal_max': 45}
            },
            'feminino': {
                'testosterona_total': {'min': 15, 'max': 70, 'unidade': 'ng/dL', 'ideal_min': 25, 'ideal_max': 50},
                'testosterona_livre': {'min': 0.3, 'max': 3.2, 'unidade': 'pg/mL', 'ideal_min': 1, 'ideal_max': 2.5},
                'lh': {'min': 2.4, 'max': 12.6, 'unidade': 'mIU/mL', 'ideal_min': 4, 'ideal_max': 10},
                'fsh': {'min': 3.5, 'max': 12.5, 'unidade': 'mIU/mL', 'ideal_min': 4, 'ideal_max': 10},
                'estradiol': {'min': 12.5, 'max': 166, 'unidade': 'pg/mL', 'ideal_min': 50, 'ideal_max': 120},
                'prolactina': {'min': 4.8, 'max': 23.3, 'unidade': 'ng/mL', 'ideal_min': 6, 'ideal_max': 18},
                'shbg': {'min': 26, 'max': 110, 'unidade': 'nmol/L', 'ideal_min': 35, 'ideal_max': 85}
            },
            'geral': {
                'tsh': {'min': 0.27, 'max': 4.2, 'unidade': 'uUI/mL', 'ideal_min': 1, 'ideal_max': 2.5},
                't3_livre': {'min': 2.0, 'max': 4.4, 'unidade': 'pg/mL', 'ideal_min': 2.5, 'ideal_max': 4.0},
                't4_livre': {'min': 0.93, 'max': 1.7, 'unidade': 'ng/dL', 'ideal_min': 1.1, 'ideal_max': 1.5},
                't3_reverso': {'min': 10, 'max': 24, 'unidade': 'ng/dL', 'ideal_min': 12, 'ideal_max': 20},
                'ast': {'min': 0, 'max': 40, 'unidade': 'U/L', 'ideal_min': 15, 'ideal_max': 30},
                'alt': {'min': 0, 'max': 41, 'unidade': 'U/L', 'ideal_min': 15, 'ideal_max': 35},
                'ggt': {'min': 0, 'max': 60, 'unidade': 'U/L', 'ideal_min': 10, 'ideal_max': 40},
                'creatinina': {'min': 0.7, 'max': 1.3, 'unidade': 'mg/dL', 'ideal_min': 0.8, 'ideal_max': 1.1},
                'ureia': {'min': 10, 'max': 50, 'unidade': 'mg/dL', 'ideal_min': 15, 'ideal_max': 40},
                'tfg': {'min': 90, 'max': 120, 'unidade': 'mL/min/1.73m²', 'ideal_min': 100, 'ideal_max': 120},
                'pcr': {'min': 0, 'max': 3.0, 'unidade': 'mg/L', 'ideal_min': 0, 'ideal_max': 1.0},
                'ferritina_m': {'min': 30, 'max': 400, 'unidade': 'ng/mL', 'ideal_min': 50, 'ideal_max': 200},
                'ferritina_f': {'min': 15, 'max': 150, 'unidade': 'ng/mL', 'ideal_min': 25, 'ideal_max': 100},
                'glicemia': {'min': 70, 'max': 99, 'unidade': 'mg/dL', 'ideal_min': 80, 'ideal_max': 95},
                'insulina': {'min': 2.6, 'max': 24.9, 'unidade': 'uUI/mL', 'ideal_min': 4, 'ideal_max': 12},
                'homa_ir': {'min': 0, 'max': 2.5, 'unidade': '', 'ideal_min': 0.5, 'ideal_max': 1.5},
                'hb_glicada': {'min': 4.0, 'max': 5.6, 'unidade': '%', 'ideal_min': 4.5, 'ideal_max': 5.2},
                'hdl_m': {'min': 40, 'max': 60, 'unidade': 'mg/dL', 'ideal_min': 50, 'ideal_max': 70},
                'hdl_f': {'min': 50, 'max': 70, 'unidade': 'mg/dL', 'ideal_min': 60, 'ideal_max': 80},
                'ldl': {'min': 0, 'max': 100, 'unidade': 'mg/dL', 'ideal_min': 60, 'ideal_max': 90},
                'triglicerides': {'min': 0, 'max': 150, 'unidade': 'mg/dL', 'ideal_min': 50, 'ideal_max': 100},
                'colesterol_total': {'min': 0, 'max': 200, 'unidade': 'mg/dL', 'ideal_min': 160, 'ideal_max': 190},
                'vitamina_d': {'min': 30, 'max': 100, 'unidade': 'ng/mL', 'ideal_min': 40, 'ideal_max': 80},
                'zinco': {'min': 70, 'max': 120, 'unidade': 'ug/dL', 'ideal_min': 80, 'ideal_max': 110},
                'magnesio': {'min': 1.7, 'max': 2.2, 'unidade': 'mg/dL', 'ideal_min': 1.8, 'ideal_max': 2.1},
                'b12': {'min': 211, 'max': 946, 'unidade': 'pg/mL', 'ideal_min': 400, 'ideal_max': 700},
                'acido_folico': {'min': 2.7, 'max': 17.0, 'unidade': 'ng/mL', 'ideal_min': 5, 'ideal_max': 15}
            }
        }
        
        self.interpretacoes_clinicas = {
            'testosterona_baixa': {
                'sintomas': ['Fadiga', 'Diminuição da libido', 'Perda de massa muscular', 'Dificuldade de concentração'],
                'causas': ['Hipogonadismo', 'Stress crônico', 'Sobrepeso/obesidade', 'Idade avançada'],
                'recomendacoes': ['Avaliação endocrinológica', 'Otimização do sono', 'Redução do stress', 'Exercícios de força']
            },
            'tsh_elevado': {
                'sintomas': ['Fadiga', 'Ganho de peso', 'Intolerância ao frio', 'Constipação'],
                'causas': ['Hipotireoidismo subclínico/clínico', 'Tireoidite de Hashimoto', 'Deficiência de iodo'],
                'recomendacoes': ['Avaliação endocrinológica', 'Dosagem de anti-TPO', 'Suplementação de selênio']
            },
            'ferritina_baixa': {
                'sintomas': ['Fadiga', 'Diminuição da performance', 'Unhas quebradiças', 'Queda de cabelo'],
                'causas': ['Deficiência de ferro', 'Sangramento oculto', 'Dieta inadequada'],
                'recomendacoes': ['Suplementação de ferro', 'Investigação de sangramento', 'Otimização dietética']
            }
        }
    
    def analisar_exames(self, dados):
        """
        Analisa exames laboratoriais e gera relatório interpretativo
        """
        try:
            exames = dados.get('exames', {})
            sexo = dados.get('sexo', 'masculino').lower()
            idade = dados.get('idade', 30)
            
            if not exames:
                return jsonify({
                    'success': False,
                    'message': 'Nenhum exame fornecido para análise'
                })
            
            # Análise individual dos marcadores
            analise_marcadores = self._analisar_marcadores_individuais(exames, sexo)
            
            # Análise correlacional
            analise_correlacional = self._analisar_correlacoes(exames, sexo)
            
            # Identificação de padrões patológicos
            padroes_patologicos = self._identificar_padroes_patologicos(exames, sexo)
            
            # Recomendações específicas
            recomendacoes = self._gerar_recomendacoes_especificas(exames, sexo, analise_marcadores)
            
            # Protocolo de correção
            protocolo_correcao = self._gerar_protocolo_correcao(exames, sexo, analise_marcadores)
            
            # Encaminhamentos médicos
            encaminhamentos = self._avaliar_necessidade_encaminhamentos(analise_marcadores, padroes_patologicos)
            
            resultado = {
                'success': True,
                'analise_completa': {
                    'resumo_executivo': self._gerar_resumo_executivo(analise_marcadores, padroes_patologicos),
                    'marcadores_individuais': analise_marcadores,
                    'analise_correlacional': analise_correlacional,
                    'padroes_identificados': padroes_patologicos,
                    'nivel_risco': self._calcular_nivel_risco(analise_marcadores),
                    'recomendacoes_especificas': recomendacoes,
                    'protocolo_correcao': protocolo_correcao,
                    'encaminhamentos_medicos': encaminhamentos,
                    'proxima_reavaliacao': self._sugerir_reavaliacao(analise_marcadores)
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify(resultado)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erro na análise hematológica: {str(e)}'
            })
    
    def _analisar_marcadores_individuais(self, exames, sexo):
        """Analisa cada marcador individualmente"""
        analise = {}
        
        for marcador, valor in exames.items():
            if not isinstance(valor, (int, float)):
                continue
                
            marcador_lower = marcador.lower().replace(' ', '_').replace('-', '_')
            
            # Buscar referência específica por sexo ou geral
            referencia = None
            if sexo in self.valores_referencia and marcador_lower in self.valores_referencia[sexo]:
                referencia = self.valores_referencia[sexo][marcador_lower]
            elif marcador_lower in self.valores_referencia['geral']:
                referencia = self.valores_referencia['geral'][marcador_lower]
            elif sexo == 'feminino' and marcador_lower == 'ferritina':
                referencia = self.valores_referencia['geral']['ferritina_f']
            elif sexo == 'masculino' and marcador_lower == 'ferritina':
                referencia = self.valores_referencia['geral']['ferritina_m']
            elif sexo == 'feminino' and marcador_lower == 'hdl':
                referencia = self.valores_referencia['geral']['hdl_f']
            elif sexo == 'masculino' and marcador_lower == 'hdl':
                referencia = self.valores_referencia['geral']['hdl_m']
            
            if referencia:
                status = self._classificar_valor(valor, referencia)
                analise[marcador] = {
                    'valor': valor,
                    'unidade': referencia['unidade'],
                    'referencia_laboratorio': f"{referencia['min']}-{referencia['max']}",
                    'referencia_ideal': f"{referencia['ideal_min']}-{referencia['ideal_max']}",
                    'status': status,
                    'interpretacao': self._interpretar_valor(marcador_lower, valor, referencia, status),
                    'nivel_prioridade': self._definir_prioridade_correcao(status)
                }
        
        return analise
    
    def _classificar_valor(self, valor, referencia):
        """Classifica o valor do exame"""
        if valor < referencia['min']:
            return 'BAIXO'
        elif valor > referencia['max']:
            return 'ELEVADO'
        elif valor < referencia['ideal_min']:
            return 'SUBÓTIMO_BAIXO'
        elif valor > referencia['ideal_max']:
            return 'SUBÓTIMO_ALTO'
        else:
            return 'IDEAL'
    
    def _interpretar_valor(self, marcador, valor, referencia, status):
        """Gera interpretação clínica do valor"""
        interpretacoes = {
            'testosterona_total': {
                'BAIXO': 'Hipogonadismo - Necessária avaliação endocrinológica urgente',
                'SUBÓTIMO_BAIXO': 'Testosterona subótima - Pode impactar performance e composição corporal',
                'IDEAL': 'Níveis ideais para performance e bem-estar',
                'ELEVADO': 'Possível uso exógeno ou tumor produtor de andrógenos'
            },
            'tsh': {
                'BAIXO': 'Possível hipertireoidismo - Avaliação médica necessária',
                'SUBÓTIMO_BAIXO': 'TSH suprimido - Investigar causas',
                'IDEAL': 'Função tireoidiana ótima',
                'ELEVADO': 'Hipotireoidismo subclínico/clínico - Avaliação endocrinológica'
            },
            'creatinina': {
                'BAIXO': 'Possível baixa massa muscular',
                'IDEAL': 'Função renal normal',
                'ELEVADO': 'Possível comprometimento da função renal'
            }
        }
        
        if marcador in interpretacoes and status in interpretacoes[marcador]:
            return interpretacoes[marcador][status]
        
        # Interpretação genérica baseada no status
        if status == 'BAIXO':
            return f'{marcador.title()} abaixo do normal - Investigar causas'
        elif status == 'ELEVADO':
            return f'{marcador.title()} elevado - Monitorar e investigar'
        elif status in ['SUBÓTIMO_BAIXO', 'SUBÓTIMO_ALTO']:
            return f'{marcador.title()} fora da faixa ideal para performance'
        else:
            return f'{marcador.title()} dentro da faixa ideal'
    
    def _analisar_correlacoes(self, exames, sexo):
        """Analisa correlações entre marcadores"""
        correlacoes = []
        
        # Eixo hipofisário-gonadal
        if all(key in exames for key in ['testosterona_total', 'lh', 'fsh']):
            if exames['testosterona_total'] < 300 and exames['lh'] < 2:
                correlacoes.append({
                    'tipo': 'Hipogonadismo Hipogonadotrópico',
                    'marcadores': ['testosterona_total', 'lh', 'fsh'],
                    'interpretacao': 'Disfunção do eixo hipotálamo-hipófise-gonadal',
                    'severidade': 'ALTA'
                })
        
        # Resistência à insulina
        if all(key in exames for key in ['glicemia', 'insulina']):
            homa_ir = (exames['glicemia'] * exames['insulina']) / 405
            if homa_ir > 2.5:
                correlacoes.append({
                    'tipo': 'Resistência à Insulina',
                    'marcadores': ['glicemia', 'insulina', 'homa_ir'],
                    'interpretacao': 'Padrão compatível com resistência insulínica',
                    'severidade': 'MÉDIA'
                })
        
        # Função tireoidiana
        if all(key in exames for key in ['tsh', 't3_livre', 't4_livre']):
            if exames['tsh'] > 2.5 and exames['t4_livre'] < 1.1:
                correlacoes.append({
                    'tipo': 'Hipotireoidismo Subclínico',
                    'marcadores': ['tsh', 't3_livre', 't4_livre'],
                    'interpretacao': 'Função tireoidiana comprometida',
                    'severidade': 'MÉDIA'
                })
        
        # Perfil inflamatório
        if all(key in exames for key in ['pcr', 'ferritina']):
            if exames['pcr'] > 3.0 and exames['ferritina'] > 200:
                correlacoes.append({
                    'tipo': 'Processo Inflamatório',
                    'marcadores': ['pcr', 'ferritina'],
                    'interpretacao': 'Possível processo inflamatório sistêmico',
                    'severidade': 'MÉDIA'
                })
        
        return correlacoes
    
    def _identificar_padroes_patologicos(self, exames, sexo):
        """Identifica padrões patológicos específicos"""
        padroes = []
        
        # Síndrome metabólica
        criterios_sm = 0
        if 'triglicerides' in exames and exames['triglicerides'] >= 150:
            criterios_sm += 1
        if 'hdl' in exames:
            if (sexo == 'masculino' and exames['hdl'] < 40) or (sexo == 'feminino' and exames['hdl'] < 50):
                criterios_sm += 1
        if 'glicemia' in exames and exames['glicemia'] >= 100:
            criterios_sm += 1
        
        if criterios_sm >= 2:
            padroes.append({
                'padrao': 'Síndrome Metabólica',
                'criterios_presentes': criterios_sm,
                'risco': 'ALTO',
                'recomendacao': 'Intervenção imediata no estilo de vida'
            })
        
        # Overtraining syndrome
        if 'testosterona_total' in exames and 'cortisol' in exames:
            ratio_t_c = exames['testosterona_total'] / exames.get('cortisol', 1)
            if ratio_t_c < 0.35:
                padroes.append({
                    'padrao': 'Possível Overtraining',
                    'criterios_presentes': 'Ratio T:C baixo',
                    'risco': 'MÉDIO',
                    'recomendacao': 'Reduzir volume de treino e priorizar recuperação'
                })
        
        return padroes
    
    def _gerar_recomendacoes_especificas(self, exames, sexo, analise):
        """Gera recomendações específicas baseadas nos achados"""
        recomendacoes = {
            'nutricionais': [],
            'suplementacao': [],
            'estilo_vida': [],
            'farmacologicas': [],
            'treinamento': []
        }
        
        for marcador, dados in analise.items():
            if dados['status'] in ['BAIXO', 'SUBÓTIMO_BAIXO']:
                marcador_lower = marcador.lower().replace(' ', '_')
                
                if 'vitamina_d' in marcador_lower:
                    recomendacoes['suplementacao'].append('Vitamina D3: 2000-4000 UI/dia')
                    recomendacoes['estilo_vida'].append('Exposição solar diária 15-20 minutos')
                
                elif 'testosterona' in marcador_lower:
                    recomendacoes['estilo_vida'].extend([
                        'Sono 7-9h/noite',
                        'Redução do stress',
                        'Manutenção do peso corporal ideal'
                    ])
                    recomendacoes['suplementacao'].extend([
                        'Zinco: 15mg/dia',
                        'Magnésio: 400mg/dia',
                        'Vitamina D3: 3000-4000 UI/dia'
                    ])
                    recomendacoes['treinamento'].append('Exercícios de força com sobrecarga')
                
                elif 'ferritina' in marcador_lower:
                    recomendacoes['suplementacao'].append('Ferro quelato: 14-18mg/dia')
                    recomendacoes['nutricionais'].append('Aumentar consumo de carnes vermelhas')
                
                elif 'b12' in marcador_lower:
                    recomendacoes['suplementacao'].append('Vitamina B12: 1000mcg/dia')
        
        return recomendacoes
    
    def _gerar_protocolo_correcao(self, exames, sexo, analise):
        """Gera protocolo de correção estruturado"""
        protocolo = {
            'fase1_urgente': [],
            'fase2_otimizacao': [],
            'fase3_manutencao': [],
            'monitoramento': []
        }
        
        # Identificar prioridades urgentes
        for marcador, dados in analise.items():
            if dados['nivel_prioridade'] == 'URGENTE':
                protocolo['fase1_urgente'].append({
                    'marcador': marcador,
                    'acao': 'Avaliação médica imediata',
                    'prazo': '7 dias'
                })
        
        # Otimizações de médio prazo
        for marcador, dados in analise.items():
            if dados['status'] in ['SUBÓTIMO_BAIXO', 'SUBÓTIMO_ALTO']:
                protocolo['fase2_otimizacao'].append({
                    'marcador': marcador,
                    'acao': self._definir_acao_otimizacao(marcador, dados),
                    'prazo': '4-8 semanas'
                })
        
        # Protocolos de manutenção
        protocolo['fase3_manutencao'] = [
            'Reavaliação laboratorial a cada 3-6 meses',
            'Monitoramento de biofeedback semanal',
            'Ajustes finos baseados na resposta individual'
        ]
        
        return protocolo
    
    def _definir_acao_otimizacao(self, marcador, dados):
        """Define ação específica para otimização do marcador"""
        acoes = {
            'testosterona_total': 'Protocolo de otimização natural + avaliação para TRT se necessário',
            'vitamina_d': 'Suplementação com D3 + exposição solar',
            'ferritina': 'Suplementação com ferro + investigação de perdas',
            'tsh': 'Avaliação tireoidiana completa + possível suplementação'
        }
        
        return acoes.get(marcador.lower(), 'Protocolo individualizado baseado no marcador')
    
    def _avaliar_necessidade_encaminhamentos(self, analise, padroes):
        """Avalia necessidade de encaminhamentos médicos"""
        encaminhamentos = []
        
        # Endocrinologista
        indicacoes_endo = ['testosterona', 'tsh', 't3', 't4', 'insulina', 'cortisol']
        for marcador, dados in analise.items():
            if any(ind in marcador.lower() for ind in indicacoes_endo) and dados['status'] in ['BAIXO', 'ELEVADO']:
                encaminhamentos.append({
                    'especialidade': 'Endocrinologia',
                    'urgencia': 'ALTA' if dados['nivel_prioridade'] == 'URGENTE' else 'MÉDIA',
                    'motivo': f'Alteração em {marcador}',
                    'prazo': '15 dias' if dados['nivel_prioridade'] == 'URGENTE' else '30 dias'
                })
                break
        
        # Cardiologista
        if any('Síndrome Metabólica' in p['padrao'] for p in padroes):
            encaminhamentos.append({
                'especialidade': 'Cardiologia',
                'urgencia': 'MÉDIA',
                'motivo': 'Avaliação cardiovascular - síndrome metabólica',
                'prazo': '30 dias'
            })
        
        # Hepatologista
        hepaticos = ['ast', 'alt', 'ggt']
        for marcador, dados in analise.items():
            if any(hep in marcador.lower() for hep in hepaticos) and dados['status'] == 'ELEVADO':
                encaminhamentos.append({
                    'especialidade': 'Hepatologia',
                    'urgencia': 'MÉDIA',
                    'motivo': 'Elevação de enzimas hepáticas',
                    'prazo': '30 dias'
                })
                break
        
        return list({enc['especialidade']: enc for enc in encaminhamentos}.values())
    
    def _definir_prioridade_correcao(self, status):
        """Define prioridade de correção baseada no status"""
        prioridades = {
            'BAIXO': 'URGENTE',
            'ELEVADO': 'ALTA',
            'SUBÓTIMO_BAIXO': 'MÉDIA',
            'SUBÓTIMO_ALTO': 'MÉDIA',
            'IDEAL': 'BAIXA'
        }
        return prioridades.get(status, 'MÉDIA')
    
    def _calcular_nivel_risco(self, analise):
        """Calcula nível de risco geral baseado nos achados"""
        pontuacao_risco = 0
        
        for dados in analise.values():
            if dados['nivel_prioridade'] == 'URGENTE':
                pontuacao_risco += 3
            elif dados['nivel_prioridade'] == 'ALTA':
                pontuacao_risco += 2
            elif dados['nivel_prioridade'] == 'MÉDIA':
                pontuacao_risco += 1
        
        if pontuacao_risco >= 6:
            return 'ALTO'
        elif pontuacao_risco >= 3:
            return 'MODERADO'
        else:
            return 'BAIXO'
    
    def _gerar_resumo_executivo(self, analise, padroes):
        """Gera resumo executivo da análise"""
        alteracoes_significativas = [
            marcador for marcador, dados in analise.items()
            if dados['status'] in ['BAIXO', 'ELEVADO']
        ]
        
        alteracoes_subotimas = [
            marcador for marcador, dados in analise.items()
            if dados['status'] in ['SUBÓTIMO_BAIXO', 'SUBÓTIMO_ALTO']
        ]
        
        return {
            'total_marcadores_analisados': len(analise),
            'alteracoes_significativas': len(alteracoes_significativas),
            'alteracoes_subotimas': len(alteracoes_subotimas),
            'padroes_patologicos': len(padroes),
            'marcadores_criticos': alteracoes_significativas[:3],
            'principais_achados': [p['padrao'] for p in padroes],
            'necessita_intervencao_imediata': any(
                dados['nivel_prioridade'] == 'URGENTE' for dados in analise.values()
            )
        }
    
    def _sugerir_reavaliacao(self, analise):
        """Sugere cronograma de reavaliação"""
        tem_alteracao_severa = any(
            dados['nivel_prioridade'] == 'URGENTE' for dados in analise.values()
        )
        
        if tem_alteracao_severa:
            return {
                'prazo_recomendado': '4-6 semanas',
                'marcadores_prioritarios': [
                    marcador for marcador, dados in analise.items()
                    if dados['nivel_prioridade'] in ['URGENTE', 'ALTA']
                ],
                'exames_adicionais': [
                    'Painel hormonal completo se alterações endócrinas',
                    'Ecocardiograma se síndrome metabólica',
                    'USG abdome se alterações hepáticas'
                ]
            }
        else:
            return {
                'prazo_recomendado': '12-16 semanas',
                'marcadores_prioritarios': list(analise.keys()),
                'exames_adicionais': ['Manter protocolo padrão']
            }
