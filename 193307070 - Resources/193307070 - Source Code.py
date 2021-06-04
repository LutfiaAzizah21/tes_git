from tkinter import *
# import io
from tkcalendar import Calendar, DateEntry
import time
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import pymysql

class AssetManagement:
    def __init__(self,parent, title):
        self.parent = parent
        self.parent.title(title)
        self.layoutKomponen()

    def layoutKomponen(self):
        mainfr = Frame(self.parent, bg="white")
        mainfr.pack(fill=BOTH, expand=1)

        frame1 = Frame(mainfr, width=1156, height=130, bg="#AE1A1A", highlightbackground="black", highlightthicknes=1)
        frame1.place(x=199, y=10)
        frame1.propagate(False)
        Label(frame1, font= "Arial 30 normal", fg="white", text = "  MANAJEMEN GUDANG SR12", bg = "#AE1A1A").place(relx=.5, rely=.3, anchor="center")
        Label(frame1, font= "Arial 20 italic", fg="white", text = "Beauty is not A Dream, Bringing Back Your Beauty", bg = "#AE1A1A").place(relx=.245, rely=.45)

        frame2 = Frame(mainfr, width=188, height=766, bg="#FDF4F4", highlightbackground="black", highlightthicknes=1)
        frame2.place(x=12, y=10)
        frame2.propagate(False)

        load = Image.open("red.png")
        load = load.resize((95, 95), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Button(frame2, image=render, bd=0, command=self.home, bg ="#FDF4F4")
        img.image = render
        img.place(relx=.5, y=55, anchor="center")

        load = Image.open("stock.png")
        load = load.resize((35, 35), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        self.img = Button(frame2, image=render, bd=0, command=self.databarang, bg ="#FDF4F4", fg = "#1aa333")
        self.img.image = render
        self.img.place(relx=.15, y=147, anchor="center")
        Button(frame2, command=self.databarang, font= "Arial 13 normal", relief=FLAT,
        text = "Data Barang", bg = "#FDF4F4").place(relx=.6, y=147, anchor="center")

        load = Image.open("export.png")
        load = load.resize((35, 35), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        self.img1 = Button(frame2, image=render, bd=0,bg ="#FDF4F4", command=self.datakeluar)
        self.img1.image = render
        self.img1.place(relx=.15, y=220, anchor="center")
        Button(frame2, font= "Arial 13 normal", command=self.datakeluar, text = "Barang Keluar", relief=FLAT,
        bg = "#FDF4F4").place(relx=.6, y=220, anchor="center")

        load = Image.open("masuk.png")
        load = load.resize((35, 35), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Button(frame2, image=render, command=self.datamasuk, bd=0,bg ="#FDF4F4")
        img.image = render
        img.place(relx=.15, y=293, anchor="center")
        Button(frame2, font= "Arial 13 normal", command=self.datamasuk, text = "Barang Masuk", relief=FLAT,
         bg = "#FDF4F4").place(relx=.6, y=293, anchor="center")

        #frame home
        self.frame3 = Frame(mainfr, width=1156, height=766, bg="#FDF4F4", 
                        highlightbackground="black", highlightthicknes=1)
        self.frame3.place(x=199, y=119)
        self.frame3.propagate(False)

        #frame content
        self.framedata = Frame(self.frame3, width=1125, height=100, bg="white",
                        highlightbackground="black", highlightthicknes=1)
        # self.framedata.place(x=10, y=10)
        # self.framedata.propagate(False)

        #Menu Data Barang
        self.var_IDbarang=StringVar()
        self.var_namabarang=StringVar()
        self.var_kategori=StringVar()
        self.var_harga=StringVar()
        self.var_kuantitas=StringVar()
        self.search_by=StringVar()
        self.search_txt=StringVar()

        self.btn11 = Button(self.framedata, bg="white", text="Daftar Barang",command=self.daftar, font="Arial 12 bold", fg='black', relief=FLAT)
        self.btn11.place(relx=.075, rely=.65, anchor="center")

        self.btn12 = Button(self.framedata, bg="white", text="Kelola Data", command=self.tambah, font="Arial 12 bold", fg='black',relief=FLAT)
        self.btn12.place(relx=.2, rely=.65, anchor="center")
        
        self.lbl_search= Label(self.framedata, text="Search By", font="Arial 12 bold", fg='black', bg="#ffffff")
        self.lbl_search.place(relx=.45, rely=.65, anchor="center")

        self.combo_search = ttk.Combobox(self.framedata,textvariable=self.search_by, width = 15, font=("Arial", 12), state = "readonly")
        self.combo_search['values'] = ("idBarang", "namaBarang", "kategori", "harga")
        self.combo_search.place(relx=.575, rely=.65, anchor="center")

        self.txt_search = Entry(self.framedata, textvariable=self.search_txt, width = 15,font=("Arial", 12), bd = 2, bg="#AFEEEE")
        self.txt_search.place(relx=.725, rely=.65, anchor="center")

        load = Image.open("search.png")
        load = load.resize((25, 25), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        self.img = Button(self.framedata, image=render, bd=0, command=self.search_data, bg ="white", fg = "#1aa333")
        self.img.image = render
        self.img.place(relx=.81, rely=.65, anchor="center")

        self.btnShowall = Button(self.framedata, command=self.fetch_data, text="Show All", bg="#42ADF3", fg="white", font="Arial 12 bold")
        self.btnShowall.place(relx=.875, rely=.65, anchor="center")

        # FRAME DAFTAR
        self.frameDaftar = Frame(self.frame3, width=1125, height=450, bg="white", highlightbackground="black", highlightthicknes=1)

        self.table = Frame (self.frameDaftar, bd=4, relief=RIDGE, bg="white")
        self.table.place(relx=.05, rely=.1, width=1000, height=350)
        scrolly= Scrollbar(self.table, orient=VERTICAL)
        scrollx= Scrollbar(self.table, orient=HORIZONTAL)
        self.table_lap=ttk.Treeview(self.table,columns=("ID","namabarang", "kategori", "harga","stok","deskripsi", "aksi"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.pack(side=BOTTOM,fill=X)
        scrollx.config(command=self.table_lap.xview)
        scrolly.config(command=self.table_lap.yview)

        self.table_lap.heading("ID",text="ID")
        self.table_lap.heading("namabarang",text="NAMA BARANG")
        self.table_lap.heading("kategori",text="KATEGORI")
        self.table_lap.heading("harga",text="HARGA")
        self.table_lap.heading("stok",text="STOK")
        self.table_lap.heading("deskripsi",text="DESKRIPSI")

        self.table_lap['show']='headings'
        self.table_lap.column("ID",width=70)
        self.table_lap.column("namabarang",width=170)
        self.table_lap.column("kategori",width=150)
        self.table_lap.column("harga",width=150)
        self.table_lap.column("stok",width=100)
        self.table_lap.column("deskripsi",width=340)
        self.table_lap.pack(fill=BOTH,expand=3)
        self.table_lap.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()


        # FRAME TAMBAH
        self.frameTambah = Frame(self.frame3, width=1125, height=450, bg="white", highlightbackground="black", highlightthicknes=1)

        lblID = Label(self.frameTambah, text="ID", font="Arial 12 bold", fg='black', bg="white")
        lblID.place(relx=.1, rely=.1)   
        self.entID = Entry(self.frameTambah, textvariable=self.var_IDbarang, font="Arial 12", fg='black', bg="white", bd=3)
        self.entID.place(relx=.3, rely=.1)    

        lblNamaBrg = Label(self.frameTambah, text="Nama Barang", font="Arial 12 bold", fg='black', bg="white")
        lblNamaBrg.place(relx=.1, rely=.2) 
        self.entNamaBrg = Entry(self.frameTambah, textvariable=self.var_namabarang, font="Arial 12", fg='black', bg="white", bd=3)
        self.entNamaBrg.place(relx=.3, rely=.2)     

        lblKategori = Label(self.frameTambah, text="Kategori", font="Arial 12 bold", fg='black', bg="white")
        lblKategori.place(relx=.1, rely=.3)  
        self.entKategori = Entry(self.frameTambah, textvariable=self.var_kategori,  font="Arial 12", fg='black', bg="white", bd=3)
        self.entKategori.place(relx=.3, rely=.3)    

        lblHarga = Label(self.frameTambah, text="Harga", font="Arial 12 bold", fg='black', bg="white")
        lblHarga.place(relx=.1, rely=.4)  
        self.entHarga = Entry(self.frameTambah, textvariable=self.var_harga, font="Arial 12", fg='black', bg="white", bd=3)
        self.entHarga.place(relx=.3, rely=.4)   

        lblKuantitas = Label(self.frameTambah, text="Stok", font="Arial 12 bold", fg='black', bg="white")
        lblKuantitas.place(relx=.1, rely=.5)
        self.entKuantitas = Entry(self.frameTambah, textvariable=self.var_kuantitas, font="Arial 12", fg='black', bg="white", bd=3)
        self.entKuantitas.place(relx=.3, rely=.5)  

        lblDeskripsi = Label(self.frameTambah, text="Deskripsi", font="Arial 12 bold", fg='black', bg="white")
        lblDeskripsi.place(relx=.1, rely=.6)
        self.entDeskripsi = Text(self.frameTambah, font="Arial 12", fg='black', bg="white", bd=3, height=5)
        self.entDeskripsi.place(relx=.3, rely=.6)   

        self.btnSave = Button(self.frameTambah,  command=self.save_data, font="Arial 12 bold", width=8, text="SAVE", bg="#915FE6", fg="white")
        self.btnSave.place(relx=.3, rely=.875)

        self.btnCancel = Button(self.frameTambah,  command=self.clear, font="Arial 12 bold", width=8, text="CLEAR", bg="#EF4747", fg="white")
        self.btnCancel.place(relx=.4, rely=.875)

        self.btnEdit = Button(self.frameTambah, command=self.update_data,  font="Arial 12 bold", width=8, text="EDIT", bg="#25F848", fg="white")
        self.btnEdit.place(relx=.5, rely=.875)

        self.btnDel = Button(self.frameTambah, command=self.delete_data,  font="Arial 12 bold", width=8, text="DELETE", bg="grey", fg="white")
        self.btnDel.place(relx=.6, rely=.875)

        # Menu Barang Keluar
        self.var_IDbarang2=StringVar()
        self.var_namabarang2=StringVar()
        self.var_tanggal2=StringVar()
        self.var_tujuan=StringVar()
        self.var_kuantitas2=StringVar()
        self.search_by2=StringVar()
        self.search_txt2=StringVar()

        self.framekeluar = Frame(self.frame3, width=1125, height=100, bg="white", highlightbackground="black", highlightthicknes=1)

        self.btn21 = Button(self.framekeluar, bg="white", command=self.daftar2,text="Daftar Barang Keluar", font="Arial 12 bold", fg='black', relief=FLAT)
        self.btn21.place(relx=.1, rely=.65, anchor="center")

        self.btn22 = Button(self.framekeluar, bg="white", command=self.tambah2, text="Kelola data", font="Arial 12 bold", fg='black',relief=FLAT)
        self.btn22.place(relx=.25, rely=.65, anchor="center")

        self.lbl_search= Label(self.framekeluar, text="Search By", font="Arial 12 bold", fg='black', bg="#ffffff")
        self.lbl_search.place(relx=.45, rely=.65, anchor="center")

        self.combo_search = ttk.Combobox(self.framekeluar, textvariable=self.search_by2, width = 15, font=("Arial", 12), state = "readonly")
        self.combo_search['values'] = ("idPengiriman", "namaBarang", "tglPengiriman", "tujuan")
        self.combo_search.place(relx=.575, rely=.65, anchor="center")

        self.txt_search = Entry(self.framekeluar, textvariable=self.search_txt2, width = 15,font=("Arial", 12), bd = 2, bg="#AFEEEE")
        self.txt_search.place(relx=.725, rely=.65, anchor="center")

        load = Image.open("search.png")
        load = load.resize((25, 25), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        self.img = Button(self.framekeluar, command=self.search_data2, image=render, bd=0,  bg ="white", fg = "#1aa333")
        self.img.image = render
        self.img.place(relx=.81, rely=.65, anchor="center")

        self.btnShowall = Button(self.framekeluar, command=self.fetch_data2,  text="Show All", bg="#42ADF3", fg="white", font="Arial 12 bold")
        self.btnShowall.place(relx=.875, rely=.65, anchor="center")

        # self.frame6 = Frame(self.frame3, width=1125, height=450, bg="white", highlightbackground="black", highlightthicknes=1)
        
        # FRAME DAFTAR2
        self.frameDaftar2 = Frame(self.frame3, width=1125, height=450, bg="white", highlightbackground="black", highlightthicknes=1)

        self.table = Frame (self.frameDaftar2, bd=4, relief=RIDGE, bg="white")
        self.table.place(relx=.05, rely=.1, width=1000, height=350)
        scrolly= Scrollbar(self.table, orient=VERTICAL)
        scrollx= Scrollbar(self.table, orient=HORIZONTAL)
        self.table_lap2=ttk.Treeview(self.table,columns=("ID","namabarang", "tanggal", "tujuan","kuantitas","deskripsi", "aksi"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.pack(side=BOTTOM,fill=X)
        scrollx.config(command=self.table_lap2.xview)
        scrolly.config(command=self.table_lap2.yview)

        self.table_lap2.heading("ID",text="ID")
        self.table_lap2.heading("namabarang",text="NAMA BARANG")
        self.table_lap2.heading("tanggal",text="TANGGAL")
        self.table_lap2.heading("tujuan",text="TUJUAN")
        self.table_lap2.heading("kuantitas",text="KUANTITAS")
        self.table_lap2.heading("deskripsi",text="DESKRIPSI")

        self.table_lap2['show']='headings'
        self.table_lap2.column("ID",width=70)
        self.table_lap2.column("namabarang",width=170)
        self.table_lap2.column("tanggal",width=150)
        self.table_lap2.column("tujuan",width=150)
        self.table_lap2.column("kuantitas",width=100)
        self.table_lap2.column("deskripsi",width=340)
        self.table_lap2.pack(fill=BOTH,expand=1)
        self.table_lap2.bind("<ButtonRelease-1>",self.get_cursor2)
        self.fetch_data2()

        # FRAME TAMBAH2
        self.frameTambah2 = Frame(self.frame3, width=1125, height=450, bg="white", highlightbackground="black", highlightthicknes=1)

        lblID = Label(self.frameTambah2, text="ID", font="Arial 12 bold", fg='black', bg="white")
        lblID.place(relx=.1, rely=.1)   
        self.entID = Entry(self.frameTambah2, textvariable=self.var_IDbarang2, font="Arial 12", fg='black', bg="white", bd=3)
        self.entID.place(relx=.3, rely=.1)    

        lblNamaBrg = Label(self.frameTambah2, text="Nama Barang", font="Arial 12 bold", fg='black', bg="white")
        lblNamaBrg.place(relx=.1, rely=.2) 
        self.entNamaBrg = Entry(self.frameTambah2,textvariable=self.var_namabarang2,  font="Arial 12", fg='black', bg="white", bd=3)
        self.entNamaBrg.place(relx=.3, rely=.2)     

        lblTgl = Label(self.frameTambah2, text="Tanggal", font="Arial 12 bold", fg='black', bg="white")
        lblTgl.place(relx=.1, rely=.3)  
        self.entTgl = DateEntry(self.frameTambah2,textvariable=self.var_tanggal2,state='readonly',date_pattern='y-mm-dd',width=24, background='#ffffff',foreground='black',font="Arial 10", borderwidth=4,Calendar =2021)
        self.entTgl.place(relx=.3, rely=.3)    

        lblTujuan = Label(self.frameTambah2, text="Tujuan", font="Arial 12 bold", fg='black', bg="white")
        lblTujuan.place(relx=.1, rely=.4)  
        self.entTujuan = Entry(self.frameTambah2, textvariable=self.var_tujuan, font="Arial 12", fg='black', bg="white", bd=3)
        self.entTujuan.place(relx=.3, rely=.4)   

        lblKuantitas = Label(self.frameTambah2, text="Kuantitas", font="Arial 12 bold", fg='black', bg="white")
        lblKuantitas.place(relx=.1, rely=.5)
        self.entKuantitas = Entry(self.frameTambah2, textvariable=self.var_kuantitas2, font="Arial 12", fg='black', bg="white", bd=3)
        self.entKuantitas.place(relx=.3, rely=.5)  

        lblDeskripsi = Label(self.frameTambah2, text="Deskripsi", font="Arial 12 bold", fg='black', bg="white")
        lblDeskripsi.place(relx=.1, rely=.6)
        self.entDeskripsi2 = Text(self.frameTambah2, font="Arial 12", fg='black', bg="white", bd=3, height=5)
        self.entDeskripsi2.place(relx=.3, rely=.6)   

        self.btnSave = Button(self.frameTambah2, command=self.save_data2, font="Arial 12 bold", width=8, text="SAVE", bg="#915FE6", fg="white")
        self.btnSave.place(relx=.3, rely=.875)

        self.btnCancel = Button(self.frameTambah2,  command=self.clear2, font="Arial 12 bold", width=8, text="CLEAR", bg="#EF4747", fg="white")
        self.btnCancel.place(relx=.4, rely=.875)

        self.btnEdit = Button(self.frameTambah2,  command=self.update_data2, font="Arial 12 bold", width=8, text="EDIT", bg="#25F848", fg="white")
        self.btnEdit.place(relx=.5, rely=.875) 

        self.btnDel = Button(self.frameTambah2, command=self.delete_data2,  font="Arial 12 bold", width=8, text="DELETE", bg="grey", fg="white")
        self.btnDel.place(relx=.6, rely=.875)

        # Menu Barang Masuk        
        self.var_IDbarang3=StringVar()
        self.var_namabarang3=StringVar()
        self.var_tanggal3=StringVar()
        self.var_sumber=StringVar()
        self.var_kuantitas3=StringVar()
        self.search_by3=StringVar()
        self.search_txt3=StringVar()

        self.framemasuk = Frame(self.frame3, width=1125, height=100, bg="white",
                        highlightbackground="black", highlightthicknes=1)
        
        self.btn31 = Button(self.framemasuk, bg="white", command=self.daftar3, text="Daftar Barang Masuk", font="Arial 12 bold", fg='black', relief=FLAT)
        self.btn31.place(relx=.1, rely=.65, anchor="center")

        self.btn32 = Button(self.framemasuk, bg="white", command=self.tambah3, text="Kelola Data", font="Arial 12 bold", fg='black',relief=FLAT)
        self.btn32.place(relx=.25, rely=.65, anchor="center")

        self.lbl_search= Label(self.framemasuk, text="Search By", font="Arial 12 bold", fg='black', bg="#ffffff")
        self.lbl_search.place(relx=.45, rely=.65, anchor="center")

        self.combo_search = ttk.Combobox(self.framemasuk, textvariable=self.search_by3, width = 15, font=("Arial", 12), state = "readonly")
        self.combo_search['values'] = ("idPenerimaan", "namaBarang", "tglPermintaan", "sumber")
        self.combo_search.place(relx=.575, rely=.65, anchor="center")

        self.txt_search = Entry(self.framemasuk, textvariable=self.search_txt3, width = 15,font=("Arial", 12), bd = 2, bg="#AFEEEE")
        self.txt_search.place(relx=.725, rely=.65, anchor="center")

        load = Image.open("search.png")
        load = load.resize((25, 25), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        self.img = Button(self.framemasuk, command=self.search_data3, image=render, bd=0,  bg ="white", fg = "#1aa333")
        self.img.image = render
        self.img.place(relx=.81, rely=.65, anchor="center")

        self.btnShowall = Button(self.framemasuk,  command=self.fetch_data3, text="Show All", bg="#42ADF3", fg="white", font="Arial 12 bold")
        self.btnShowall.place(relx=.875, rely=.65, anchor="center")

        # FRAME DAFTAR3
        self.frameDaftar3 = Frame(self.frame3, width=1125, height=450, bg="white", highlightbackground="black", highlightthicknes=1)


        self.table = Frame (self.frameDaftar3, bd=4, relief=RIDGE, bg="white")
        self.table.place(relx=.05, rely=.1, width=1000, height=350)
        scrollx= Scrollbar(self.table, orient=HORIZONTAL)        
        scrolly= Scrollbar(self.table, orient=VERTICAL)
        self.table_lap3=ttk.Treeview(self.table,columns=("ID","namabarang", "tanggal", "sumber","kuantitas","deskripsi", "aksi"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.pack(side=BOTTOM,fill=X)        
        scrolly.config(command=self.table_lap3.yview)
        scrollx.config(command=self.table_lap3.xview)

        self.table_lap3.heading("ID",text="ID")
        self.table_lap3.heading("namabarang",text="NAMA BARANG")
        self.table_lap3.heading("tanggal",text="TANGGAL")
        self.table_lap3.heading("sumber",text="SUMBER")
        self.table_lap3.heading("kuantitas",text="KUANTITAS")
        self.table_lap3.heading("deskripsi",text="DESKRIPSI")

        self.table_lap3['show']='headings'
        self.table_lap3.column("ID",width=70)
        self.table_lap3.column("namabarang",width=170)
        self.table_lap3.column("tanggal",width=150)
        self.table_lap3.column("sumber",width=150)
        self.table_lap3.column("kuantitas",width=100)
        self.table_lap3.column("deskripsi",width=340)
        self.table_lap3.pack(fill=BOTH,expand=1)
        self.table_lap3.bind("<ButtonRelease-1>",self.get_cursor3)
        self.fetch_data3()

        # FRAME TAMBAH3
        self.frameTambah3 = Frame(self.frame3, width=1125, height=450, bg="white", highlightbackground="black", highlightthicknes=1)
         
        lblID = Label(self.frameTambah3, text="ID", font="Arial 12 bold", fg='black', bg="white")
        lblID.place(relx=.1, rely=.1)   
        self.entID = Entry(self.frameTambah3, textvariable=self.var_IDbarang3, font="Arial 12", fg='black', bg="white", bd=3)
        self.entID.place(relx=.3, rely=.1)    

        lblNamaBrg = Label(self.frameTambah3, text="Nama Barang", font="Arial 12 bold", fg='black', bg="white")
        lblNamaBrg.place(relx=.1, rely=.2) 
        self.entNamaBrg = Entry(self.frameTambah3, textvariable=self.var_namabarang3, font="Arial 12", fg='black', bg="white", bd=3)
        self.entNamaBrg.place(relx=.3, rely=.2)     

        lblTgl = Label(self.frameTambah3, text="Tanggal", font="Arial 12 bold", fg='black', bg="white")
        lblTgl.place(relx=.1, rely=.3)  
        self.entTgl = DateEntry(self.frameTambah3, textvariable=self.var_tanggal3,state='readonly',date_pattern='y-mm-dd',width=24, background='#ffffff',foreground='black',font="Arial 10", borderwidth=4,Calendar =2021)
        self.entTgl.place(relx=.3, rely=.3)    

        lblSumber = Label(self.frameTambah3, text="Sumber", font="Arial 12 bold", fg='black', bg="white")
        lblSumber.place(relx=.1, rely=.4)  
        self.entSumber = Entry(self.frameTambah3, textvariable=self.var_sumber, font="Arial 12", fg='black', bg="white", bd=3)
        self.entSumber.place(relx=.3, rely=.4)   

        lblKuantitas = Label(self.frameTambah3, text="Kuantitas", font="Arial 12 bold", fg='black', bg="white")
        lblKuantitas.place(relx=.1, rely=.5)
        self.entKuantitas = Entry(self.frameTambah3, textvariable=self.var_kuantitas3, font="Arial 12", fg='black', bg="white", bd=3)
        self.entKuantitas.place(relx=.3, rely=.5)  

        lblDeskripsi = Label(self.frameTambah3, text="Deskripsi", font="Arial 12 bold", fg='black', bg="white")
        lblDeskripsi.place(relx=.1, rely=.6)
        self.entDeskripsi3 = Text(self.frameTambah3, font="Arial 12", fg='black', bg="white", bd=3, height=5)
        self.entDeskripsi3.place(relx=.3, rely=.6)   

        self.btnSave = Button(self.frameTambah3, command=self.save_data3, font="Arial 12 bold", width=8, text="SAVE", bg="#915FE6", fg="white")
        self.btnSave.place(relx=.3, rely=.875)

        self.btnCancel = Button(self.frameTambah3, command=self.clear3, font="Arial 12 bold", width=8, text="CLEAR", bg="#EF4747", fg="white")
        self.btnCancel.place(relx=.4, rely=.875)

        self.btnEdit = Button(self.frameTambah3,  command=self.update_data3, font="Arial 12 bold", width=8, text="EDIT", bg="#25F848", fg="white")
        self.btnEdit.place(relx=.5, rely=.875) 

        self.btnDel = Button(self.frameTambah3, command=self.delete_data3,  font="Arial 12 bold", width=8, text="DELETE", bg="grey", fg="white")
        self.btnDel.place(relx=.6, rely=.875)

    def home(self, event=None):
        self.frame3.place(x=199, y=119) 

    def databarang(self, event=None):
        self.frameDaftar.place(x=10, y=110)
        # self.frameDaftar2.place(x=10, y=110)
        # self.frameDaftar3.place(x=10, y=110)
        self.framedata.place(x=10, y=10) 
        # self.framekeluar.place(x=10, y=10)
        # self.framemasuk.place(x=10, y=10)
        self.frameTambah.place_forget()
        self.frameTambah2.place_forget()
        self.frameTambah3.place_forget()
        # self.frameDaftar.place_forget()
        self.frameDaftar2.place_forget()
        self.frameDaftar3.place_forget()
        # self.framedata.place_forget()
        self.framekeluar.place_forget()
        self.framemasuk.place_forget()
        

    def tambah(self, event=None):
        self.frameTambah.place(x=10, y=110)
        # self.frameTambah2.place(x=10, y=110)
        # self.frameTambah3.place(x=10, y=110)
        self.framedata.place(x=10, y=10) 
        # self.framekeluar.place(x=10, y=10)
        # self.framemasuk.place(x=10, y=10)
        # self.frameTambah.place_forget()
        self.frameTambah2.place_forget()
        self.frameTambah3.place_forget()
        self.frameDaftar.place_forget()
        self.frameDaftar2.place_forget()
        self.frameDaftar3.place_forget()
        # self.framedata.place_forget()
        self.framekeluar.place_forget()
        self.framemasuk.place_forget()

    def daftar(self, event=None):
        self.frameDaftar.place(x=10, y=110)
        # self.frameDaftar2.place(x=10, y=110)
        # self.frameDaftar3.place(x=10, y=110)
        self.framedata.place(x=10, y=10) 
        # self.framekeluar.place(x=10, y=10)
        # self.framemasuk.place(x=10, y=10)
        self.frameTambah.place_forget()
        self.frameTambah2.place_forget()
        self.frameTambah3.place_forget()
        # self.frameDaftar.place_forget()
        self.frameDaftar2.place_forget()
        self.frameDaftar3.place_forget()
        # self.framedata.place_forget()
        self.framekeluar.place_forget()
        self.framemasuk.place_forget()

    def save_data(self):
        if self.var_IDbarang.get()=="" or self.var_namabarang.get()=="":
                messagebox.showerror("Error", "Isi Data Di Atas Terlebih Dahulu !!")
        else:
                con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
                cur=con.cursor()
                cur.execute("insert into t_barang values(%s,%s,%s,%s,%s,%s)", (self.var_IDbarang.get(),
                                                                               self.var_namabarang.get(),
                                                                               self.var_kategori.get(),
                                                                               self.var_harga.get(),
                                                                               self.var_kuantitas.get(),
                                                                               self.entDeskripsi.get('1.0', END)
                                                                               ))
                con.commit()
                self.fetch_data()
                self.clear()
                con.close()
                messagebox.showinfo("Success","Data Berhasil Tersimpan")      

    def fetch_data(self):
        con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
        cur=con.cursor()
        cur.execute("select * from t_barang order by idBarang")
        rows=cur.fetchall()
        if len(rows)!=0:
                self.table_lap.delete(*self.table_lap.get_children())
                for row in rows:
                        self.table_lap.insert('',END,values=row)
                con.commit()
        con.close()

    def get_cursor(self,ev):
        curosor_row=self.table_lap.focus()
        contents=self.table_lap.item(curosor_row)
        row=contents['values']
        self.var_IDbarang.set(row[0])
        self.var_namabarang.set(row[1])
        self.var_kategori.set(row[2])
        self.var_kuantitas.set(row[4])
        self.var_harga.set(row[3])
        self.entDeskripsi.delete("1.0",END)
        self.entDeskripsi.insert(END,row[5])

    def clear(self):
        self.var_IDbarang.set("")
        self.var_namabarang.set("")
        self.var_kategori.set("")
        self.var_kuantitas.set("")
        self.var_harga.set("")
        self.entDeskripsi.delete("1.0", END)

    def update_data(self):
        con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
        cur=con.cursor()
        cur.execute("update t_barang set idBarang=%s,namaBarang=%s,kategori=%s,harga=%s,kuantitas=%s,deskripsi=%s where idBarang=%s",(
                                                                                                                            self.var_IDbarang.get(),
                                                                                                                            self.var_namabarang.get(),
                                                                                                                            self.var_kategori.get(),
                                                                                                                            self.var_harga.get(),
                                                                                                                            self.var_kuantitas.get(),
                                                                                                                            self.entDeskripsi.get('1.0', END),
                                                                                                                            self.var_IDbarang.get()))
        
        con.commit()
        self.fetch_data()
        self.clear()
        messagebox.showinfo("Success","Data Berhasil Tersimpan")
        con.close()

    def delete_data(self):
        con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
        cur=con.cursor()
        cur.execute("delete from t_barang where idBarang=%s",self.var_IDbarang.get())
        con.commit()
        con.close()
        self.fetch_data()
        self.clear()

    def search_data(self):

        con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
        cur=con.cursor()
        cur.execute("select * from t_barang where "+str(self.search_by.get())+" LIKE '%"+str(self.search_txt.get())+"%'")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.table_lap.delete(*self.table_lap.get_children())
            for row in rows:
                self.table_lap.insert('',END,values=row)
            con.commit()
        else:
            self.table_lap.delete(*self.table_lap.get_children())
        con.close()
    
    def datakeluar(self, event=None):
        # self.frameDaftar.place(x=10, y=110)
        self.frameDaftar2.place(x=10, y=110)
        # self.frameDaftar3.place(x=10, y=110)
        # self.framedata.place(x=10, y=10) 
        self.framekeluar.place(x=10, y=10)
        # self.framemasuk.place(x=10, y=10)
        self.frameTambah.place_forget()
        self.frameTambah2.place_forget()
        self.frameTambah3.place_forget()
        self.frameDaftar.place_forget()
        # self.frameDaftar2.place_forget()
        self.frameDaftar3.place_forget()
        self.framedata.place_forget()
        # self.framekeluar.place_forget()
        self.framemasuk.place_forget()
        

    def tambah2(self, event=None):
        # self.frameTambah.place(x=10, y=110)
        self.frameTambah2.place(x=10, y=110)
        # self.frameTambah3.place(x=10, y=110)
        # self.framedata.place(x=10, y=10) 
        self.framekeluar.place(x=10, y=10)
        # self.framemasuk.place(x=10, y=10)
        self.frameTambah.place_forget()
        # self.frameTambah2.place_forget()
        self.frameTambah3.place_forget()
        self.frameDaftar.place_forget()
        self.frameDaftar2.place_forget()
        self.frameDaftar3.place_forget()
        self.framedata.place_forget()
        # self.framekeluar.place_forget()
        self.framemasuk.place_forget()

    def daftar2(self, event=None):
        # self.frameDaftar.place(x=10, y=110)
        self.frameDaftar2.place(x=10, y=110)
        # self.frameDaftar3.place(x=10, y=110)
        # self.framedata.place(x=10, y=10) 
        self.framekeluar.place(x=10, y=10)
        # self.framemasuk.place(x=10, y=10)
        self.frameTambah.place_forget()
        self.frameTambah2.place_forget()
        self.frameTambah3.place_forget()
        self.frameDaftar.place_forget()
        # self.frameDaftar2.place_forget()
        self.frameDaftar3.place_forget()
        self.framedata.place_forget()
        # self.framekeluar.place_forget()
        self.framemasuk.place_forget()

    def save_data2(self):
        if self.var_IDbarang2.get()=="" or self.var_namabarang2.get()=="":
                messagebox.showerror("Error", "Isi Data Di Atas Terlebih Dahulu !!")
        else:
                con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
                cur=con.cursor()
                cur.execute("insert into t_pengiriman values(%s,%s,%s,%s,%s,%s)", (self.var_IDbarang2.get(),
                                                                               self.var_namabarang2.get(),
                                                                               self.var_tanggal2.get(),
                                                                               self.var_tujuan.get(),
                                                                               self.var_kuantitas2.get(),
                                                                               self.entDeskripsi2.get('1.0', END)
                                                                               ))
                con.commit()
                self.fetch_data2()
                # self.clear2()
                con.close()
                messagebox.showinfo("Success","Data Berhasil Tersimpan")      

    def fetch_data2(self):
        con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
        cur=con.cursor()
        cur.execute("select * from t_pengiriman")
        rows=cur.fetchall()
        if len(rows)!=0:
                self.table_lap2.delete(*self.table_lap2.get_children())
                for row in rows:
                        self.table_lap2.insert('',END,values=row)
                con.commit()
        con.close()

    def get_cursor2(self,ev):
        curosor_row=self.table_lap2.focus()
        contents=self.table_lap2.item(curosor_row)
        row=contents['values']
        self.var_IDbarang2.set(row[0])
        self.var_namabarang2.set(row[1])
        self.var_tanggal2.set(row[2])
        self.var_tujuan.set(row[3])
        self.var_kuantitas2.set(row[4])
        self.entDeskripsi2.delete("1.0",END)
        self.entDeskripsi2.insert(END,row[5])

    def clear2(self):
        self.var_IDbarang2.set("")
        self.var_namabarang2.set("")
        self.var_tanggal2.set("")
        self.var_tujuan.set("")
        self.var_kuantitas2.set("")
        self.entDeskripsi2.delete("1.0", END)

    def update_data2(self):
        con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
        cur=con.cursor()
        cur.execute("update t_pengiriman set idPengiriman=%s,namaBarang=%s,tglPengiriman=%s,tujuan=%s,kuantitas=%s,deskripsi=%s where idPengiriman=%s",(
                                                                                                                            self.var_IDbarang2.get(),
                                                                                                                            self.var_namabarang2.get(),
                                                                                                                            self.var_tanggal2.get(),
                                                                                                                            self.var_tujuan.get(),
                                                                                                                            self.var_kuantitas2.get(),
                                                                                                                            self.entDeskripsi2.get('1.0', END),
                                                                                                                            self.var_IDbarang2.get()))
        
        con.commit()
        self.fetch_data2()
        self.clear2()
        messagebox.showinfo("Success","Data Berhasil Tersimpan")
        con.close()

    def delete_data2(self):
        con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
        cur=con.cursor()
        cur.execute("delete from t_pengiriman where namaBarang=%s",self.var_namabarang2.get())
        con.commit()
        con.close()
        self.fetch_data2()
        self.clear2()

    def search_data2(self):

        con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
        cur=con.cursor()
        cur.execute("select * from t_pengiriman where "+str(self.search_by2.get())+" LIKE '%"+str(self.search_txt2.get())+"%'")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.table_lap2.delete(*self.table_lap2.get_children())
            for row in rows:
                self.table_lap2.insert('',END,values=row)
            con.commit()
        else:
            self.table_lap2.delete(*self.table_lap2.get_children())
        con.close()

    def datamasuk(self, event=None):
        # self.frameDaftar.place(x=10, y=110)
        # self.frameDaftar2.place(x=10, y=110)
        self.frameDaftar3.place(x=10, y=110)
        # self.framedata.place(x=10, y=10) 
        # self.framekeluar.place(x=10, y=10)
        self.framemasuk.place(x=10, y=10)
        self.frameTambah.place_forget()
        self.frameTambah2.place_forget()
        self.frameTambah3.place_forget()
        self.frameDaftar.place_forget()
        self.frameDaftar2.place_forget()
        # self.frameDaftar3.place_forget()
        self.framedata.place_forget()
        self.framekeluar.place_forget()
        # self.framemasuk.place_forget()

    def tambah3(self, event=None):
        # self.frameTambah.place(x=10, y=110)
        # self.frameTambah2.place(x=10, y=110)
        self.frameTambah3.place(x=10, y=110)
        # self.framedata.place(x=10, y=10) 
        # self.framekeluar.place(x=10, y=10)
        self.framemasuk.place(x=10, y=10)
        self.frameTambah.place_forget()
        self.frameTambah2.place_forget()
        # self.frameTambah3.place_forget()
        self.frameDaftar.place_forget()
        self.frameDaftar2.place_forget()
        self.frameDaftar3.place_forget()
        self.framedata.place_forget()
        self.framekeluar.place_forget()
        # self.framemasuk.place_forget()

    def daftar3(self, event=None):
        # self.frameDaftar.place(x=10, y=110)
        # self.frameDaftar2.place(x=10, y=110)
        self.frameDaftar3.place(x=10, y=110)
        # self.framedata.place(x=10, y=10) 
        # self.framekeluar.place(x=10, y=10)
        self.framemasuk.place(x=10, y=10)
        self.frameTambah.place_forget()
        self.frameTambah2.place_forget()
        self.frameTambah3.place_forget()
        self.frameDaftar.place_forget()
        self.frameDaftar2.place_forget()
        # self.frameDaftar3.place_forget()
        self.framedata.place_forget()
        self.framekeluar.place_forget()
        # self.framemasuk.place_forget()

    def save_data3(self):
        if self.var_IDbarang3.get()=="" or self.var_namabarang3.get()=="":
                messagebox.showerror("Error", "Isi Data Di Atas Terlebih Dahulu !!")
        else:
                con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
                cur=con.cursor()
                cur.execute("insert into t_permintaan values(%s,%s,%s,%s,%s,%s)", (self.var_IDbarang3.get(),
                                                                               self.var_namabarang3.get(),
                                                                               self.var_tanggal3.get(),
                                                                               self.var_sumber.get(),
                                                                               self.var_kuantitas3.get(),
                                                                               self.entDeskripsi3.get("1.0", END)
                                                                               ))
                con.commit()
                self.fetch_data3()
                self.clear3()
                con.close()
                messagebox.showinfo("Success","Data Berhasil Tersimpan")      

    def fetch_data3(self):
        con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
        cur=con.cursor()
        cur.execute("select * from t_permintaan")
        rows=cur.fetchall()
        if len(rows)!=0:
                self.table_lap3.delete(*self.table_lap3.get_children())
                for row in rows:
                        self.table_lap3.insert('',END,values=row)
                con.commit()
        con.close()

    def get_cursor3(self,ev):
        curosor_row=self.table_lap3.focus()
        contents=self.table_lap3.item(curosor_row)
        row=contents['values']
        self.var_IDbarang3.set(row[0])
        self.var_namabarang3.set(row[1])
        self.var_tanggal3.set(row[2])
        self.var_sumber.set(row[3])
        self.var_kuantitas3.set(row[4])
        self.entDeskripsi3.delete("1.0",END)
        self.entDeskripsi3.insert(END,row[5])

    def clear3(self):
        self.var_IDbarang3.set("")
        self.var_namabarang3.set("")
        self.var_tanggal3.set("")
        self.var_sumber.set("")
        self.var_kuantitas3.set("")
        self.entDeskripsi3.delete("1.0", END)

    def update_data3(self):
        con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
        cur=con.cursor()
        cur.execute("update t_permintaan set idPenerimaan=%s,namaBarang=%s,tglPenerimaan=%s,sumber=%s,kuantitas=%s,deskripsi=%s where idPenerimaan=%s",(
                                                                                                                            self.var_IDbarang3.get(),
                                                                                                                            self.var_namabarang3.get(),
                                                                                                                            self.var_tanggal3.get(),
                                                                                                                            self.var_sumber.get(),
                                                                                                                            self.var_kuantitas3.get(),
                                                                                                                            self.entDeskripsi3.get('1.0', END),
                                                                                                                            self.var_IDbarang3.get()))
        
        con.commit()
        self.fetch_data3()
        self.clear3()
        messagebox.showinfo("Success","Data Berhasil Tersimpan")
        con.close()
    
    def delete_data3(self):
        con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
        cur=con.cursor()
        cur.execute("delete from t_permintaan where namaBarang=%s",self.var_namabarang3.get())
        con.commit()
        con.close()
        self.fetch_data3()
        self.clear3()

    def search_data3(self):

        con=pymysql.connect(host='127.0.0.1',user="root", passwd="" , database="gudangsr12")
        cur=con.cursor()
        cur.execute("select * from t_permintaan where "+str(self.search_by3.get())+" LIKE '%"+str(self.search_txt3.get())+"%'")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.table_lap3.delete(*self.table_lap3.get_children())
            for row in rows:
                self.table_lap3.insert('',END,values=row)
            con.commit()
        else:
            self.table_lap3.delete(*self.table_lap3.get_children())
        con.close()
     

    mydb = mysql.connector.connect(
       host = '127.0.0.1',
       user = "root",
       passwd = "",
       database = "gudangsr12"
    )
       
if __name__ == '__main__':
    
    root = Tk()
    spt = AssetManagement(root, "Software Manajemen Gudang SR12")
    root.state("zoomed")
    root.mainloop()
