# -*- coding: utf-8 -*-
"""
Algerian Payroll - Standalone desktop MVP
Python 3.10+ / Tkinter / SQLite. No Excel required.
"""
import os, sys, sqlite3, calendar, datetime, tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pathlib import Path

APP_NAME = "تسيير الأجور الجزائر"
APP_VERSION = "1.0.1"

def data_dir():
    root = Path(os.environ.get("APPDATA", Path.home())) / "AlgeriaPayroll"
    root.mkdir(parents=True, exist_ok=True)
    return root

DB_PATH = data_dir() / "payroll.db"


def resource_path(filename):
    """Locate bundled assets in development and in a PyInstaller executable."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / filename

I18N = {
 "AR": {
  "title":"نظام تسيير الأجور - الجزائر", "employees":"العمال", "attendance":"الحضور والغياب",
  "entries":"المنح والتسبيقات والاقتطاعات", "payroll":"حساب الرواتب", "settings":"الإعدادات",
  "add":"إضافة عامل", "edit":"تعديل", "delete":"حذف", "refresh":"تحديث",
  "id":"رقم العامل", "name":"الاسم واللقب", "job":"المنصب", "hire":"تاريخ التوظيف",
  "salary":"الأجر الأساسي الشهري (دج)", "active":"نشط", "save":"حفظ", "cancel":"إلغاء",
  "month":"الشهر", "year":"السنة", "day":"اليوم", "status":"الحالة",
  "present":"حضور", "absent":"غياب", "half":"نصف يوم", "quarter":"ربع يوم",
  "bonus":"منحة", "advance":"تسبيق", "deduction":"اقتطاع", "type":"النوع",
  "amount":"المبلغ (دج)", "cnas":"خاضع لـ CNAS", "irg":"خاضع لـ IRG", "note":"ملاحظة",
  "record":"تسجيل", "calculate":"حساب الرواتب", "employee":"العامل", "gross":"الأجر الخام",
  "cnas_emp":"CNAS العامل", "irg_amount":"IRG", "advances":"التسبيقات",
  "deductions":"الاقتطاعات", "net":"الصافي للدفع", "cnas_company":"CNAS المؤسسة",
  "fnpos":"FNPOS", "cost":"التكلفة الإجمالية", "export":"تصدير كشف CSV",
  "language":"اللغة", "rates":"النسب", "worker_rate":"CNAS العامل %", "company_rate":"CNAS المؤسسة %",
  "fnpos_rate":"FNPOS %", "saved":"تم الحفظ بنجاح", "required":"يرجى ملء الحقول المطلوبة",
  "confirm_delete":"هل تريد حذف العامل المحدد؟", "select_employee":"اختر عاملاً أولاً",
  "all":"الكل", "search":"بحث", "backup":"نسخ احتياطي", "about":"حول البرنامج",
  "attendance_help":"أدخل 1 للحضور، 0 للغياب، 0.5 لنصف يوم، 0.25 لربع يوم.",
  "tax_warning":"الحسابات الضريبية والاجتماعية قابلة للتهيئة ويجب مراجعتها مع مختص أجور جزائري قبل اعتماد الرواتب.",
  "no_data":"لا توجد بيانات", "close":"إغلاق"
 },
 "EN": {
  "title":"Algerian Payroll System", "employees":"Employees", "attendance":"Attendance",
  "entries":"Bonuses / Advances / Deductions", "payroll":"Payroll", "settings":"Settings",
  "add":"Add employee", "edit":"Edit", "delete":"Delete", "refresh":"Refresh",
  "id":"Employee ID", "name":"Full name", "job":"Position", "hire":"Hire date",
  "salary":"Monthly base salary (DZD)", "active":"Active", "save":"Save", "cancel":"Cancel",
  "month":"Month", "year":"Year", "day":"Day", "status":"Status",
  "present":"Present", "absent":"Absent", "half":"Half day", "quarter":"Quarter day",
  "bonus":"Bonus", "advance":"Advance", "deduction":"Deduction", "type":"Type",
  "amount":"Amount (DZD)", "cnas":"Subject to CNAS", "irg":"Subject to IRG", "note":"Note",
  "record":"Save entry", "calculate":"Calculate payroll", "employee":"Employee", "gross":"Gross pay",
  "cnas_emp":"Employee CNAS", "irg_amount":"IRG", "advances":"Advances",
  "deductions":"Deductions", "net":"Net pay", "cnas_company":"Employer CNAS",
  "fnpos":"FNPOS", "cost":"Total cost", "export":"Export CSV",
  "language":"Language", "rates":"Rates", "worker_rate":"Employee CNAS %", "company_rate":"Employer CNAS %",
  "fnpos_rate":"FNPOS %", "saved":"Saved successfully", "required":"Please complete required fields",
  "confirm_delete":"Delete selected employee?", "select_employee":"Select an employee first",
  "all":"All", "search":"Search", "backup":"Backup", "about":"About",
  "attendance_help":"Enter 1 present, 0 absent, 0.5 half day, 0.25 quarter day.",
  "tax_warning":"Tax and social calculations are configurable. Verify with an Algerian payroll specialist before payment.",
  "no_data":"No data", "close":"Close"
 },
 "FR": {
  "title":"Gestion de paie - Algérie", "employees":"Employés", "attendance":"Présence",
  "entries":"Primes / Avances / Retenues", "payroll":"Paie", "settings":"Paramètres",
  "add":"Ajouter employé", "edit":"Modifier", "delete":"Supprimer", "refresh":"Actualiser",
  "id":"Matricule", "name":"Nom et prénom", "job":"Poste", "hire":"Date d'embauche",
  "salary":"Salaire mensuel de base (DZD)", "active":"Actif", "save":"Enregistrer", "cancel":"Annuler",
  "month":"Mois", "year":"Année", "day":"Jour", "status":"Statut",
  "present":"Présent", "absent":"Absent", "half":"Demi-journée", "quarter":"Quart de journée",
  "bonus":"Prime", "advance":"Avance", "deduction":"Retenue", "type":"Type",
  "amount":"Montant (DZD)", "cnas":"Soumis CNAS", "irg":"Soumis IRG", "note":"Note",
  "record":"Enregistrer", "calculate":"Calculer la paie", "employee":"Employé", "gross":"Brut",
  "cnas_emp":"CNAS salarié", "irg_amount":"IRG", "advances":"Avances",
  "deductions":"Retenues", "net":"Net à payer", "cnas_company":"CNAS employeur",
  "fnpos":"FNPOS", "cost":"Coût total", "export":"Exporter CSV",
  "language":"Langue", "rates":"Taux", "worker_rate":"CNAS salarié %", "company_rate":"CNAS employeur %",
  "fnpos_rate":"FNPOS %", "saved":"Enregistré", "required":"Veuillez remplir les champs obligatoires",
  "confirm_delete":"Supprimer l'employé sélectionné ?", "select_employee":"Sélectionnez un employé",
  "all":"Tous", "search":"Recherche", "backup":"Sauvegarde", "about":"À propos",
  "attendance_help":"Saisir 1 présent, 0 absent, 0.5 demi-journée, 0.25 quart de journée.",
  "tax_warning":"Les calculs fiscaux et sociaux doivent être vérifiés par un spécialiste algérien avant paiement.",
  "no_data":"Aucune donnée", "close":"Fermer"
 }
}

def month_name(m, lang):
    names = {
      "AR":["جانفي","فيفري","مارس","أفريل","ماي","جوان","جويلية","أوت","سبتمبر","أكتوبر","نوفمبر","ديسمبر"],
      "EN":list(calendar.month_name)[1:],
      "FR":["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
    }
    return names[lang][m-1]

class Store:
    def __init__(self):
        self.con=sqlite3.connect(DB_PATH)
        self.con.execute("PRAGMA foreign_keys=ON")
        self.init_db()
    def init_db(self):
        c=self.con.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS employees(
          id TEXT PRIMARY KEY, name TEXT NOT NULL, job TEXT, hire_date TEXT,
          base_salary REAL NOT NULL DEFAULT 0, active INTEGER NOT NULL DEFAULT 1)""")
        c.execute("""CREATE TABLE IF NOT EXISTS attendance(
          id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id TEXT NOT NULL, year INTEGER NOT NULL,
          month INTEGER NOT NULL, day INTEGER NOT NULL, value REAL NOT NULL,
          UNIQUE(employee_id,year,month,day), FOREIGN KEY(employee_id) REFERENCES employees(id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS entries(
          id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id TEXT NOT NULL, year INTEGER NOT NULL,
          month INTEGER NOT NULL, kind TEXT NOT NULL, label TEXT, amount REAL NOT NULL,
          subject_cnas INTEGER DEFAULT 0, subject_irg INTEGER DEFAULT 0, note TEXT,
          FOREIGN KEY(employee_id) REFERENCES employees(id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT NOT NULL)""")
        defaults={"lang":"AR","cnas_worker":"9","cnas_company":"25","fnpos":"0.5","snmg":"24000"}
        for k,v in defaults.items(): c.execute("INSERT OR IGNORE INTO settings VALUES(?,?)",(k,v))
        self.con.commit()
    def setting(self,k): return self.con.execute("SELECT value FROM settings WHERE key=?",(k,)).fetchone()[0]
    def set_setting(self,k,v): self.con.execute("INSERT OR REPLACE INTO settings VALUES(?,?)",(k,str(v))); self.con.commit()
    def employees(self, include_inactive=False):
        q="SELECT id,name,job,hire_date,base_salary,active FROM employees"
        if not include_inactive:q+=" WHERE active=1"
        return self.con.execute(q+" ORDER BY name").fetchall()
    def close(self): self.con.close()

def progressive_irg(taxable):
    """Monthly progressive scale, then DGI-style reduction approximation.
    Keep thresholds/rules editable in later releases and validate annually."""
    x=max(0.0,float(taxable))
    if x<=30000: return 0.0
    tax=0.0
    brackets=[(20000,0.00),(20000,0.23),(40000,0.27),(80000,0.30),(160000,0.33)]
    rem=x
    for width,rate in brackets:
        part=min(rem,width); tax+=part*rate; rem-=part
        if rem<=0: break
    if rem>0: tax+=rem*0.35
    # General 40% reduction capped between 1,000 and 1,500 DZD.
    reduction=min(1500.0,max(1000.0,tax*0.40))
    result=max(0.0,tax-reduction)
    # Special relief band for taxable income 30,001..35,000.
    if 30000 < x <= 35000:
        result=max(0.0,(tax-reduction)*(137/51)-(27925/8))
    return round(result,2)

class PayrollApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.store=Store()
        self.lang=self.store.setting("lang")
        self.title(I18N[self.lang]["title"])
        self.geometry("1120x720")
        self.minsize(940,620)
        self.configure(bg="#f3f5f8")
        self.style=ttk.Style(self)
        try:self.style.theme_use("clam")
        except:pass
        self.style.configure("Treeview",rowheight=28,font=("Arial",10))
        self.style.configure("Treeview.Heading",font=("Arial",10,"bold"))
        self.style.configure("TButton",font=("Arial",10))
        self.build()
        self.protocol("WM_DELETE_WINDOW",self.on_close)

    def t(self,k): return I18N[self.lang].get(k,k)
    def build(self):
        for w in self.winfo_children():w.destroy()
        top=ttk.Frame(self,padding=10);top.pack(fill="x")
        # Company logo supplied by the user; bundled inside the Windows EXE.
        try:
            self.logo_image = tk.PhotoImage(file=str(resource_path("logo.png")))
            # Keep the logo compact so the application remains comfortable on small screens.
            factor = max(1, (self.logo_image.width() + 259) // 260)
            if factor > 1:
                self.logo_image = self.logo_image.subsample(factor, factor)
            ttk.Label(top, image=self.logo_image).pack(side="right", padx=(12, 4))
        except Exception:
            self.logo_image = None
        ttk.Label(top,text=self.t("title"),font=("Arial",18,"bold")).pack(side="right", padx=8)
        self.lang_var=tk.StringVar(value=self.lang)
        ttk.Label(top,text=self.t("language")).pack(side="left",padx=(18,4))
        cb=ttk.Combobox(top,textvariable=self.lang_var,values=["AR","EN","FR"],width=5,state="readonly")
        cb.pack(side="left");cb.bind("<<ComboboxSelected>>",self.change_lang)
        ttk.Button(top,text=self.t("backup"),command=self.backup).pack(side="left",padx=10)
        self.nb=ttk.Notebook(self);self.nb.pack(fill="both",expand=True,padx=12,pady=8)
        self.emp_tab=ttk.Frame(self.nb,padding=10);self.att_tab=ttk.Frame(self.nb,padding=10)
        self.entry_tab=ttk.Frame(self.nb,padding=10);self.pay_tab=ttk.Frame(self.nb,padding=10)
        self.settings_tab=ttk.Frame(self.nb,padding=10)
        for tab,key in [(self.emp_tab,"employees"),(self.att_tab,"attendance"),(self.entry_tab,"entries"),(self.pay_tab,"payroll"),(self.settings_tab,"settings")]:
            self.nb.add(tab,text=self.t(key))
        self.build_employees();self.build_attendance();self.build_entries();self.build_payroll();self.build_settings()

    def tree(self,parent,cols,headings,widths=None):
        wrap=ttk.Frame(parent);wrap.pack(fill="both",expand=True,pady=8)
        tv=ttk.Treeview(wrap,columns=cols,show="headings")
        for i,c in enumerate(cols):
            tv.heading(c,text=headings[i]);tv.column(c,width=(widths[i] if widths else 130),anchor="center")
        sy=ttk.Scrollbar(wrap,orient="vertical",command=tv.yview);tv.configure(yscrollcommand=sy.set)
        tv.pack(side="left",fill="both",expand=True);sy.pack(side="right",fill="y")
        return tv

    def build_employees(self):
        bar=ttk.Frame(self.emp_tab);bar.pack(fill="x")
        ttk.Button(bar,text=self.t("add"),command=self.employee_dialog).pack(side="left",padx=3)
        ttk.Button(bar,text=self.t("edit"),command=self.edit_employee).pack(side="left",padx=3)
        ttk.Button(bar,text=self.t("delete"),command=self.deactivate_employee).pack(side="left",padx=3)
        ttk.Button(bar,text=self.t("refresh"),command=self.refresh_employees).pack(side="left",padx=3)
        self.emp_tree=self.tree(self.emp_tab,("id","name","job","hire","salary","active"),
          [self.t("id"),self.t("name"),self.t("job"),self.t("hire"),self.t("salary"),self.t("active")],
          [100,230,150,120,150,80])
        self.refresh_employees()
    def refresh_employees(self):
        if not hasattr(self,"emp_tree"):return
        self.emp_tree.delete(*self.emp_tree.get_children())
        for r in self.store.employees(True):
            self.emp_tree.insert("", "end", values=(r[0],r[1],r[2] or "",r[3] or "",f"{r[4]:,.2f}",self.t("active") if r[5] else "—"))
    def employee_dialog(self,row=None):
        win=tk.Toplevel(self);win.title(self.t("add"));win.transient(self);win.grab_set();win.geometry("420x360")
        fields=[("id",row[0] if row else ""),("name",row[1] if row else ""),("job",row[2] if row else ""),("hire",row[3] if row else datetime.date.today().isoformat()),("salary",row[4] if row else "")]
        vars={}
        for i,(k,val) in enumerate(fields):
            ttk.Label(win,text=self.t(k)).grid(row=i,column=0,padx=12,pady=9,sticky="e")
            v=tk.StringVar(value=str(val));vars[k]=v
            ttk.Entry(win,textvariable=v,width=30).grid(row=i,column=1,padx=12,pady=9)
        def save():
            try:
                empid=vars["id"].get().strip();name=vars["name"].get().strip();salary=float(vars["salary"].get().replace(",",""))
                if not empid or not name or salary<0:raise ValueError()
                if row:
                    self.store.con.execute("UPDATE employees SET name=?,job=?,hire_date=?,base_salary=? WHERE id=?",
                      (name,vars["job"].get(),vars["hire"].get(),salary,empid))
                else:
                    self.store.con.execute("INSERT INTO employees(id,name,job,hire_date,base_salary) VALUES(?,?,?,?,?)",
                      (empid,name,vars["job"].get(),vars["hire"].get(),salary))
                self.store.con.commit();win.destroy();self.refresh_employees()
            except sqlite3.IntegrityError:messagebox.showerror("Error","Employee ID already exists.")
            except:messagebox.showerror("Error",self.t("required")+" / Invalid salary")
        ttk.Button(win,text=self.t("save"),command=save).grid(row=6,column=1,pady=15,sticky="e")
    def selected_employee(self):
        sel=self.emp_tree.selection()
        if not sel:return None
        vals=self.emp_tree.item(sel[0],"values")
        return self.store.con.execute("SELECT id,name,job,hire_date,base_salary,active FROM employees WHERE id=?",(vals[0],)).fetchone()
    def edit_employee(self):
        r=self.selected_employee()
        if not r:messagebox.showinfo("",self.t("select_employee"));return
        self.employee_dialog(r)
    def deactivate_employee(self):
        r=self.selected_employee()
        if not r:messagebox.showinfo("",self.t("select_employee"));return
        if messagebox.askyesno("",self.t("confirm_delete")):
            self.store.con.execute("UPDATE employees SET active=0 WHERE id=?",(r[0],));self.store.con.commit();self.refresh_employees()

    def selectors(self,parent):
        bar=ttk.Frame(parent);bar.pack(fill="x")
        emps=self.store.employees()
        self.emp_pick=ttk.Combobox(bar,values=[f"{e[0]} | {e[1]}" for e in emps],width=30,state="readonly")
        self.emp_pick.pack(side="left",padx=4)
        mvar=tk.StringVar(value=str(datetime.date.today().month));yvar=tk.StringVar(value=str(datetime.date.today().year))
        ttk.Label(bar,text=self.t("month")).pack(side="left");ttk.Entry(bar,textvariable=mvar,width=5).pack(side="left",padx=4)
        ttk.Label(bar,text=self.t("year")).pack(side="left");ttk.Entry(bar,textvariable=yvar,width=7).pack(side="left",padx=4)
        return self.emp_pick,mvar,yvar

    def build_attendance(self):
        ttk.Label(self.att_tab,text=self.t("attendance_help")).pack(anchor="e",pady=5)
        bar=ttk.Frame(self.att_tab);bar.pack(fill="x")
        self.att_emp,self.att_m,self.att_y=self.selectors(self.att_tab)
        ttk.Label(bar,text=self.t("day")).pack(side="left")
        self.att_day=tk.StringVar(value=str(datetime.date.today().day));ttk.Entry(bar,textvariable=self.att_day,width=6).pack(side="left",padx=5)
        ttk.Label(bar,text=self.t("status")).pack(side="left")
        self.att_value=tk.StringVar(value="1")
        ttk.Combobox(bar,textvariable=self.att_value,values=["1","0","0.5","0.25"],width=8,state="readonly").pack(side="left",padx=5)
        ttk.Button(bar,text=self.t("record"),command=self.save_attendance).pack(side="left",padx=8)
        self.att_tree=self.tree(self.att_tab,("day","value"),[self.t("day"),self.t("status")],[140,180])
        ttk.Button(self.att_tab,text=self.t("refresh"),command=self.refresh_attendance).pack(anchor="e")
    def selected_id(self,combo):
        v=combo.get()
        return v.split(" | ",1)[0] if " | " in v else ""
    def save_attendance(self):
        try:
            eid=self.selected_id(self.att_emp);m=int(self.att_m.get());y=int(self.att_y.get());d=int(self.att_day.get());v=float(self.att_value.get())
            if not eid or not 1<=m<=12 or not 1<=d<=calendar.monthrange(y,m)[1] or v not in (0,0.25,0.5,1):raise ValueError()
            self.store.con.execute("""INSERT INTO attendance(employee_id,year,month,day,value) VALUES(?,?,?,?,?)
              ON CONFLICT(employee_id,year,month,day) DO UPDATE SET value=excluded.value""",(eid,y,m,d,v))
            self.store.con.commit();self.refresh_attendance();messagebox.showinfo("",self.t("saved"))
        except:messagebox.showerror("Error",self.t("required"))
    def refresh_attendance(self):
        if not hasattr(self,"att_tree"):return
        self.att_tree.delete(*self.att_tree.get_children())
        eid=self.selected_id(self.att_emp)
        if not eid:return
        try:
            rows=self.store.con.execute("SELECT day,value FROM attendance WHERE employee_id=? AND year=? AND month=? ORDER BY day",
                (eid,int(self.att_y.get()),int(self.att_m.get()))).fetchall()
            for d,v in rows:self.att_tree.insert("","end",values=(d,v))
        except:pass

    def build_entries(self):
        self.entry_emp,self.entry_m,self.entry_y=self.selectors(self.entry_tab)
        form=ttk.Frame(self.entry_tab);form.pack(fill="x",pady=12)
        self.entry_kind=tk.StringVar(value="bonus");self.entry_label=tk.StringVar();self.entry_amount=tk.StringVar()
        self.entry_cnas=tk.IntVar(value=1);self.entry_irg=tk.IntVar(value=1);self.entry_note=tk.StringVar()
        ttk.Label(form,text=self.t("type")).grid(row=0,column=0,padx=5,pady=6)
        ttk.Combobox(form,textvariable=self.entry_kind,values=["bonus","advance","deduction"],state="readonly",width=15).grid(row=0,column=1,padx=5)
        ttk.Label(form,text=self.t("name")).grid(row=0,column=2,padx=5)
        ttk.Entry(form,textvariable=self.entry_label,width=22).grid(row=0,column=3,padx=5)
        ttk.Label(form,text=self.t("amount")).grid(row=1,column=0,padx=5,pady=6)
        ttk.Entry(form,textvariable=self.entry_amount,width=15).grid(row=1,column=1,padx=5)
        ttk.Checkbutton(form,text=self.t("cnas"),variable=self.entry_cnas).grid(row=1,column=2)
        ttk.Checkbutton(form,text=self.t("irg"),variable=self.entry_irg).grid(row=1,column=3)
        ttk.Label(form,text=self.t("note")).grid(row=2,column=0,padx=5)
        ttk.Entry(form,textvariable=self.entry_note,width=45).grid(row=2,column=1,columnspan=3,padx=5,sticky="w")
        ttk.Button(form,text=self.t("record"),command=self.save_entry).grid(row=3,column=3,pady=10,sticky="e")
        self.entries_tree=self.tree(self.entry_tab,("kind","label","amount","month","year"),[self.t("type"),self.t("name"),self.t("amount"),self.t("month"),self.t("year")],[130,200,150,100,100])
    def save_entry(self):
        try:
            eid=self.selected_id(self.entry_emp);m=int(self.entry_m.get());y=int(self.entry_y.get());amt=float(self.entry_amount.get())
            kind=self.entry_kind.get()
            if not eid or not 1<=m<=12 or amt<=0:raise ValueError()
            self.store.con.execute("""INSERT INTO entries(employee_id,year,month,kind,label,amount,subject_cnas,subject_irg,note)
              VALUES(?,?,?,?,?,?,?,?,?)""",(eid,y,m,kind,self.entry_label.get(),amt,self.entry_cnas.get(),self.entry_irg.get(),self.entry_note.get()))
            self.store.con.commit();self.entry_amount.set("");messagebox.showinfo("",self.t("saved"))
        except:messagebox.showerror("Error",self.t("required"))

    def build_payroll(self):
        bar=ttk.Frame(self.pay_tab);bar.pack(fill="x")
        self.pay_m=tk.StringVar(value=str(datetime.date.today().month));self.pay_y=tk.StringVar(value=str(datetime.date.today().year))
        ttk.Label(bar,text=self.t("month")).pack(side="left");ttk.Entry(bar,textvariable=self.pay_m,width=5).pack(side="left",padx=5)
        ttk.Label(bar,text=self.t("year")).pack(side="left");ttk.Entry(bar,textvariable=self.pay_y,width=7).pack(side="left",padx=5)
        ttk.Button(bar,text=self.t("calculate"),command=self.calculate_payroll).pack(side="left",padx=12)
        ttk.Button(bar,text=self.t("export"),command=self.export_payroll).pack(side="left")
        cols=("id","name","gross","cnas","irg","advance","deductions","net","employer","fnpos","cost")
        heads=[self.t("id"),self.t("name"),self.t("gross"),self.t("cnas_emp"),self.t("irg_amount"),self.t("advances"),self.t("deductions"),self.t("net"),self.t("cnas_company"),self.t("fnpos"),self.t("cost")]
        self.pay_tree=self.tree(self.pay_tab,cols,heads,[80,160,100,95,90,95,95,105,110,80,110])
        self.pay_note=ttk.Label(self.pay_tab,text=self.t("tax_warning"),wraplength=1000,foreground="#9b5b00")
        self.pay_note.pack(anchor="e",pady=6)
        self.pay_results=[]
    def calculate_payroll(self):
        try:m=int(self.pay_m.get());y=int(self.pay_y.get())
        except:messagebox.showerror("Error","Invalid month/year");return
        if not 1<=m<=12:messagebox.showerror("Error","Month must be 1..12");return
        self.pay_tree.delete(*self.pay_tree.get_children());self.pay_results=[]
        days=calendar.monthrange(y,m)[1]
        rw=float(self.store.setting("cnas_worker"))/100
        rc=float(self.store.setting("cnas_company"))/100
        rf=float(self.store.setting("fnpos"))/100
        for e in self.store.employees():
            eid,name,job,hire,salary,active=e
            att=self.store.con.execute("SELECT SUM(value) FROM attendance WHERE employee_id=? AND year=? AND month=?",(eid,y,m)).fetchone()[0]
            # If no daily attendance was entered, assume full month and visibly warn in notes in future release.
            worked=float(att) if att is not None else days
            base=salary*min(1,worked/days)
            entries=self.store.con.execute("SELECT kind,amount,subject_cnas,subject_irg FROM entries WHERE employee_id=? AND year=? AND month=?",(eid,y,m)).fetchall()
            bonus=sum(a for k,a,c,i in entries if k=="bonus")
            cnas_bonus=sum(a for k,a,c,i in entries if k=="bonus" and c)
            irg_bonus=sum(a for k,a,c,i in entries if k=="bonus" and i)
            advances=sum(a for k,a,c,i in entries if k=="advance")
            deductions=sum(a for k,a,c,i in entries if k=="deduction")
            gross=base+bonus
            cnas_base=base+cnas_bonus
            cnas=round(cnas_base*rw,2)
            irg_base=max(0,base+irg_bonus-cnas)
            irg=progressive_irg(irg_base)
            emp_cnas=round(cnas_base*rc,2);fnpos=round(cnas_base*rf,2)
            net=round(gross-cnas-irg-advances-deductions,2)
            cost=round(gross+emp_cnas+fnpos,2)
            vals=(eid,name,gross,cnas,irg,advances,deductions,net,emp_cnas,fnpos,cost)
            self.pay_results.append(vals)
            self.pay_tree.insert("","end",values=(eid,name,*[f"{v:,.2f}" for v in vals[2:]]))
        self.pay_note.configure(text=self.t("tax_warning")+f"  |  {month_name(m,self.lang)} {y}")
    def export_payroll(self):
        if not self.pay_results:messagebox.showinfo("",self.t("no_data"));return
        import csv
        from tkinter import filedialog
        path=filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV","*.csv")],initialfile=f"Payroll_{self.pay_y.get()}_{self.pay_m.get()}.csv")
        if not path:return
        with open(path,"w",newline="",encoding="utf-8-sig") as f:
            w=csv.writer(f);w.writerow(["Employee ID","Name","Gross","Employee CNAS","IRG","Advances","Deductions","Net","Employer CNAS","FNPOS","Total cost"]);w.writerows(self.pay_results)
        messagebox.showinfo("",self.t("saved"))
    def build_settings(self):
        form=ttk.Frame(self.settings_tab);form.pack(anchor="ne",pady=12)
        self.rate_vars={}
        for i,(key,label) in enumerate([("cnas_worker","worker_rate"),("cnas_company","company_rate"),("fnpos","fnpos_rate")]):
            ttk.Label(form,text=self.t(label)).grid(row=i,column=0,padx=8,pady=8,sticky="e")
            v=tk.StringVar(value=self.store.setting(key));self.rate_vars[key]=v
            ttk.Entry(form,textvariable=v,width=14).grid(row=i,column=1,padx=8,pady=8)
        ttk.Button(form,text=self.t("save"),command=self.save_settings).grid(row=4,column=1,pady=12,sticky="e")
        ttk.Label(self.settings_tab,text=self.t("tax_warning"),wraplength=900,foreground="#9b5b00").pack(anchor="e",pady=20)
        ttk.Label(self.settings_tab,text=f"{APP_NAME} v{APP_VERSION} | SQLite local database").pack(anchor="w",side="bottom")
    def save_settings(self):
        try:
            for k,v in self.rate_vars.items():
                n=float(v.get())
                if not 0<=n<=100:raise ValueError()
                self.store.set_setting(k,n)
            messagebox.showinfo("",self.t("saved"))
        except:messagebox.showerror("Error","Invalid rate")
    def change_lang(self,event=None):
        lang=self.lang_var.get()
        if lang not in I18N:return
        self.lang=lang;self.store.set_setting("lang",lang);self.build()
    def backup(self):
        from tkinter import filedialog
        path=filedialog.asksaveasfilename(defaultextension=".db",filetypes=[("SQLite database","*.db")],initialfile=f"payroll_backup_{datetime.date.today().isoformat()}.db")
        if not path:return
        import shutil
        shutil.copy2(DB_PATH,path);messagebox.showinfo("",self.t("saved"))
    def on_close(self):
        self.store.close();self.destroy()

if __name__=="__main__":
    PayrollApp().mainloop()
