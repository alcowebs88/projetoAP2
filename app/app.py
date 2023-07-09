from tkinter import *
from tkinter import ttk,messagebox
from functools import partial
import sqlite3
from PIL import Image,ImageTk


def img(url,*tam):
    i = Image.open(url)
    i = i.resize(tam)
    return ImageTk.PhotoImage(i)
	


def con():
    c = sqlite3.connect('agenda.db')
    cur = c.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS contatos (
    id       INTEGER PRIMARY KEY AUTOINCREMENT
                     NOT NULL,
    nome     TEXT    NOT NULL,
    email    TEXT,
    telefone TEXT    NOT NULL
);''')
    c.commit()
    return c


 
global tree

def limpa_form():
    e_nome.delete(0,'end')
    e_email.delete(0,'end')
    e_telefone.delete(0,'end') 

def update(i):
    p_nome = e_nome.get()
    p_email = e_email.get()
    p_telefone = e_telefone.get()
    sql = f'UPDATE contatos SET nome="{p_nome}",email="{p_email}",telefone="{p_telefone}" WHERE id={i}'
    print(sql)
    with con() as c:
        cur = c.cursor()
        cur.execute(sql)
        c.commit()
        treeview()
    limpa_form()
    global atu
    atu.destroy()


    
def atualizar():
    
    p = tree.focus()
    if p:
        pos = tree.item(p)['values']
        i,nome,email,telefone = pos
        e_nome.insert('end',nome)
        e_email.insert('end',email)
        e_telefone.insert('end',telefone)

        global atu
        atu  = Button(app,text='Aplicar Mudança',command=partial(update,i))
        atu.place(x=100,y=290)
    else:
        messagebox.showwarning(title='Atenção',message='Nenhum Registro Selecionado')


def active_b_excluir(event):
    b_deletar['state']='normal'

def delete():
    p = tree.focus()
    pos = tree.item(p)
    sql = f'delete from contatos where id ={pos["values"][0]}'
    c = con()
    cur = c.cursor()
    ex = messagebox.askokcancel(title='Confirme',message='Deseja Remover Esse Registro')
    if ex:
        cur.execute(sql)
        c.commit()
        treeview()
    else:
        pass
    b_deletar['state']='disabled'
    
def select(): 
    dados = []
    sql = 'select * from contatos'
    c = con()
    cur = c.cursor()
    cur.execute(sql)
    for i in cur.fetchall():
        dados.append(i)
    return dados


def insert():
    c = con()
    nome = e_nome.get()
    email = e_email.get()
    telefone = e_telefone.get()
    if nome != '' and telefone != '':
        
        sql = f'insert into contatos (nome,email,telefone) values("{nome}","{email}","{telefone}")'
 
        result = c.cursor()
        result.execute(sql)
        c.commit()
        for i in frame_direita.winfo_children():
            i.destroy()
        treeview()

        limpa_form() 
        e_nome.focus()
        

    else:
        messagebox.showwarning(title='Atenção',message='Preencha Todos Os Campos')

app = Tk()
app.iconbitmap('icon.ico')
app.title('Agenda')
app.geometry('1010x453')
app.resizable(0,0)


frame_cima = Frame(app,width=310,bg='green',height='50',relief='flat')
frame_cima.grid(row=0,column=0)



frame_baixo = Frame(app,width=310,bg='white',height='403',relief='flat')
frame_baixo.grid(row=1,column=0,padx=0,pady=1,sticky=NSEW)


frame_direita = Frame(app,width=588,bg='white',height='403',relief='flat')
frame_direita.grid(row=0,column=1,rowspan=2,padx=1,pady=0,sticky=NSEW)

app_nome = Label(frame_cima,font=('ivy 13 bold'),text='Agenda Telefonica',bg='green',fg='white')
app_nome.place(x=50,y=20)

img_logo = img('agenda.png',40,40)
logo = Label(image=img_logo)
logo.place(x=2,y=3)


l_nome = Label(frame_baixo,text='Nome *',anchor=NW,font=('ivy 10 bold'))
l_nome.place(x=10,y=10)

e_nome = Entry(frame_baixo,width=45,justify='left',relief='solid')
e_nome.place(x=15,y=40)


l_email = Label(frame_baixo,text='Email *',anchor=NW,font=('ivy 10 bold'))
l_email.place(x=10,y=70)

e_email = Entry(frame_baixo,width=45,justify='left',relief='solid')
e_email.place(x=15,y=100)


l_telefone = Label(frame_baixo,text='Telefone *',anchor=NW,font=('ivy 10 bold'))
l_telefone.place(x=10,y=130)

e_telefone = Entry(frame_baixo,width=45,justify='left',relief='solid')
e_telefone.place(x=15,y=160)


b_inserir = Button(frame_baixo,command=insert,bg='blue',fg='white',text='Inserir',width=10,font=('Ivy 9 bold'),relief='raised')
b_inserir.place(x=20,y=200)

b_atualizar = Button(frame_baixo,command=atualizar,bg='green',fg='white',text='Atualizar',width=10,font=('Ivy 9 bold'),relief='raised')
b_atualizar.place(x=105,y=200)

b_deletar = Button(frame_baixo,command=delete,bg='red',fg='white',text='Deletar',width=10,font=('Ivy 9 bold'),relief='raised',state=DISABLED)
b_deletar.place(x=190,y=200)


def treeview():
    global tree
    user = select()
    e_nome.focus()
    cabeca = ['Id','Nome','Email','Telefone']
    tree = ttk.Treeview(frame_direita,columns=cabeca,show='headings')
   
    tree.heading('Id',text='Id')
    tree.heading('Nome',text='Nome')
    tree.heading('Email',text='Email')
    tree.heading('Telefone',text='Telefone')
    
    tree.column('Id',width='80')

    tree.column('Nome',width='300')

    tree.column('Telefone',width='100')


    tree.column('Email',width='200')


    vsb = ttk.Scrollbar(frame_direita,orient='vertical',command=tree.yview)
    hsb = ttk.Scrollbar(frame_direita,orient='horizontal',command=tree.xview)

    tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)

    tree.grid(column=0,row=0,sticky='nsew')
    vsb.grid(column=1,row=0,sticky='ns')
    hsb.grid(column=0,row=1,sticky='ew')
    frame_direita.grid_rowconfigure(0,weight=12)
    
    for i in user:
        tree.insert('', END,values=i)
    


    tree.bind('<<TreeviewSelect>>',active_b_excluir)



treeview()



app.mainloop()


