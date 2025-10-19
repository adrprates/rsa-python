# 🔒 RSA Criptografia do Zero

Este repositório contém uma implementação **do zero** do algoritmo **RSA** (Rivest-Shamir-Adleman) em Python. O objetivo é demonstrar e entender o funcionamento interno deste sistema criptográfico de chave pública, sem depender de bibliotecas criptográficas externas.

O código permite gerar chaves, cifrar e decifrar mensagens, além de criar e validar assinaturas digitais de forma interativa.

## 💡 Sobre o Algoritmo RSA

O **RSA** é um sistema de criptografia assimétrica que se baseia na dificuldade de fatorar números inteiros grandes (o problema da fatoração). Ele utiliza um **par de chaves**:

- **Chave Pública ($\mathbf{n}, \mathbf{e}$):** Distribuída livremente, usada para **cifrar** mensagens.
- **Chave Privada ($\mathbf{n}, \mathbf{d}$):** Mantida em segredo, usada para **decifrar** mensagens.

Além da confidencialidade, o RSA é fundamental para **Autenticidade** e **Não-Repúdio** por meio das **Assinaturas Digitais**:
- A chave **privada** é usada para **assinar** uma mensagem.
- A chave **pública** é usada para **verificar** a autenticidade da assinatura.

---

## 🛠️ Funcionalidades Implementadas

Todas as funções essenciais para o RSA foram implementadas manualmente (from scratch):

| Função | Conceito Criptográfico |
| :--- | :--- |
| **`gerar_chaves`** | Geração do par $(\mathbf{n}, \mathbf{e})$ e $(\mathbf{n}, \mathbf{d})$. |
| **`primo_provavel`** | Teste de Primalidade **Miller-Rabin** (garantindo primos fortes). |
| **`inverso_modular`** | Cálculo de $\mathbf{d}$ (chave privada) via Algoritmo de Euclides Estendido. |
| **`cifrar` / `decifrar`** | Cifragem e Decifragem Modular $C = M^e \pmod n$ e $M = C^d \pmod n$. |
| **`assinar` / `verificar`** | Geração e validação de Assinaturas Digitais. |
| **Blocagem** | Conversão de texto para blocos de inteiros (compatíveis com $n$). |

---

## 🚀 Como Executar o Projeto

1.  Certifique-se de ter **Python 3.x** instalado.
2.  Clone este repositório:
    ```bash
    git clone [https://github.com/adrprates/rsa-python.git](https://github.com/adrprates/rsa-python.git)
    cd rsa-python
    ```
3.  Execute o script Python (assumindo que o nome do arquivo é `rsa.py`):

    ```bash
    python rsa.py
    ```

### 📋 Menu Interativo

Ao iniciar, o programa gera um novo par de chaves RSA de **512 bits** e abre o menu principal:



\==========================
Menu:
1 - Cifrar
2 - Decifrar (cole os blocos)
3 - Validar assinatura
4 - Sair



| Opção | Descrição da Interação |
| :--- | :--- |
| **1 - Cifrar** | Solicita a mensagem, **cifra** com a chave pública e **assina** com a chave privada. Exibe os blocos cifrados e a assinatura. |
| **2 - Decifrar** | Pede que você cole os blocos cifrados (ex: `[123,456]` ou `123,456`). **Decifra** usando a chave privada e exibe a mensagem original. |
| **3 - Validar Assinatura** | Pede os blocos cifrados e o número da assinatura. **Decifra** a mensagem, e usa a chave pública para verificar se a assinatura é **válida** para o texto decifrado. |
| **4 - Sair** | Encerra a aplicação. |

---

## 📝 Observações Técnicas

* **Segurança (Chaves):** As chaves são geradas com **512 bits** por padrão. Para aplicações reais, são recomendados 2048 bits ou mais. A geração utiliza o módulo `secrets` para aleatoriedade criptograficamente segura.
* **Chaves em Memória:** As chaves geradas (`pub` e `priv`) são mantidas apenas na memória durante a execução do programa e não são salvas em disco.
* **Dependências:** O código não depende de nenhuma biblioteca externa (como `pycryptodome` ou `cryptography`), utilizando apenas módulos padrão como `math`, `secrets` e `ast`.

---

## 📚 Referências

* [RSA na Wikipedia](https://pt.wikipedia.org/wiki/RSA)
* [Explicação matemática e detalhes de implementação do RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem))

