# Prompt few-shot — primeira versão

Três exemplos completos entraram no prompt. Os três eram o mesmo tipo
de situação: as quatro fontes respondem e o resumo é produzido.

```text
Gere testes de integração do pipeline do RPA_SMART_NEWS:
coleta nas fontes, deduplicação e sumarização.
Use notícias fictícias. Não acesse sites reais.
Siga o formato dos exemplos.

Exemplo 1
Entrada: tema Tecnologia; G1, BBC, Agência Brasil e R7 devolvem uma notícia cada
Resposta esperada: o resumo tem 4 fontes

Exemplo 2
Entrada: tema Esportes; as quatro fontes devolvem uma notícia cada
Resposta esperada: o resumo tem 4 fontes

Exemplo 3
Entrada: tema Economia; as quatro fontes devolvem uma notícia cada
Resposta esperada: o resumo tem 4 fontes
```

O resultado repetiu o caminho feliz com temas diferentes. Não apareceu
fonte indisponível, duplicata nem coleta vazia. O ajuste está em
`PROMPT-AJUSTADO.md`.
