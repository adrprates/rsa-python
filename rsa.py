import secrets
import math
import ast
import sys

def primo_provavel(n, k=20):
    if n < 2:
        return False
    pequenos = [2,3,5,7,11,13,17,19,23,29]
    for p in pequenos:
        if n % p == 0:
            return n == p
    r, d = 0, n-1
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = secrets.randbelow(n-3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(r-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

def gerar_primo(bits):
    while True:
        candidato = secrets.randbits(bits)
        candidato |= (1 << (bits-1)) | 1
        if primo_provavel(candidato):
            return candidato

def mdc_estendido(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x1, y1 = mdc_estendido(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return (g, x, y)

def inverso_modular(a, m):
    g, x, _ = mdc_estendido(a, m)
    if g != 1:
        raise ValueError("Não existe inverso modular")
    return x % m

def gerar_chaves(bits=512):
    print("Gerando primos (pode levar alguns segundos)...")
    p = gerar_primo(bits // 2)
    q = gerar_primo(bits // 2)
    while q == p:
        q = gerar_primo(bits // 2)
    n = p * q
    phi = (p-1)*(q-1)
    e = 65537
    if math.gcd(e, phi) != 1:
        e = 3
        while math.gcd(e, phi) != 1:
            e += 2
    d = inverso_modular(e, phi)
    return (n, e), (n, d)

def texto_para_inteiros(texto, n):
    dados = texto.encode('utf-8')
    n_bytes = (n.bit_length() + 7) // 8
    max_tamanho = n_bytes - 1
    blocos = []
    for i in range(0, len(dados), max_tamanho):
        parte = dados[i:i+max_tamanho]
        blocos.append(int.from_bytes(parte, 'big'))
    return blocos

def inteiros_para_texto(blocos):
    if not blocos:
        return ""
    partes = []
    for b in blocos:
        length = (b.bit_length() + 7) // 8 or 1
        partes.append(b.to_bytes(length, 'big'))
    texto_bytes = b''.join(partes)
    return texto_bytes.decode('utf-8', errors='ignore')

def cifrar(chave_publica, mensagem):
    n, e = chave_publica
    blocos = texto_para_inteiros(mensagem, n)
    return [pow(m, e, n) for m in blocos]

def decifrar(chave_privada, blocos):
    n, d = chave_privada
    dec = [pow(c, d, n) for c in blocos]
    return inteiros_para_texto(dec)

def assinar(chave_privada, mensagem):
    n, d = chave_privada
    m_int = int.from_bytes(mensagem.encode('utf-8'), 'big')
    if m_int >= n:
        raise ValueError("Mensagem muito longa para assinatura direta.")
    return pow(m_int, d, n)

def verificar(chave_publica, mensagem, assinatura):
    n, e = chave_publica
    m_int = int.from_bytes(mensagem.encode('utf-8'), 'big')
    return pow(assinatura, e, n) == m_int

def parse_lista(texto):
    texto = texto.strip()
    if not texto:
        raise ValueError("Entrada vazia.")
    try:
        val = ast.literal_eval(texto)
        if isinstance(val, list) and all(isinstance(x, int) for x in val):
            return val
    except:
        pass
    parts = [p.strip() for p in texto.split(',') if p.strip() != '']
    if all(p.lstrip('-').isdigit() for p in parts):
        return [int(p) for p in parts]
    raise ValueError("Formato inválido, use [1,2,3] ou 1,2,3")

def main():
    pub, priv = gerar_chaves(512)

    print("\nChaves geradas (mantidas em memória durante a execução).")
    print("Chave pública n (primeiros 40 dígitos):", str(pub[0])[:40]+"...", "e:", pub[1])
    print("Chave privada gerada e mantida em memória.\n")

    while True:
        print("==========================")
        print("Menu:")
        print("1 - Cifrar")
        print("2 - Decifrar (cole os blocos)")
        print("3 - Validar assinatura")
        print("4 - Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            msg = input("Digite a mensagem a cifrar: ")
            if not msg:
                print("Mensagem vazia, cancelado.\n")
                continue
            blocos_cifrados = cifrar(pub, msg)
            assinatura = assinar(priv, msg)
            print("\nMensagem cifrada (blocos inteiros):")
            print(blocos_cifrados)
            print("Assinatura gerada:", assinatura)
            print("Fim da cifragem.\n")

        elif escolha == '2':
            entrada = input("Cole os blocos cifrados da mensagem (ex: [123,456] ou 123,456): ")
            try:
                blocos = parse_lista(entrada)
                texto = decifrar(priv, blocos)
                print("\nMensagem decifrada:", texto)
            except Exception as e:
                print("Erro:", e)
            print("Fim da decifragem.\n")

        elif escolha == '3':
            entrada = input("Cole os blocos cifrados da mensagem (ex: [123,456] ou 123,456): ")
            ass_input = input("Cole o número da assinatura: ")
            try:
                blocos = parse_lista(entrada)
                assinatura_input = int(ass_input.strip())
                texto = decifrar(priv, blocos)
                valido = verificar(pub, texto, assinatura_input)
                print("\nMensagem decifrada:", texto)
                print("Validação da assinatura:", valido)
            except Exception as e:
                print("Erro na validação:", e)
            print("Fim da verificação.\n")

        elif escolha == '4' or escolha.lower() in ('sair','q','quit','exit'):
            print("Saindo. Até logo!")
            break
        else:
            print("Opção inválida.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário. Saindo.")
        sys.exit(0)