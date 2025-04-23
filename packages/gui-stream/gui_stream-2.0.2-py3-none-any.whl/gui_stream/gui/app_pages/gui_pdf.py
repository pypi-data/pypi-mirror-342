#!/usr/bin/env python3
#

import threading
from typing import List
import os
import time

import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from gui_stream.gui.core.core_app import (
    AppPage,
    WidgetColumn,
    WidgetRow,
    WidgetFilesRow,
    WidgetProgressBar,
    WidgetScrow,
    LibProgress,
)

from gui_stream.gui.utils import (
    AppPdfStream,
    AppImageStream,
    AppDocumentPdf,
    File,
    AppImageObject,
)


#========================================================#
# Image/PDF para planilha (OCR)
#========================================================#
class PageConvertPdfs(AppPage):
    def __init__(self, *, controller):
        super().__init__(controller=controller)
        # Inscrever a página atual no objeto notificador
        self.controller.app_files.add_observer(self)
        
        self.current_page_name = '/home/convert_pdf'
        self.frame_widgets: ttk.Frame = ttk.Frame(self.frame_main)
        self.frame_widgets.pack()
        
        # Frame para importar os arquivos
        self.frame_row_buttons_files = ttk.Frame(self.frame_widgets, style='DarkOrange.TFrame')
        self.frame_row_buttons_files.pack(expand=True, fill='both', padx=1, pady=1)
        # Frame input files
        self.frame_files: WidgetFilesRow = WidgetFilesRow(
            self.frame_row_buttons_files,
            controller=self.controller
        )
        
        # Container Scrollbar
        self.frame_scrow = ttk.Frame(self.frame_widgets, style='Black.TFrame')
        self.frame_scrow.pack(expand=True, fill='both', padx=2, pady=2)
        self.scrow: WidgetScrow = WidgetScrow(
            self.frame_scrow,
            height=7,
            width=71,
        )
        
        # Widgets para exportar os arquivos.
        self.frame_row_export = ttk.Frame(self.frame_widgets)
        self.frame_row_export.pack(expand=True, fill='both', padx=1, pady=1)
        
        # Widget com botões de exportar
        self.w_row_export = WidgetRow(self.frame_row_export)
        self.w_row_export.add_button('Unir PDF', self.join_pdf)
        self.w_row_export.add_button('Dividir PDF', self.split_pdf)
        self.w_row_export.add_button('PDF para Imagens', self.pdf_to_images)
        self.w_row_export.add_button('Exportar para Excel', self.pdf_to_excel)
        
        # Frame para barra de progresso
        self.frame_pbar = ttk.Frame(self.frame_widgets)
        self.frame_pbar.pack(expand=True, fill='both', padx=2, pady=2)
        self.pbar_container: WidgetProgressBar = WidgetProgressBar(
            self.frame_pbar,
            mode=LibProgress.DETERMINATE,
        )
        
    def split_pdf(self):
        if self.is_running():
            messagebox.showwarning('Erro!', 'Exite outra operação em andamento!')
            return
        self.thread_main_create(self._run_split_pdf)
        
    def _run_split_pdf(self):
        
        self.pbar_container.start()
        stream: AppPdfStream = AppPdfStream()
        # Adicionar arquivos PDF ao stream
        files_pdf = self.controller.app_files.get_files_pdf()
        max_pdf = len(files_pdf)
        for n, file in enumerate(files_pdf):
            progress = (n/max_pdf) * 100
            self.pbar_container.update(progress, f'Adiconando arquivo: {n+1} de {max_pdf} {file.basename()}')
            stream.add_file_pdf(file)

        # Adicionar imagens ao stream
        self.pbar_container.stop()
        self.pbar_container.update(0, 'Adicionando imagens Aguarde!')
        files_image = self.controller.app_files.get_files_image()
        max_images = len(files_image)

        for n, file in enumerate(files_image):
            prog = (n/max_images) * 100
            self.pbar_container.update(prog, f'Convertendo imagem em página PDF {n+1} de {max_images}')
            stream.add_image(AppImageObject.create_from_file(file))
            
        # Dividir os arquivos
        doc = AppDocumentPdf()
        for num, page in enumerate(stream.pages):
            _prog = (num/stream.num_pages) * 100
            filename = f'página-{num+1}.pdf'
            self.pbar_container.update(_prog, f'Exportando: {num+1} e {stream.num_pages}')
            self.update_current_scrow_value(f'Exportando: {filename}')
            doc.add_page(page)
            doc.to_file_pdf(self.controller.app_files.save_dir.join_file(filename))
            doc.clear()
        
        self.pbar_container.update(100, 'Operação finalizada!')
        self.thread_main_stop()
    
    def join_pdf(self):
        if self.is_running():
            messagebox.showwarning('Erro!', 'Exite outra operação em andamento!')
            return
        self.thread_main_create(self._run_join_pdf)
    
    def _run_join_pdf(self):
        
        self.pbar_container.start()
        stream: AppPdfStream = AppPdfStream()
        
        files_pdf = self.controller.app_files.get_files_pdf()
        files_image = self.controller.app_files.get_files_image()
        max_pdf = len(files_pdf)
        
        # Adicionar arquivos PDF ao stream
        for num, pdf in enumerate(files_pdf):
            prog = (num/max_pdf) * 100
            self.pbar_container.update(prog, f'Adicionando PDF: {num+1} de {max_pdf}')
            stream.add_file_pdf(pdf)
        self.pbar_container.stop()
        
        # Adicionar as imagens ao stream
        img_stream = AppImageStream()
        img_stream.add_files_image(files_image)
        pages = img_stream.to_pages_pdf()
        for n, page in enumerate(pages):
            _prog = (n/len(pages)) * 100
            self.pbar_container.update(_prog, f'Adicionando imagem {page.page_number}')
            stream.add_page(page)
            
        # Exportar arquivo.
        stream.to_file_pdf(self.controller.app_files.save_dir.join_file('documento.pdf'))
        self.pbar_container.update(100, 'Operação finalizada!')
        self.pbar_container.stop()
        self.thread_main_stop()
    
    def pdf_to_images(self):
        if self.is_running():
            messagebox.showwarning('Erro!', 'Exite outra operação em andamento!')
            return
        self.thread_main_create(self._run_pdf_to_images)
    
    def _run_pdf_to_images(self):
        
        self.pbar_container.start()
        stream = AppPdfStream()
        stream.add_files_pdf(self.controller.app_files.get_files_pdf())
        pdf_stream = AppPdfStream()
        
        for n, page in enumerate(stream.pages):
            file_image:str = f'imagem-{n+1}.png'
            p = (n/stream.num_pages) * 100
            self.pbar_container.update(p, f'Exportando imagem: {n+1} de {stream.num_pages} | {file_image}')
            pdf_stream.add_page(page)
            pdf_stream.to_images()[0].to_file(self.controller.app_files.save_dir.join_file(file_image))
            pdf_stream.clear()
        self.pbar_container.update(100, 'Operação finalizada!')
        #self.pbar_container.stop()
        self.thread_main_stop()
    
    def pdf_to_excel(self):
        if self.is_running():
            messagebox.showwarning('Erro!', 'Exite outra operação em andamento!')
            return
        self.thread_main_create(self._run_pdf_to_excel)
    
    def _run_pdf_to_excel(self):
        self.pbar_container.start()
        stream = AppPdfStream()
        stream.add_files_pdf(self.controller.app_files.get_files_pdf())
        data: List[pd.DataFrame] = []
        doc = AppDocumentPdf()
        for num, page in enumerate(stream.pages):
            p = (num/stream.num_pages) * 100
            self.pbar_container.update(p, f'Extraindo texto da página: {num+1} de {stream.num_pages}')
            doc.add_page(page)
            try:
                df = doc.to_data()
            except:
                continue
            if not df.empty:
                data.append(df)
            doc.clear()
            
        if len(data) > 0:
            self.pbar_container.update(p, 'Exportando planilha!')
            table = pd.concat(data)
            table.to_excel(self.controller.app_files.save_dir.join_file('Documento.xlsx').absolute(), index=False)
    
        self.pbar_container.update(100, 'Operação finalizada!')
        self.thread_main_stop()
    
    def update_current_scrow_value(self, value: str):
        self.scrow.update_text(value)
        
    def update_current_scrow_values(self, values: List[str], include_info=None):
        self.scrow.update_texts(values, include_info)
            
    def clear_current_scrow_bar(self):
        self.scrow.clear()
        
    def update_notify(self, notify_provide=None):
        print(f'{__class__.__name__} os arquivos foram atualizados')
        self.clear_current_scrow_bar()
        self.update_current_scrow_values(
            [x.basename() for x in self.controller.app_files.files]
        )
        
    def set_size_screen(self):
        self.controller.geometry("620x310")
        self.controller.title(f"Conversão de PDFs")

    def update_state(self):
        pass
