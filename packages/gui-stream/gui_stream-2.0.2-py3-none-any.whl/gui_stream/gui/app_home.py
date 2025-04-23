#!/usr/bin/env python3
#
from __future__ import annotations
from tkinter import ttk

from gui_stream.gui.core.core_app import (
    WidgetRow,    
    AppPage,
    ControllerApp,
    PreferencesApp,
    PreferencesDir,
    AppFileDialog,
    AppSelectedFiles,
    AppBar,
    AppStyles,
)

from gui_stream.gui.app_pages import (
    PageEditImages, PageConvertPdfs, PageRecognizePDF,
    PageDocsToi, PageFilesToExcel, PageMoveFiles, PageSoupSheets,
)
   
class HomePage(AppPage):
    def __init__(self, *, controller):
        super().__init__(controller=controller)
        self.current_page_name = '/home'
        self.app_styles: AppStyles = AppStyles(self.controller)
        
        # Frame para botões
        self.frame_buttons = ttk.Frame(self.frame_main, style='DarkPurple.TFrame')
        self.frame_buttons.pack(expand=True, fill='both', padx=1, pady=1)
        # Frame para conversão de documentos.
        self.frame_row_docs = ttk.Frame(self.frame_buttons)
        self.frame_row_docs.pack(expand=True, fill='both', padx=2, pady=2)
        self.widget_row_docs = WidgetRow(self.frame_row_docs)
        self.widget_row_docs.add_button(
                'Conversão de PDF', 
                lambda: self.controller.navigator_pages.push('/home/convert_pdf')
            )
        self.widget_row_docs.add_button(
                'OCR Documentos', 
                lambda: self.controller.navigator_pages.push('/home/ocr')
            )
        
        self.widget_row_docs.add_button(
            'Editar Imagens',
            lambda: self.controller.navigator_pages.push('/home/images')
        )
        
        # Frame para Edição de planilhas
        self.frame_row_edit_sheets = ttk.Frame(self.frame_buttons)
        self.frame_row_edit_sheets.pack(expand=True, fill='both', padx=2, pady=2)
        self.widget_row_edit_sheets = WidgetRow(self.frame_row_edit_sheets)
        self.widget_row_edit_sheets.add_button(
                'Planilhar Pasta', 
                lambda: self.controller.navigator_pages.push('/home/folder_to_excel')
            )
        self.widget_row_edit_sheets.add_button(
                'Filtrar planilhas', 
                lambda: self.controller.navigator_pages.push('/home/soup_sheets')
            )
        self.widget_row_edit_sheets.add_button(
            'Mover Arquivos',
            lambda: self.controller.navigator_pages.push('/home/page_mv_files')
        )
        self.widget_row_edit_sheets.add_button(
            'Especial',
            lambda: self.controller.navigator_pages.push('/home/page_toi')
        )
        self.initUI()
        
    def initUI(self):
        pass
    
    def set_size_screen(self):
        self.controller.geometry("500x80")
        self.controller.title(f"Home")


class MyApplication(object):
    def __init__(
                    self, 
                    *,
                    title: str = 'App',
                    controller: ControllerApp,
                    app_bar: AppBar = None, 
                ):
        self.title: str = title
        self.controller: ControllerApp = controller
        self.app_bar: AppBar = app_bar
        
        self.controller.geometry("450x230")
        self.controller.title(self.title)
        
        pages = (
            HomePage,
            PageConvertPdfs,
            PageRecognizePDF,
            PageEditImages,
            PageDocsToi, 
            PageFilesToExcel, 
            PageMoveFiles, 
            PageSoupSheets,
        )
        
        for page in pages:
            self.controller.navigator_pages.add_page(page)
        self.controller.navigator_pages.push('/home')
        
# Criação da janela principal e execução da interface do aplicativo
def runApp():
    preferences_dir = PreferencesDir.create_default()
    file_dialog: AppFileDialog = AppFileDialog(preferences_dir)
    
    app_controller: ControllerApp = ControllerApp(
        app_prefs = PreferencesApp.create_default(),
        app_files = AppSelectedFiles(file_dialog, max_files=2000),
    )
    
    app_bar: AppBar = AppBar(controller=app_controller, version='2.0')
    myapp: MyApplication = MyApplication(
        title = 'Conversor de Documentos',
        controller = app_controller,
        app_bar = app_bar,
    )
    myapp.controller.mainloop()
    
if __name__ == "__main__":
    runApp()

