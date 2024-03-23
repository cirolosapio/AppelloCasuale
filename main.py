"""
Example script for testing the Azure ttk theme
Author: rdbende
License: MIT license
Source: https://github.com/rdbende/ttk-widget-factory
"""


import tkinter as tk
from tkinter import ttk, font
from tkinter import messagebox
from appello import AppelloCasuale
import random
import os
import sys

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        self.appello = AppelloCasuale()
        self.numero_tentativi = 0
        self.mod_min = 2
        self.mod_max = 4
        self.modificatore = 0
        self.combo_list_classi = []
        self.parent = parent
        # Make the app responsive
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=20)
        self.rowconfigure(index=0, weight=5)
        self.rowconfigure(index=1, weight=1)
        
        self.setup_widgets()

    def setup_widgets(self):
        self.combo_list_classi = self.__scan_list()
        #frame_setting a sinistra
        self.setting_frame = ttk.LabelFrame(self, text="Impostazioni", padding=(20, 10))
        self.setting_frame.columnconfigure(index=(0,1), weight=1)
        self.setting_frame.rowconfigure(index=(0,1,2,3,4), weight=1)
        
        
        #posizionamento
        self.setting_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nswe")
        
        
        self.label_class = ttk.Label(self.setting_frame, text="Classe", justify="center", font=("-family", "Roboto", "-size", 12, "-weight", "bold", ))
        self.label_class.grid(row=0, column=0, pady=10, sticky='e')
        self.combobox = ttk.Combobox(self.setting_frame, values=self.combo_list_classi, state='readonly', width=8)
        self.combobox.current(0)
        self.combobox.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        
        self.label_mosse = ttk.Label(self.setting_frame, text="Mosse", justify="center", font=("-family", "Roboto", "-size", 12, "-weight", "bold"))
        self.label_mosse.grid(row=1, column=0, pady=10, sticky='e')
        
        self.entry = ttk.Entry(self.setting_frame, width=7)
        self.entry.insert(0, "20")
        self.entry.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="w")
        
        self.label_mosse = ttk.Label(self.setting_frame, text="Min", justify="center", font=("-family", "Roboto", "-size", 12))
        self.label_mosse.grid(row=2, column=0, sticky='e')
        
        self.spinbox_min = ttk.Spinbox(self.setting_frame, from_=0, to=20, increment=1, width=5)
        self.spinbox_min.insert(0, "2")
        self.spinbox_min.grid(row=2, column=0, padx=5, pady=10, sticky="w")
        
        self.spinbox_min.grid(row=2, column=1)

        self.label_mosse = ttk.Label(self.setting_frame, text="Max", justify="center", font=("-family", "Roboto", "-size", 12))
        self.label_mosse.grid(row=3, column=0, sticky='e')
        
        self.spinbox_max = ttk.Spinbox(self.setting_frame, from_=0, to=20, increment=1, width=5)
        self.spinbox_max.insert(0, "4")
        self.spinbox_max.grid(row=3, column=0, padx=5, pady=10, sticky="w")
        
        self.spinbox_max.grid(row=3, column=1)
        
        self.btn_setting = ttk.Button(self.setting_frame, text="Conferma", style="Accent.TButton", command=self.__setting_submit)
        self.btn_setting.grid(row=4, column=0, columnspan=2)

        
        
        
        #frame_estrazione a destra
        self.estr_frame = ttk.LabelFrame(self, text="Estrazione", padding=(20, 10))
        self.estr_frame.columnconfigure(index=(0,1), weight=1)
        self.estr_frame.rowconfigure(index=(0,1,2,3), weight=1)
        self.estr_frame.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        
        self.label_etichetta_estrazione = ttk.Label(self.estr_frame, text="Estrazione in corso...", font=("-size", 15, "-weight", "bold"))
        self.label_etichetta_estrazione.grid(row=0, column=0, pady=10, columnspan=2, sticky='n')
        
        self.label_nome_cognome = ttk.Label(self.estr_frame, text="Nome Cognome", font=("-size", 12, "-weight", "bold"))
        self.label_nome_cognome.grid(row=1, column=0, pady=10, sticky='s')
        self.label_mosse_rimanenti = ttk.Label(self.estr_frame, text="Mosse rimanenti", font=("-size", 12, "-weight", "bold"))
        self.label_mosse_rimanenti.grid(row=1, column=1, pady=10, sticky='s')
        
        
        self.label_alunno = ttk.Label(self.estr_frame, text="...(...)", font=("-size", 12))
        self.label_alunno.grid(row=2, column=0, pady=10, sticky='n')
        
        self.label_n_mosse = ttk.Label(self.estr_frame, text="__", font=("-size", 18))
        self.label_n_mosse.grid(row=2, column=1, pady=10, sticky='n')
        
        self.btn_reset = ttk.Button(self.estr_frame, text="Reset", command=self.reset)
        self.btn_reset.grid(row=3, column=0)
        
        self.btn_estrai = ttk.Button(self.estr_frame, text="Estrai", style="Accent.TButton", command=self.estrazione)
        self.btn_estrai.grid(row=3, column=1)
        
        for widget in self.estr_frame.winfo_children():
                widget.configure(state='disabled')
    
        self.estr_frame.config(text='BLOCCATO')
        
        #frame indicazioni
        self.info_frame = ttk.LabelFrame(self, text="Info", padding=(20, 10))
        self.info_frame.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky='we')
        
        self.label_info = ttk.Label(self.info_frame, 
                                    text="Riquadro Impostazioni:\n\t1. Seleziona classe\n\t2. Inserisci il numero di mosse totali\n\t3. Inserisci il numero minimo e massimo di mosse per alunno\n\t4. Conferma(blocca il riquadro delle impostazioni)\nRiquadro Estrazione:\n\t[Estrai]Estrae un nuovo alunno\n\t[Reset]Abilità il riquadro delle impostazioni",
                                    font=("-size", 10))
        self.label_info.grid(row=0, column=0, sticky='we')

    def estrazione(self):
        modificatore = random.randint(self.mod_min, self.mod_max)
        print(f'modificatore:{self.modificatore} n_tentetivi:{self.numero_tentativi} min:{self.mod_min} max:{self.mod_max}')  
        
        if(modificatore >= self.numero_tentativi):
            self.label_n_mosse.config(text=f"{0}")
            if(modificatore == self.numero_tentativi):
                self.label_alunno.config(text=f"{self.appello.chiamare_ragazzo()}({1})")
            else:
                self.label_alunno.config(text=f"{self.appello.chiamare_ragazzo()}({self.numero_tentativi})")
            self.numero_tentativi = 0
            self.label_etichetta_estrazione.config(text=f"Estrazione terminata")
            for widget in self.estr_frame.winfo_children():
                widget.configure(state='disabled')
            self.estr_frame.config(text='BLOCCATO')
            for widget in self.setting_frame.winfo_children():
                widget.configure(state='normal')
            self.setting_frame.config(text='Impostazioni')

            print('reset fine partita')

        else:
            self.numero_tentativi -= modificatore
            self.label_n_mosse.config(text=f"{self.numero_tentativi}")
            self.label_alunno.config(text=f"{self.appello.chiamare_ragazzo()}({modificatore})")
            print('qui')
        
    
    def on_closing(self):
        risposta = messagebox.askokcancel("Conferma", "(Attenzione!!!)Se chiudi la finestra l'appello causale viene resettato - Sei sicuro di voler chiudere la finestra?")
        if risposta:
            self.parent.destroy()
        
    def __get_exe_path(self):
        if getattr(sys, 'frozen', False):
            # L'applicazione è congelata (eseguibile standalone)
            return sys.executable
        elif __file__:
            # L'applicazione è in esecuzione come script
            return os.path.abspath(__file__)

    def __get_current_directory(self):
        return os.path.dirname(self.__get_exe_path())

    def __setting_submit(self):
        self.mod_min = int(self.spinbox_min.get())
        self.mod_max = int(self.spinbox_max.get())
        if(self.mod_min <= self.mod_max):
            self.numero_tentativi = int(self.entry.get())
            self.label_n_mosse.config(text=f"{self.numero_tentativi}")
            
            self.spinbox_max['state'] = 'disabled'
            self.spinbox_min['state'] = 'disabled'

            cur_dir = os.path.basename(os.getcwd())
            print(cur_dir)
            if cur_dir == 'Programma_Appello':
                dir = os.path.join(self.__get_current_directory(), 'classi')
            else:
                dir = os.path.join(self.__get_current_directory(), '..', 'classi')
            print(dir)

            scelta = self.combobox.get()
            print(f'scelta:{scelta}')
            if(scelta not in self.combo_list_classi):
                print('Err classe inesistente')
            else:
                if scelta in self.combo_list_classi:
                    self.appello.set_classe(dir, scelta)
                    print('Appello: ' + scelta + ' inserito')
                self.combobox['state'] = 'disabled'
            
            for widget in self.setting_frame.winfo_children():
                widget.configure(state='disabled')
            self.setting_frame.config(text='BLOCCATO')

            for widget in self.estr_frame.winfo_children():
                widget.configure(state='normal')
            self.estr_frame.config(text='Estrazione')
        else:
            self.setting_frame.config(text="Errore min/max")

    def reset(self):
        for widget in self.setting_frame.winfo_children():
            widget.configure(state='normal')
        self.setting_frame.config(text='Impostazioni')
         
        for widget in self.setting_frame.winfo_children():
            widget.configure(state='normal')
        self.setting_frame.config(text='Impostazioni')

        for widget in self.estr_frame.winfo_children():
            widget.configure(state='disabled')
        self.estr_frame.config(text='BLOCCATO')
        print('reset')
    
    def __scan_list(self):
        cur_dir = os.path.basename(os.getcwd())
        print(cur_dir)
        if cur_dir == 'Programma_Appello':
            dir = os.path.join(self.__get_current_directory(), 'classi')
        else:
            dir = os.path.join(self.__get_current_directory(), '..', 'classi')
        file_list = os.listdir(dir)
        print(file_list)
        return file_list

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('xpnative') #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    print(font.families())
    root.title("Appello Casuale")
    root.geometry("800x500")
    root.resizable(False, False)
    print(style.theme_names())

    app = App(root)
    app.pack(fill="both", expand=True)
    
    # Set a minsize for the window, and place it in the middle of the screen
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


#per l'installer python PyInstaller -m nomefile.py --onefile -w