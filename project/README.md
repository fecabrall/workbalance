# WorkBalance AI

Ferramenta de linha de comando em Python para análise de bem-estar e produtividade no ambiente de trabalho. O WorkBalance AI interpreta rotinas, identifica sinais de sobrecarga cognitiva, classifica riscos e gera recomendações personalizadas com estatística (NumPy) e automação de relatórios.

## Contribuidores

- Augusto Oliveira Codo  
- Felipe de Oliveira Cabral  
- Sofia Bueris Netto

## 📋 Índice

- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Exemplos de Uso](#exemplos-de-uso)
- [Formato dos Dados](#formato-dos-dados)
- [Saídas do Sistema](#saídas-do-sistema)

## 🚀 Funcionalidades

### Funcionalidades Principais

- **Coleta de Dados**: Sistema interativo para coleta de dados de colaboradores com validação completa
- **Análise Estatística**: Cálculos com NumPy (média, desvio padrão, mediana, correlações)
- **Classificação de Riscos**: Identificação automática de colaboradores em risco (crítico, moderado, baixo)
- **Feedback Personalizado**: Geração de mensagens individuais baseadas no perfil de cada colaborador
- **Análise Departamental**: Agregação de métricas por departamento
- **Previsão de Estresse**: Modelo de regressão linear para prever níveis de estresse
- **Relatórios Detalhados**: Geração de relatórios completos em texto e JSON
- **Exportação de Dados**: Salvamento de dados brutos e análises para auditoria

### Dados Coletados

Para cada colaborador, o sistema coleta:
- Nome completo
- Departamento
- Horas trabalhadas no dia (formato HH:MM, ex: 8:30, 08:00)
- Quantidade de pausas realizadas
- Nível de estresse percebido (escala de 1 a 5)
- Número de tarefas concluídas

### Sistema de Horas

O sistema utiliza formato de relógio (HH:MM) para representar horas trabalhadas, onde:
- **HH** representa as horas (00 a 23)
- **MM** representa os minutos (00 a 59)
- Exemplos válidos: `8:30`, `08:00`, `12:45`, `23:59`

Internamente, as horas são convertidas para minutos para facilitar cálculos estatísticos precisos. No relatório gerado, os valores são exibidos novamente no formato HH:MM para melhor legibilidade.

## 📦 Requisitos

- Python 3.8 ou superior
- NumPy (instalado automaticamente via pip)

## 🔧 Instalação

1. Clone ou baixe o repositório
2. Instale as dependências:

```bash
pip install numpy
```

Ou instale diretamente do arquivo de requisitos (se houver):

```bash
pip install -r requirements.txt
```

## 💻 Uso

### Modo Interativo (Padrão)

Execute o programa sem argumentos para entrar no modo interativo. O sistema solicitará os dados de 5 colaboradores:

```bash
python workbalance_ai.py
```

### Modo Demonstração

Use a flag `--demo` para testar o sistema com dados de exemplo:

```bash
python workbalance_ai.py --demo
```

### Carregar Dados de um Arquivo JSON

Para carregar dados previamente coletados de um arquivo JSON:

```bash
python workbalance_ai.py --carregar-json dados_anteriores.json
```

### Personalizar Arquivos de Saída

Especifique arquivos personalizados para o relatório e dados JSON:

```bash
python workbalance_ai.py --demo --saida meu_relatorio.txt --json meus_dados.json
```

### Argumentos da Linha de Comando

| Argumento | Descrição | Padrão |
|-----------|-----------|--------|
| `--demo` | Usa dados de demonstração em vez de coleta interativa | - |
| `--saida` | Arquivo de saída para o relatório | `relatorio_workbalance.txt` |
| `--json` | Arquivo JSON para salvar os dados brutos | `dados_colaboradores.json` |
| `--carregar-json` | Arquivo JSON com colaboradores previamente coletados | - |

### Obter Ajuda

Para ver todas as opções disponíveis:

```bash
python workbalance_ai.py --help
```

## 📁 Estrutura do Projeto

```
workbalance-ai/
│
├── workbalance_ai.py           # Arquivo principal do sistema
├── relatorio_workbalance.txt   # Relatório gerado (criado após execução)
├── dados_colaboradores.json    # Dados exportados em JSON (criado após execução)
├── README.md                   # Este arquivo
├── GUIA_USO_CLI.md             # Arquivo explicativo da CLI
└── EXPLICACAO_RELATORIO.md     # Arquivo explicativo do relatório
```

## 📊 Exemplos de Uso

### Exemplo 1: Execução Básica com Dados de Demonstração

```bash
python workbalance_ai.py --demo
```

**Saída esperada:**
- Relatório exibido no terminal
- Arquivo `relatorio_workbalance.txt` criado
- Arquivo `dados_colaboradores.json` criado

### Exemplo 2: Coleta Interativa de Dados

```bash
python workbalance_ai.py
```

O sistema solicitará:
```
============================================================
Coleta de dados para 5 colaboradores
============================================================

────────────────────────────────────────────────────────────
Colaborador 1 de 5
────────────────────────────────────────────────────────────
Nome completo (ex: João Silva): João Silva
Departamento (ex: TI): TI
Horas trabalhadas no dia (formato HH:MM, ex: 8:30, 08:00, 12:45): 8:30
Pausas realizadas (formato: número inteiro, ex: 2): 2
Nível de estresse (formato: número inteiro, ex: 3): 3
Tarefas concluídas (número inteiro): 5
Dados do colaborador 1 registrados com sucesso!
...
```

### Exemplo 3: Carregar Dados Existentes e Gerar Relatório

```bash
python workbalance_ai.py --carregar-json dados_colaboradores.json --saida relatorio_customizado.txt
```

### Exemplo 4: Uso Programático (em outro script Python)

```python
from workbalance_ai import (
    coletar_dados_interativo,
    gerar_relatorio_texto,
    salvar_relatorio,
    calc_estatisticas,
    colaboradores_produtivos,
    alerta_equilibrio
)

# Coletar dados
colaboradores = coletar_dados_interativo(qtd=5)

# Calcular estatísticas
stats = calc_estatisticas(colaboradores)
print(f"Média de horas: {stats['media_horas']:.2f}h")

# Identificar colaboradores produtivos
produtivos = colaboradores_produtivos(colaboradores)
print(f"Colaboradores produtivos: {produtivos}")

# Gerar e salvar relatório
relatorio = gerar_relatorio_texto(colaboradores)
salvar_relatorio(relatorio, caminho="meu_relatorio.txt")
```

## 📝 Formato dos Dados

### Estrutura de um Colaborador

Cada colaborador é representado como um dicionário Python com os seguintes campos:

```python
{
    "nome": "João Silva",           # String (mínimo 3 caracteres)
    "departamento": "TI",            # String (mínimo 2 caracteres)
    "horas": "8:30",                 # String no formato HH:MM ou int (minutos)
    "pausas": 2,                     # Inteiro (>= 0)
    "estresse": 3,                   # Inteiro (1 a 5)
    "tarefas": 6                     # Inteiro (>= 0)
}
```

**Nota sobre horas**: O sistema aceita horas em formato string (HH:MM) ou número inteiro (minutos). Durante a coleta interativa, use o formato HH:MM. Em arquivos JSON, você pode usar strings como "8:30" ou números inteiros representando minutos (ex: 510 para 8 horas e 30 minutos).

### Formato JSON de Entrada

Ao carregar dados de um arquivo JSON, o sistema aceita dois formatos:

**Formato 1: Lista de colaboradores**
```json
[
    {
        "nome": "Ana",
        "departamento": "RH",
        "horas": "8:00",
        "pausas": 2,
        "estresse": 3,
        "tarefas": 6
    },
    {
        "nome": "Pedro",
        "departamento": "TI",
        "horas": "9:30",
        "pausas": 1,
        "estresse": 4,
        "tarefas": 5
    }
]
```

**Formato 2: Objeto com chave "colaboradores"**
```json
{
    "colaboradores": [
        {
            "nome": "Ana",
            "departamento": "RH",
            "horas": "8:00",
            "pausas": 2,
            "estresse": 3,
            "tarefas": 6
        }
    ]
}
```

**Nota**: Você também pode usar números inteiros para horas (representando minutos). Por exemplo, `480` representa 8 horas (8 * 60 = 480 minutos).

## 📄 Saídas do Sistema

### Relatório de Texto

O arquivo `relatorio_workbalance.txt` contém:

- **Indicadores principais**: Média e desvio padrão de horas, média e mediana de estresse
- **Análise de riscos**: Classificação de colaboradores por nível de risco
- **Análise departamental**: Métricas agregadas por departamento
- **Tendências gerais**: Correlações, percentis, médias de pausas e tarefas
- **Previsão de estresse**: Coeficientes do modelo de regressão e estimativas
- **Planos de ação**: Recomendações personalizadas para cada colaborador
- **Feedback individual**: Mensagens de feedback para cada colaborador

### Arquivo JSON

O arquivo `dados_colaboradores.json` contém:

```json
{
    "timestamp": "2024-01-15T10:30:00",
    "colaboradores": [...],
    "estatisticas": {
        "media_horas": 7.8,
        "desvio_horas": 1.2,
        "media_estresse": 3.2,
        ...
    },
    "insights": {
        "riscos": {...},
        "tendencias": {...},
        "previsao": {...},
        "recomendacoes": {...}
    }
}
```

## 🔍 Validações e Tratamento de Erros

O sistema implementa validações robustas:

- **Validação de entrada**: Todas as entradas são validadas antes do processamento
- **Tratamento de erros**: Mensagens claras para erros de entrada
- **Validação de arquivos**: Verificação de existência e formato de arquivos JSON
- **Tratamento de exceções**: Captura e tratamento de erros de I/O

### Validações Aplicadas

- Nome: mínimo de 3 caracteres
- Departamento: mínimo de 2 caracteres
- Horas: formato HH:MM onde HH é de 00 a 23 e MM é de 00 a 59
- Pausas: número inteiro não negativo (>= 0)
- Estresse: número inteiro entre 1 e 5 (inclusive)
- Tarefas: número inteiro não negativo (>= 0)

## 🧪 Testes

### Teste Rápido com Dados de Demonstração

```bash
python workbalance_ai.py --demo
```

Verifique se os arquivos foram criados:
- `relatorio_workbalance.txt`
- `dados_colaboradores.json`

### Teste de Validação de Entrada

Execute o modo interativo e teste entradas inválidas:
- Tente inserir estresse = 6 (deve ser rejeitado - máximo é 5)
- Tente inserir horas no formato inválido como "25:00" (deve ser rejeitado - máximo é 23:59)
- Tente inserir horas com minutos inválidos como "8:60" (deve ser rejeitado - máximo é 59)
- Tente inserir nome vazio (deve ser rejeitado - mínimo 3 caracteres)
- Tente inserir pausas negativas (deve ser rejeitado)

## 📚 Funções Disponíveis

### Funções principais (núcleo da análise)

- `calcular_media_horas(lista_colaboradores)`: Calcula média de horas trabalhadas
- `maior_estresse(lista_colaboradores)`: Retorna nome(s) do(s) colaborador(es) com maior estresse
- `colaboradores_produtivos(lista_colaboradores)`: Lista colaboradores com 5+ tarefas
- `alerta_equilibrio(lista_colaboradores)`: Identifica colaboradores com estresse >= 4 e pausas <= 1

### Funções de Análise Avançada

- `calc_estatisticas(lista_colaboradores)`: Calcula estatísticas descritivas
- `classificar_risco(colaborador)`: Classifica nível de risco
- `feedback(colaborador)`: Gera feedback personalizado
- `analise_departamental(lista_colaboradores)`: Agrega dados por departamento
- `avaliar_tendencias(lista_colaboradores)`: Calcula correlações e percentis
- `prever_estresse_por_regressao(lista_colaboradores)`: Previsão usando regressão linear
- `sintetizar_insights(lista_colaboradores)`: Combina todas as análises

### Funções de Entrada e Saída

- `coletar_dados_interativo(qtd=5)`: Coleta dados interativamente
- `dados_demo()`: Retorna dados de demonstração
- `gerar_relatorio_texto(colaboradores)`: Gera relatório em texto
- `salvar_relatorio(texto, caminho)`: Salva relatório em arquivo
- `salvar_dados_json(colaboradores, caminho)`: Exporta dados em JSON

## 🎯 Casos de Uso

### Caso de Uso 1: Análise Diária

Execute o sistema diariamente para monitorar o bem-estar da equipe:

```bash
python workbalance_ai.py --saida relatorio_$(date +%Y%m%d).txt
```

### Caso de Uso 2: Análise Semanal

Acumule dados durante a semana e gere um relatório consolidado:

```bash
# Dia 1
python workbalance_ai.py --saida segunda_feira.json

# Dia 2
python workbalance_ai.py --saida terca_feira.json

# ... (outros dias)

# Análise final (carregar todos os JSONs e consolidar)
```

### Caso de Uso 3: Análise por Departamento

Execute o sistema e analise os resultados por departamento no relatório gerado.

## ⚠️ Limitações e Considerações

- O sistema requer pelo menos 3 colaboradores para gerar previsões de regressão linear
- A análise de correlação requer variância nos dados
- O modelo de previsão é simples (regressão linear) e pode não capturar relações complexas
- Os dados são armazenados localmente (não há banco de dados)

## 🔮 Melhorias Futuras

Possíveis melhorias para versões futuras:

- Interface gráfica (GUI)
- Banco de dados para armazenamento persistente
- Modelos de machine learning mais avançados
- Visualizações gráficas (gráficos e dashboards)
- Exportação para Excel/CSV
- API REST para integração com outros sistemas
- Autenticação e controle de acesso
- Histórico de análises e comparações temporais

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique se todos os requisitos estão instalados
2. Execute o sistema com `--demo` para verificar se está funcionando
3. Verifique os arquivos de log (se houver)
4. Consulte a documentação das funções no código

## Licença

Código disponibilizado para portfólio e referência. Uso comercial ou redistribuição: alinhar com os autores.