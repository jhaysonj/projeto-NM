# Explicação do ataque ao WPA2-PSK com clientes conectados à rede

Nesse tipo de conexão, é necessário compartilhar uma chave antes da autenticação no Wi-Fi, a chave PSK (Pre-Shared Key).

## Defindo PSK, PMK e PTK
Para segurança, a senha do Wi-Fi não é transmitida em texto claro durante a autenticação. Em vez disso, ocorre um processo de derivação da chave PSK para gerar outra chave, denominada PMK (Pairwise Master Key).

**Processo de derivação da PSK**

Podemos utilizar o binário `wpa_passphrase` para gerar a chave PSK a partir de uma senha e SSID:
`$ wpa_passphrase [ssid] [passphrase]`

Para gerarmos a chave PSK, usamos as informações abaixo:
`PSK = PBKDF2(HMAC-SHA1, passphrase, SSID, 4096, 256)`
Onde:
- **HMAC-SHA1**: Algoritmo de hash usado para derivar a chave.
- **passphrase**: Senha fornecida pelo usuário.
- **SSID**: Nome da rede Wi-Fi.
- **4096**: Número de iterações do algoritmo para aumentar a segurança.
- **256**: Tamanho da chave resultante em bits.

Por exemplo, para o Wi-Fi com SSID `wifi_GR1S` e senha `grisgris`, o comando seria:
```
$ wpa_passphrase wifi_GR1S grisgris
network={
	ssid="wifi_GR1S"
	#psk="grisgris"
	psk=9c0798375fc724c678e1f65b5755cbae8635c5918db6f6ae1f1cedb4ca7a8c9b
}
     
```

**Processo de derivação da PMK**
A PMK é derivada da PSK usando a função PBKDF2 (Password-Based Key Derivation Function 2) com o algoritmo HMAC-SHA1:
`PMK = PBKDF2(HMAC-SHA1, PSK, SSID, 4096, 256)`
onde:
- HMAC-SHA1: é o algoritmo de hash
- SSID: nome da rede Wi-Fi
- 4096: quantidade de iterações do algoritmo
- 256: tamanho em bits da chave, equivalente a 32 bytes



O cliente envia um pacote de associação (Association Request) para o access point, dando início ao 4-way handshake, explicado abaixo.

## Processo de Autenticação (4-Way Handshake)

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeHbFVoopx_3bdpcoGsmry-aUcnzSAKJVQ-f2L-DGiyLU1w4Gq26kXU3c49wDVTPcxEoJuXT9Ib7Sps68EWEh5gt3Dl9Jvt9uVFcHTGrEPi5W8dFAbvJutquuED1yfzvoaYxs6JAFzpOeR5Zi2Fsx2tGuHh?key=qibF_DzbWbmVB-P_9nKHwQ)

**Passo 1**: O Access Point (AP) envia um nonce (ANonce) para o STA (Station). Um nonce é um número aleatório utilizado uma única vez.

**Passo 2**: O STA gera seu próprio nonce (SNonce) e usa a PSK, o ANonce, e o SNonce para derivar a Pairwise Transient Key (PTK). O STA envia o SNonce de volta ao AP junto com uma chave de verificação de integridade de mensagem (MIC - Message Integrity Check).

**Passo 3**: O AP, já conhecendo a PSK e o ANonce, e recebendo o SNonce do STA, também calcula a PTK. O AP verifica o MIC recebido para garantir que o STA possui a PSK correta. Se tudo estiver correto, o AP envia outro pacote com o MIC para o STA.

**Passo 4**: O STA verifica o MIC do AP, confirmando que ambos compartilham a mesma chave. Se o MIC for válido, o STA envia uma mensagem final ao AP, estabelecendo uma comunicação segura.

  
  
**Processo de derivação da PTK**

A chave PTK (Pairwise Transient Key) é uma chave temporária, uma chave de transição, utilizada para validar o processo de autenticação. 

`PTK = PRF(PMK || ANonce || SNonce || AMAC || SMAC)`

onde:
- **||** é o operador de concatenação.
- **AMAC** é o endereço MAC do Access Point (Autenticador).
- **SMAC** é o endereço MAC do STA (Suplicante), que deseja se conectar à rede Wi-Fi.
- **PRF** é uma função Pseudo-aleatória (PRF). Para WPA, o PRF é baseado em SHA1, e para WPA2, é baseado em SHA256.

  

**Bruteforce**

Dentre todas as informações utilizadas no processo de autenticação (4-way handshake), a única informação que não possuímos é a senha do wifi, as outras informações ou são informações públicas ou podem ser obtidas a partir do monitoramento da rede alvo. Por conta disso, basta realizarmos um ataque de tentativa e erro na senha, e verificarmos se com a senha utilizada obtemos a mesma PTK do Access Point.


## PoC WPA2-PSK com cliente conectado à rede

O ataque consiste em capturar o handshake e fazer bruteforce das possíveis senhas.

### Colocar a placa no modo de monitoramento
	comando `airmon-ng start wlan0` coloca a placa em modo de monitoramento

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXd3TNoLfG_R7hoFbgMWMMmXPWGNCS2jlCWLMpDAj_FKGhuq9zGo46ep7ubNLN_0j1iNBkMFFm3rnVKQl3qKSZKFm_5oacfN3eTB7nolv5wr6UaBwzJngXYzH14yw2vloPgtzoYwQz8fa0k_Z31rsiwAI0_d?key=qibF_DzbWbmVB-P_9nKHwQ)

obs: Após esse comando, é possível que a interface (placa) tenha mudado de nome.

Para verificar se o nome do dispositivo mudou, basta executar o comando `iwconfig`. Após executarmos esse comando, percebemos que a placa manteve o mesmo nome “wlan0”, mas em alguns casos há adição de um `mon`(monitor) ao final do nome, resultando em `wlan0mon`


![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeIKAlM6pPPI-0u1ZtDopjsyk0AvFGd1J6cm13JPztIzuN7n_3S-duxVtaEezPMnAOO54M6HhPq21Pdw9r_rAkOHj-CSTd8FCMbnNyUEhsDo4KLdBsESuBY2lQsF-K2QfD6rYWKC24QCc4tD2xHLHomb1w?key=qibF_DzbWbmVB-P_9nKHwQ)

  
### Monitorar as redes para selecionar o alvo
O comando `airodump-ng wlan0` monitora as redes Wi-Fi

**informações do alvo:**
**essid** = “baby yoda comunista”
bssid = “40:EE:DD:39:C7:E8”

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfUU7HOsYx5vcGvgmrbfwblMLBcbWryIDhalr3jKbQtiKpWnYWCRJGG2DUB_lZSJA1KKhaU-4t-0N5IzjBSZNlRpCG8PdKsFPwobyIr4RUJHHtXhPafG87tNWvS6oEINSCV1J56qMr3fPmyN3n_2--9gBYj?key=qibF_DzbWbmVB-P_9nKHwQ)

### Trocar o canal da placa para o mesmo canal da rede alvo
1. `ifconfig wlan0 down`  - derruba a placa para fazermos as modificações
2. `iwconfig wlan0 channel 6` - troca o canal da placa para a mesma da rede alvo
3. `ifconfig wlan0 up` - sobe a placa após fazermos as modificações
4. `iwlist wlan0 channel` - mostra todos os canais da placa e o canal atual da placa

No github dessa apresentação tem um script em python para automatizar os passos acima
https://github.com/jhaysonj/projeto-NM/blob/main/wifi.sh
  

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcf4izSSncCF8fqk42BYH-Tk3JYyhgV6u9Eh-PwPVeHYMzvFPy1Qqqdjjt4qIxDJFm-2CqlQBo4JLGEvQLzl6_o1Cl_uDyqhyNLHNRhOsd0UtTzkNu-ErWgKYB9ztSAFRIM_82_RRq4dIQ8zrA90jKcT3sP?key=qibF_DzbWbmVB-P_9nKHwQ)
### Monitorar a rede alvo 
o comando `airodump-ng wlan0 --bssid 40:EE:DD:39:C7:E8 --channel 8 -w wpa_baby_yoda` monitora a rede e salva as informações monitoradas em arquivos de nome “wpa_baby_yoda”

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdKVNbIvhqF6AedjJQJtdufAbbkWbJ-iNvmJ28CUDNwLhTQCVXmztwZBa47Oi03XVCi0P3yi4Z3r8COI5lZ-L5WwOdM7u4qyJfqYDmYTrHZOqlUflh9Lxl-iq7s85Vpj2c7fA1W7doR9mTJ8-Xna9TFcnoz?key=qibF_DzbWbmVB-P_9nKHwQ)

Todos os endereços macs das “STATION” são dispositivos conectados à rede

**Arquivos gerados**
  
![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXez_tqZ_Yu6YW1X-U79RRgkn_eJFt2Uaxg-upn9iGrC64ya0_1tzMG4udhR_TF3d94KAi9R32aUuMXXlde8B4Usc_mrOw0T-_Gw2CqRnVlt4DuIOKUizVzcCTWXwwPms5Az4eyPnrVizonPuzF7j2O4pwrW?key=qibF_DzbWbmVB-P_9nKHwQ)

  
### Captura de handshake
O handshake é feito toda vez que um dispositivo se conecta à rede, podemos simplesmente esperar um dispositivo se conectar.
   
Para facilitar o processo de captura de handshake, utilizaremos um ataque chamado ataque de desautenticação, onde forçamos a desconexão do dispositivo, para que o alvo se reconecte e assim capturamos o handshake.

O comando `aireplay-ng -0 10 -a 40:EE:DD:39:C7:E8 wlan0 -c 64:A2:00:0D:04:0E` envia pacotes que desautenticam o dispositivo.

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeFeWwJmOArfq3_dEh0nPyBSe9j8E7emRf4IesthqgBOlk9Ii1TpRLNldqo8VYUp8UuO62L1OVfz9NR9byRctgmPzvI_Ep_sW7IbrErjFs29-RPjpiNqqXtsbX-5Gv7oIRcOyS3duYeEyvcJaC8XhVWpDUY?key=qibF_DzbWbmVB-P_9nKHwQ)

**Capturamos o handshake**    

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXeb-X4i1A48S2euhMqCFwB4HA-UGuRdH-sw1XVSQwH2Crcpg5o1RPRcjPC40bFvHDCfreZacnsPTYVjdgoVP8cKWdXHNM0IpKX5miWwmku4vSlWGGTkJNy-2C_TGPESFD08rg7N58Nd08zfI-YC__9UoSNE?key=qibF_DzbWbmVB-P_9nKHwQ)

  ### Realizar a quebra da senha
  O comando `aircrack-ng -a 2 -b 40:EE:DD:39:C7:E8 -w ./Documents/wordlist_numerica.txt ./Desktop/wpa_baby_yoda-02.cap` faz um bruteforce para realizar a quebra da senha

![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcZode3EZTTVHh3inEvtfFUUZv8ibUQgQc8tdmEeSDWK--TUZxBrxcW6fNJbwmB81kf6iieAIJLj0TQ-qaVUzukd2VmIkAvcN2YLO6q2GgpXBGeOL-Z8dKF-RSJjrZOQQ0yHtF-4TqFnY2TAGuMK6sNxBVu?key=qibF_DzbWbmVB-P_9nKHwQ)

### Poc WPA2-psk PMKid (sem clientes conectados à rede)


# Explicação do ataque ao WPA2-PSK sem clientes conectados à rede

O **PMKID** é um identificador que é derivado da chave mestra (PMK) e pode ser usado para autenticar clientes em redes Wi-Fi. Ele é parte do processo de autenticação no protocolo WPA/WPA2, especificamente quando o protocolo Fast BSS Transition (também conhecido como 802.11r) ou algumas outras implementações do WPA2 estão em uso.
- O PMKID é gerado pela seguinte fórmula:
   `PMKID = HMAC-SHA1-128(PMK, "PMK Name" || BSSID || StaMac)`
onde:
- **PMK** (Pairwise Master Key) é derivada da senha PSK (Pre-Shared Key) e do SSID.
- **"PMK Name"** é uma string constante.
- **BSSID** é o endereço MAC do ponto de acesso.
- **StaMac/SMac** é o endereço MAC do cliente (Station/Supplicant).

**Ponto de vulnerabilidade**
 Algumas implementações do WPA/WPA2 enviam o PMKID no primeiro pacote de autenticação (Association Response) sem que o cliente tenha que responder com qualquer dado. Isso significa que o atacante pode solicitar a autenticação de um ponto de acesso sem precisar realizar um handshake completo, e o ponto de acesso responde com um pacote que contém o PMKID.

## Etapas do Ataque ao PMKID

- **1. Captura do PMKID:**
    - O atacante envia uma solicitação de autenticação (Association Request) ao ponto de acesso (AP).
    - O AP responde com um pacote contendo o PMKID.
- **2. Brute-Force da PSK:**
    - Com o PMKID capturado, o atacante pode tentar realizar um ataque de força bruta para derivar a PSK original.
    - O processo envolve gerar PMKs a partir de diferentes combinações de possíveis senhas e o SSID conhecido da rede e calcular o PMKID correspondente usando o mesmo método que o AP utilizou.
    - Quando o PMKID calculado corresponde ao PMKID capturado, o atacante sabe que a senha PSK correta foi encontrada.

## Vantagens do Ataque ao PMKID:
- **Não é Necessário Desautenticar Clientes:** Ao contrário dos ataques de captura de handshake tradicionais, este ataque não requer a desautenticação de um cliente para capturar o handshake, o que torna o ataque mais discreto e rápido.
- **Facilidade na Captura:** Como o PMKID é enviado no primeiro pacote de autenticação, ele pode ser capturado diretamente, sem a necessidade de esperar por um cliente ativo se conectar à rede.

## **Proteção Contra o Ataque:**
- **Atualização de Firmware:** Os fabricantes de roteadores podem corrigir essa vulnerabilidade em suas implementações do WPA2 através de atualizações de firmware que evitam o envio do PMKID de forma desnecessária.
- **Uso de WPA3:** O WPA3, a próxima geração de segurança Wi-Fi, mitiga este tipo de ataque com a introdução de um processo de autenticação mais robusto que não é vulnerável a ataques baseados no PMKID.
- **Senhas Fortes:** Usar uma PSK complexa e difícil de adivinhar reduz significativamente a viabilidade de ataques de força bruta.