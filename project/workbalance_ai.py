"""
WorkBalance AI - Sistema de Análise de Bem-Estar no Trabalho

CLI em Python que analisa rotinas de trabalho, sugere melhorias e ajuda a
identificar sinais de sobrecarga cognitiva com automação de dados e relatórios.

Funcionalidades:
- Coleta e validação de dados de colaboradores
- Análise estatística com NumPy (média, desvio padrão, correlações)
- Classificação de riscos e geração de feedback personalizado
- Análise departamental e previsão de estresse por regressão linear
- Geração de relatórios detalhados em texto e JSON
- Exportação de dados para auditoria e análise posterior
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, Iterable, List, Tuple

try:
    import numpy as np
except ImportError as exc:
    raise ImportError(
        "NumPy é obrigatório. Instale com: pip install numpy"
    ) from exc


# ===========================================================================
# Estruturas de dados e utilitários
# ===========================================================================
# Define as estruturas básicas para representar colaboradores e funções
# auxiliares para normalização de dados
# ===========================================================================

@dataclass
class Colaborador:
    nome: str
    departamento: str
    horas: float  # Armazenado em minutos para cálculos internos
    pausas: int
    estresse: int
    tarefas: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


ColaboradorRegistro = Dict[str, Any]


# ===========================================================================
# Funções de conversão de horas (formato HH:MM)
# ===========================================================================

def horas_para_minutos(horas_str: str) -> int:
    """
    Converte string no formato HH:MM para minutos totais.
    Aceita formatos: "8:30", "08:30", "8:00", "08:00"
    """
    try:
        partes = horas_str.strip().split(":")
        if len(partes) != 2:
            raise ValueError("Formato inválido. Use HH:MM (ex: 8:30)")
        
        horas = int(partes[0])
        minutos = int(partes[1])
        
        if horas < 0 or horas > 23:
            raise ValueError("Horas devem estar entre 00 e 23")
        if minutos < 0 or minutos > 59:
            raise ValueError("Minutos devem estar entre 00 e 59")
        
        return horas * 60 + minutos
    except ValueError as e:
        raise ValueError(f"Formato de hora inválido: {e}") from e


def minutos_para_horas_str(minutos: int) -> str:
    """
    Converte minutos totais para string no formato HH:MM.
    """
    horas = minutos // 60
    mins = minutos % 60
    return f"{horas:02d}:{mins:02d}"


def minutos_para_horas_decimal(minutos: int) -> float:
    """
    Converte minutos totais para horas decimais (para cálculos).
    """
    return minutos / 60.0


def horas_decimal_para_minutos(horas_decimal: float) -> int:
    """
    Converte horas decimais para minutos totais.
    """
    return int(round(horas_decimal * 60))


def _normalizar_registro(colaborador: Colaborador | ColaboradorRegistro) -> ColaboradorRegistro:
    """
    Aceita instâncias ou dicts e devolve um dicionário padronizado.
    As horas são sempre armazenadas em minutos internamente.
    """
    if isinstance(colaborador, Colaborador):
        return colaborador.to_dict()
    
    horas = colaborador.get("horas", 0)
    # Se horas for string (HH:MM), converter para minutos
    if isinstance(horas, str):
        horas = horas_para_minutos(horas)
    # Se horas for float (horas decimais), converter para minutos
    elif isinstance(horas, float):
        horas = horas_decimal_para_minutos(horas)
    # Se já for int (minutos), usar diretamente
    elif not isinstance(horas, int):
        horas = 0
    
    return {
        "nome": colaborador.get("nome", "").strip(),
        "departamento": colaborador.get("departamento", "").strip(),
        "horas": int(horas),  # Sempre em minutos
        "pausas": int(colaborador.get("pausas", 0)),
        "estresse": int(colaborador.get("estresse", 0)),
        "tarefas": int(colaborador.get("tarefas", 0)),
    }


def _normalizar_lista(colaboradores: Iterable[Colaborador | ColaboradorRegistro]) -> List[ColaboradorRegistro]:
    return [_normalizar_registro(c) for c in colaboradores]


# ===========================================================================
# Funções de análise básicas (superfície pública do módulo)
# - Média de horas trabalhadas
# - Colaborador(es) com maior estresse
# - Colaboradores produtivos (5+ tarefas)
# - Alerta de equilíbrio (estresse alto e poucas pausas)
# ===========================================================================

def calcular_media_horas(lista_colaboradores: Iterable[Colaborador | ColaboradorRegistro]) -> int:
    """Retorna a média de horas trabalhadas em minutos."""
    registros = _normalizar_lista(lista_colaboradores)
    minutos = [c["horas"] for c in registros]  # horas está em minutos
    return int(np.mean(minutos)) if minutos else 0


def maior_estresse(lista_colaboradores: Iterable[Colaborador | ColaboradorRegistro]) -> str:
    """Retorna o nome do colaborador com maior nível de estresse (empate retorna nomes separados por vírgula)."""
    registros = _normalizar_lista(lista_colaboradores)
    if not registros:
        return ""
    max_estresse = max(c["estresse"] for c in registros)
    nomes = [c["nome"] for c in registros if c["estresse"] == max_estresse]
    return ", ".join(nomes)


def colaboradores_produtivos(lista_colaboradores: Iterable[Colaborador | ColaboradorRegistro]) -> List[str]:
    """Retorna os nomes dos colaboradores com 5 ou mais tarefas concluídas."""
    registros = _normalizar_lista(lista_colaboradores)
    return [c["nome"] for c in registros if c["tarefas"] >= 5]


def alerta_equilibrio(lista_colaboradores: Iterable[Colaborador | ColaboradorRegistro]) -> List[str]:
    """Retorna colaboradores com estresse >= 4 e pausas <= 1."""
    registros = _normalizar_lista(lista_colaboradores)
    return [c["nome"] for c in registros if c["estresse"] >= 4 and c["pausas"] <= 1]


# ===========================================================================
# Análises estatísticas (NumPy)
# ===========================================================================
# Utiliza NumPy para calcular estatísticas descritivas:
# - Média e desvio padrão de horas trabalhadas
# - Média e mediana de níveis de estresse
# - Valores mínimos e máximos
# ===========================================================================

def calc_estatisticas(lista_colaboradores: Iterable[Colaborador | ColaboradorRegistro]) -> Dict[str, Any]:
    """Calcula estatísticas principais com NumPy. Horas retornadas em minutos."""
    registros = _normalizar_lista(lista_colaboradores)
    if not registros:
        return {
            "media_horas": 0,  # em minutos
            "desvio_horas": 0,  # em minutos
            "media_estresse": 0.0,
            "mediana_estresse": 0.0,
            "max_horas": 0,  # em minutos
            "min_horas": 0,  # em minutos
        }

    minutos = np.array([c["horas"] for c in registros], dtype=int)  # horas está em minutos
    estresse = np.array([c["estresse"] for c in registros], dtype=float)

    return {
        "media_horas": int(np.mean(minutos)),  # média em minutos
        "desvio_horas": int(np.std(minutos, ddof=0)),  # desvio em minutos
        "media_estresse": float(np.mean(estresse)),
        "mediana_estresse": float(np.median(estresse)),
        "max_horas": int(np.max(minutos)),  # máximo em minutos
        "min_horas": int(np.min(minutos)),  # mínimo em minutos
    }


# ===========================================================================
# Análises avançadas e extensões
# ===========================================================================
# Funcionalidades adicionais para análise profunda:
# - Classificação de risco (crítico, moderado, baixo)
# - Geração de feedback personalizado
# - Análise departamental
# - Avaliação de tendências e correlações
# - Previsão de estresse usando regressão linear
# - Síntese de insights e recomendações
# ===========================================================================

def classificar_risco(colaborador: ColaboradorRegistro) -> Tuple[str, int]:
    """
    Classifica o nível de risco de um colaborador com base em fatores
    como estresse, pausas, horas trabalhadas e produtividade.
    Retorna a faixa de risco ('critico', 'moderado', 'baixo') e o score calculado.
    Horas estão em minutos (10 horas = 600 minutos).
    """
    score = 0
    if colaborador["estresse"] >= 4:
        score += 3
    if colaborador["pausas"] <= 1:
        score += 2
    # 10 horas = 600 minutos
    if colaborador["horas"] > 600:
        score += 2
    if colaborador["tarefas"] < 3:
        score += 1

    if score >= 5:
        return "critico", score
    if score >= 3:
        return "moderado", score
    return "baixo", score


def feedback(colaborador: Colaborador | ColaboradorRegistro) -> str:
    """
    Gera uma mensagem de feedback personalizada para o colaborador
    com base no seu nível de estresse, produtividade, pausas e horas trabalhadas.
    Horas estão em minutos (10 horas = 600 minutos).
    """
    c = _normalizar_registro(colaborador)
    nome = c["nome"] or "Colaborador"
    est = c["estresse"]
    pausas = c["pausas"]
    tarefas = c["tarefas"]
    horas_minutos = c["horas"]  # em minutos

    if tarefas >= 5 and est <= 2 and pausas >= 2:
        return f"{nome}: desempenho excelente e equilíbrio saudável. Continue assim!"
    if tarefas >= 5 and est >= 4:
        return f"{nome}: produtividade alta, mas com estresse elevado. Inclua pausas e redistribua tarefas."
    if est >= 4 and pausas <= 1:
        return f"{nome}: alerta crítico de sobrecarga. Planeje pausas imediatas e reavalie prioridades."
    # 10 horas = 600 minutos
    if horas_minutos > 600:
        return f"{nome}: jornada longa identificada. Otimize agenda e considere delegar atividades."
    if tarefas < 3 and est <= 2:
        return f"{nome}: baixo volume entregue. Revise metas e busque suporte do time."
    if pausas < 2 and est >= 3:
        return f"{nome}: aumente as pausas para aliviar o estresse e manter foco."
    return f"{nome}: bom ritmo geral. Mantenha o equilíbrio entre produtividade e bem-estar."


def gerar_feedbacks(lista_colaboradores: Iterable[Colaborador | ColaboradorRegistro]) -> List[str]:
    return [feedback(c) for c in lista_colaboradores]


def mapear_riscos(lista_colaboradores: Iterable[Colaborador | ColaboradorRegistro]) -> Dict[str, List[str]]:
    registros = _normalizar_lista(lista_colaboradores)
    riscos = {"critico": [], "moderado": [], "baixo": []}
    for c in registros:
        faixa, _ = classificar_risco(c)
        riscos[faixa].append(c["nome"])
    return riscos


def analise_departamental(lista_colaboradores: Iterable[Colaborador | ColaboradorRegistro]) -> Dict[str, Dict[str, Any]]:
    """
    Analisa dados agrupados por departamento.
    Horas são armazenadas em minutos.
    """
    registros = _normalizar_lista(lista_colaboradores)
    departamentos: Dict[str, Dict[str, Any]] = {}
    for c in registros:
        depto = c["departamento"] or "Indefinido"
        info = departamentos.setdefault(
            depto,
            {"colaboradores": [], "total_tarefas": 0, "soma_estresse": 0.0, "soma_horas": 0},  # soma_horas em minutos
        )
        info["colaboradores"].append(c["nome"])
        info["total_tarefas"] += c["tarefas"]
        info["soma_estresse"] += c["estresse"]
        info["soma_horas"] += c["horas"]  # em minutos

    for depto, info in departamentos.items():
        total = len(info["colaboradores"])
        info["media_estresse"] = round(info["soma_estresse"] / total, 2) if total else 0.0
        info["media_horas"] = int(info["soma_horas"] / total) if total else 0  # média em minutos
        del info["soma_estresse"]
        del info["soma_horas"]

    return departamentos


def avaliar_tendencias(lista_colaboradores: Iterable[Colaborador | ColaboradorRegistro]) -> Dict[str, Any]:
    """
    Gera métricas adicionais como correlação e percentis.
    Horas são trabalhadas em minutos para cálculos.
    """
    registros = _normalizar_lista(lista_colaboradores)
    if not registros:
        return {
            "correlacao_horas_estresse": 0.0,
            "percentil_25_estresse": 0.0,
            "percentil_75_estresse": 0.0,
            "media_pausas": 0.0,
            "media_tarefas": 0.0,
        }

    minutos = np.array([c["horas"] for c in registros], dtype=float)  # em minutos
    estresse = np.array([c["estresse"] for c in registros], dtype=float)
    pausas = np.array([c["pausas"] for c in registros], dtype=float)
    tarefas = np.array([c["tarefas"] for c in registros], dtype=float)

    if minutos.size > 1 and np.std(minutos) > 0 and np.std(estresse) > 0:
        correlacao = float(np.corrcoef(minutos, estresse)[0, 1])
    else:
        correlacao = 0.0

    return {
        "correlacao_horas_estresse": correlacao,
        "percentil_25_estresse": float(np.percentile(estresse, 25)),
        "percentil_75_estresse": float(np.percentile(estresse, 75)),
        "media_pausas": float(np.mean(pausas)),
        "media_tarefas": float(np.mean(tarefas)),
    }


def prever_estresse_por_regressao(lista_colaboradores: Iterable[Colaborador | ColaboradorRegistro]) -> Dict[str, Any]:
    """
    Executa uma regressão linear simples para prever estresse com base em horas e pausas.
    Horas são trabalhadas em minutos para cálculos.
    """
    registros = _normalizar_lista(lista_colaboradores)
    if len(registros) < 3:
        return {
            "coeficientes": None,
            "rmse": None,
            "previstos": {},
        }

    minutos = np.array([c["horas"] for c in registros], dtype=float)  # em minutos
    pausas = np.array([c["pausas"] for c in registros], dtype=float)
    y = np.array([c["estresse"] for c in registros], dtype=float)

    # Monta matriz de features com termo de bias
    X = np.column_stack([np.ones_like(minutos), minutos, pausas])

    try:
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    except np.linalg.LinAlgError:
        return {
            "coeficientes": None,
            "rmse": None,
            "previstos": {},
        }

    y_pred = X.dot(beta)
    rmse = float(np.sqrt(np.mean((y - y_pred) ** 2)))

    previstos = {
        reg["nome"]: round(float(pred), 2)
        for reg, pred in zip(registros, y_pred)
    }

    return {
        "coeficientes": {
            "bias": round(float(beta[0]), 4),
            "horas_minutos": round(float(beta[1]), 6),  # coeficiente para minutos
            "pausas": round(float(beta[2]), 4),
        },
        "rmse": round(rmse, 4),
        "previstos": previstos,
    }


def sintetizar_insights(colaboradores: Iterable[Colaborador | ColaboradorRegistro]) -> Dict[str, Any]:
    """Gera matriz de insights combinando risco, tendência e previsão."""
    registros = _normalizar_lista(colaboradores)
    riscos = mapear_riscos(registros)
    tendencias = avaliar_tendencias(registros)
    previsao = prever_estresse_por_regressao(registros)

    recomendacoes: Dict[str, str] = {}
    previstos = previsao.get("previstos", {})
    for reg in registros:
        nome = reg["nome"]
        previsto = previstos.get(nome)
        delta = None if previsto is None else previsto - reg["estresse"]

        faixa, score = classificar_risco(reg)
        if faixa == "critico":
            recomendacoes[nome] = "Agendar intervenção com RH e planejamento emergencial de pausas."
        elif faixa == "moderado":
            recomendacoes[nome] = "Promover coaching de produtividade e revisar cronogramas semanais."
        else:
            recomendacoes[nome] = "Manter acompanhamento periódico e reforçar boas práticas."

        if delta is not None and delta > 0.8:
            recomendacoes[nome] += " Modelo prevê estresse ainda maior; antecipar ações preventivas."
        elif delta is not None and delta < -0.8:
            recomendacoes[nome] += " Tendência de queda no estresse; compartilhar boas práticas com o time."

    return {
        "riscos": riscos,
        "tendencias": tendencias,
        "previsao": previsao,
        "recomendacoes": recomendacoes,
    }


# ===========================================================================
# Entrada e validação de dados
# ===========================================================================
# Funções para coletar e validar dados dos colaboradores:
# - Validação de entradas numéricas e texto
# - Coleta interativa de dados
# - Dataset de demonstração para testes
# ===========================================================================

def _input_texto(prompt: str, minimo: int = 1, exemplo: str = "") -> str:
    """
    Solicita entrada de texto com validação de tamanho mínimo.
    """
    prompt_completo = prompt
    if exemplo:
        prompt_completo = f"{prompt} (ex: {exemplo}) "
    while True:
        valor = input(prompt_completo).strip()
        if len(valor) >= minimo:
            return valor
        print(f"Valor inválido. Informe ao menos {minimo} caractere(s).")


def _input_float(prompt: str, minimo: float = 0.0, maximo: float | None = None) -> float:
    while True:
        try:
            valor = float(input(prompt).strip())
        except ValueError:
            print("Entrada inválida. Digite um número (ex.: 8 ou 7.5).")
            continue
        if valor < minimo:
            print(f"O valor deve ser >= {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"O valor deve ser <= {maximo}.")
            continue
        return valor


def _input_int(prompt: str, minimo: int = 0, maximo: int | None = None, exemplo: str = "") -> int:
    """
    Solicita entrada de número inteiro com validação de intervalo.
    """
    prompt_completo = prompt
    if exemplo:
        prompt_completo = f"{prompt} (formato: número inteiro, ex: {exemplo}) "
    else:
        prompt_completo = f"{prompt} (número inteiro) "
    
    while True:
        try:
            valor = int(input(prompt_completo).strip())
        except ValueError:
            print("Entrada inválida. Digite um número inteiro (ex: 0, 1, 2, 3, 4, 5).")
            continue
        if valor < minimo:
            print(f"O valor deve ser maior ou igual a {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"O valor deve ser menor ou igual a {maximo}.")
            continue
        return valor


def _input_horas(prompt: str = "Horas trabalhadas") -> int:
    """
    Solicita entrada de horas no formato HH:MM e retorna em minutos.
    Aceita formatos: "8:30", "08:30", "8:00", "08:00"
    """
    prompt_completo = f"{prompt} (formato HH:MM, ex: 8:30, 08:00, 12:45): "
    while True:
        try:
            valor = input(prompt_completo).strip()
            minutos = horas_para_minutos(valor)
            return minutos
        except ValueError as e:
            print(f"Erro: {e}")
            print("Formato esperado: HH:MM onde HH é de 00 a 23 e MM é de 00 a 59")
            print("Exemplos válidos: 8:30, 08:00, 12:45, 23:59")
            continue


def coletar_dados_interativo(qtd: int = 5) -> List[ColaboradorRegistro]:
    print(f"\n{'='*60}")
    print(f"Coleta de dados para {qtd} colaboradores")
    print(f"{'='*60}\n")
    registros: List[ColaboradorRegistro] = []
    for idx in range(1, qtd + 1):
        print(f"{'─'*60}")
        print(f"Colaborador {idx} de {qtd}")
        print(f"{'─'*60}")
        nome = _input_texto("Nome completo", minimo=3, exemplo="João Silva")
        departamento = _input_texto("Departamento", minimo=2, exemplo="TI")
        horas_minutos = _input_horas("Horas trabalhadas no dia")
        pausas = _input_int("Pausas realizadas", minimo=0, exemplo="2")
        estresse = _input_int("Nível de estresse", minimo=1, maximo=5, exemplo="3")
        tarefas = _input_int("Tarefas concluídas", minimo=0, exemplo="5")
        registros.append(
            {
                "nome": nome.title(),
                "departamento": departamento.title(),
                "horas": horas_minutos,  # em minutos
                "pausas": pausas,
                "estresse": estresse,
                "tarefas": tarefas,
            }
        )
        print(f"Dados do colaborador {idx} registrados com sucesso!\n")
    return registros


def dados_demo() -> List[ColaboradorRegistro]:
    """
    Retorna um conjunto de dados de exemplo para demonstração do sistema.
    Útil para testes rápidos sem necessidade de entrada manual.
    Horas são fornecidas como strings no formato HH:MM e convertidas para minutos.
    """
    return [
        {"nome": "Felipe", "departamento": "Backend", "horas": "8:00", "pausas": 2, "estresse": 3, "tarefas": 5},
        {"nome": "Augusto", "departamento": "Frontend", "horas": "9:00", "pausas": 4, "estresse": 5, "tarefas": 8},
        {"nome": "Sofia", "departamento": "Dados", "horas": "7:00", "pausas": 6, "estresse": 4, "tarefas": 9},
        {"nome": "Leonardo", "departamento": "Scrum Master", "horas": "4:00", "pausas": 4, "estresse": 1, "tarefas": 5},
        {"nome": "Bruno", "departamento": "Cloud", "horas": "6:00", "pausas": 3, "estresse": 2, "tarefas": 4},
    ]


# ===========================================================================
# Relatórios e persistência
# ===========================================================================
# Funcionalidades para gerar e salvar relatórios:
# - Formatação de relatório completo em texto
# - Salvamento em arquivo de texto
# - Exportação de dados e estatísticas em JSON
# ===========================================================================

def gerar_relatorio_texto(colaboradores: Iterable[Colaborador | ColaboradorRegistro]) -> str:
    registros = _normalizar_lista(colaboradores)
    stats = calc_estatisticas(registros)
    produtivos = colaboradores_produtivos(registros)
    alertas = alerta_equilibrio(registros)
    mais_estressado = maior_estresse(registros)
    riscos = mapear_riscos(registros)
    departamentos = analise_departamental(registros)
    feedbacks = gerar_feedbacks(registros)
    insights = sintetizar_insights(registros)

    # Converter minutos para formato HH:MM para exibição
    media_horas_str = minutos_para_horas_str(stats['media_horas'])
    desvio_horas_str = minutos_para_horas_str(stats['desvio_horas'])
    min_horas_str = minutos_para_horas_str(stats['min_horas'])
    max_horas_str = minutos_para_horas_str(stats['max_horas'])

    linhas = [
        "RELATÓRIO WORKBALANCE AI",
        "-" * 60,
        f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total de colaboradores: {len(registros)}",
        "",
        "Indicadores principais:",
        f"- Média de horas trabalhadas: {media_horas_str}",
        f"- Desvio padrão de horas: {desvio_horas_str}",
        f"- Média de estresse: {stats['media_estresse']:.2f}",
        f"- Mediana de estresse: {stats['mediana_estresse']:.2f}",
        f"- Faixa de horas: {min_horas_str} a {max_horas_str}",
        f"- Colaborador(es) mais estressado(s): {mais_estressado or 'N/A'}",
        f"- Colaboradores com 5+ tarefas: {produtivos or 'Nenhum'}",
        f"- Alerta de equilíbrio (estresse >=4 e pausas <=1): {alertas or 'Nenhum'}",
        "",
        "Análise de riscos:",
        f"- Risco crítico: {riscos['critico'] or ['Nenhum']}",
        f"- Risco moderado: {riscos['moderado'] or ['Nenhum']}",
        f"- Risco baixo: {riscos['baixo'] or ['Nenhum']}",
        "",
        "Análise por departamento:",
    ]

    if departamentos:
        for depto, info in departamentos.items():
            media_depto_str = minutos_para_horas_str(info['media_horas'])
            linhas.append(f"- {depto}:")
            linhas.append(f"  Pessoas: {len(info['colaboradores'])}, média de horas: {media_depto_str}, média de estresse: {info['media_estresse']}")
            linhas.append(f"  Total de tarefas: {info['total_tarefas']}")
    else:
        linhas.append("- Nenhum departamento informado.")

    linhas.extend(
        [
            "",
            "Tendências gerais:",
            f"- Correlação horas x estresse: {insights['tendencias']['correlacao_horas_estresse']:.2f}",
            f"- Percentil 25 de estresse: {insights['tendencias']['percentil_25_estresse']:.2f}",
            f"- Percentil 75 de estresse: {insights['tendencias']['percentil_75_estresse']:.2f}",
            f"- Média de pausas: {insights['tendencias']['media_pausas']:.2f}",
            f"- Média de tarefas: {insights['tendencias']['media_tarefas']:.2f}",
        ]
    )

    previsao = insights["previsao"]
    if previsao["coeficientes"]:
        coefs = previsao['coeficientes']
        # Formatar coeficientes de forma mais legível
        coef_str = f"bias={coefs.get('bias', 0):.4f}, horas_minutos={coefs.get('horas_minutos', 0):.6f}, pausas={coefs.get('pausas', 0):.4f}"
        linhas.extend(
            [
                "",
                "Previsão de estresse (regressão linear):",
                f"- Coeficientes: {coef_str}",
                f"- RMSE do modelo: {previsao['rmse']}",
                "- Estresse estimado por colaborador:",
            ]
        )
        for nome, valor in previsao["previstos"].items():
            linhas.append(f"  * {nome}: {valor}")
    else:
        linhas.extend(
            [
                "",
                "Previsão de estresse: dados insuficientes para ajustar modelo confiável.",
            ]
        )

    linhas.append("")
    linhas.append("Planos de ação sugeridos:")
    for nome, recomendacao in insights["recomendacoes"].items():
        linhas.append(f"- {nome}: {recomendacao}")

    linhas.append("")
    linhas.append("Feedback individual:")
    for texto in feedbacks:
        linhas.append(f"- {texto}")

    return "\n".join(linhas)


def salvar_relatorio(texto: str, caminho: str = "relatorio_workbalance.txt") -> None:
    try:
        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)
    except Exception as exc:
        raise IOError(f"Não foi possível salvar o relatório em '{caminho}': {exc}") from exc


def salvar_dados_json(colaboradores: Iterable[Colaborador | ColaboradorRegistro], caminho: str = "dados_colaboradores.json") -> None:
    registros = _normalizar_lista(colaboradores)
    try:
        insights = sintetizar_insights(registros)
        stats = calc_estatisticas(registros)
        payload = {
            "timestamp": datetime.now().isoformat(),
            "colaboradores": registros,
            "estatisticas": stats,
            "insights": insights,
        }
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(payload, arquivo, ensure_ascii=False, indent=2)
    except Exception as exc:
        print(f"Aviso: falha ao salvar '{caminho}': {exc}")


# ===========================================================================
# CLI e ponto de entrada
# ===========================================================================
# Função principal que orquestra todo o fluxo do sistema:
# - Processamento de argumentos da linha de comando
# - Carregamento ou coleta de dados
# - Geração e exibição de relatórios
# - Salvamento de resultados
# ===========================================================================

def main(argv: List[str] | None = None) -> int:
    """
    Função principal do programa. Processa argumentos da linha de comando,
    coleta ou carrega dados, gera relatórios e salva resultados.
    """
    parser = argparse.ArgumentParser(
        description="WorkBalance AI - Sistema de Análise de Bem-Estar no Trabalho",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--demo", action="store_true", help="Usa dados de demonstração em vez da coleta interativa")
    parser.add_argument("--saida", type=str, default="relatorio_workbalance.txt", help="Arquivo de saída para o relatório")
    parser.add_argument("--json", type=str, default="dados_colaboradores.json", help="Arquivo JSON para salvar os dados brutos")
    parser.add_argument("--carregar-json", type=str, help="Arquivo JSON com colaboradores previamente coletados")
    args = parser.parse_args(argv)

    if args.carregar_json:
        try:
            with open(args.carregar_json, "r", encoding="utf-8") as arquivo:
                payload = json.load(arquivo)
            colaboradores = payload.get("colaboradores") or payload
            if not isinstance(colaboradores, list):
                raise ValueError("Estrutura de dados inválida no JSON de entrada.")
            colaboradores = _normalizar_lista(colaboradores)
            print(f"Carregados {len(colaboradores)} colaboradores de {args.carregar_json}.\n")
        except Exception as exc:
            print(f"Erro ao carregar '{args.carregar_json}': {exc}")
            return 1
    elif args.demo:
        colaboradores = dados_demo()
        print("Executando em modo demonstração.\n")
    else:
        colaboradores = coletar_dados_interativo(qtd=5)

    relatorio = gerar_relatorio_texto(colaboradores)
    print(relatorio)

    try:
        salvar_relatorio(relatorio, caminho=args.saida)
        print(f"\nRelatório salvo em: {args.saida}")
    except IOError as exc:
        print(f"Erro ao salvar relatório: {exc}")
        return 1

    salvar_dados_json(colaboradores, caminho=args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())