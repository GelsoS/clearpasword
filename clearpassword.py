import PyPDF2
import tkinter as tk
from tkinter import filedialog
from PyPDF2.errors import PdfReadError


def remover_senha_pdf(arquivo_entrada, senha, arquivo_saida):
    try:
        with open(arquivo_entrada, "rb") as arquivo:
            leitor_pdf = PyPDF2.PdfReader(arquivo)

            if leitor_pdf.decrypt(senha):
                escritor_pdf = PyPDF2.PdfWriter()

                for pagina_num in range(len(leitor_pdf.pages)):
                    pagina = leitor_pdf.pages[pagina_num]
                    escritor_pdf.add_page(pagina)
                # Verifica se o diretório de saída é acessível
                try:
                    with open(arquivo_saida, "wb") as saida:
                        escritor_pdf.write(saida)
                        return "PDF processado com sucesso!.\n"
                except PermissionError:
                    return "Erro: Diretório de saída negado,escolha outro!"
            else:
                return "Senha incorreta!"
    except PdfReadError:
        return "Erro: Arquivo não criptografado"


def selecionar_arquivo():
    arquivo_entrada = filedialog.askopenfilename(
        title="Selecione o arquivo PDF com senha",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    entrada_var.set(arquivo_entrada)


def selecionar_saida():
    arquivo_saida = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        title="Escolha o local e nome do arquivo de saída"
    )
    saida_var.set(arquivo_saida)


def processar():
    arquivo_entrada = entrada_var.get()
    senha = senha_var.get()
    arquivo_saida = saida_var.get()

    if arquivo_entrada and senha and arquivo_saida:
        log_text.delete(1.0, tk.END)  # Limpa o campo de log
        resultado = remover_senha_pdf(arquivo_entrada, senha, arquivo_saida)
        log_text.insert(tk.END, "Iniciando processamento...\n")
        log_text.insert(tk.END, f"--->{resultado}\n")
    else:
        log_text.insert(tk.END, "Preencha todos os campos.\n")


# Interface gráfica
root = tk.Tk()
root.title("Remover Senha de PDF")
# Criar a janela principal
root.geometry("400x300")
root.configure(bg="#9fa3a7")
root.maxsize(500, 400)

# Variáveis de controle
entrada_var = tk.StringVar()
saida_var = tk.StringVar()
senha_var = tk.StringVar()
entrada_var = tk.StringVar()


# Rótulos e entradas
tk.Label(root, text="Arquivo PDF com senha:", bg="#9fa3a7").pack()
tk.Button(
    root,
    text="Selecionar Arquivo",
    bg="#000000",
    fg="#ffffff",
    command=selecionar_arquivo,
    cursor="hand2",
    width=18,
).pack()
tk.Entry(
    root,
    textvariable=entrada_var,
    state="disabled",
    width=50,
    disabledforeground="#1c6000",
    disabledbackground="#9fa3a7",
).pack()

tk.Label(root, text="Senha do PDF:", bg="#9fa3a7").pack()
tk.Entry(root, textvariable=senha_var, show="").pack()

tk.Label(root, text="Arquivo de saída:", bg="#9fa3a7").pack()
tk.Button(
    root,
    text="Selecionar Saída",
    bg="#000000",
    fg="#ffffff",
    command=selecionar_saida,
    cursor="hand2",
    width=18,
).pack()
tk.Entry(
    root,
    textvariable=saida_var,
    state="disabled",
    width=50,
    disabledforeground="#1c6000",
    disabledbackground="#9fa3a7",
).pack()

# Botão de processamento
tk.Button(
    root,
    text="Processar",
    bg="#000000",
    fg="#ffffff",
    command=processar,
    cursor="hand2",
    width=18,
).pack()

# Campo para logs
log_text = tk.Text(root, wrap="word", height=10, bg="black", fg="green")
log_text.pack(expand=True, fill="both")

# Associa a função remove_hover aos eventos de entrada e saída do mouse

root.mainloop()
