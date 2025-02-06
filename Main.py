import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog, colorchooser
import json
import os

CONFIG_FILE = "config.json"

class TabelaCustosApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Tabelas de Custos")
        self.geometry("750x550")
        self.configure(bg="#f0f0f0")

        self.tabelas = {}
        self.criar_tabela("Default")
        self.tabela_atual = "Default"
        self.data_folder = None
        self.carregar_config()

        self.criar_widgets()

        if self.data_folder:
            self.carregar_dados()

    def criar_widgets(self):
        frame_persistencia = tk.Frame(self, bg="#f0f0f0")
        frame_persistencia.pack(pady=5, fill="x")
        btn_selecionar_pasta = tk.Button(frame_persistencia, text="Selecionar Pasta de Dados",
                                         command=self.selecionar_pasta, bg="#3F51B5", fg="white", padx=10)
        btn_selecionar_pasta.pack(side="left", padx=10)
        self.label_pasta = tk.Label(frame_persistencia, text=self.get_label_pasta(), bg="#f0f0f0")
        self.label_pasta.pack(side="left", padx=5)

        frame_tabelas = tk.Frame(self, bg="#f0f0f0")
        frame_tabelas.pack(pady=10, fill="x")

        tk.Label(frame_tabelas, text="Tabela:", bg="#f0f0f0", font=("Arial", 10)).pack(side="left", padx=5)
        self.combobox_tabelas = ttk.Combobox(frame_tabelas, values=list(self.tabelas.keys()), state="readonly", width=20)
        self.combobox_tabelas.set(self.tabela_atual)
        self.combobox_tabelas.pack(side="left", padx=5)
        self.combobox_tabelas.bind("<<ComboboxSelected>>", self.selecionar_tabela)

        btn_nova_tabela = tk.Button(frame_tabelas, text="Nova Tabela", command=self.nova_tabela, bg="#2196F3", fg="white")
        btn_nova_tabela.pack(side="left", padx=5)

        btn_apagar_tabela = tk.Button(frame_tabelas, text="Apagar Tabela", command=self.apagar_tabela, bg="#F44336", fg="white")
        btn_apagar_tabela.pack(side="left", padx=5)

        frame_entrada = tk.Frame(self, bg="#f0f0f0")
        frame_entrada.pack(pady=10)

        tk.Label(frame_entrada, text="Nome:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome = tk.Entry(frame_entrada, width=15)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_entrada, text="Custo:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)
        self.entry_custo = tk.Entry(frame_entrada, width=10)
        self.entry_custo.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_entrada, text="Quantidade:", bg="#f0f0f0").grid(row=0, column=4, padx=5, pady=5)
        self.entry_quantidade = tk.Entry(frame_entrada, width=10)
        self.entry_quantidade.grid(row=0, column=5, padx=5, pady=5)

        btn_inserir = tk.Button(frame_entrada, text="Inserir", command=self.inserir_item, bg="#4CAF50", fg="white", padx=10)
        btn_inserir.grid(row=0, column=6, padx=5, pady=5)

        self.tree = ttk.Treeview(self, columns=("Nome", "Custo", "Quantidade", "Total"),
                                 show="headings", selectmode="browse")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Custo", text="Custo")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Total", text="Total")
        self.tree.column("Nome", width=200, anchor="center")
        self.tree.column("Custo", width=100, anchor="center")
        self.tree.column("Quantidade", width=100, anchor="center")
        self.tree.column("Total", width=100, anchor="center")
        self.tree.pack(pady=10, fill="both", expand=True)

        frame_botoes = tk.Frame(self, bg="#f0f0f0")
        frame_botoes.pack(pady=5)

        btn_remover = tk.Button(frame_botoes, text="Remover Item", command=self.remover_item, bg="#F44336", fg="white", padx=10)
        btn_remover.pack(side="left", padx=10)

        btn_editar = tk.Button(frame_botoes, text="Editar Item", command=self.editar_item, bg="#FF9800", fg="white", padx=10)
        btn_editar.pack(side="left", padx=10)

        self.label_total = tk.Label(self, text="Total Geral: R$ 0.00", font=("Arial", 12), bg="#f0f0f0")
        self.label_total.pack(pady=10)

        self.atualizar_exibicao()

    def salvar_config(self):
        config = {"data_folder": self.data_folder} if self.data_folder else {}
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            messagebox.showerror("Erro ao Salvar Configuração", f"Não foi possível salvar a configuração:\n{e}")

    def carregar_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                self.data_folder = config.get("data_folder")
            except Exception as e:
                messagebox.showerror("Erro ao Carregar Configuração", f"Não foi possível carregar a configuração:\n{e}")

    def get_label_pasta(self):
        return f"Pasta: {self.data_folder}" if self.data_folder else "Pasta não selecionada"

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta para armazenar os dados")
        if pasta:
            self.data_folder = pasta
            self.label_pasta.config(text=self.get_label_pasta())
            self.salvar_config()
            self.carregar_dados()

    def salvar_dados(self):
        if not self.data_folder:
            return
        dados = {
            "tabelas": self.tabelas,
            "tabela_atual": self.tabela_atual
        }
        file_path = os.path.join(self.data_folder, "dados.json")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4)
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar os dados:\n{e}")

    def carregar_dados(self):
        if not self.data_folder:
            return
        file_path = os.path.join(self.data_folder, "dados.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                self.tabelas = dados.get("tabelas", {})
                for tabela in self.tabelas.values():
                    for item in tabela["itens"]:
                        if "cor" not in item:
                            item["cor"] = ""
                self.tabela_atual = dados.get("tabela_atual", next(iter(self.tabelas), "Default"))
                if hasattr(self, "combobox_tabelas"):
                    self.combobox_tabelas['values'] = list(self.tabelas.keys())
                    self.combobox_tabelas.set(self.tabela_atual)
                self.atualizar_exibicao()
            except Exception as e:
                messagebox.showerror("Erro ao Carregar", f"Não foi possível carregar os dados:\n{e}")

    def criar_tabela(self, nome):
        if nome in self.tabelas:
            messagebox.showerror("Erro", f"A tabela '{nome}' já existe.")
            return
        self.tabelas[nome] = {"itens": [], "total": 0.0}

    def nova_tabela(self):
        nome = simpledialog.askstring("Nova Tabela", "Informe o nome da nova tabela:")
        if nome:
            nome = nome.strip()
            if nome == "":
                messagebox.showerror("Erro", "O nome não pode ser vazio.")
                return
            if nome in self.tabelas:
                messagebox.showerror("Erro", "Já existe uma tabela com esse nome.")
                return
            self.criar_tabela(nome)
            self.combobox_tabelas['values'] = list(self.tabelas.keys())
            self.combobox_tabelas.set(nome)
            self.tabela_atual = nome
            self.atualizar_exibicao()
            self.salvar_dados()

    def selecionar_tabela(self, event=None):
        tabela = self.combobox_tabelas.get()
        if tabela in self.tabelas:
            self.tabela_atual = tabela
            self.atualizar_exibicao()
            self.salvar_dados()

    def apagar_tabela(self):
        confirma = tk.Toplevel(self)
        confirma.title("Confirmar Exclusão")
        confirma.geometry("300x120")
        confirma.resizable(False, False)
        confirma.grab_set()

        tk.Label(confirma, text=f"Tem certeza que deseja apagar a tabela '{self.tabela_atual}'?",
                 wraplength=280, justify="center").pack(pady=10)

        def confirmar():
            del self.tabelas[self.tabela_atual]
            if not self.tabelas:
                self.criar_tabela("Default")
                self.tabela_atual = "Default"
            else:
                self.tabela_atual = next(iter(self.tabelas))
            self.combobox_tabelas['values'] = list(self.tabelas.keys())
            self.combobox_tabelas.set(self.tabela_atual)
            self.atualizar_exibicao()
            self.salvar_dados()
            confirma.destroy()

        def cancelar():
            confirma.destroy()

        frame_botoes_confirma = tk.Frame(confirma)
        frame_botoes_confirma.pack(pady=10)
        btn_confirmar = tk.Button(frame_botoes_confirma, text="Confirmar", command=confirmar,
                                  bg="#349133", fg="white", width=10)
        btn_confirmar.pack(side="left", padx=5)
        btn_cancelar = tk.Button(frame_botoes_confirma, text="Cancelar", command=cancelar,
                                 bg="#F44336", fg="white", width=10)
        btn_cancelar.pack(side="left", padx=5)

    def atualizar_exibicao(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        itens = self.tabelas[self.tabela_atual]["itens"]
        cores_presentes = set()
        for idx, dado in enumerate(itens):
            cor = dado.get("cor", "")
            tags = (cor,) if cor else ()
            self.tree.insert("", "end", iid=str(idx),
                             values=(dado["nome"], f'{dado["custo"]:.2f}',
                                     f'{dado["quantidade"]:.2f}', f'{dado["total"]:.2f}'),
                             tags=tags)
            if cor:
                cores_presentes.add(cor)
        for cor in cores_presentes:
            self.tree.tag_configure(cor, background=cor)
        total = self.tabelas[self.tabela_atual]["total"]
        self.label_total.config(text=f"Total Geral: R$ {total:.2f}")

    def inserir_item(self):
        nome = self.entry_nome.get().strip()
        custo_str = self.entry_custo.get().strip()
        quantidade_str = self.entry_quantidade.get().strip()

        if not nome or not custo_str or not quantidade_str:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        try:
            custo = float(custo_str)
            quantidade = float(quantidade_str)
        except ValueError:
            messagebox.showerror("Erro", "Custo e Quantidade devem ser números.")
            return

        total = custo * quantidade
        novo_item = {
            "nome": nome,
            "custo": custo,
            "quantidade": quantidade,
            "total": total,
            "cor": ""
        }

        self.tabelas[self.tabela_atual]["itens"].append(novo_item)
        self.tabelas[self.tabela_atual]["total"] += total

        self.atualizar_exibicao()
        self.salvar_dados()

        self.entry_nome.delete(0, tk.END)
        self.entry_custo.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.entry_nome.focus()

    def remover_item(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um item para remover.")
            return
        indice = int(selecionado[0])
        item = self.tabelas[self.tabela_atual]["itens"].pop(indice)
        self.tabelas[self.tabela_atual]["total"] -= item["total"]
        self.atualizar_exibicao()
        self.salvar_dados()

    def editar_item(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um item para editar.")
            return
        indice = int(selecionado[0])
        item = self.tabelas[self.tabela_atual]["itens"][indice]

        editor = tk.Toplevel(self)
        editor.title("Editar Item")
        editor.grab_set()

        tk.Label(editor, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        entry_nome = tk.Entry(editor, width=15)
        entry_nome.grid(row=0, column=1, padx=5, pady=5)
        entry_nome.insert(0, item["nome"])

        tk.Label(editor, text="Custo:").grid(row=1, column=0, padx=5, pady=5)
        entry_custo = tk.Entry(editor, width=10)
        entry_custo.grid(row=1, column=1, padx=5, pady=5)
        entry_custo.insert(0, f'{item["custo"]:.2f}')

        tk.Label(editor, text="Quantidade:").grid(row=2, column=0, padx=5, pady=5)
        entry_quantidade = tk.Entry(editor, width=10)
        entry_quantidade.grid(row=2, column=1, padx=5, pady=5)
        entry_quantidade.insert(0, f'{item["quantidade"]:.2f}')

        # Corrigir a cor inicial
        cor_inicial = item.get("cor", "")
        tk.Label(editor, text="Cor de Fundo:").grid(row=3, column=0, padx=5, pady=5)
        preview_cor = tk.Label(editor, width=5, bg=cor_inicial if cor_inicial else "white")
        preview_cor.grid(row=3, column=1, padx=5, pady=5)
        btn_escolher_cor = tk.Button(editor, text="Escolher", command=lambda: escolher_cor())
        btn_escolher_cor.grid(row=3, column=2, padx=5, pady=5)

        cor_atual = cor_inicial  # Manter o valor original

        def escolher_cor():
            nonlocal cor_atual
            cor = colorchooser.askcolor()
            if cor and cor[1] is not None:
                cor_atual = cor[1]
                preview_cor.config(bg=cor_atual)
            else:
                # Se o usuário cancelar, mantemos a cor atual
                pass

        def salvar_edicao():
            novo_nome = entry_nome.get().strip()
            custo_str = entry_custo.get().strip()
            quantidade_str = entry_quantidade.get().strip()

            if not novo_nome or not custo_str or not quantidade_str:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
                return

            try:
                novo_custo = float(custo_str)
                nova_quantidade = float(quantidade_str)
            except ValueError:
                messagebox.showerror("Erro", "Custo e Quantidade devem ser números.")
                return

            novo_total = novo_custo * nova_quantidade

            self.tabelas[self.tabela_atual]["total"] -= item["total"]
            self.tabelas[self.tabela_atual]["total"] += novo_total

            item["nome"] = novo_nome
            item["custo"] = novo_custo
            item["quantidade"] = nova_quantidade
            item["total"] = novo_total
            item["cor"] = cor_atual if cor_atual else ""  # Salvar vazio se não houver cor

            self.atualizar_exibicao()
            self.salvar_dados()
            editor.destroy()

        btn_salvar = tk.Button(editor, text="Salvar", command=salvar_edicao, bg="#4CAF50", fg="white")
        btn_salvar.grid(row=4, column=0, columnspan=3, pady=10)

if __name__ == "__main__":
    app = TabelaCustosApp()
    app.mainloop()