#!/usr/bin/env python3
#
import threading
from gui_stream.gui.models import ABCNotifyProvider
from gui_stream.gui.core.core_files import PreferencesApp
from gui_stream.gui.utils import File, Directory, AppInputFiles, LibraryDocs
from gui_stream.gui.core import (
    AppPage,
    WidgetColumn,
    WidgetRow,
    WidgetFilesSheetRow,
    WidgetProgressBar,
    WidgetScrow,
    LibProgress,
    AppFileDialog,

)

from gui_stream.gui.core.app_progress_bar import ProgressBarAdapter
from gui_stream.sheets.load import SheetInputStream

import pandas as pd
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

#========================================================#
# Filtrar TOI
#========================================================#
class PageDocsToi(AppPage):
    """
        Recebe uma planilha com texto bruto OCR de obtido de alguns documentos
    e filtra os dados UC e TOI.
    """
    def __init__(self, *, controller):
        super().__init__(controller=controller)
        self.current_page_name = '/home/page_toi'
        # Frame Principal desta Tela
        
        self.initUI()
        
    def initUI(self):
        pass
        
    def select_files_pdf(self):
        """Importar arquivos PDF"""
        pass
    
    def action_move_files(self):
        pass
        
    def _run_action_move_files(self):
        """Mover os arquivos com base no texto reconhecido OCR"""
        pass
        
    def convert_to_excel(self):
        pass
    
    def _execute_convert_to_excel(self):
        """filtrar TOI"""
        pass
        
    def set_size_screen(self):
        self.controller.geometry("625x260")
        self.controller.title(f"Especial")

#========================================================#
# Filtrar Planilha
#========================================================#
class PageSoupSheets(AppPage):
    """
        Página para filtrar textos em planilha Excel.
    
    """
    def __init__(self, *, controller):
        super().__init__(controller=controller)
        self.current_page_name = '/home/soup_sheets'
        #                  {basename(): {sheet_name: DataFrame()}}
        self.files_data: dict[str, dict[str, pd.DataFrame]] = {}
        #                  {basename(): File()}
        self.files_paths: dict[str, File] = {}
        self.files_loaded: set[str] = set()
        self.data: pd.DataFrame = None
        self.file_sheet_filter: File = None
        self.initUI()
        # Inscrever-se no notificador de arquivos
        # e notificador de tema/estilo
        self.controller.app_files.add_observer(self)
        self.controller.app_prefs.add_observer(self) # Preferências do usuário.
        self.controller.app_prefs.notify_all()
        
    def initUI(self):
        # Frames
        self.frame_widgets = ttk.Frame(self.frame_main)
        self.frame_widgets.pack(expand=True, fill='both', padx=1, pady=1)
        # Frame input Files
        self.frame_input = ttk.Frame(self.frame_widgets, style='DarkPurple.TFrame')
        self.frame_input.pack(expand=True, fill='both', padx=2, pady=2)
        
        # Frame para edição de dados
        self.frame_edit_sheet = ttk.Frame(self.frame_widgets)
        self.frame_edit_sheet.pack(expand=True, fill='both', padx=1, pady=1)
        # Frame para botões centrais
        self.frame_buttons = ttk.Frame(self.frame_edit_sheet, style='DarkPurple.TFrame')
        self.frame_buttons.pack(expand=True, fill='both', padx=1, pady=1)
        
        # Frame parar filtrar os dados.
        self.frame_filter = ttk.Frame(self.frame_edit_sheet)
        self.frame_filter.pack(expand=True, fill='both', padx=1, pady=1)
        
        # Frame para concatenar
        self.frame_concat = ttk.Frame(self.frame_edit_sheet, style='DarkPurple.TFrame')
        self.frame_concat.pack(expand=True, fill='both', padx=1, pady=1)
        
        # Frame para nomes das abas e arquivos
        self.frame_info_sheets = ttk.Frame(self.frame_widgets)
        self.frame_info_sheets.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        # Frame para srow bar.
        self.frame_scrow = ttk.Frame(self.frame_widgets, style='Black.TFrame')
        self.frame_scrow.pack(expand=True, fill='both', padx=2, pady=2)
        # Frame para opções de exportação.
        self.frame_export = ttk.Frame(self.frame_widgets, style='Black.TFrame')
        self.frame_export.pack(expand=True, fill='both', padx=1, pady=1)
        # Frame para barra de progresso.
        self.frame_pbar = ttk.Frame(self.frame_main)
        self.frame_pbar.pack(expand=True, fill='both', padx=2, pady=1)
        
        #-----------------------------------------------------#
        # Container superior
        #-----------------------------------------------------#
        # Input Files
        self.w_row_files: WidgetFilesSheetRow = WidgetFilesSheetRow(
                self.frame_input, 
                controller=self.controller
            )
        
        #-----------------------------------------------------#
        # Container a esquerda
        #-----------------------------------------------------#
        # Combobox para mostrar os arquivos
        self.frame_combo_files = ttk.Frame(self.frame_info_sheets, style='Black.TFrame')
        self.frame_combo_files.pack(expand=True, fill='both', padx=1, pady=1)
        self.lb_info_sheets = ttk.Label(self.frame_combo_files, text='Arquivos e Abas')
        self.lb_info_sheets.pack(expand=True, fill='both', padx=1, pady=1)
        self.lb_files_names = ttk.Label(self.frame_combo_files, text='Arquivo: ')
        self.lb_files_names.pack(expand=True, fill='both')
        self.combobox_files_names: ttk.Combobox = ttk.Combobox(self.frame_combo_files, values=['-'])
        self.combobox_files_names.pack()
        self.combobox_files_names.set('-')
        
        # Combobox para mostrar as abas do arquivo.
        self.frame_combo_sheet_names = ttk.Frame(self.frame_info_sheets)
        self.frame_combo_sheet_names.pack()
        self.lb_sheet_names = ttk.Label(self.frame_combo_sheet_names, text=' Aba: ')
        self.lb_sheet_names.pack()
        self.combobox_sheet_names = ttk.Combobox(self.frame_combo_sheet_names, values=['-'])
        self.combobox_sheet_names.set('-')
        self.combobox_sheet_names.pack()
        self.combobox_files_names.bind("<<ComboboxSelected>>", self.update_combobox_sheet_names)
        
        # Combobox para mostar as colunas da aba selecionada
        self.frame_combo_columns = ttk.Frame(self.frame_info_sheets)
        self.frame_combo_columns.pack()
        self.lb_columns = ttk.Label(self.frame_combo_columns, text='Coluna: ')
        self.lb_columns.pack()
        self.combobox_columns = ttk.Combobox(self.frame_combo_columns, values=['-'])
        self.combobox_columns.set('-')
        self.combobox_columns.pack()
        self.combobox_columns.bind("<<ComboboxSelected>>", self.update_scrow_col)
        
        # Frame para o botão carregar
        self.frame_buttons_read = ttk.Frame(self.frame_info_sheets)
        self.frame_buttons_read.pack(expand=True, fill='both', padx=1, pady=1)
        self.w_col_buttons = WidgetColumn(self.frame_buttons_read)
        self.w_col_buttons.add_button('Carregar dados', self.set_current_data_frame)        
        
        #-----------------------------------------------------#
        # Container central
        #-----------------------------------------------------#
        # Botões de ação.
        self.frame_lb_info = ttk.Frame(self.frame_buttons)
        self.frame_lb_info.pack(expand=True, fill='both', padx=1, pady=1)
        self.lb_info_actions = ttk.Label(self.frame_lb_info, text='Edição e filtro de dados')
        self.lb_info_actions.pack()
        self.w_row_buttons = WidgetRow(self.frame_buttons)        
        self.w_row_buttons.add_button('Apagar Linhas vazias', self.action_delet_null_lines)
        self.w_row_buttons.add_button('Apagar Coluna selecionada', self.action_delet_current_column)
        self.w_row_buttons.add_button('Filtrar Texto', self.action_filter_text)
        self.w_row_buttons.add_button('Filtrar Arquivo', self.action_filter_with_file)
        
        #-----------------------------------------------------#
        # Container filtro de dados
        #-----------------------------------------------------#
        # Frame para o texto a ser filtrado
        self.frame_filter_main = ttk.Frame(self.frame_filter)
        self.frame_filter_main.pack(expand=True, fill='both', padx=2, pady=1)
        self.lb_info_filter = ttk.Label(self.frame_filter_main, text='Filtrar texto ou arquivo')
        self.lb_info_filter.pack()
        
        self.frame_filter_text = ttk.Frame(self.frame_filter, style='DarkPurple.TFrame')
        self.frame_filter_text.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        self.lb_text_filter = ttk.Label(self.frame_filter_text, text='Filtrar texto: ')
        self.lb_text_filter.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        self.text_entry: ttk.Entry = ttk.Entry(self.frame_filter_text)
        self.text_entry.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        self.frame_filter_file = ttk.Frame(self.frame_filter, style='DarkPurple.TFrame')
        self.frame_filter_file.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        self.btn_select_sheet_filter = ttk.Button(
                self.frame_filter_file, 
                text='Planilha filtro', 
                command=self.open_file_filter,
            )
        self.btn_select_sheet_filter.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        self.lb_filter_file = ttk.Label(self.frame_filter_file, text='Nenhum arquivo selecionado')
        self.lb_filter_file.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        # Concatenar
        self.btn_concat: ttk.Button = ttk.Button(
                self.frame_concat, 
                text='Concatenar', 
                command=self.action_concat_columns,
            )
        self.btn_concat.pack(side=tk.LEFT)
        # combo com 3 colunas
        self.combo_conc_1 = ttk.Combobox(self.frame_concat, values=[''])
        self.combo_conc_1.set('-')
        self.combo_conc_1.pack(side=tk.LEFT)
        
        self.combo_conc_2 = ttk.Combobox(self.frame_concat, values=[''])
        self.combo_conc_2.set('-')
        self.combo_conc_2.pack(side=tk.LEFT)
        
        self.combo_conc_3 = ttk.Combobox(self.frame_concat, values=[''])
        self.combo_conc_3.set('-')
        self.combo_conc_3.pack(side=tk.LEFT)
        
        # Scrow bar
        self.lb_info_scrow = ttk.Label(self.frame_scrow, text='Texto das coluna(s)')
        self.lb_info_scrow.pack(expand=True, fill='both', padx=2, pady=2)
        self.scrow = WidgetScrow(self.frame_scrow, height=5)
        
        # Exportar dados.
        self.frame_lb_export = ttk.Frame(self.frame_export)
        self.frame_lb_export.pack(expand=True, fill='both', padx=1, pady=1)
        self.lb_info_export = ttk.Label(self.frame_lb_export, text='Exportação de dados')
        self.lb_info_export.pack()
        
        self.frame_buttons_export = ttk.Frame(self.frame_export)
        self.frame_buttons_export.pack(expand=True, fill='both', padx=1, pady=1)
        self.checkbox_var = tk.IntVar()
        self.checkbox = ttk.Checkbutton(
                                self.frame_buttons_export,
                                text="Exportar arquivos filtrando itens da coluna atual",
                                variable=self.checkbox_var,
                                command=()
                            )
        self.checkbox.pack()
        self.w_row_export = WidgetRow(self.frame_buttons_export)
        self.w_row_export.add_button('Exportar Dado', self.action_export_current_data)
        self.w_row_export.add_button('Exportar Coluna', self.action_export_current_column)
        
        #-----------------------------------------------------#
        # Container inferior
        #-----------------------------------------------------#
        # Barra de progresso
        self.pbar: WidgetProgressBar = WidgetProgressBar(
                self.frame_pbar,
                mode=LibProgress.DETERMINATE
        )
        
    def update_theme(self):
        if self.controller.app_prefs.dark_mode == True:
            self.frame_main.config(style='Black.TFrame')
            self.frame_widgets.config(style='Black.TFrame')
            self.frame_widgets.pack(expand=True, fill='both', padx=2, pady=2)
            self.frame_pbar.config(style='Black.TFrame')
            
        elif self.controller.app_prefs.dark_mode == False:
            self.frame_widgets.config(style='CinzaFrame.TFrame')
            self.frame_widgets.pack(expand=True, fill='both', padx=2, pady=2)
            self.frame_main.config(style='CinzaFrame.TFrame')
            self.frame_pbar.config(style='CinzaFrame.TFrame')
            
    def action_delet_null_lines(self):
        self.thread_main_create(self._run_delet_null_lines)
    
    def _run_delet_null_lines(self):
        if not self.combobox_columns.get() in self.data.columns.tolist():
            messagebox.showerror(
                'Coluna não encontrada', f'A coluna {self.combobox_columns.get()} não existe no dado atual!'
            )
            return
        
        self.pbar.start()
        self.pbar.update(0, f'Apagando linhas vazias: {self.combobox_columns.get()}')
        col = self.combobox_columns.get()
        self.data = self.data.dropna(subset=[self.combobox_columns.get()])
        self.data = self.data[self.data[col] != "nan"]
        self.data = self.data[self.data[col] != "None"]
        self.data = self.data[self.data[col] != ""]
        self.pbar.update(100, f'Linhas vazias apagadas: {self.combobox_columns.get()}')
        self.thread_main_stop()
    
    def action_delet_current_column(self):
        self.thread_main_create(self._run_delet_current_column)
    
    def _run_delet_current_column(self):
        current_column = self.combobox_columns.get()
        self.pbar.update(0, f'Apagando coluna {current_column}')
        if not current_column in self.data.columns.tolist():
            messagebox.showerror('Coluna não encontrada', f'A coluna {current_column} não existe no dado atual!')
            return
        self.data = self.data.drop([current_column], axis=1)
        self.update_combobox_columns()
        self.pbar.update(100, f'Coluna apagada: {current_column}')
    
    def action_concat_columns(self):
        self.thread_main_create(self._run_action_concat)
    
    def _run_action_concat(self):
        col1 = self.combo_conc_1.get()
        col2 = self.combo_conc_2.get()
        col3 = self.combo_conc_3.get()
        if not col1 in self.data.columns.tolist():
            messagebox.showwarning('Coluna inválida', f'Verifique a coluna {col1}')
            return
        if not col2 in self.data.columns.tolist():
            messagebox.showwarning('Coluna inválida', f'Verifique a coluna {col2}')
            return
        if not col3 in self.data.columns.tolist():
            messagebox.showwarning('Coluna inválida', f'Verifique a coluna {col3}')
            return
        self.pbar.start()
        self.pbar.update(0, 'Concatenando colunas')
        # Concatena as colunas 'coluna1', 'coluna2' e 'coluna3'
        new_col = f'{col1}_{col2}_{col3}'
        #self.current_data[new_col] = self.current_data[col1] + self.current_data[col2] + self.current_data[col3]
        # Concatena as colunas com um separador (por exemplo, "-")
        self.data[new_col] = self.data[col1].str.cat([self.data[col2], self.data[col3]], sep='_')

        self.update_combobox_columns()
        self.pbar.update(100, 'Colunas concatenadas com sucesso!')
        self.thread_main_stop()
    
    def action_export_current_data(self):
        if (self.data is None) or (self.data.empty):
            messagebox.showerror('Dados vazios', 'Clique no botão carregar dados!')
            return
        if not self.combobox_columns.get() in self.data.columns.tolist():
            messagebox.showerror(
                'Coluna inválida', f'A coluna {self.combobox_columns.get()} não existe!'
            )
            return
        
        if self.checkbox_var.get() == 1:
            self.thread_main_create(self._run_export_current_data_multi)
        else:
            self.thread_main_create(self._run_export_current_data)
        
    def _run_export_current_data_multi(self):
        col = self.combobox_columns.get()
        values = self.data[col].drop_duplicates().values.tolist()
        out_dir: Directory = self.controller.app_files.save_dir.concat('Exportado', create=True)
        max_values = len(values)
        self.pbar.start()
        self.scrow.clear()
        for num, item in enumerate(values):
            output_file: File = out_dir.join_file(f'{item}.xlsx')
            prog = (num+1)/(max_values) * (100)
            self.pbar.update(prog, f'Exportando:[{num+1} de {max_values}] {output_file.basename()}')
            self.scrow.update_text(f'Exportando:[{num+1} de {max_values}] {output_file.basename()}')
            try:
                df = self.data[self.data[col] == item]
            except Exception as e:
                self.scrow.update_text(e)
            else:
                df.to_excel(output_file.absolute(), index=False)
        self.pbar.update(100, 'Operação finalizada!')        
        self.thread_main_stop()
    
    def _run_export_current_data(self):
        output_file: File = self.controller.app_files.save_dir.join_file('output_data.xlsx')
        self.pbar.start()
        self.pbar.update(0, f'Exportando arquivo: {output_file.basename()}')
        self.data.to_excel(output_file.absolute(), index=False)
        
        self.pbar.update(100, 'OK')
        self.thread_main_stop()
    
    def action_export_current_column(self):
        self.thread_main_create(self._run_action_export_current_column)
    
    def _run_action_export_current_column(self):
        current_column = self.combobox_columns.get()
        if not current_column in self.data.columns.tolist():
            messagebox.showerror('Coluna não encontrada', f'A coluna {current_column} não existe no dado atual!')
            return
        output_path: File = self.controller.app_files.save_dir.join_file(f'output-{current_column}.xlsx')
        self.pbar.update(0, f'Exportando coluna {current_column}')
        df = self.data[[current_column]]
        df = df.drop_duplicates()
        df.to_excel(output_path.absolute(), index=False)
        self.pbar.update(100, f'Coluna exportada! {current_column}')
        self.thread_main_stop()
        
    def action_filter_text(self):
        self.thread_main_create(self._run_action_filter_text)
    
    def _run_action_filter_text(self):
        current_text: str = self.text_entry.get()
        current_column: str = self.combobox_columns.get()
        if (current_text is None) or (current_text == ""):
            messagebox.showerror('Texto Vazio', 'Adicione textos na caixa de texto!')
            return
        self.pbar.update(0, f'Filtrando texto: {current_text} na coluna: {current_column}')
        # df = self.data[self.data[col].str.contains(text, case=False, na=False)]
        self.data = self.data[self.data[current_column] == current_text]
        self.pbar.update(100, f'Texto filtrado: {current_text}')
        self.thread_main_stop()
    
    def action_filter_with_file(self):
        self.thread_main_create(self._run_action_filter_with_file)

    def _run_action_filter_with_file(self):
        current_col: str = self.combobox_columns.get()
        if not current_col in self.data.columns.tolist():
            messagebox.showerror('Coluna inválida', f'A coluna {current_col} não existe no Dado atual!')
            return
        if (self.file_sheet_filter is None) or (not self.file_sheet_filter.path.exists()):
            messagebox.showinfo('Aviso', 'Planilha de filtros, inválida!')
            return
        
        # Obter a coluna a ser filtrada no arquivo de filtro
        stream = SheetInputStream(self.file_sheet_filter, progress=self.pbar.progress_adapter)
        df = stream.read().drop_duplicates()
        if not self.combobox_columns.get() in df.columns.tolist():
            messagebox.showerror('Erro', f'A coluna {self.combobox_columns.get()} não existe na planilha de filtro!')
            return
        values: list[str] = df.astype('str')[self.combobox_columns.get()].values.tolist()
        df_filter = self.data[self.data[self.combobox_columns.get()].isin(values)]
        self.data = df_filter.astype('str')
        
    def open_file_filter(self):
        file: str = self.controller.app_files.file_dialog.open_file_sheet()
        if (file is None) or (file == ''):
            return
        self.file_sheet_filter = File(file)
        self.lb_filter_file.config(text=f'Planilha para filtro: {self.file_sheet_filter.basename()}')
        
    def update_combobox_sheet_names(self, event=None):
        current_file_name: str = self.combobox_files_names.get()
        current_file_dict: dict[str, dict[str, pd.DataFrame]] = self.files_data[current_file_name]
        sheet_values: list = list(current_file_dict.keys())
        self.combobox_sheet_names['values'] = sheet_values
        self.combobox_sheet_names.set(sheet_values[0] or '-')
        
    def update_combobox_columns(self):
        if self.data is None:
            current_file = self.combobox_files_names.get()
            if not current_file in self.files_paths:
                return
            
            current_file_path: File = self.files_paths[current_file]
            current_sheet = self.combobox_sheet_names.get()
            #self.data = pd.read_excel(current_file_path.absolute(), sheet_name=current_sheet)
            stream = SheetInputStream(current_file_path, sheet_name=current_sheet, progress=self.pbar.progress_adapter)
            self.data = stream.read().astype('str')
            self.files_data[current_file][current_sheet] = self.data
            
        columns = self.data.columns.tolist()        
        self.combobox_columns['values'] = columns
        self.combobox_columns.set(columns[0] or '-')
        self.combo_conc_1['values'] = columns
        self.combo_conc_2['values'] = columns
        self.combo_conc_3['values'] = columns
        
    def update_scrow_col(self, event=None):
        col = self.combobox_columns.get()
        if not col in self.data.columns.tolist():
            return
        values = self.data[col].values.tolist()
        self.scrow.clear()
        for num, item in enumerate(values):
            self.scrow.update_text(f'Coluna {col} index {num} => {item}')
            if num >= 10:
                break
        
    def set_current_data_frame(self):
        """
            Alterar a propriedade que contém o DataFrame atual
        com base no arquivo selecionado na combobox.
        """
        if self.controller.app_files.num_files_sheet == 0:
            messagebox.showinfo('Aviso', 'Adicione planilhas para prosseguir!')
            return
        self.thread_main_create(self._run_set_current_data_frame)
    
    def _run_set_current_data_frame(self):
        current_file_name:str = self.combobox_files_names.get()
        current_sheet_name: str = self.combobox_sheet_names.get()
        if not current_file_name in self.files_paths:
            file_path: File = self.controller.app_files.get_files_sheets()[0]
            current_sheet_name = None
        else:
            file_path: File = self.files_paths[current_file_name]
            
        if len(self.files_data) == 0:
            # Dicionário vazio, necessário carregar do arquivo
            stream = SheetInputStream(file_path, sheet_name=current_sheet_name, progress=self.pbar.progress_adapter)
            self.data = stream.read()
            self.files_data[file_path.basename()][current_sheet_name] = self.data
            self.files_paths[file_path.basename()] = file_path
        elif self.files_data[current_file_name][current_sheet_name].empty: 
            # DataFrame vazio, necessário carregar do arquivo
            file_path: File = self.files_paths[current_file_name]
            stream = SheetInputStream(file_path, sheet_name=current_sheet_name, progress=self.pbar.progress_adapter)
            self.data = stream.read().astype('str')
            self.files_data[current_file_name][current_sheet_name] = self.data
        else:
            # o arquivo já foi carregado anteriormente, apenas alterar a propriedade.
            self.data = self.files_data[current_file_name][current_sheet_name]
        self.update_combobox_columns()
        self.thread_main_stop()
        
    def update_files_sheet_names(self):
        """
            Atualizar os nomes das abas de cada planilha selecionada pelo usuário.
        """
        self.thread_main_create(self._run_update_sheet_names)
    
    def _run_update_sheet_names(self):
        self.pbar.update(0, f'Atualizando aguarde.')
        files = self.controller.app_files.get_files_sheets()
        for num, file in enumerate(files):
            self.pbar.update((num/len(files)*100), f'Lendo: {file.basename()}')
            
            if not file.basename() in self.files_paths:
                # Ler as abas do arquivo atual, e atualizar o combo.
                stream = SheetInputStream(file, progress=self.pbar.progress_adapter)
                current_sheet_names = stream.get_sheet_names()
                self.files_paths[file.basename()] = file
                #with pd.ExcelFile(file.absolute()) as xls:
                #    current_sheet_names = xls.sheet_names
                #current_file_values: dict[str, pd.DataFrame] = stream.read_sheets()
                current_file_values: dict[str, pd.DataFrame] = {}
                for sheet_name in current_sheet_names:
                    # Inicializar um DataFrame vazio para cada aba da planilha.
                    # os valores reais serão carregados apenas quando necessário o uso.
                    current_file_values[sheet_name] = pd.DataFrame()
                self.files_data[file.basename()] = current_file_values
        # Atualizar os combos com nome de arquivo, abas e colunas.
        files_list = list(self.files_data.keys())
        self.combobox_files_names['values'] = files_list
        self.combobox_files_names.set(files_list[0] or '-')
        self.update_combobox_sheet_names()
        self.update_combobox_columns()
        self.pbar.update(100, 'OK')
        self.thread_main_stop()
       
    def update_notify(self, notify_provide:PreferencesApp = None):
        """
            Sempre que esse método for chamado, significa que o usuário
        alterou a seleção de arquivos, limpar ou adicionar. Sendo necessário
        atualizar as propriedades de DataFrame e arquivos.
        """
        if isinstance(notify_provide, PreferencesApp):
            self.update_theme()    
            return
        
        if self.controller.app_files.num_files == 0:
            # O usuário limpou os arquivos
            self.files_data.clear()
            self.files_paths.clear()
            self.combobox_columns['values'] = ['-']
            self.combobox_columns.set('-')
            self.combobox_files_names['values'] = ['-']
            self.combobox_files_names.set('-')
            self.combobox_sheet_names['values'] = ['-']
            self.combobox_sheet_names.set('-')
            return
        self.update_files_sheet_names()
        
    def set_size_screen(self):
        """Redimensionar o tamanho da janela quando esta página for aberta."""
        self.controller.title("Filtra texto em planilhas")
        self.controller.geometry("670x470")

    def update_state(self):
        """
            Carregar algumas informações enquanto a janela é exibida.
        """
        pass

#========================================================#
# Planilhar Pasta
#========================================================#
class PageFilesToExcel(AppPage):
    """
        Página para planilhar pasta.
    """
    def __init__(self, *, controller):
        super().__init__(controller=controller)
        self.current_page_name = '/home/folder_to_excel'
        
        self.initUI()

    def initUI(self):
        pass
     
    
    def convert_folder_to_excel(self):
        """
            Planilhar os arquivos selecionados.
        """
        pass
        
    def _operation_convet_folder_to_excel(self):
        """
            -
        """
        pass
        
    def convert_folder_to_csv(self):
        """
            -
        """
        pass
        
    def _operation_convert_to_csv(self):
        pass
        
    def __get_info_files(self) -> pd.DataFrame:
        """
            Obter uma lista de com os nomes dos arquivos selecionados pelo usuário.
        """
        pass
        
    def set_size_screen(self):
        self.controller.geometry("625x260")
        self.controller.title(f"Planilhar Pasta")

    def update_state(self):
        pass
    
    
#========================================================#
# Mover arquivos
#========================================================#
class PageMoveFiles(AppPage):
    def __init__(self, *, controller):
        super().__init__(controller=controller)
        self.current_page_name = '/home/page_mv_files'
        
        self.initUI()

    def initUI(self):
        pass
        
    def action_move_files(self):
        pass
        
    def __execute_move_files(self):
        pass
    
    def get_data_move_files(self) -> pd.DataFrame | None:
        """
            Usar o DataFrame da planilha de dados para gerar uma coluna com o nome dos 
        arquivos a serem movidos/renomeados
        """
        pass
                
    def action_export_sheet(self):
        pass
        
    def __execute_export_sheet(self):
        pass
        
    def _update_page(self):
        pass
        
    def __execute_update_page(self):
        pass

    def set_size_screen(self):
        self.controller.geometry("645x300")
        self.controller.title(f"Mover arquivos")

    def update_state(self):
        pass



