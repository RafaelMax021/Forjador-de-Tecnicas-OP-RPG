import streamlit as st
import math

st.set_page_config(page_title="Forja de Técnicas OP RPG 2.0", layout="wide")

st.title("⚔️ Forja de Técnicas - Edição Mestre (OP RPG 2.0)")
st.markdown("Motor feito de fã para fã, criado por um mestre que quer facilitar a vida dos seus amados players mesmo que eles sejam safados, abraço para o bando do Cuzão. Criado por Eru")
st.markdown("---")

# ==========================================
# 0. BASE DE DADOS DO SISTEMA
# ==========================================
DICIONARIO_CONDICOES = {
    "Abalado": 1, "Agarrado": 1, "Caído": 1, "Sangramento": 1, "Surdo": 1, "Vulnerável": 1,
    "Cego": 2, "Assustado": 2, "Enfeitiçado": 2, "Envenenado": 2, "Fadigado": 2, "Impedido": 2, "Provocado": 2,
    "Atordoado": 3, "Confuso": 3, "Petrificado": 3,
    "Exausto": 4, "Paralisado": 4,
    "Inconsciente": 5
}

# ==========================================
# 1. PARÂMETROS GERAIS
# ==========================================
col1, col2, col3 = st.columns(3)
with col1:
    nome = st.text_input("Nome da Técnica", "Nova Técnica")
    tipo = st.selectbox("Tipo de Técnica", ["Combate", "Auxiliar"])
    grau = st.number_input("Grau da Técnica", min_value=1, max_value=7, value=3)
    
with col2:
    acao_base = st.selectbox("Ação Base Exigida", ["Ação Poderosa", "Ação Bonus","Reação"])
    duracao_base = st.selectbox("Duração", ["Instantâneo", "1 Turno", "1 Minuto", "10 Minutos", "1 Hora", "Concentração", "Especial"])
    if duracao_base == "Especial":
        duracao_base = st.text_input("Especifique a Duração", "Até o alvo passar no teste")
    requisitos_extras = st.text_input("Requisitos (Opcional)", "Ex: Arma Cortante, Ope-Ope no Mi...")
    
with col3:
    alvo = st.selectbox("Tipo de Alvo", ["Único", "Área (Múltiplos)", "Aliados/Próprio Usuário"])
    forma_area = st.selectbox("Forma da Área", ["Esfera", "Cone", "Linha", "Cilindro", "Cubo"]) if alvo == "Área (Múltiplos)" else "Nenhuma"
    alcance_base_tipo = st.selectbox("Alcance Base", ["Toque", "Pessoal", "Distância (Metros)", "Arma Corpo-a-Corpo"])
    alcance_base_metros = st.number_input("Metros do Alcance", min_value=0, value=9) if alcance_base_tipo == "Distância (Metros)" else 0

st.markdown("---")

# ==========================================
# 2. SISTEMA DE ABAS
# ==========================================
tab_ofensivo, tab_controle, tab_suporte, tab_reducoes = st.tabs([
    "⚔️ OFENSIVO", "⚙️ CONTROLE", "🛡️ SUPORTE", "📉 REDUÇÕES"
])

with tab_ofensivo:
    st.subheader("Dano e Ataque")
    limite_dano = grau * 2 if tipo == "Combate" else 0
    pp_dano = st.number_input(f"PP Investido em Dano Base (Máx {limite_dano})", min_value=0, max_value=limite_dano, value=limite_dano if tipo == "Combate" else 0)
    
    col_dmg1, col_dmg2 = st.columns(2)
    categoria_dano = col_dmg1.selectbox("Categoria de Dano", ["Físico [0 PP]", "Básico [+1 PP]", "Avançado [+2 PP]", "Supremo [+3 PP]"])
    
    if "Físico" in categoria_dano:
        elemento_dano = col_dmg2.selectbox("Elemento Específico", ["Cortante", "Perfurante", "Contundente"])
        custo_tipo_dano = 0
    elif "Básico" in categoria_dano:
        elemento_dano = col_dmg2.selectbox("Elemento Específico", ["Ácido", "Elétrico", "Fogo", "Frio", "Veneno"])
        custo_tipo_dano = 1
    elif "Avançado" in categoria_dano:
        elemento_dano = col_dmg2.selectbox("Elemento Específico", ["Energia", "Psíquico", "Trovejante"])
        custo_tipo_dano = max(1, min(2, math.ceil(grau/2)))
    else:
        elemento_dano = col_dmg2.selectbox("Elemento Específico", ["Verdadeiro"])
        custo_tipo_dano = max(1, min(3, math.ceil(grau/2)))
    
    col_of1, col_of2 = st.columns(2)
    acerto_automatico = col_of1.checkbox("Acerto Automático (+ Grau PP)")
    ataque_cerco = col_of1.checkbox("Ataque de Cerco (+2 PP) - Dobra dano em estruturas")
    add_critico = col_of2.selectbox("Adicionar Crítico", ["Nenhum", "19-20 (+1 PP)", "18-20 (+2 PP)"])
    ataques_multiplos = col_of2.checkbox("Ataques Múltiplos (+6 PP) - +2 ataques")

with tab_controle:
    st.subheader("Manipulação do Campo e Ação")
    col_ct1, col_ct2 = st.columns(2)
    
    condicoes_selecionadas = col_ct1.multiselect(
        "Impor Condições ao Alvo",
        options=list(DICIONARIO_CONDICOES.keys()),
        format_func=lambda x: f"{x} (+{DICIONARIO_CONDICOES[x]} PP)"
    )
    custo_condicao = sum([DICIONARIO_CONDICOES[c] for c in condicoes_selecionadas])
    
    # REGRA OFICIAL DA TÉCNICA RÁPIDA (Limitada ao Grau 4)
    tecnica_rapida = col_ct1.checkbox(f"Técnica Rápida: Muda a ação para Bônus ou Reação (+{grau} PP)") if grau <= 4 else False
    if grau > 4 and tipo == "Combate":
        col_ct1.warning("Técnica Rápida só é permitida em técnicas de até 4º Grau.")
    
    add_empurrao = col_ct2.number_input("Adicionar Empurrão (Metros)", min_value=0, step=3, help="+1 PP a cada 3m")
    add_vantagem = st.checkbox("Adicionar Vantagem/Desvantagem (+4 PP ou Metade do Grau)")
    aumentar_area = st.number_input("Aumentar Área do Golpe (Metros)", min_value=0, step=3, help="+1 PP a cada 3m")

with tab_suporte:
    st.subheader("Buffs, Curas e Utilidade")
    col_sp1, col_sp2 = st.columns(2)
    pp_cura = col_sp1.number_input("Adicionar Cura (PP Investido)", min_value=0, value=0)
    pp_pv_temp = col_sp1.number_input("Adicionar PV Temporários (PP Investido)", min_value=0, value=0)
    add_voo = col_sp2.number_input("Adicionar Voo (Metros extras)", min_value=0, step=3, help="+1 PP a cada 3m")
    add_cr = col_sp2.number_input("Aumentar CR (Classe de Resistência)", min_value=0, value=0, help="+1 PP por cada +1 na CR")

with tab_reducoes:
    st.subheader("Reduções Oficiais de Custo (- PP)")
    conc_crucial = st.checkbox("Concentração Crucial (-2 PP) - Exige concentração total")
    col_red1, col_red2 = st.columns(2)
    colateral_dano = col_red1.number_input("Efeito Colateral: Dano ao Usuário (- PP)", min_value=0, max_value=4, value=0, help="Limita a redução em até 4 PP")
    
    colateral_condicao_sel = col_red2.selectbox(
        "Efeito Colateral: Condição Sofrida pelo Usuário",
        options=["Nenhuma"] + list(DICIONARIO_CONDICOES.keys()),
        format_func=lambda x: f"{x} (-{DICIONARIO_CONDICOES[x]} PP)" if x != "Nenhuma" else "Nenhuma (0 PP)"
    )
    colateral_condicao = min(4, DICIONARIO_CONDICOES[colateral_condicao_sel]) if colateral_condicao_sel != "Nenhuma" else 0
    
    desconto_natural = st.checkbox("Aplicar Desconto Natural da Criação de Técnica", value=True)
    desc_narrativa = st.text_area("Narrativa Base da Técnica", "O usuário usa seus poderes para...")

# ==========================================
# 3. MOTOR DE CÁLCULO
# ==========================================
custo_total = pp_dano + pp_cura + pp_pv_temp + custo_tipo_dano

if acerto_automatico: custo_total += grau
if ataque_cerco: custo_total += 2
if add_critico == "19-20 (+1 PP)": custo_total += 1
elif add_critico == "18-20 (+2 PP)": custo_total += 2
if ataques_multiplos: custo_total += 6

custo_total += custo_condicao
custo_total += (add_empurrao // 3)
custo_total += (aumentar_area // 3)
if add_vantagem: custo_total += 4 if tipo == "Auxiliar" else math.ceil(grau/2)
if tecnica_rapida: custo_total += grau

custo_total += (add_voo // 3)
custo_total += add_cr

desconto = 0
if conc_crucial: desconto += 2
# A regra oficial limita Efeito Colateral a 4 PP totais
desconto += min(8, colateral_dano + colateral_condicao) 

if desconto_natural:
    desconto += math.floor(grau / 2) if tipo == "Combate" else 1

pp_final = max(1, custo_total - desconto)

# ==========================================
# 4. CONSTRUTOR DE TEXTO
# ==========================================
alcance_str = f"{alcance_base_metros} metros" if alcance_base_tipo == "Distância (Metros)" else alcance_base_tipo
if alvo == "Área (Múltiplos)":
    area_tam = f" (+{aumentar_area}m extra)" if aumentar_area > 0 else ""
    alcance_str += f" | Área: {forma_area}{area_tam}"

dados_acoes = []
if pp_dano > 0:
    dado = "d10" if alvo == "Único" else "d6"
    dados_acoes.append(f"{pp_dano}{dado} de dano {elemento_dano}")
if pp_cura > 0: dados_acoes.append(f"Cura {pp_cura}d10 PV")
if pp_pv_temp > 0: dados_acoes.append(f"Concede {pp_pv_temp}d10 PV Temporário")
impacto_str = " | ".join(dados_acoes) if dados_acoes else "Nenhum"

efeitos_auto = []
if acerto_automatico: efeitos_auto.append("Acerto Automático: Dispensa jogada de ataque.")
if ataque_cerco: efeitos_auto.append("Ataque de Cerco: Dobra dano contra estruturas.")
if add_critico != "Nenhum": efeitos_auto.append(f"Margem de Crítico aumentada para {add_critico[:5]}.")
if condicoes_selecionadas: efeitos_auto.append(f"Condição: O alvo sofre [{', '.join(condicoes_selecionadas)}] se falhar em Salvaguarda.")
if add_empurrao > 0: efeitos_auto.append(f"Empurrão: Arremessa o alvo em {add_empurrao} metros.")
if add_vantagem: efeitos_auto.append("Vantagem/Desvantagem concedida.")
if add_cr > 0: efeitos_auto.append(f"Aumento de +{add_cr} na CR.")

if conc_crucial: efeitos_auto.append("[REDUÇÃO] Concentração Crucial ativada.")
if colateral_dano > 0: efeitos_auto.append(f"[REDUÇÃO] O usuário sofre {colateral_dano * 5} pontos de dano pelo uso.")
if colateral_condicao_sel != "Nenhuma": efeitos_auto.append(f"[REDUÇÃO] O usuário sofre [{colateral_condicao_sel}].")

texto_efeitos = desc_narrativa + "\n\nEfeitos Mecânicos:\n"
if efeitos_auto:
    for ef in efeitos_auto: texto_efeitos += f"- {ef}\n"
else: texto_efeitos += "- Sem efeitos adicionais mecânicos."

# Tratando o requisito de Ação de acordo com o livro
req_final = "Ação Bônus ou Reação" if tecnica_rapida else acao_base
if requisitos_extras and "Ex:" not in requisitos_extras:
    req_final += f", {requisitos_extras}"

st.markdown("---")
st.header("📋 Ficha Final Gerada")
st.success(f"Custo de PP Calculado: {pp_final} PP")

ficha_final = f"""{nome}
(Técnica de {tipo} - {grau}º Grau)

Pontos de Poder: {pp_final}
Alcance: {alcance_str}
Duração: {duracao_base}
Requisito: {req_final}
Impacto: {impacto_str}

Efeito:
{texto_efeitos}"""
st.text_area("Cópia Exata para o VTT ou Ficha:", value=ficha_final, height=400)
