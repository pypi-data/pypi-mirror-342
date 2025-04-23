#!/usr/bin/env python3
from __future__ import annotations
import os
import threading
from typing import List, Callable
from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple, List, Dict
from time import sleep
from tkinter import (
    ttk,
    Tk,
    Menu,  
    filedialog, 
    messagebox,
)
import tkinter as tk 

from gui_stream.gui.models import ABCNotifyProvider, ABCObserver
from gui_stream.gui.utils import (
    File,
    Directory,
    AppInputFiles,
    UserFileSystem,
    AppJsonConvert,
    AppJsonData,
    LibraryDocs,
    ABCObserver,
    ABCNotifyProvider,
    KERNEL_TYPE,
) 

from gui_stream.gui.core.core_files import (
    AppFileDialog, AppInputFiles, AppSelectedFiles, PreferencesApp, PreferencesDir,
)

from gui_stream.gui.core.app_progress_bar import (
    ABCProgressBar,
    ProgressBarAdapter,
    ProgressBarTkIndeterminate,
    ProgressBarTkDeterminate,
)

class LibProgress(Enum):
    INDETERMINATE = 'indeterminate'
    DETERMINATE = 'determinate'
   
   
class AppStyles(object):
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.rootStyle = ttk.Style(self.root)
        
        #==============================================================#
        # Estilo para os Frames
        #==============================================================#
        # Defina as cores para o estilo "LightFrame"
        self.styleLight = ttk.Style(self.root)
        self.styleLight.configure(
                "LightFrame.TFrame",
                background="white",
                relief="solid",
                borderwidth=1
            )
        
        self.styleGray = ttk.Style(self.root)
        self.styleGray.configure(
                    "CinzaFrame.TFrame",
                    background="lightgray",
                    relief="solid",
                    borderwidth=1
                )
        
        self.styleFrameBlack = ttk.Style(self.root)
        self.styleFrameBlack.theme_use("default")
        self.styleFrameBlack.configure(
                            "Black.TFrame", 
                            background="#2C2C2C"
                        )  # Cor de fundo preta

        # Fundo Roxo Claro
        self.styleFrameLightPurple = ttk.Style(self.root)
        self.styleFrameLightPurple.theme_use("default")
        self.styleFrameLightPurple.configure(
            "LightPurple.TFrame",  # Nome do estilo alterado
            background="#9370DB"   # Roxo claro (MediumPurple)
        )
        
        # Fundo Roxo Escuro
        self.styleFrameDarkPurple = ttk.Style(self.root)
        self.styleFrameDarkPurple.theme_use("default")
        self.styleFrameDarkPurple.configure(
            "DarkPurple.TFrame", 
            background="#4B0082"  # Roxo escuro
        )
        
        # Fundo Cinza escuro
        self.styleFrameDarkGray = ttk.Style(self.root)
        self.styleFrameDarkGray.theme_use("default")
        self.styleFrameDarkGray.configure(
            "DarkGray.TFrame",  # Nome do estilo alterado
            background="#2F4F4F"  # Cinza escuro (DarkSlateGray)
        )
        
        # Laranja escuro
        self.styleFrameDarkOrange = ttk.Style(self.root)
        self.styleFrameDarkOrange.theme_use("default")
        self.styleFrameDarkOrange.configure(
            "DarkOrange.TFrame",  # Nome do estilo alterado
            background="#FF8C00"  # Laranja escuro (DarkOrange)
        )

        #==============================================================#
        # Estilo para os botões
        #==============================================================#
        self.styleButtonGreen = ttk.Style(self.root)
        self.styleButtonGreen.theme_use("default")
        self.styleButtonGreen.configure(
                "TButton",
                foreground="white",
                background="#4CAF50",  # Verde padrão
                font=("Helvetica", 12),
                #padding=10,
            )
        
        self.styleButtonGreen.map(
            'TButton',             # Nome do estilo
            background=[('active', 'darkblue')],  # Cor de fundo ao passar o mouse
            foreground=[('disabled', 'gray')]    # Cor do texto quando desabilitado
        )
        
        self.styleButtonBlue = ttk.Style(self.root)
        self.styleButtonBlue.configure(
            "Custom.TButton",         # Nome do estilo
            font=("Helvetica", 14),   # Fonte personalizada
            foreground="white",       # Cor do texto
            background="blue"         # Cor de fundo
        )
        
        #==============================================================#
        # Estilo para Labels
        ##==============================================================#
        self.stylePurple = ttk.Style(self.root)
        self.stylePurple.configure(
            "LargeFont.TLabel",  # Nome do estilo
            font=("Helvetica", 14),  # Fonte maior
            background="#9370DB",    # Cor de fundo roxo claro
            foreground="white"       # Cor do texto branco
        )
        
        # Default
        self.styleDefault = ttk.Style(self.root)
        self.styleDefault.configure(
            "BoldLargeFont.TLabel",  # Nome do estilo
            font=("Helvetica", 14, "bold")  # Fonte maior e negrito
        )


class ThreadManagerBase(object):
    _instance = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ThreadManagerBase, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.threadMain = None
        self.threadStopEvent = threading.Event()
        self.threadRunning = False
        self._running = False

    def is_running(self) -> bool:
        return self.threadRunning and self._running

    def thread_main_create(self, cmd: callable) -> None:
        """Cria e inicia a thread principal da operação."""
        if self.threadRunning:
            print(f'{self.__class__.__name__}: Já existe uma operação em andamento.')
            return

        if self.threadMain is not None:
            print(f'{self.__class__.__name__}: Thread principal já foi criada.')
            return

        self.threadStopEvent.clear()
        self._running = True
        self.threadRunning = True

        def wrapper():
            print(f'{self.__class__.__name__}: Iniciando execução da thread...')
            try:
                cmd()
                
            except Exception as e:
                print(f'{self.__class__.__name__}: Erro na thread: {e}')
            finally:
                self._running = False
                self.threadRunning = False
                self.threadMain = None
                print(f'{self.__class__.__name__}: Thread finalizada.')

        self.threadMain = threading.Thread(target=wrapper, daemon=True)
        self.threadMain.start()
        print(f'{self.__class__.__name__}: Thread principal criada.')

    def thread_main_stop(self):
        """Sinaliza para a thread parar e aguarda sua finalização."""
        if self.threadMain and self.threadMain.is_alive():
            print(f'{self.__class__.__name__}: Parando a Thread principal com Event.set()')
            self.threadStopEvent.set()
            self.threadMain.join(timeout=3)

            if self.threadMain.is_alive():
                print(f'{self.__class__.__name__}: Atenção: Thread ainda viva após timeout 3.')
            else:
                print(f'{self.__class__.__name__}: Thread parada com sucesso.')

        self.threadMain = None
        self._running = False
        self.threadRunning = False


class ControllerApp(Tk):
    """
        Controlador de páginas
    """
    _instance_controller = None

    def __new__(cls, *args, **kwargs):
        if cls._instance_controller is None:
            cls._instance_controller = super(ControllerApp, cls).__new__(cls)
        return cls._instance_controller
    
    def __init__(
                    self, 
                    *,
                    app_prefs: PreferencesApp = PreferencesApp.create_default(), 
                    app_files: AppSelectedFiles = AppSelectedFiles(AppFileDialog()), 
                ):
        super().__init__()
        self.app_prefs: PreferencesApp = app_prefs
        self.app_files: AppSelectedFiles = app_files
        self.navigator_pages: Navigator = Navigator(controller=self)
            
    def set_local_user_prefs(self, file_json: File):
        """
            Ler as configurações de um arquivo JSON local se existir
        """
        if not file_json.path.exists():
            return
        
        convert: AppJsonConvert = AppJsonConvert.from_file(file_json)
        json_data_dict: dict = convert.to_json_data().to_dict()
        config_app: PreferencesApp = PreferencesApp.create_default()
        if 'tesseract_path' in json_data_dict:
            config_app.tesseract_path = json_data_dict['tesseract_path']
        if 'tesseract_data_dir' in json_data_dict:
            config_app.tesseract_data_dir = json_data_dict['tesseract_data_dir']
        self.app_prefs = config_app
            
        print('-----------------------------------------------')
        for _k in json_data_dict.keys():
            print(f'{_k}: {json_data_dict[_k]}')
        print('-----------------------------------------------')
        
    def go_back_page(self):
        self.navigator_pages.pop()
        
    def exit_app(self):
        current_page: AppPage = self.navigator_pages.current_page
        if current_page is not None:
            current_page.thread_main_stop()
            
        # Espera a thread terminar (se ainda existir)
        if current_page.threadManager.threadMain is not None:
            print("Aguardando thread finalizar...")
            current_page.threadManager.threadMain.join(timeout=5)
        print("Thread finalizada. Encerrando GUI.")
        self.quit()
       

class AppPage(ttk.Frame, ABCObserver):
   
    def __init__(self, *, controller:ControllerApp):
        super().__init__(controller)
        self.controller:ControllerApp = controller
        #
        self.current_page_name:str = None
        self.frame_main:ttk.Frame = ttk.Frame(self, relief="groove", style="Black.TFrame")
        self.frame_main.config(style="Black.TFrame")
        self.frame_main.pack(expand=True, fill='both', padx=1, pady=1)
        #
        self.threadManager: ThreadManagerBase = ThreadManagerBase()
        self.set_size_screen()
        
    def update_notify(self, notify_provide:ABCNotifyProvider = None):
        """
            Receber notificações externas de outros objetos.
        """
        pass
                
    def is_running(self):
        return self.threadManager.is_running()
    
    def check_running(self) -> bool:
        """
            Verifica se já existe outra operação em andamento.
        """
        if self.is_running():
            messagebox.showwarning("Aviso", "Existe outra operação em andamento, aguarde!")
            return False
        return True
    
    def thread_main_create(self, cmd:callable) -> None:
        self.threadManager.thread_main_create(cmd)
        
    def thread_main_stop(self):
        self.threadManager.thread_main_stop()

    def command_stop_button(self):
        """
            Esse método pode ser conectado a um botão para parar a Thread principal.
        Podendo ser conectado diretamente ou indiretamente.
        """
        self.threadManager.thread_main_stop()

    def go_back_page(self):
        self.thread_main_stop()
        self.controller.navigator_pages.pop()
    
    def set_size_screen(self):
        self.controller.geometry("400x250")
        self.controller.title(f"App")

    def update_state(self):
        pass


class Navigator(object):
    def __init__(self, *, controller:ControllerApp):  
        self.controller:ControllerApp = controller # Janela principal ou root
        self.pages:Dict[str, AppPage] = {}  # Dicionário para armazenar as páginas
        self.current_page = None  # Página atualmente exibida
        self.historyPages:List[str] = []  # Pilha para armazenar o histórico de navegação

    def add_page(self, page_class: AppPage):
        """
        Adiciona uma página ao navegador.

        :param page: Instância da página (AppPage).
        """
        p:AppPage = page_class(controller=self.controller)
        self.pages[p.current_page_name] = p
        print(f'Página adicionada: {p.current_page_name}')

    def push(self, page_name: str):
        """
        Exibe a página especificada.

        :param page_name: Nome da página a ser exibida.
        """
        print(f'Navegando para {page_name}')
        if page_name not in self.pages:
            messagebox.showwarning("Aviso", f'Página não encontrada!\n{page_name}')
            return 

        # Esconde a página atual, se houver
        if self.current_page is not None:
            self.historyPages.append(self.current_page.current_page_name)  # Salva no histórico
            self.current_page.pack_forget()
        # Mostra a nova página
        self.current_page: AppPage = self.pages[page_name]
        self.current_page.set_size_screen()
        self.current_page.update_state()
        self.current_page.pack()

    def pop(self):
        """
        Retorna à página anterior no histórico de navegação.
        """
        if not self.historyPages:
            messagebox.showwarning("Aviso", "Não há páginas anteriores no histórico para retornar.")
            return

        # Esconde a página atual
        if self.current_page is not None:
            self.current_page.pack_forget()

        # Recupera a página anterior do histórico
        previous_page_name = self.historyPages.pop()
        self.current_page: AppPage = self.pages[previous_page_name]
        self.current_page.set_size_screen()
        self.current_page.update_state()
        self.current_page.pack()
        print(f'Retornado para anterior: {previous_page_name}')


class WidgetApp(ABC):
    def __init__(self, frame: ttk.Frame):
        self.current_frame: ttk.Frame = frame
        self.current_pbar: WidgetProgressBar = None
        
    @abstractmethod
    def add_button(self, name:str, cmd:callable):
        pass
        
    @abstractmethod
    def add_label(self, text:str):
        pass

    @abstractmethod
    def add_progress_bar(self, mode:LibProgress=LibProgress.INDETERMINATE):
        pass
    

class WidgetColumn(WidgetApp):
    def __init__(self, frame):
        super().__init__(frame)
        self._label: ttk.Label = None
        self._button: ttk.Button = None
        
    def add_button(self, name:str, cmd:callable):
        if self._button is not None:
            pass
        self._button = ttk.Button(self.current_frame, text=name, command=cmd, style='TButton')
        self._button.pack(expand=True, fill='both', padx=1, pady=1)
        
    def add_label(self, text:str):
        self._label = ttk.Label(self.current_frame, text=text)
        self._label.pack(expand=True, padx=1, pady=1)
        
    def add_progress_bar(self, mode:LibProgress=LibProgress.INDETERMINATE):
        if self.current_pbar is not None:
            pass
        self.current_pbar = WidgetProgressBar(self.current_frame, mode=mode)
        
               
class WidgetRow(WidgetApp):
    def __init__(self, frame):
        super().__init__(frame)
        self._label: ttk.Label = None
        self._button: ttk.Button = None
        
    def add_button(self, name:str, cmd:callable):
        if self._button is not None:
            pass
        self._button = ttk.Button(self.current_frame, text=name, command=cmd, style='TButton')
        self._button.pack(side=tk.LEFT, expand=True, fill='both', pady=1, padx=1)
        
    def add_label(self, text:str):
        if self._label is not None:
            pass
        self._label = ttk.Label(self.current_frame, text=text)
        self._label.pack(side=tk.LEFT, expand=True, fill='both', pady=1, padx=1)
        
    def add_progress_bar(self, mode:LibProgress=LibProgress.INDETERMINATE):
        if self.current_pbar is not None:
            pass
        self.current_pbar = WidgetProgressBar(self.current_frame, mode=mode)
        

class WidgetFilesRow(object):
    def __init__(self, frame, *, controller: ControllerApp):
        self.controller: ControllerApp = controller
        self.current_frame: ttk.Frame = frame
        
        # Frame para os botões
        self.frame_buttons: ttk.Frame = ttk.Frame(self.current_frame)
        self.frame_buttons.pack(expand=True, fill='both', padx=1, pady=1)
        # Frame para Labels
        self.frame_row_labels: ttk.Frame = ttk.Frame(self.current_frame)
        self.frame_row_labels.pack(expand=True, fill='both', padx=1, pady=1)
        
        # Widget para botões
        self.w_buttons = WidgetRow(self.frame_buttons)
        
        self.w_buttons.add_button('Adicionar PDFs', self.add_files_pdf)
        self.w_buttons.add_button('Adicionar imagens', self.add_files_image)
        self.w_buttons.add_button('Importar pasta', self.add_folder)
        self.w_buttons.add_button('Pasta para Salvar', self.select_ouput_folder)
        # Limpar
        self.w_buttons.add_button('Limpar', self.clear_files)
        
        self.lb_pdfs = ttk.Label(self.frame_row_labels, text='PDFs selecionados: 0')
        self.lb_pdfs.pack(side=tk.LEFT, expand=True, fill='both')
        
        self.lb_images = ttk.Label(self.frame_row_labels, text=' | Imagens adicionadas: 0')
        self.lb_images.pack(side=tk.LEFT, expand=True, fill='both')
        
        self.lb_outdir = ttk.Label(
            self.frame_row_labels, 
            text=f' | Salvar em: {self.controller.app_files.file_dialog.preferences.save_dir.basename()}'
        )
        self.lb_outdir.pack(side=tk.LEFT, expand=True, fill='both')
        
    def add_files_pdf(self):
        self.controller.app_files.select_files(LibraryDocs.PDF)
        self.lb_pdfs.config(
            text=f'PDFs selecionados: {self.controller.app_files.num_files_pdf}'
        )
        
    def add_files_image(self):
        self.controller.app_files.select_files(LibraryDocs.IMAGE)
        self.lb_images.config(
            text=f' | Images selecionadas: {self.controller.app_files.num_files_image}'
        )
        
    def add_folder(self):
        self.controller.app_files.select_dir(LibraryDocs.ALL_DOCUMENTS)
        
        self.lb_pdfs.config(
            text=f'PDFs selecionados: {self.controller.app_files.num_files_pdf}'
        )
        self.lb_images.config(
            text=f' | Images selecionadas: {self.controller.app_files.num_files_image}'
        )
        
    def select_ouput_folder(self):
        self.controller.app_files.select_output_dir()
        self.lb_outdir.config(
            text=f' | Salvar em: {self.controller.app_files.save_dir.basename()}'
        )
        
    def clear_files(self):
        """Limpar a lista de arquivos selecionados"""
        self.controller.app_files.clear()
        
        self.lb_pdfs.config(
            text=f'PDFs selecionados: {self.controller.app_files.num_files_pdf}'
        )
        self.lb_images.config(
            text=f'Images selecionadas: {self.controller.app_files.num_files_image}'
        )


class WidgetFilesColumn(object):
    def __init__(self, frame, *, controller: ControllerApp):
        self.controller: ControllerApp = controller
        self.current_frame: ttk.Frame = frame
        
        # Frame para os botões
        self.frame_buttons: ttk.Frame = ttk.Frame(self.current_frame)
        self.frame_buttons.pack(expand=True, fill='both', padx=1, pady=1)
        # Frame para Labels
        self.frame_row_labels: ttk.Frame = ttk.Frame(self.current_frame)
        self.frame_row_labels.pack(expand=True, fill='both', padx=1, pady=1)
        
        # Widget para botões
        self.w_buttons = WidgetColumn(self.frame_buttons)
        
        self.w_buttons.add_button('Adicionar PDFs', self.add_files_pdf)
        self.w_buttons.add_button('Adicionar imagens', self.add_files_image)
        self.w_buttons.add_button('Importar pasta', self.add_folder)
        self.w_buttons.add_button('Pasta para Salvar', self.select_ouput_folder)
        # Limpar arquivos selecionados
        self.w_buttons.add_button('Limpar', self.clear_files)
        
        self.lb_pdfs = ttk.Label(self.frame_row_labels, text='PDFs selecionados: 0')
        self.lb_pdfs.pack(expand=True, fill='both')
        
        self.lb_images = ttk.Label(self.frame_row_labels, text='Imagens adicionadas: 0')
        self.lb_images.pack(expand=True, fill='both')
        
        self.lb_outdir = ttk.Label(
            self.frame_row_labels, 
            text=f'Salvar em: {self.controller.app_files.file_dialog.preferences.save_dir.basename()}'
        )
        self.lb_outdir.pack(expand=True, fill='both')
        
    def add_files_pdf(self):
        self.controller.app_files.select_files(LibraryDocs.PDF)
        self.lb_pdfs.config(
            text=f'PDFs selecionados: {self.controller.app_files.num_files_pdf}'
        )
        
    def add_files_image(self):
        self.controller.app_files.select_files(LibraryDocs.IMAGE)
        self.lb_images.config(
            text=f'Images selecionadas: {self.controller.app_files.num_files_image}'
        )
        
    def add_folder(self):
        self.controller.app_files.select_dir(LibraryDocs.ALL_DOCUMENTS)
        
        self.lb_pdfs.config(
            text=f'PDFs selecionados: {self.controller.app_files.num_files_pdf}'
        )
        self.lb_images.config(
            text=f'Images selecionadas: {self.controller.app_files.num_files_image}'
        )
        
    def select_ouput_folder(self):
        self.controller.app_files.select_output_dir()
        self.lb_outdir.config(
            text=f'Salvar em: {self.controller.app_files.save_dir.basename()}'
        )
        
    def clear_files(self):
        """Limpar a lista de arquivos selecionados"""
        self.controller.app_files.clear()
        
        self.lb_pdfs.config(
            text=f'PDFs selecionados: {self.controller.app_files.num_files_pdf}'
        )
        self.lb_images.config(
            text=f'Images selecionadas: {self.controller.app_files.num_files_image}'
        )
        

class WidgetFilesImages(object):
    def __init__(self, frame, *, controller: ControllerApp):
        self.controller: ControllerApp = controller
        self.current_frame: ttk.Frame = frame
        
        # Frame para os botões
        self.frame_buttons: ttk.Frame = ttk.Frame(self.current_frame)
        self.frame_buttons.pack(expand=True, fill='both', padx=1, pady=1)
        # Frame para Labels
        self.frame_row_labels: ttk.Frame = ttk.Frame(self.current_frame)
        self.frame_row_labels.pack(expand=True, fill='both', padx=1, pady=1)
        
        # Widget para botões
        self.w_buttons = WidgetColumn(self.frame_buttons)
        
        self.w_buttons.add_button('Adicionar imagens', self.add_files_image)
        self.w_buttons.add_button('Importar pasta', self.add_folder)
        self.w_buttons.add_button('Pasta para Salvar', self.select_ouput_folder)
        # Limpar arquivos selecionados
        self.w_buttons.add_button('Limpar', self.clear_files)
        
        self.lb_images = ttk.Label(self.frame_row_labels, text='Imagens adicionadas: 0')
        self.lb_images.pack(expand=True, fill='both')
        
        self.lb_outdir = ttk.Label(
            self.frame_row_labels, 
            text=f'Salvar em: {self.controller.app_files.file_dialog.preferences.save_dir.basename()}'
        )
        self.lb_outdir.pack(expand=True, fill='both')
        
    def add_files_image(self):
        self.controller.app_files.select_files(LibraryDocs.IMAGE)
        self.lb_images.config(
            text=f'Images selecionadas: {self.controller.app_files.num_files_image}'
        )
        
    def add_folder(self):
        self.controller.app_files.select_dir(LibraryDocs.IMAGE)
        self.lb_images.config(
            text=f'Images selecionadas: {self.controller.app_files.num_files_image}'
        )
        
    def select_ouput_folder(self):
        self.controller.app_files.select_output_dir()
        self.lb_outdir.config(
            text=f'Salvar em: {self.controller.app_files.save_dir.basename()}'
        )
        
    def clear_files(self):
        """Limpar a lista de arquivos selecionados"""
        self.controller.app_files.clear()
        
        self.lb_images.config(
            text=f'Images selecionadas: {self.controller.app_files.num_files_image}'
        )
  
  
class WidgetFilesSheetRow(object):
    def __init__(self, frame, *, controller: ControllerApp):
        self.controller: ControllerApp = controller
        self.current_frame: ttk.Frame = frame
        
        # Frame para os botões
        self.frame_buttons: ttk.Frame = ttk.Frame(self.current_frame)
        self.frame_buttons.pack(expand=True, fill='both', padx=1, pady=1)
        # Frame para Labels
        self.frame_row_labels: ttk.Frame = ttk.Frame(self.current_frame)
        self.frame_row_labels.pack(expand=True, fill='both', padx=1, pady=1)
        
        # Widget para botões
        self.w_buttons = WidgetRow(self.frame_buttons)
        
        self.w_buttons.add_button('Adicionar Planilhas', self.add_sheets)
        self.w_buttons.add_button('Importar pasta', self.add_folder)
        self.w_buttons.add_button('Pasta para Salvar', self.select_ouput_folder)
        # Limpar
        self.w_buttons.add_button('Limpar', self.clear_files)
        
        self.lb_sheets = ttk.Label(self.frame_row_labels, text='Planilhas selecionadas: 0')
        self.lb_sheets.pack(side=tk.LEFT, expand=True, fill='both')
        
        self.lb_outdir = ttk.Label(
            self.frame_row_labels, 
            text=f' | Salvar em: {self.controller.app_files.file_dialog.preferences.save_dir.basename()}'
        )
        self.lb_outdir.pack(side=tk.LEFT, expand=True, fill='both')
        
    def add_sheets(self):
        self.controller.app_files.select_files(LibraryDocs.SHEET)
        self.lb_sheets.config(
            text=f'Planilhas selecionadas: {self.controller.app_files.num_files_sheet}'
        )
        
    def add_folder(self):
        self.controller.app_files.select_dir(LibraryDocs.SHEET)
        self.lb_sheets.config(
            text=f'Planilhas selecionadas: {self.controller.app_files.num_files_sheet}'
        )
        
    def select_ouput_folder(self):
        self.controller.app_files.select_output_dir()
        self.lb_outdir.config(
            text=f' | Salvar em: {self.controller.app_files.save_dir.basename()}'
        )
        
    def clear_files(self):
        """Limpar a lista de arquivos selecionados"""
        self.controller.app_files.clear()
        
        self.lb_sheets.config(
            text=f'Planilhas Selecionadas: {self.controller.app_files.num_files_sheet}'
        )
        

class WidgetProgressBar(object):
    """
        Criar uma barra de progresso padrão.
    """
    def __init__(
                    self, 
                    frame:ttk.Frame, 
                    *, 
                    mode: LibProgress = LibProgress.INDETERMINATE, 
                    orientation:str='horizontal', 
                    default_text:str='0%'
                ):
        """Barra de progresso."""
        self.mode: LibProgress = mode
        self._label_text: ttk.Label = ttk.Label(frame, text='-')
        self._label_text.pack()
        self._label_progress: ttk.Label = ttk.Label(frame, text=default_text)
        self._label_progress.pack()
        self._pbar: ttk.Progressbar = ttk.Progressbar(frame, orient=orientation)
        self._pbar.pack(expand=True, fill='both', padx=1, pady=1)
        
        if self.mode == LibProgress.INDETERMINATE:
            self.implement_pbar:ProgressBarTkIndeterminate =  ProgressBarTkIndeterminate(
                label_text=self._label_text,
                label_progress=self._label_progress,
                progress_bar=self._pbar,
            )
        elif self.mode == LibProgress.DETERMINATE:
            self.implement_pbar:ProgressBarTkDeterminate =  ProgressBarTkDeterminate(
                label_text=self._label_text,
                label_progress=self._label_progress,
                progress_bar=self._pbar,
            )
        else:
            raise ValueError(f'{__class__.__name__} Use: determinate OU indeterminate')
        self.progress_adapter:ProgressBarAdapter = ProgressBarAdapter(self.implement_pbar)
        
    def update(self, prog:float, text:str):
        self.progress_adapter.update_progress(prog, text)
        
    def get_progress(self) -> int:
        return self.progress_adapter.get_current_percent()
    
    def start(self):
        self.progress_adapter.start()
        
    def stop(self):
        self.progress_adapter.stop()
  
  
class WidgetScrow(object):
    def __init__(self, frame: ttk.Frame, *, width:int = 48, height: int = 8):
        self.frame: ttk.Frame = frame 
        #self.frame.pack(expand=True, fill='both', padx=1, pady=1)
        
        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=True, padx=1, pady=1)
        
        # Listbox
        self.listbox: tk.Listbox = tk.Listbox(
            self.frame, 
            yscrollcommand=self.scrollbar.set, 
            width=width, 
            height=height,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Conectar a scrollbar à listbox
        self.scrollbar.config(command=self.listbox.yview)
        
    def update_text(self, value: str):
        """Inserir novo texto na scrowbar"""
        # Adicionar textos
        self.listbox.insert(tk.END, value)
        
    def update_texts(self, values: List[str], include_info:str=None):
        """Adiciona uma lista de textos na scrowbar"""
        for value in values:
            if include_info is None:
                self.listbox.insert(tk.END, value)
            else:
                self.listbox.insert(tk.END, f"{include_info} {value}")
            
    def clear(self):
        """Limpar o texto da scrowbar"""
        self.listbox.delete(0, tk.END)  # Limpa todos os itens
                
     
class AppBar(ABCObserver):
    
    def __init__(self, *, controller: ControllerApp, version='-'):
        super().__init__()
        self.controller: ControllerApp = controller
        self.version = version
        self.dark_mode: bool = True
        self.initMenuBar()
        self.controller.app_prefs.add_observer(self)
        self.add_theme_style()
        
    def initMenuBar(self):
        self.menu_bar: tk.Menu = tk.Menu(self.controller)
        self.controller.config(menu=self.menu_bar)
        self.create_menu_file()
        self.create_menu_config()
        self.create_menu_style()
        self.create_menu_about()
        
    def update_notify(self, notify_provide: PreferencesApp = None):
        """
            Receber notificações quando as preferências do app forem
        atualizadas.
        """
        if notify_provide is None:
            return
        self.dark_mode = notify_provide.dark_mode
        self.add_theme_style()
    
    def create_menu_file(self):
        """Menu arquivo"""
        # Criar o menu Arquivo
        self.menu_file: tk.Menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Arquivo", menu=self.menu_file)
        
        # Adicionar itens ao menu Arquivo
        self.tesseract_index = self.add_item_menu_file(
            label="Tesseract",
            tooltip=self.controller.app_prefs.tesseract_path,
            command=lambda: self.select_bin_file_tesseract("tesseract"),
        ) # Indice para adicionar esse item no menu
        
        self.command_back_page = self.add_item_menu_file(
            label='Voltar',
            tooltip='Voltar para a página anterior',
            command=lambda: self.controller.go_back_page(),
        )

        self.exit_cmd = self.add_item_menu_file(
            label='Sair', 
            tooltip='Sair do programa', 
            command=self.controller.exit_app
        )

    def add_item_menu_file(self, label: str, tooltip: str, command: callable) -> int:
        """
        Adiciona um item ao menu 'Arquivo' com um tooltip.

        :param label: Nome do item no menu.
        :param tooltip: Texto do tooltip exibido no menu.
        :param command: Função a ser chamada ao clicar no item.
        :return: Índice do item adicionado no menu.
        """
        self.menu_file.add_command(
            label=f"{label} ({tooltip})",
            command=command,
        )
        return self.menu_file.index(tk.END)
    
    def create_menu_config(self):
        """Menu Configurações"""
        self.menu_config: tk.Menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Configurações", menu=self.menu_config)
        
        # Incluir itens no menu configurações
        self.menu_config.add_command(
            label=f"Arquivo de configuração: -",
            command=self.change_file_config,
        )
        self.menu_config.index(tk.END)

    def select_bin_file_tesseract(self, label: str) -> None:
        """
        Abre um diálogo para selecionar um arquivo e armazenar o caminho em uma variável.

        :param label: Rótulo do item no menu.
        """
        path_file: str = self.controller.app_files.file_dialog.open_filename(LibraryDocs.ALL)
        
        if path_file:
            # Armazena o caminho do arquivo selecionado na variável correspondente
            if label == "tesseract":
                self.controller.app_prefs.tesseract_path = path_file
                self.menu_file.entryconfig(self.tesseract_index, label=f"Tesseract: {path_file}")
            elif label == "ocrmypdf":
                pass
            messagebox.showinfo(label, f"Caminho selecionado:\n{path_file}")
        else:
            messagebox.showinfo(label, "Nenhum arquivo foi selecionado.")
            
    def create_menu_style(self):
        # Menu Estilo
        self.style_menu = tk.Menu(self.menu_bar, tearoff=0)
        #self.style_menu.add_command(label="Light Mode", command=self.set_light_mode)
        #self.style_menu.add_command(label="Dark Mode", command=self.set_dark_mode)
        self.style_menu.add_command(
                label="Light Mode", 
                command=self.controller.app_prefs.set_theme_light,
            )
        self.style_menu.add_command(
                label="Dark Mode", 
                command=self.controller.app_prefs.set_theme_dark,
            )
        self.menu_bar.add_cascade(label="Tema", menu=self.style_menu)
        
    def add_theme_style(self):
        if self.dark_mode:
            bg_color = "gray15"
            fg_color = "white"
            active_bg_color = "gray30"
            active_fg_color = "white"
        else:
            bg_color = "white"
            fg_color = "black"
            active_bg_color = "lightgray"
            active_fg_color = "black"

        self.menu_bar.config(
                        bg=bg_color, 
                        fg=fg_color,
                        activebackground=active_bg_color, 
                        activeforeground=active_fg_color
                    )

    def create_menu_about(self) -> None:
        """Exibe informações sobre o programa."""
         
        self.menu_about_bar: tk.Menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Sobre", menu=self.menu_about_bar)
        self.add_items_menu_about()
        self.controller.config(menu=self.menu_bar)
    
    def add_items_menu_about(self):
        """Adicionar itens ao Menu Sobre"""
        self.version_text: str = f'Versão: {self.version}'
        self.menu_about_bar.add_command(label=self.version_text)
        #self.menu_about_bar.add_command(label=self.version_lib)

    def change_file_config(self) -> None:
        """
            Alterar o arquivo de configuração
        """
        filename:str = filedialog.askopenfilename(
            title=f"Selecione um arquivo para JSON",
            initialdir=self.controller.app_files.file_dialog.preferences.initial_input_dir.absolute(),
            filetypes=[("Arquivos JSON", "*.json")]
        )
        if not filename:
            return
        if not os.path.isfile(filename):
            return
        self.file_config_json: File = File(filename)
        self.update_state()

    def update_menu_bar(self):
        """Atualizar as opções do Menu"""
        self.menu_config.entryconfig(
            0,
            label=f'Arquivo: {self.file_config_json.absolute()}'
        )
        
    def update_state(self):
        self.update_menu_bar()

