# Casos gerados pelo prompt zero-shot

Registro fiel do que a LLM devolveu na primeira tentativa.
Os títulos e as URLs abaixo são fictícios. Nenhum site real foi acessado.

## Caso 1 — caminho feliz, sem contrato

A LLM descreveu um único cenário: o usuário escolhe o tema Tecnologia,
as quatro fontes devolvem notícias e o robô gera um PDF. Não há
afirmação sobre duplicata, fonte fora do ar ou resumo vazio.

## Caso 2 — alucinação de API

A LLM inventou um endpoint que o projeto não possui:

- `GET /api/noticias?tema=tecnologia` deveria responder HTTP 200
- o corpo teria `id`, `headline` e `published`

No RPA_SMART_NEWS a coleta é feita por Page Object no navegador.
Não existe essa API. O caso não pode entrar na suíte.

## Caso 3 — o único caso aproveitável

Quatro fontes devolvem uma notícia cada, todas com título diferente.
O resumo precisa citar as quatro. Esse caso virou o arquivo
`test_integracao_zero_shot.py`. Ele passa, mas não exercita falha,
duplicata nem coleta vazia.
