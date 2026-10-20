# Prompt few-shot — versão ajustada

O ajuste colocou o contrato real dos módulos e trocou os três exemplos
de sucesso por três situações diferentes.

```text
Gere testes de integração em pytest para o pipeline do RPA_SMART_NEWS.

Contrato:
- coletar_noticias percorre as fontes. Se uma fonte lança exceção,
  as outras continuam.
- dedupe remove URL canônica repetida e título normalizado repetido.
- summarize só roda se sobrar notícia. A coleta vazia não chama a IA.
- Use o cliente stub. Não chame OpenAI e não abra o navegador.
- Notícias fictícias, no modelo NewsArticle
  (title, url, source, topic).
- Não invente endpoint HTTP. A coleta entra por Page Object.

Siga a diversidade dos exemplos. Não repita o mesmo desfecho.

Exemplo 1
Entrada: G1 devolve duas URLs iguais, BBC falha, Agência Brasil e R7
devolvem títulos diferentes.
Resposta esperada: a BBC fica de fora, a URL repetida sai uma vez só,
e o resumo lista as fontes que sobraram.

Exemplo 2
Entrada: G1 e R7 devolvem o mesmo título em URLs diferentes.
Resposta esperada: dedupe mantém uma notícia.

Exemplo 3
Entrada: as quatro fontes devolvem lista vazia.
Resposta esperada: _run_pipeline devolve None e summarize não é chamado.
```
