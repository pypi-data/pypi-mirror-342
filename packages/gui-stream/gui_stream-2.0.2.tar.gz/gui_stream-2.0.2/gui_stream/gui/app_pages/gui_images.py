#!/usr/bin/env python3
#
from gui_stream.gui.utils import AppImageObject, File
from gui_stream.gui.core.app_progress_bar import ProgressBarAdapter, ProgressBarTkDeterminate
from gui_stream.gui.core import (
    AppPage,
    WidgetRow,
    WidgetFilesImages,
    WidgetScrow,
)

from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

class PageEditImages(AppPage):
    def __init__(self, *, controller):
        super().__init__(controller=controller)
        self.current_page_name = '/home/images'
        self.frame_widgets = ttk.Frame(self.frame_main)
        self.frame_widgets.pack()
        self.initUI()
        
        # Inscrever a página atual no objeto notificador de arquivos.
        self.controller.app_files.add_observer(self)
        self.processed_images: set[AppImageObject] = set()
        self._processed_paisagem: bool = False
        self._processed_gray: bool = False
        
    def initUI(self):
        # Widget com input files
        self.frame_input = ttk.Frame(self.frame_widgets)
        self.frame_input.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        self.w_row_input = WidgetFilesImages(self.frame_input, controller=self.controller)
        
        self.frame_base = ttk.Frame(self.frame_widgets)
        self.frame_base.pack(expand=True, fill='both', padx=1, pady=1)
        
        # Frame para scrow e botões de exportação
        self.frame_scrow = ttk.Frame(self.frame_base)
        self.frame_scrow.pack(side=tk.LEFT, expand=True, fill='both', padx=1, pady=1)
        
        # Scrow
        self.scrow = WidgetScrow(self.frame_scrow)
        
        # Frames para barra de progresso e botões de exportação.
        self.frame_pbar = ttk.Frame(self.frame_base)
        self.frame_pbar.pack(expand=True, fill='both', padx=1, pady=1)
        # Frame para botões
        self.frame_buttons = ttk.Frame(self.frame_widgets)
        self.frame_buttons.pack(expand=True, fill='both', padx=1, pady=1)
        # label info text progress
        self.lb_info = ttk.Label(self.frame_buttons, text='-')
        self.lb_info.pack()
        # Label num progress
        self.lb_num_progress = ttk.Label(self.frame_pbar, text='0%')
        self.lb_num_progress.pack()
        # progress bar tk
        self.tk_bar: ttk.Progressbar = ttk.Progressbar(
                                    self.frame_pbar, 
                                    mode='determinate',
                                    orient='vertical',
                                )
        self.tk_bar.pack(expand=True, fill='both', padx=1, pady=1)
        # Barra de progresso
        implement_pbar = ProgressBarTkDeterminate(
            label_text = self.lb_info,
            label_progress = self.lb_num_progress,
            progress_bar = self.tk_bar,
        )
        self.pbar: ProgressBarAdapter = ProgressBarAdapter(implement_pbar)
        
        # Botões de exportação
        self.buttons = WidgetRow(self.frame_buttons)
        self.buttons.add_button('Rotacionar como paisagem', self.images_set_paisagem)
        self.buttons.add_button('Melhorar Texto embutido', self.images_set_gray)
        self.buttons.add_button('Exportar', self.images_export)
        
    def images_set_paisagem(self):
        if not self.check_running():
            return
        if self.controller.app_files.num_files_image < 1:
            messagebox.showwarning('Aviso', 'Adicione imagens para prosseguir!')
            return
        if self._processed_paisagem == True:
            messagebox.showinfo('OK', 'As imagens já foram definidas como paisagem!')
            return
        self.thread_main_create(self._run_set_paisagem)
        
    def _run_set_paisagem(self):
        if len(self.processed_images) == 0:
            files: list[File] = self.controller.app_files.get_files_image()
            max_images = len(files)
            for num, file in enumerate(files):
                prog = (num/max_images) * 100
                self.pbar.update_progress(prog, f'Processando imagem: {num+1} de {max_images}')
                self.scrow.update_text(f'Processando imagem: {num+1} de {max_images}')
                img: AppImageObject = AppImageObject.create_from_file(file)
                img.set_paisagem()
                self.processed_images.add(img)
        else:
            max_images = len(self.processed_images)
            for n, image in enumerate(self.processed_images):
                prog = (n/max_images) * 100
                self.pbar.update_progress(prog, f'Processando imagem: {n+1} de {max_images}')
                self.scrow.update_text(f'Processando imagem: {n+1} de {max_images}')
                image.set_paisagem()
        
        self.pbar.update_progress(100, 'Operação finalizada!')
        self._processed_paisagem = True
        self.thread_main_stop()
        
    def images_set_gray(self):
        if not self.check_running():
            return
        if self.controller.app_files.num_files_image < 1:
            messagebox.showwarning('Aviso', 'Adicione imagens para prosseguir!')
            return
        if self._processed_gray == True:
            messagebox.showinfo('OK', 'As imagens já foram definidas como Cinza escuro!')
            return
        self.thread_main_create(self._run_image_gray)
    
    def _run_image_gray(self):
        if len(self.processed_images) == 0:
            files: list[File] = self.controller.app_files.get_files_image()
            max_images = len(files)
            for num, file in enumerate(files):
                prog = (num/max_images) * 100
                self.pbar.update_progress(prog, f'Processando imagem: {num+1} de {max_images}')
                self.scrow.update_text(f'Processando imagem: {num+1} de {max_images}')
                img: AppImageObject = AppImageObject.create_from_file(file)
                img.set_background_gray()
                self.processed_images.add(img)
        else:
            max_images = len(self.processed_images)
            for n, image in enumerate(self.processed_images):
                prog = (n/max_images) * 100
                self.pbar.update_progress(prog, f'Processando imagem: {n+1} de {max_images}')
                self.scrow.update_text(f'Processando imagem: {n+1} de {max_images}')
                image.set_background_gray()
        
        self.pbar.update_progress(100, 'Operação finalizada!')
        self._processed_gray = True
        self.thread_main_stop()   
    
    def images_export(self):
        if not self.check_running():
            return
        if self.controller.app_files.num_files_image < 1:
            messagebox.showwarning('Aviso', 'Adicione imagens para prosseguir!')
            return
        if len(self.processed_images) < 1:
            messagebox.showinfo('OK', 'Nenhuma imagem foi processada!')
            return
        self.thread_main_create(self._run_export)
        
    def _run_export(self):
        ignored: int = 0 # Arquivos repetidos.
        exported: int = 0
        out = self.controller.app_files.save_dir.concat('Imagens Processadas', create=True)
        max_images = len(self.processed_images)
        for num, img in enumerate(self.processed_images):
            output_path: File = out.join_file(f'imagem-{num+1}.png')
            if output_path.path.exists():
                self.scrow.update_text(f'PULANDO: o arquivo já existe: {output_path.basename()}')
                ignored += 1
                continue
            
            prog = (num/max_images) * 100
            self.pbar.update_progress(prog, f'Exportando: {num+1} de {max_images}')
            self.scrow.update_text(f'Exportando: {num+1} de {max_images}')
            img.to_file(output_path)
            exported += 1
            
        self.pbar.update_progress(100, f'Arquivos exportados {exported} | ignorados/repetidos {ignored}')
        self.thread_main_stop()
    
    def update_notify(self, notify_provide = None):
        """
            Recebe atualização de estado do objetos notificadores
        """
        # Verifica se atualização de estado foi a limpeza dos arquivos 
        # selecionados pelo usuário, se sim, limpar a propriedade .processed_images: set
        if self.controller.app_files.num_files == 0:
            print('----------------------------------------------------')
            print(f'{__class__.__name__} O usuário limpou os arquivos')
            self.processed_images.clear()
    
    def set_size_screen(self):
        self.controller.geometry('665x220')
        self.controller.title('Editar Imagens')