# Metodologia e qualidade dos dados

A base contém **1.803 observações diárias consecutivas**, de **24/03/2017 a 28/02/2022**, com máxima, mínima, abertura, fechamento, volume e fechamento ajustado.

Não foram identificadas datas ausentes, datas duplicadas ou valores ausentes. `Close` e `Adj Close` são idênticos na base fornecida.

## Pergunta central

**Como preço, retorno, volatilidade, volume e risco de queda do Bitcoin evoluíram entre março de 2017 e fevereiro de 2022?**

## Indicadores

- retorno acumulado;
- CAGR;
- retorno diário;
- volatilidade anualizada;
- volatilidade móvel de 30 dias;
- drawdown e drawdown máximo;
- extremos diários;
- retorno por ano dentro da amostra;
- volume registrado.

## Anualização

Como Bitcoin negocia todos os dias, a volatilidade é anualizada com `sqrt(365)`.

## Anos parciais

2017 e 2022 são períodos parciais na base e não devem ser interpretados como anos-calendário completos.

## Causalidade

A análise é descritiva. A base não contém variáveis explicativas suficientes para atribuir os movimentos de preço a fatores específicos.
