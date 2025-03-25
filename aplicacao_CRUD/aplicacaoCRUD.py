import tkinter as tk
from tkinter import ttk
import crud as crud

class PrincipalBD:
    def __init__(self, win):
        self.objBD = crud.AppBD()  # Instância do CRUD para banco de dados

        # Labels
        self.lbCodigo = tk.Label(win, text='Código do Produto:')
        self.lblNome = tk.Label(win, text='Nome do Produto:')
        self.lblPreco = tk.Label(win, text='Preço:')

        # Campos de entrada
        self.txtCodigo = tk.Entry(bd=3)
        self.txtNome = tk.Entry()
        self.txtPreco = tk.Entry()

        # Botões
        self.btnCadastrar = tk.Button(win, text='Cadastrar', command=self.fCadastrarProduto)
        self.btnAtualizar = tk.Button(win, text='Atualizar', command=self.fAtualizarProduto)
        self.btnExcluir = tk.Button(win, text='Excluir', command=self.fExcluirProduto)
        self.btnLimpar = tk.Button(win, text='Limpar', command=self.fLimparTela)

        # TreeView e Scrollbar
        self.dadosColunas = ("Código", "Nome", "Preço")
        self.treeProdutos = ttk.Treeview(win, columns=self.dadosColunas, show="headings", selectmode='browse')
        self.verscrlbar = ttk.Scrollbar(win, orient="vertical", command=self.treeProdutos.yview)
        self.treeProdutos.configure(yscrollcommand=self.verscrlbar.set)

        # Configurar colunas do TreeView
        for col in self.dadosColunas:
            self.treeProdutos.heading(col, text=col)
            self.treeProdutos.column(col, minwidth=0, width=100)

        # Eventos
        self.treeProdutos.bind("<<TreeviewSelect>>", self.apresentarRegistrosSelecionados)

        # Layout
        self.lbCodigo.place(x=100, y=50)
        self.txtCodigo.place(x=250, y=50)
        self.lblNome.place(x=100, y=100)
        self.txtNome.place(x=250, y=100)
        self.lblPreco.place(x=100, y=150)
        self.txtPreco.place(x=250, y=150)
        self.btnCadastrar.place(x=100, y=200)
        self.btnAtualizar.place(x=200, y=200)
        self.btnExcluir.place(x=300, y=200)
        self.btnLimpar.place(x=400, y=200)
                   
        self.treeProdutos.place(x=100, y=300)
        self.verscrlbar.place(x=605, y=300, height=225)        
        self.carregarDadosIniciais()
#-----------------------------------------------------------------------------
    def apresentarRegistrosSelecionados(self, event):  
        self.fLimparTela()  
        for selection in self.treeProdutos.selection():  
            item = self.treeProdutos.item(selection)  
            codigo,nome,preco = item["values"][0:3]  
            self.txtCodigo.insert(0, codigo)  
            self.txtNome.insert(0, nome)  
            self.txtPreco.insert(0, preco)  
#-----------------------------------------------------------------------------
    def carregarDadosIniciais(self):
        try:
          self.id = 0
          self.iid = 0          
          registros=self.objBD.selecionarDados()
          print("************ dados dsponíveis no BD ***********")        
          for item in registros:
              codigo=item[0]
              nome=item[1]
              preco=item[2]
              print("Código = ", codigo)
              print("Nome = ", nome)
              print("Preço  = ", preco, "\n")
                        
              self.treeProdutos.insert('', 'end',
                                   iid=self.iid,                                   
                                   values=(codigo,
                                           nome,
                                           preco))                        
              self.iid = self.iid + 1
              self.id = self.id + 1
          print('Dados da Base')        
        except:
          print('Ainda não existem dados para carregar')            
#-----------------------------------------------------------------------------
#LerDados da Tela
#-----------------------------------------------------------------------------           
    def fLerCampos(self):
        try:
          print("************ dados dsponíveis ***********") 
          codigo = int(self.txtCodigo.get())
          print('codigo', codigo)
          nome=self.txtNome.get()
          print('nome', nome)
          preco=float(self.txtPreco.get())          
          print('preco', preco)
          print('Leitura dos Dados com Sucesso!')        
        except:
          print('Não foi possível ler os dados.')
        return codigo, nome, preco
#-----------------------------------------------------------------------------
#Cadastrar Produto
#-----------------------------------------------------------------------------           
    def fCadastrarProduto(self):
        try:
          print("************ dados dsponíveis ***********") 
          codigo, nome, preco= self.fLerCampos()                    
          self.objBD.inserirDados(codigo, nome, preco)                    
          self.treeProdutos.insert('', 'end',
                                iid=self.iid,                                   
                                values=(codigo,
                                        nome,
                                        preco))                        
          self.iid = self.iid + 1
          self.id = self.id + 1
          self.fLimparTela()
          print('Produto Cadastrado com Sucesso!')        
        except:
          print('Não foi possível fazer o cadastro.')
#-----------------------------------------------------------------------------
#Atualizar Produto
#-----------------------------------------------------------------------------           
    def fAtualizarProduto(self):
        try:
          print("************ dados dsponíveis ***********")        
          codigo, nome, preco= self.fLerCampos()
          self.objBD.atualizarDados(codigo, nome, preco)          
          #recarregar dados na tela
          self.treeProdutos.delete(*self.treeProdutos.get_children()) 
          self.carregarDadosIniciais()
          self.fLimparTela()
          print('Produto Atualizado com Sucesso!')        
        except:
          print('Não foi possível fazer a atualização.')
#-----------------------------------------------------------------------------
#Excluir Produto
#-----------------------------------------------------------------------------                  
    def fExcluirProduto(self):
        try:
          print("************ dados dsponíveis ***********")        
          codigo, nome, preco= self.fLerCampos()
          self.objBD.excluirDados(codigo)          
          #recarregar dados na tela
          self.treeProdutos.delete(*self.treeProdutos.get_children()) 
          self.carregarDadosIniciais()
          self.fLimparTela()
          print('Produto Excluído com Sucesso!')        
        except:
          print('Não foi possível fazer a exclusão do produto.')
#-----------------------------------------------------------------------------
#Limpar Tela
#-----------------------------------------------------------------------------                 
    def fLimparTela(self):
        try:
          print("************ dados dsponíveis ***********")        
          self.txtCodigo.delete(0, tk.END)
          self.txtNome.delete(0, tk.END)
          self.txtPreco.delete(0, tk.END)
          print('Campos Limpos!')        
        except:
          print('Não foi possível limpar os campos.')
#-----------------------------------------------------------------------------
#Programa Principal
#-----------------------------------------------------------------------------          
janela=tk.Tk()
principal=PrincipalBD(janela)
janela.title('Bem Vindo a Aplicação de Banco de Dados')
janela.geometry("720x600+10+10")
janela.mainloop()
#-----------------------------------------------------------------------------




