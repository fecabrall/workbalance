# Guia Rápido de Uso da CLI - WorkBalance AI

## 📖 Como Usar a Interface de Linha de Comando

### 1. Execução Básica (Modo Interativo)

Execute o programa sem argumentos. O sistema pedirá os dados de 5 colaboradores:

```bash
python workbalance_ai.py
```

**O que acontece:**
1. Sistema solicita dados de cada colaborador (nome, departamento, horas, pausas, estresse, tarefas)
2. Valida cada entrada (se errar, pede novamente)
3. Gera e exibe o relatório no terminal
4. Salva o relatório em `relatorio_workbalance.txt`
5. Salva os dados em `dados_colaboradores.json`

### 2. Modo Demonstração (Teste Rápido)

Use `--demo` para testar sem inserir dados manualmente:

```bash
python workbalance_ai.py --demo
```

**O que acontece:**
- Usa dados de exemplo pré-definidos
- Gera relatório completo
- Cria os arquivos de saída

### 3. Carregar Dados de um Arquivo JSON

Se você já tem dados salvos em JSON:

```bash
python workbalance_ai.py --carregar-json meu_arquivo.json
```

**Formato do JSON esperado:**
```json
[
    {
        "nome": "João",
        "departamento": "TI",
        "horas": 8.5,
        "pausas": 2,
        "estresse": 3,
        "tarefas": 6
    }
]
```

Ou:
```json
{
    "colaboradores": [
        {
            "nome": "João",
            "departamento": "TI",
            "horas": 8.5,
            "pausas": 2,
            "estresse": 3,
            "tarefas": 6
        }
    ]
}
```

### 4. Personalizar Nomes dos Arquivos de Saída

```bash
python workbalance_ai.py --demo --saida relatorio_customizado.txt --json dados_customizados.json
```

### 5. Ver Todas as Opções

```bash
python workbalance_ai.py --help
```

## 🎯 Exemplos Práticos

### Exemplo 1: Análise Diária

```bash
# Execute pela manhã para coletar dados do dia anterior
python workbalance_ai.py

# Ou use dados salvos
python workbalance_ai.py --carregar-json dados_ontem.json --saida relatorio_hoje.txt
```

### Exemplo 2: Teste Rápido

```bash
# Teste rápido com dados de exemplo
python workbalance_ai.py --demo
```

### Exemplo 3: Análise com Arquivo Personalizado

```bash
# Carregue dados e salve com nome específico
python workbalance_ai.py --carregar-json entrada.json --saida saida_personalizada.txt
```

### Exemplo 4: Pipeline Completo

```bash
# 1. Colete dados interativamente
python workbalance_ai.py --saida relatorio_segunda.txt --json dados_segunda.json

# 2. No dia seguinte, carregue os dados anteriores e compare
python workbalance_ai.py --carregar-json dados_segunda.json --saida comparacao_terca.txt
```

## 📝 Entrada de Dados (Modo Interativo)

Quando executar sem `--demo`, o sistema pedirá:

```
Coleta de dados para 5 colaboradores.

--- Colaborador 1 ---
Nome: [Digite o nome - mínimo 3 caracteres]
Departamento: [Digite o departamento - mínimo 2 caracteres]
Horas trabalhadas no dia: [Digite um número - ex: 8 ou 8.5]
Pausas realizadas (quantidade): [Digite um número inteiro - ex: 2]
Nível de estresse (1 a 5): [Digite um número de 1 a 5]
Tarefas concluídas: [Digite um número inteiro - ex: 6]
```

### Validações Aplicadas

- **Nome**: Deve ter pelo menos 3 caracteres
- **Departamento**: Deve ter pelo menos 2 caracteres
- **Horas**: Deve ser entre 0.0 e 24.0
- **Pausas**: Deve ser um número inteiro >= 0
- **Estresse**: Deve ser um número inteiro entre 1 e 5
- **Tarefas**: Deve ser um número inteiro >= 0

**Se errar:** O sistema pede para digitar novamente com uma mensagem de erro clara.

## 📤 Saídas Geradas

### Arquivo de Relatório (`relatorio_workbalance.txt`)

Contém:
- Indicadores principais (médias, desvios)
- Análise de riscos
- Análise por departamento
- Tendências gerais
- Previsões de estresse
- Planos de ação
- Feedback individual

### Arquivo JSON (`dados_colaboradores.json`)

Contém:
- Dados brutos dos colaboradores
- Estatísticas calculadas
- Insights e análises
- Timestamp da geração

## 🔧 Troubleshooting

### Erro: "NumPy é obrigatório"

**Solução:**
```bash
pip install numpy
```

### Erro: "Arquivo não encontrado" ao usar --carregar-json

**Solução:**
- Verifique se o caminho do arquivo está correto
- Use caminho absoluto se necessário: `--carregar-json C:\caminho\completo\arquivo.json`

### Erro ao salvar relatório

**Solução:**
- Verifique permissões de escrita no diretório
- Verifique se o arquivo não está aberto em outro programa
- Tente com um nome de arquivo diferente usando `--saida`

### Entrada inválida durante coleta interativa

**Solução:**
- Leia a mensagem de erro exibida
- Digite novamente seguindo as validações
- Para cancelar: pressione `Ctrl+C`

## 💡 Dicas de Uso

1. **Use --demo primeiro**: Teste o sistema com `--demo` antes de usar dados reais
2. **Salve backups**: Mantenha cópias dos arquivos JSON gerados
3. **Nomeie arquivos com data**: Use `--saida relatorio_2024_01_15.txt` para organizar
4. **Valide dados JSON**: Verifique o formato antes de carregar
5. **Combine com scripts**: Use em scripts de automação para análises periódicas

## 🚀 Automação

### Script Windows (PowerShell)

Crie um arquivo `executar_analise.ps1`:

```powershell
# Executar análise diária
$data = Get-Date -Format "yyyyMMdd"
python workbalance_ai.py --saida "relatorio_$data.txt" --json "dados_$data.json"
```

### Script Linux/Mac (Bash)

Crie um arquivo `executar_analise.sh`:

```bash
#!/bin/bash
# Executar análise diária
DATA=$(date +%Y%m%d)
python workbalance_ai.py --saida "relatorio_$DATA.txt" --json "dados_$DATA.json"
```

Torne executável:
```bash
chmod +x executar_analise.sh
```

## 📊 Integração com Outros Sistemas

### Carregar dados de um sistema externo

1. Exporte os dados do sistema externo para JSON no formato esperado
2. Use `--carregar-json` para carregar
3. Gere o relatório

### Usar em scripts Python

```python
from workbalance_ai import (
    coletar_dados_interativo,
    gerar_relatorio_texto,
    salvar_relatorio,
    calc_estatisticas
)

# Seus dados
colaboradores = [
    {"nome": "João", "departamento": "TI", "horas": 8.0, 
     "pausas": 2, "estresse": 3, "tarefas": 6}
]

# Gerar relatório
relatorio = gerar_relatorio_texto(colaboradores)
salvar_relatorio(relatorio, "meu_relatorio.txt")

# Usar estatísticas
stats = calc_estatisticas(colaboradores)
print(f"Média: {stats['media_horas']}")
```

## ❓ Perguntas Frequentes

**P: Posso usar menos de 5 colaboradores?**  
R: Sim, mas algumas análises (como regressão linear) requerem pelo menos 3 colaboradores.

**P: Posso usar mais de 5 colaboradores?**  
R: Sim, modifique a função `coletar_dados_interativo(qtd=5)` ou use `--carregar-json` com mais dados.

**P: Os arquivos são sobrescritos?**  
R: Sim, por padrão. Use `--saida` e `--json` para criar arquivos com nomes diferentes.

**P: Posso executar sem salvar arquivos?**  
R: O sistema sempre salva. Você pode ignorar os arquivos gerados ou deletá-los após visualizar.

**P: Como faço para ver apenas o relatório sem coletar dados?**  
R: Use `--carregar-json` com dados existentes ou `--demo` para dados de exemplo.

---

Para mais informações, consulte o [README.md](README.md) completo.