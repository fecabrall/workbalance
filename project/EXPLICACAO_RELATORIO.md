# Explicação das Análises do Relatório WorkBalance AI

## Seção: Tendências Gerais

Esta seção apresenta análises estatísticas avançadas sobre os dados coletados dos colaboradores.

### Correlação Horas x Estresse

A correlação mede o relacionamento entre duas variáveis. Valores próximos de:
- **1.0**: Correlação positiva forte (quanto mais horas, mais estresse)
- **0.0**: Sem correlação (não há relação)
- **-1.0**: Correlação negativa forte (quanto mais horas, menos estresse)

**Exemplo**: Se a correlação for 0.90, significa que há uma forte relação positiva entre horas trabalhadas e nível de estresse. Isso indica que colaboradores que trabalham mais horas tendem a ter níveis de estresse mais altos.

### Percentil 25 e Percentil 75 de Estresse

Os percentis dividem os dados em quartis:
- **Percentil 25**: 25% dos colaboradores têm estresse igual ou menor que este valor
- **Percentil 75**: 75% dos colaboradores têm estresse igual ou menor que este valor

**Exemplo**: Se o percentil 25 é 2.00 e o percentil 75 é 4.00:
- 25% dos colaboradores têm estresse ≤ 2.0 (baixo estresse)
- 50% dos colaboradores têm estresse entre 2.0 e 4.0 (estresse moderado)
- 25% dos colaboradores têm estresse > 4.0 (alto estresse)

### Média de Pausas e Tarefas

Valores médios simples que indicam o comportamento geral da equipe:
- **Média de pausas**: Quantidade média de pausas realizadas por colaborador
- **Média de tarefas**: Quantidade média de tarefas concluídas por colaborador

## Seção: Previsão de Estresse (Regressão Linear)

Esta seção utiliza um modelo matemático para prever níveis de estresse com base em horas trabalhadas e quantidade de pausas.

### Coeficientes do Modelo

O modelo de regressão linear utiliza a fórmula:
```
Estresse Previsto = bias + (horas_minutos × coeficiente_horas) + (pausas × coeficiente_pausas)
```

**Componentes**:
- **bias**: Valor base de estresse quando horas e pausas são zero
- **horas_minutos**: Quanto o estresse aumenta por minuto trabalhado
- **pausas**: Quanto o estresse diminui por pausa realizada

**Exemplo de interpretação**:
- `bias = -4.0000`: Valor base negativo (sem horas e pausas, o estresse seria negativo, o que não faz sentido - isso é normal em modelos)
- `horas_minutos = 0.012992`: Cada minuto trabalhado aumenta o estresse em aproximadamente 0.013 pontos
- `pausas = 0.4472`: Cada pausa aumenta o estresse em 0.45 pontos (pode parecer estranho, mas depende dos dados)

**Nota**: Os coeficientes podem variar dependendo dos dados. Um coeficiente positivo para pausas pode indicar que colaboradores com mais pausas também têm mais estresse (talvez porque estão sobrecarregados e precisam de mais pausas).

### RMSE (Root Mean Squared Error)

O RMSE mede a precisão do modelo:
- **Valores baixos** (próximos de 0): Modelo muito preciso
- **Valores altos**: Modelo menos preciso

**Exemplo**: Se o RMSE é 0.1295, significa que, em média, o modelo erra por aproximadamente 0.13 pontos na escala de estresse (que vai de 1 a 5). Isso é uma precisão razoável.

### Estresse Estimado por Colaborador

Para cada colaborador, o modelo calcula um valor estimado de estresse com base nas horas trabalhadas e pausas. Compare este valor com o estresse real informado pelo colaborador:

- **Valores próximos**: O modelo está prevendo bem
- **Valores muito diferentes**: Pode haver fatores não considerados (como complexidade das tarefas, pressão externa, etc.)

**Exemplo**:
- Felipe: Estresse real = 3, Estresse previsto = 3.13 (muito próximo - modelo preciso)
- Augusto: Estresse real = 5, Estresse previsto = 4.8 (próximo - modelo razoável)
- Leonardo: Estresse real = 1, Estresse previsto = 0.91 (muito próximo - modelo preciso)

## Interpretação Prática

### Quando a Correlação é Alta (próximo de 1.0)

Isso indica que há uma relação forte entre horas trabalhadas e estresse. Ações recomendadas:
- Monitorar jornadas de trabalho
- Implementar políticas de limitação de horas extras
- Incentivar pausas regulares

### Quando o RMSE é Baixo (< 1.0)

O modelo está conseguindo prever bem os níveis de estresse. Isso permite:
- Antecipar problemas antes que ocorram
- Planejar intervenções preventivas
- Identificar colaboradores em risco

### Quando os Percentis Mostram Alta Dispersão

Se a diferença entre percentil 25 e 75 é grande, significa que há muita variabilidade no estresse da equipe. Ações recomendadas:
- Investigar causas específicas para colaboradores com alto estresse
- Compartilhar boas práticas de colaboradores com baixo estresse
- Personalizar intervenções por perfil

## Limitações do Modelo

1. **Dados Limitados**: Com apenas 5 colaboradores, o modelo pode não capturar todas as relações complexas
2. **Fatores Não Considerados**: O modelo não considera complexidade de tarefas, pressão de prazos, relacionamentos interpessoais, etc.
3. **Modelo Simples**: A regressão linear assume relações lineares, mas a realidade pode ser mais complexa
4. **Causalidade vs Correlação**: Correlação não implica causalidade - mais horas podem não causar mais estresse diretamente

## Conclusão

Essas análises fornecem insights valiosos sobre o bem-estar da equipe, mas devem ser interpretadas com cautela e complementadas com outras informações contextuais. Use os dados como ferramenta de apoio à decisão, não como única fonte de verdade.