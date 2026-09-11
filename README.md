# O Voto Imparcial

Plataforma interativa de transparência eleitoral desenvolvida para apresentar informações públicas de candidatos de forma objetiva, permitindo que o usuário conheça os dados antes de revelar a identidade política.

## Sobre o projeto

O **O Voto Imparcial** foi desenvolvido com uma abordagem centrada em dados públicos e apresentação neutra das informações eleitorais.

A aplicação permite que o usuário explore candidatos inicialmente de forma anônima, analisando informações como:

- patrimônio declarado;
- histórico de cargos públicos;
- atuação legislativa;
- propostas de governo;
- informações eleitorais;
- cobertura dos dados disponíveis.

A identidade do candidato é revelada somente após a seleção do perfil.

O projeto não atribui notas, não cria rankings e não recomenda candidatos.

## Objetivo

Criar uma experiência de consulta eleitoral baseada em dados públicos, reduzindo a influência inicial de elementos como:

- nome;
- partido;
- gênero;
- imagem;
- identificação política.

A proposta é permitir que o usuário examine primeiro as informações disponíveis e posteriormente conheça a identidade do candidato.

## Como funciona

### 1. Exploração anônima

Na página inicial, os candidatos são apresentados por identificadores anônimos.

Cada perfil possui uma identificação visual própria, sem exibir inicialmente o nome do candidato.

### 2. Análise do perfil

Ao acessar um candidato, o usuário pode consultar os dados disponíveis sobre seu histórico e suas declarações.

Entre as informações apresentadas estão:

- patrimônio declarado;
- bens e direitos;
- histórico de cargos políticos;
- atuação legislativa;
- propostas de governo;
- dados eleitorais.

### 3. Revelação da identidade

Depois da análise, o usuário pode selecionar o candidato para revelar sua identidade e consultar seus dados eleitorais.

## Dados utilizados

O projeto utiliza informações provenientes de bases públicas relacionadas às eleições e à atividade parlamentar.

### Tribunal Superior Eleitoral — TSE

Dados eleitorais e patrimoniais dos candidatos, incluindo:

- candidaturas;
- partidos;
- número de urna;
- gênero;
- bens declarados;
- propostas de governo;
- informações eleitorais complementares.

### Câmara dos Deputados

Dados relacionados à atuação parlamentar e proposições legislativas.

### Senado Federal

Dados relacionados às matérias e proposições de autoria dos candidatos que possuem histórico no Senado.

## Processamento dos dados

O projeto possui uma estrutura separada para coleta, transformação e armazenamento dos dados.

```text
dados/
├── brutos/
├── intermediarios/
└── processado/

src/
├── carga/
├── transformacao/
└── app.py