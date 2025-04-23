#!/usr/bin/env python3
#
from typing import List
import os

import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from gui_stream.gui.core.core_app import (
    AppPage,
    WidgetRow,
    WidgetFilesColumn,
    WidgetProgressBar,
    WidgetScrow,
    LibProgress,
)

from gui_stream.gui.utils import (
    AppPageDocumentPdf,
    AppPdfStream,
    AppDocumentPdf,
    File,
    AppImageObject,
    LibraryOCR,
    AppRecoginzeImage,
    AppRecognizePdf,
    KERNEL_TYPE,
)
from gui_stream.gui.utils import LibraryPDF

#========================================================#
# Reconhecer Texto em PDF
#========================================================#
class PageRecognizePDF(AppPage):
    def __init__(self, *, controller):
        super().__init__(controller=controller)
        # Inscreverse no objeto notificador
        self.controller.app_files.add_observer(self)
        self.current_page_name = '/home/ocr'
        self.frame_widgets = ttk.Frame(self.frame_main)
        self.frame_widgets.pack(expand=True, fill='both', padx=1, pady=1)
        self.reconized_pages: set[AppPageDocumentPdf] = set()
        self.initUI()

    def initUI(self):
        # Frame para os botões de input
        self.frame_input_files = ttk.Frame(self.frame_widgets, style='LightPurple.TFrame')
        self.frame_input_files.pack(side=tk.LEFT, expand=True, fill='both', padx=2, pady=3)
        self.widget_input = WidgetFilesColumn(self.frame_input_files, controller=self.controller)

        # Frame a direita
        self.frame_r = ttk.Frame(self.frame_widgets, style='DarkOrange.TFrame')
        self.frame_r.pack(expand=True, padx=3, pady=2)

        # botões de ação
        self.frame_btns = ttk.Frame(self.frame_r)
        self.frame_btns.pack(expand=True, fill='both', padx=1, pady=1)
        self.widget_row_buttons = WidgetRow(self.frame_btns)
        self.widget_row_buttons.add_button('Exportar lote PDF', self.recognize_to_pdfs)
        self.widget_row_buttons.add_button('Exportar único PDF', self.recognize_to_uniq_pdf)

        # Label tesseract
        self.lb_tesseract = ttk.Label(self.frame_r, text=f'Tesseract: {self.controller.app_prefs.tesseract_path}')
        self.lb_tesseract.pack()
        
        # Container Scrollbar
        self.frame_scrow = ttk.Frame(self.frame_r)
        self.frame_scrow.pack(expand=True, fill='both', padx=1, pady=1)
        self.scrow: WidgetScrow = WidgetScrow(self.frame_scrow, height=4)        

        # Frame para barra de progresso
        self.frame_pbar = ttk.Frame(self.frame_r)
        self.frame_pbar.pack(expand=True, fill='both', padx=1, pady=1)
        self.pbar_container: WidgetProgressBar = WidgetProgressBar(
            self.frame_pbar,
            mode=LibProgress.DETERMINATE,
        )

    def recognize_to_pdfs(self):
        tesserct: File = self.get_path_tesserct()
        if tesserct is None:
            messagebox.showerror('Erro', 'Instale o tesseract para prosseguir!')
            return
        if self.is_running():
            messagebox.showwarning('Erro', 'Existe outra operação em andamento, aguarde!')
            return
        if (self.controller.app_files.num_files_image < 1) and (self.controller.app_files.num_files_pdf < 1):
            messagebox.showinfo('Selecione documentos', 'Selecione uma imagem ou PDF para prosseguir!')
            return
        self.thread_main_create(self._run_recognize_to_pdfs)
        
    def _run_recognize_to_pdfs(self):
        """
            Reconhecer os arquivos PDF e Imagens adicionadas e exportar para PDFs individuais.
        """
        self.pbar_container.start()
        files_image = self.controller.app_files.get_files_image()
        max_images = len(files_image)
        # Reconhecer imagens.
        rec: AppRecoginzeImage = AppRecoginzeImage.create(
            LibraryOCR.PYTESSERACT,
            path_tesseract=self.get_path_tesserct(),
        )
        doc = AppDocumentPdf()
        for num, file in enumerate(files_image):
            output_path: File = self.controller.app_files.save_dir.join_file(f'{file.name()}.pdf')
            prog = (num/max_images) * 100
            if output_path.path.exists():
                #self.pbar_container.update(prog, f'[PULANDO]: o arquivo já existe: {output_path.basename()}')
                self.update_text_scrow(f'[PULANDO]: o arquivo já existe: {output_path.basename()}')
                continue

            self.pbar_container.update(prog, f'Reconhecendo imagem: {num+1} de {max_images} {file.basename()}')
            self.update_text_scrow(f'Reconhecendo imagem: {num+1} de {max_images} {file.basename()}')
            img = AppImageObject.create_from_file(file)
            img.set_paisagem()
            bt: bytes = rec.image_recognize(img).bytes_recognized
            self.pbar_container.update(prog, f'Exportando: {output_path.basename()}')
            doc.add_page(AppPageDocumentPdf.create_from_page_bytes(bt, library=LibraryPDF.FITZ))
            doc.to_file_pdf(output_path)
            doc.clear()
            if self.threadManager.threadStopEvent.is_set():
                print("Processamento interrompido por Event.set()")
                self.update_text_scrow("Processamento interrompido por Event.set()")
                break

        # Reconhecer os arquivos PDF
        files_pdf = self.controller.app_files.get_files_pdf()
        max_pdf = len(files_pdf)
        pdf_stream = AppPdfStream()
        rec_pdf: AppRecognizePdf = AppRecognizePdf(rec)
        doc.clear()
        for n, file_pdf in enumerate(files_pdf):
            progress_files = ((n+1)/(max_pdf)) * (100)
            self.pbar_container.update(progress_files, f'Adicionando arquivo: {n+1} de {max_pdf} {file_pdf.basename()}')
            self.update_text_scrow(f'Adicionando arquivo: {n+1} de {max_pdf} {file_pdf.basename()}')
            pdf_stream.add_file_pdf(file_pdf)
            
            # Converter as páginas em imagem e aplicar o OCR.
            for num_page, page in enumerate(pdf_stream.pages):
                output_path = self.controller.app_files.save_dir.join_file(f'{file_pdf.name()}-pag-{page.page_number}.pdf')
                if output_path.path.exists():
                    self.update_text_scrow(f'PULANDO: o arquivo já existe: {output_path.basename()}')
                    # Pular
                    continue
                
                self.pbar_container.update(
                        progress_files, 
                        f'OCR página: [{page.page_number} de {pdf_stream.num_pages}] Documento {n+1} de {max_pdf}'
                    )
                self.update_text_scrow(
                        f'OCR página: [{page.page_number} de {pdf_stream.num_pages}] Documento {n+1} de {max_pdf}'
                    )
                
                doc.add_page(rec_pdf.recognize_page_pdf(page))
                self.pbar_container.update(progress_files, f'Exportando: {output_path.basename()}')
                doc.to_file_pdf(output_path)
                doc.clear()
                if self.threadManager.threadStopEvent.is_set():
                    print("Processamento interrompido por Event.set()")
                    break
            pdf_stream.clear()
        
        self.pbar_container.update(100, 'Operação finalizada!')
        self.thread_main_stop()

    def recognize_to_uniq_pdf(self):
        tesserct: File = self.get_path_tesserct()
        if tesserct is None:
            messagebox.showerror('Erro', 'Instale o tesseract para prosseguir!')
            return
        if self.is_running():
            messagebox.showwarning('Erro', 'Existe outra operação em andamento, aguarde!')
            return
        if (self.controller.app_files.num_files_image < 1) and (self.controller.app_files.num_files_pdf < 1):
            messagebox.showinfo('Selecione documentos', 'Selecione uma imagem ou PDF para prosseguir!')
            return
        self.thread_main_create(self._run_recognize_uniq_pdf)

    def _run_recognize_uniq_pdf(self):
        # Configurar o documento para o máximo de 3000 páginas. ALTERE SE NECESSÁRIO.
        document = AppDocumentPdf(LibraryPDF.FITZ, 3000) 
        pdf_stream = AppPdfStream(library_pdf=LibraryPDF.FITZ)
        rec_image: AppRecoginzeImage = AppRecoginzeImage.create(
            LibraryOCR.PYTESSERACT,
            path_tesseract = self.get_path_tesserct(),
        )
        rec_pdf: AppRecognizePdf = AppRecognizePdf(rec_image)
        
        # Reconhecer as imagens e converter em páginas PDF para adionar ao documento
        files_image: list[File] = self.controller.app_files.get_files_image()
        max_images: int = len(files_image)
        for num_image, file in enumerate(files_image):
            prog: float = (num_image/max_images) * 100
            self.pbar_container.update(prog, f'Reconhecendo imagem: {num_image+1} de {max_images}')
            self.update_text_scrow(f'Reconhecendo imagem: {num_image+1} de {max_images}')
            # Converter o arquivo em imagem e aplicar o OCR
            im = AppImageObject.create_from_file(file)
            page = rec_image.image_recognize(im).to_page_pdf()
            document.add_page(page)
        
        # Reconhecer PDF.
        files_pdf: list[File] = self.controller.app_files.get_files_pdf()
        max_pdf: int = len(files_pdf)
        for num_pdf, file in enumerate(files_pdf):
            prog: float = (num_pdf/max_pdf) * 100
            self.pbar_container.update(prog, f'Reconhecendo PDF: {num_pdf} de {max_pdf}')
            pdf_stream.add_file_pdf(file)
            # Reconhecer cada página
            for page in pdf_stream.pages:
                self.pbar_container.update(
                    prog, 
                    f'Reconhecendo PDF: {num_pdf} de {max_pdf} [página {page.page_number} de {pdf_stream.num_pages}]'
                )
                self.update_text_scrow(
                    f'Reconhecendo PDF: {num_pdf} de {max_pdf} [página {page.page_number} de {pdf_stream.num_pages}]'
                )
                new_page = rec_pdf.recognize_page_pdf(page)
                document.add_page(new_page)
                pdf_stream.clear()
        # Salvar o documento
        output_path: File = self.controller.app_files.save_dir.join_file('DocumentoOCR.pdf')
        if output_path.path.exists():
            # Renomear o arquivo repetido
            _count: int = 1
            while True:
                output_path = self.controller.app_files.save_dir.join_file(f'DocumentoOCR-({_count}).pdf')
                if not output_path.path.exists():
                    break
                _count += 1
        self.pbar_container.update(prog, f'Salvando: {output_path.basename()}')        
        self.update_text_scrow(f'Salvando: {output_path.basename()}')
        document.to_file_pdf(output_path)
        self.pbar_container.update(100, 'Operação finalizada!')
        self.thread_main_stop()
        
    def get_path_tesserct(self) -> File | None:
        try:
            filepath = self.controller.app_prefs.tesseract_path
        except:
            pass
        else:
            if os.path.exists(filepath):
                return File(filepath)
            
        from shutil import which
        name = 'tesseract.exe' if KERNEL_TYPE == 'Windows' else 'tesseract'
        filepath = which(name)
        if filepath is None:
            return None
        return File(filepath)
        
    def update_text_scrow(self, value: str):
        # Adicionar textos
        self.scrow.update_text(value)
        
    def update_current_scrow_values(self, values: List[str], include_info=None):
        self.scrow.update_texts(values, include_info)
            
    def clear_current_scrow_bar(self):
        self.scrow.clear()  # Limpa todos os itens
        
    def update_notify(self, notify_provide=None):
        print(f'{__class__.__name__} os arquivos foram atualizados')
        
    def set_size_screen(self):
        self.controller.geometry("640x250")
        self.controller.title(f"Reconhecer Texto em Documentos")

    def update_state(self):
        pass

