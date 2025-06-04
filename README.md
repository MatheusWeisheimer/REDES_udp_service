# UDPService

Este projeto contém um servidor e um cliente UDP para operações matemáticas simples (soma, média, mínimo e máximo) sobre números em arquivos `.txt`.

## Como iniciar o servidor e o cliente

1. **Certifique-se de ter o Python 3 instalado.**
2. (Opcional) Instale o Tkinter, caso não esteja disponível:
   ```bash
   sudo apt-get install python3-tk
   ```

3. **Inicie o servidor UDP:**
   ```bash
   python3 udp_server.py
   ```

4. **Inicie o cliente UDP (interface gráfica):**
   ```bash
   python3 udp_client.py
   ```

## Como criar executáveis com PyInstaller

1. **Instale o PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Gere o executável do servidor:**
   ```bash
   pyinstaller --onefile udp_server.py
   ```

3. **Gere o executável do cliente:**
   ```bash
   pyinstaller --onefile udp_client.py
   ```

   Os executáveis serão criados na pasta `dist/`.

## Observações

- O cliente requer o Tkinter para a interface gráfica.
- Os arquivos `.txt` usados pelo cliente devem conter um número de ponto flutuante por linha.
- O servidor escuta por padrão em `127.0.0.1:2022`.
