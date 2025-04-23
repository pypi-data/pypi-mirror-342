#!/usr/bin/env python3
from __future__ import annotations
import os
from typing import List
from abc import ABC, abstractmethod
from typing import Tuple, List
from tkinter import filedialog

from gui_stream.gui.utils import (
    File,
    Directory,
    AppInputFiles,
    UserFileSystem,
    AppJsonConvert,
    AppJsonData,
    LibraryDocs,
    ABCNotifyProvider,
    KERNEL_TYPE,
) 

from gui_stream.gui.models import ABCNotifyProvider, ABCObserver

class PreferencesDir(object):
    """Preferencias de diretórios."""
    _instance_preferences = None # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_preferences is None:
            cls._instance_preferences = super(PreferencesDir, cls).__new__(cls)
        return cls._instance_preferences
    
    def __init__(
                self, 
                *, 
                initial_input_dir:Directory, 
                initial_output_dir:Directory, 
                save_dir: Directory = Directory(UserFileSystem().userDownloads.concat('output', create=True).absolute()),
            ):
        super().__init__()
        self.initial_input_dir: Directory = initial_input_dir
        self.initial_output_dir: Directory = initial_output_dir
        self.save_dir: Directory = save_dir
        
    @abstractmethod
    def to_json_data(self) -> AppJsonData:
        _data:dict = {
            'initial_input_dir': self.initial_input_dir.absolute(),
            'initial_output_dir': self.initial_output_dir.absolute(),
            'save_dir': self.save_dir.absolute(),
        }
        conv: AppJsonConvert = AppJsonConvert.from_dict(_data)
        return conv.to_json_data()
    
    @classmethod
    def create_from_dict(cls, prefs:dict) -> PreferencesDir | None:
        try:
            if 'save_dir' in prefs:
                        return cls(
                        initial_input_dir = Directory(prefs["initial_input_dir"]), 
                        initial_output_dir = Directory(prefs["initial_output_dir"]),
                        save_dir = Directory(prefs['save_dir']),
                    )
            else:
                return cls(
                        initial_input_dir = Directory(prefs["initial_input_dir"]), 
                        initial_output_dir = Directory(prefs["initial_output_dir"]),
                    )
        except:
            return None
        
    @classmethod
    def create_default(cls) -> PreferencesDir:
        return cls(
                    initial_input_dir=UserFileSystem().userDownloads, 
                    initial_output_dir=UserFileSystem().userDownloads,
                )
        
        
class PreferencesApp(ABCNotifyProvider):
    """Preferencias do aplicativo."""
    _instance_preferences_app = None # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_preferences_app is None:
            cls._instance_preferences_app = super(PreferencesApp, cls).__new__(cls)
        return cls._instance_preferences_app
    
    def __init__(self, *, tesseract_path:str, tesseract_data_dir:str=None, lang:str='por'):
        super().__init__()
        self.tesseract_path: str = tesseract_path
        self.tesseract_data_dir: str = tesseract_data_dir
        self.lang: str = lang
        self._dark_mode: bool = True
        
    @property
    def dark_mode(self) -> bool:
        return self._dark_mode
    
    @dark_mode.setter
    def dark_mode(self, new:bool):
        self._dark_mode = new
        self.notify_all()
        
    def add_observer(self, observer: ABCObserver):
        self._observer_list.append(observer)
        self.num_observers += 1
        print(f'Objeto inscrito nas preferências: {self.num_observers}')
    
    def notify_all(self):
        for obs in self._observer_list:
            obs.update_notify(self)
            
    def set_theme_light(self):
        self.dark_mode = False
    
    def set_theme_dark(self):
        self.dark_mode = True
    
    @classmethod
    def create_default(cls) -> PreferencesApp:
        import shutil
        default_path: str = None
        
        if KERNEL_TYPE == 'Linux':
            default_path = shutil.which('tesseract')
        elif KERNEL_TYPE == 'Windows':
            default_path = shutil.which('tesseract.exe')
        else:
            default_path = shutil.which('tesseract')
        return cls(tesseract_path=default_path)
   
class AppFileDialog(ABC):
    """Caixa de dialogo para seleção de vários tipos de arquivos."""

    _instance_file_dialog = None # Singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance_file_dialog is None:
            cls._instance_file_dialog = super(AppFileDialog, cls).__new__(cls)
        return cls._instance_file_dialog

    def __init__(self, preferences_dir: PreferencesDir = PreferencesDir.create_default()) -> None:
        self.preferences: PreferencesDir = preferences_dir
        
    def open_filename(self, input_type:LibraryDocs=LibraryDocs.ALL) -> str | None:
        """
            Caixa de dialogo para selecionar um arquivo
        """
        
        _filesTypes = [("Todos os arquivos", "*"),]
        _title = 'Selecione um arquivo'
        if input_type == LibraryDocs.SHEET:
            _filesTypes = [("Planilhas", "*.xlsx"), ("Arquivos CSV", "*.csv *.txt")]
            _title = 'Selecione uma planilha'
        elif input_type == LibraryDocs.EXCEL:
            _filesTypes = [("Arquivos Excel", "*.xlsx")]
            _title = 'Selecione uma planilha'
        elif input_type == LibraryDocs.IMAGE:
            _filesTypes = [("Arquivos de Imagem", "*.png *.jpg *.jpeg *.svg")]
            _title = 'Selecione Imagens'
        elif input_type == LibraryDocs.PDF:
            _filesTypes = [("Arquivos PDF", "*.pdf *.PDF"),]
            _title = 'Selecione arquivos PDF'
        #
        filename: str = filedialog.askopenfilename(
            title=_title,
            initialdir=self.preferences.initial_input_dir.absolute(),
            filetypes=_filesTypes,
        )
        
        if not filename:
            return None
        _dirname:str = os.path.dirname(filename)
        self.preferences.initial_input_dir = Directory(_dirname)
        return filename
    
    def open_filesname(self, input_type:LibraryDocs=LibraryDocs.ALL) -> Tuple[str]:
        """
            Selecionar um ou mais arquivos
        """
        
        _filesTypes = [("Todos os arquivos", "*"),]
        _title = 'Selecione um arquivo'
        if input_type == LibraryDocs.SHEET:
            _filesTypes = [("Planilas Excel CSV", "*.xlsx *.csv"), ("Arquivos CSV", "*.csv *.txt")]
            _title = 'Selecione uma planilha'
        elif input_type == LibraryDocs.EXCEL:
            _filesTypes = [("Arquivos Excel", "*.xlsx")]
            _title = 'Selecione uma planilha'
        elif input_type == LibraryDocs.IMAGE:
            _filesTypes = [("Arquivos de Imagem", "*.png *.jpg *.jpeg *.svg")]
            _title = 'Selecione Imagens'
        elif input_type == LibraryDocs.PDF:
            _filesTypes = [("Arquivos PDF", "*.pdf *.PDF"),]
            _title = 'Selecione arquivos PDF'
        #
        files:Tuple[str] = filedialog.askopenfilenames(
            title=_title,
            initialdir=self.preferences.initial_input_dir.absolute(),
            filetypes=_filesTypes,
        )
        
        if len(files) > 0:
            _dirname: str = os.path.abspath(os.path.dirname(files[0]))
            self.preferences.initial_input_dir = Directory(_dirname)
        return files
        
    def open_file_sheet(self) -> str | None:
        """
            Caixa de dialogo para selecionar um arquivo CSV/TXT/XLSX
        """
        return self.open_filename(LibraryDocs.SHEET)

    def open_files_sheet(self) -> list:
        """
            Selecionar uma ou mais planilhas
        """
        return self.open_filesname(LibraryDocs.SHEET)
    
    def open_files_image(self) -> List[str]:
        return self.open_filesname(LibraryDocs.IMAGE)
    
    def open_files_pdf(self) -> List[str]:
        return self.open_filesname(LibraryDocs.PDF)

    def open_folder(self, action_input=True) -> str | None:
        """Selecionar uma pasta"""
        if action_input == True:
            _initial: str = self.preferences.initial_input_dir.absolute()
        else:
            _initial: str = self.preferences.initial_output_dir.absolute()
            
        _select_dir:str = filedialog.askdirectory(
                initialdir=_initial,
                title="Selecione uma pasta",
            )
        
        if _select_dir is None:
            return None
        _dirname = os.path.abspath(_select_dir)
        if action_input == True:
            self.preferences.initial_input_dir = Directory(_dirname)
        else:
            self.preferences.initial_output_dir = Directory(_dirname)
        return _select_dir    
    
    def save_file(self, type_file: LibraryDocs = LibraryDocs.ALL_DOCUMENTS) -> str:
        """Abre uma caixa de dialogo para salvar arquivos."""
        if type_file == LibraryDocs.SHEET:
            _default = '.xlsx'
            _default_types = [("Arquivos Excel", "*.xlsx"), ("Arquivos CSV", "*.csv")]
        elif type_file == LibraryDocs.EXCEL:
            _default = '.xlsx'
            _default_types = [("Arquivos Excel", "*.xlsx")]
        elif type_file == LibraryDocs.CSV:
            _default = '.csv'
            _default_types = [("Arquivos CSV", "*.csv"), ("Arquivos de texto", "*.txt")]
        elif type_file == LibraryDocs.PDF:
            _default = '.pdf'
            _default_types = [("Arquivos PDF", "*.pdf")]
        else:
            _default = '.*'
            _default_types = [("Salvar Como", "*.*")]
        
        # Abre a caixa de diálogo "Salvar Como"
        dir_path = filedialog.asksaveasfilename(
            defaultextension=_default,  # Extensão padrão
            filetypes=_default_types,  # Tipos de arquivos suportados
            title="Salvar arquivo como",
            initialdir=self.preferences.initial_output_dir.absolute(),
        )

        if not dir_path:
            return
        self.preferences.initial_output_dir = Directory(dir_path)
        return dir_path
      
class AppSelectedFiles(ABCNotifyProvider):
    """
        Arquivos e documentos selecionados pelo usuário com os botões.
    Esta classe também pode ser usada por classes OBSERVER.
    
    use o método add_observer(self, object)
    object: precisa ter o método .notify_change_files()
    para receber as notificações quando um novo arquivo for adicionado a este item.
    """
    def __init__(self, file_dialog: AppFileDialog, *, max_files: int = 2000):
        super().__init__()
        self.file_dialog: AppFileDialog = file_dialog
        self._files: List[File] = []
        self.max_files:int = max_files
        self.num_files: int = 0
        
    @property
    def num_files_image(self) -> int: 
        return len([f for f in self.get_files_image()])
    
    @property
    def num_files_csv(self) -> int: 
        return len([f for f in self.get_files_csv()])
    
    @property
    def num_files_excel(self) -> int: 
        return len([f for f in self.get_files_excel()])
    
    @property
    def num_files_sheet(self) -> int: 
        return len([f for f in self.get_files_sheets()])

    @property
    def num_files_pdf(self) -> int:
        return len([f for f in self.get_files_pdf()])

    @property
    def files(self) -> List[File]:
        return self._files

    @files.setter
    def files(self, new:List[File]):
        if not isinstance(list, new):
            return
        if len(new) > self.max_files:
            new = new[0 : self.max_files]
        self._files = new
        self.num_files = len(self._files)

    @property
    def save_dir(self) -> Directory:
        return self.file_dialog.preferences.save_dir

    def select_file(self, type_file: LibraryDocs = LibraryDocs.ALL_DOCUMENTS):
        f: str = self.file_dialog.open_filename(type_file)
        if (f is None) or (f == ''):
            return
        fp = File(f)
        self.file_dialog.preferences.initial_input_dir = Directory(fp.absolute()).parent()
        self.add_file(fp)

    def select_files(self, type_file: LibraryDocs = LibraryDocs.ALL_DOCUMENTS):
        files: Tuple[str] = self.file_dialog.open_filesname(type_file)
        if len(files) < 1:
            return
        files_path = [File(f) for f in files]
        self.file_dialog.preferences.initial_input_dir = Directory(files_path[0].absolute()).parent()
        for fp in files_path:
            self.add_file(fp)

    def select_dir(self, type_file: LibraryDocs = LibraryDocs.ALL_DOCUMENTS):
        d: str = self.file_dialog.open_folder(True)
        if (d is None) or (d == ""):
            return
        self.file_dialog.preferences.initial_input_dir = Directory(d)
        input_files = AppInputFiles(self.file_dialog.preferences.initial_input_dir, maxFiles=self.max_files)
        files:List[File] = input_files.get_files(file_type=type_file)
        self.add_files(files)

    def save_file(self, type_file: LibraryDocs = LibraryDocs.ALL) -> File:
        f: str = self.file_dialog.save_file(type_file)
        return File(f)

    def select_output_dir(self):
        """Setar um diretório para salvar arquivos."""
        d: str = self.file_dialog.open_folder(False)
        if (d is None) or (d == ""):
            print(f'{__class__.__name__} diretório vazio')
            return
        print(f'Alterando o SaveDir: {d}')
        self.file_dialog.preferences.save_dir = Directory(d)
        
    def add_file(self, file:File) -> None:
        if self.num_files >= self.max_files:
            print(f'{__class__.__name__} o número máximo de arquivos já foi atingido: {self.max_files} !')
            return
        self._files.append(file)
        self.num_files += 1
        print(f'Arquivo adicionado: [{self.num_files}] {file.basename()}')
        self.notify_all()

    def add_files(self, files: List[File]):
        for f in files:
            self.add_file(f)

    def add_dir(self, d:Directory, *, file_type: LibraryDocs = LibraryDocs.ALL_DOCUMENTS):
        input_files: AppInputFiles = AppInputFiles(d, maxFiles=self.max_files)
        files = input_files.get_files(file_type=file_type)
        for f in files:
            self.add_file(File(f.absolute()))

    def clear(self) -> None:
        """Limpar a lista de arquivos selecionados."""
        self._files.clear()
        self.num_files = 0
        self.notify_all()

    def is_null(self) -> bool:
        return self.num_files == 0
    
    def get_files_sheets(self) -> List[File]:
        files = []
        for f in self.files:
            if f.is_sheet():
                files.append(f)
        return files

    def get_files_csv(self) -> List[File]:
        return [f for f in self.files if f.is_csv()]

    def get_files_excel(self) -> List[File]:
        return [f for f in self.files if f.is_excel()]

    def get_files_pdf(self) -> List[File]:
        return [f for f in self.files if f.is_pdf()]

    def get_files_image(self) -> List[File]:
        return [f for f in self.files if f.is_image()]
    
    def notify_all(self):
        for obs in self._observer_list:
            obs.update_notify()
        print(f'Notificação enviada para {len(self._observer_list)} observadores!')
