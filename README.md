# 💣 Campo Minado em Clojure e Python

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/downloads/) [![Clojure](https://img.shields.io/badge/Clojure-1.11+-green.svg?style=for-the-badge&logo=clojure)](https://clojure.org/) [![Babashka](https://img.shields.io/badge/Runs%20with-Babashka-purple.svg?style=for-the-badge)](https://babashka.org/)

## Descrição do Projeto

Este repositório contém o projeto final do Curso de Clojure - 2025.1 da **UFCG**.

O objetivo do projeto foi implementar o jogo Campo Minado com uma interface de linha de comando (CLI).O jogo foi desenvolvido em duas linguagens:

-   **Clojure**: Uma implementação funcional, seguindo os princípios de imutabilidade e funções puras.
-   **Python**: Uma implementação seguindo uma abordagem mais tradicional/imperativa.

## Estrutura do Repositório

O projeto está organizado em duas pastas principais, uma para cada implementação:

-   `./clojure/`: Contém todo o código-fonte da versão em Clojure.
-   `./python/`: Contém todo o código-fonte da versão em Python.

## Funcionalidades

Ambas as versões do jogo possuem as seguintes funcionalidades:

-   Tabuleiro gerado com minas posicionadas aleatoriamente.
-   Mecanismo que impede que a primeira jogada do usuário seja uma mina.
-   Interface de linha de comando (CLI) interativa.
-   Opção de revelar células.
-   Opção de marcar e desmarcar células com bandeiras (🚩).
-   Detecção automática de vitória e derrota.

## Requisitos

Certifique-se de ter os seguintes pré-requisitos instalados para executar cada versão.

#### Para a versão em Clojure:
-   [Babashka](https://github.com/babashka/babashka#installation)

#### Para a versão em Python:
-   [Python 3.x](https://www.python.org/downloads/)

## Como Executar

Siga os passos abaixo para a versão que deseja executar.

### Versão em Clojure

1.  Abra seu terminal e navegue até a pasta da implementação em Clojure:
    ```sh
    cd src/clojure
    ```
2.  Dê permissão de execução ao script:
    ```sh
    chmod +x game.clj
    ```
3.  Execute o jogo:
    ```sh
    ./game.clj
    ```
    Ou, alternativamente:
    ```sh
    bb game.clj
    ```

### Versão em Python

1.  Abra seu terminal e navegue até a pasta da implementação em Python:
    ```sh
    cd src/python
    ```
2.  Execute o jogo usando o interpretador Python 3:
    ```sh
    python3 game.py
    ```
    *(Dependendo do seu sistema, o comando pode ser apenas `python game.py`)*

## Como Jogar

Os comandos são os mesmos para ambas as versões. Após iniciar o jogo, digite uma das seguintes ações:

-   **Revelar uma célula:** `r <linha> <coluna>`
    -   *Exemplo:* `r 3 4`
-   **Marcar/Desmarcar uma bandeira:** `f <linha> <coluna>`
    -   *Exemplo:* `f 0 1`
-   **Sair do jogo:** `q`
