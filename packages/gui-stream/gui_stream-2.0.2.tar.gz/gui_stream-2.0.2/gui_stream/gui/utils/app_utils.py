#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import List
from pathlib import Path
from abc import ABC, abstractmethod

from soup_files import (
    File as file_path,
    Directory as directory_path,
    InputFiles as input_files,
    JsonConvert, JsonData, LibraryDocs,
)

from convert_stream import (
    LibraryImage, LibraryPDF, PageDocumentPdf, DocumentPdf, ImageStream, PdfStream, ImageObject,
)

from ocr_stream import RecognizeImage, RecognizePdf, LibraryOCR


class File(object):
    def __init__(self, filename):
        self.file_path:file_path = file_path(filename)
        
    @property
    def path(self) -> Path:
        return self.file_path.path
    
    @path.setter
    def path(self, new:Path):
        self.file_path.path = new

    def is_image(self) -> bool:
        return self.file_path.is_image()

    def is_pdf(self) -> bool:
        return self.file_path.is_pdf()
        
    def is_excel(self) -> bool:
        return self.file_path.is_excel()
        
    def is_csv(self) -> bool:
        return self.file_path.is_csv()

    def is_sheet(self) -> bool:
        return self.file_path.is_sheet()

    def update_extension(self, e:str) -> File:
        """
            Retorna uma instância de File() no mesmo diretório com a nova
        extensão informada.
        """
        self.file_path.update_extension(e)

    def get_text(self) -> str | None:
        return self.file_path.get_text()

    def write_string(self, s:str):
        self.file_path.write_string(s)

    def write_list(self, items:List[str]):
        self.file_path.write_list(items)

    def name(self):
        return self.file_path.name()
    
    def name_absolute(self) -> str:
        return self.file_path.name_absolute()

    def extension(self) -> str:
        return self.file_path.extension()

    def dirname(self) -> str:
        return self.file_path.dirname()

    def basename(self) -> str:
        return self.file_path.basename()

    def exists(self) -> bool:
        return self.file_path.exists()

    def absolute(self) -> str:
        return self.file_path.absolute()
    
    def size(self):
        return self.file_path.size()
    
    def md5(self) -> str | None:
        """Retorna a hash md5 de um arquivo se ele existir no disco."""
        return self.file_path.md5()
    
    
class Directory(object):
    def __init__(self, dirpath):
        self.directory_path:directory_path = directory_path(dirpath)
        
    def iterpaths(self) -> List[Path]:
        return self.directory_path.iterpaths()
    
    def content_files(self) -> List[File]:
        return self.directory_path.content_files()
    
    def basename(self) -> str:
        return self.directory_path.basename()

    def mkdir(self):
        self.directory_path.mkdir()

    def absolute(self) -> str:
        return self.directory_path.absolute()

    def concat(self, d:str, create:bool=False) -> Directory:
        return self.directory_path.concat(d, create=create)

    def parent(self) -> Directory:
        return self.directory_path.parent()

    def join_file(self, name:str) -> File:
        return self.directory_path.join_file(name)
   
   
class AppJsonData(JsonData):
    def __init__(self, string):
        super().__init__(string)
        
class AppJsonConvert(JsonConvert):
    def __init__(self, jsonData):
        super().__init__(jsonData)
   
class AppInputFiles(input_files):
    def __init__(self, d:Directory, *, maxFiles = 4000):
        super().__init__(d.directory_path, maxFiles=maxFiles)
   

class AppPageDocumentPdf(PageDocumentPdf):
    def __init__(self, page):
        super().__init__(page)

    def __eq__(self, other:AppPageDocumentPdf):
        if not isinstance(other, AppPageDocumentPdf):
            return NotImplemented
        return self.to_string() == other.to_string()

    def __hash__(self):
        return hash(self.to_string())

        
class AppDocumentPdf(DocumentPdf):
    def __init__(self, library=LibraryPDF.FITZ, max_pages:int=4100):
        super().__init__(library)
        self.max_pages:int = max_pages
        
    def add_page(self, page):
        if self.num_pages >= self.max_pages:
            print(
                f'{__class__.__name__} Erro Número máximo de páginas atingido, [{self.max_pages}]'
            )
            return
        return super().add_page(page)
    
    def add_file_pdf(self, file):
        if not file.is_pdf():
            print(f'não é um arquivo PDF! {file.basename()}')
            return
        return super().add_file_pdf(file)


class AppImageObject(ImageObject):
    def __init__(self, img_obj):
        super().__init__(img_obj)
        
    def to_file(self, f):
        self.set_paisagem()
        return super().to_file(f)


class AppImageStream(ImageStream):
    def __init__(self, *, library_image=LibraryImage.OPENCV, library_pdf=LibraryPDF.FITZ):
        super().__init__(library_image=library_image, library_pdf=library_pdf)

    def set_backgroud_black(self):
        for num, img in enumerate(self.images):
            print(f'Escurecendo imagem: [{num+1} de {self.num_images}]')
            self.images[num].set_black()

    def set_background_gray(self):

        for num, img in enumerate(self.images):
            print(f'Escurecendo imagem: [{num+1} de {self.num_images}]')
            self.images[num].set_gray()

        
class AppPdfStream(PdfStream):
    def __init__(self, *, library_pdf=LibraryPDF.FITZ, library_image=LibraryImage.OPENCV):
        super().__init__(library_pdf=library_pdf, library_image=library_image)

    def add_page(self, p):
        return super().add_page(AppPageDocumentPdf.create_from_page_bytes(p.to_bytes()))

    def to_document(self) -> AppDocumentPdf:
        doc:AppDocumentPdf = AppDocumentPdf()
        doc.add_pages(self.pages)
        return doc
    
    def add_image(self, image: AppImageObject):
        img_stream = AppImageStream()
        img_stream.add_image(image)
        self.add_pages(img_stream.to_pages_pdf())
    
class AppRecoginzeImage(RecognizeImage):
    def __init__(self, module_ocr):
        super().__init__(module_ocr)
        

class AppRecognizePdf(RecognizePdf):
    def __init__(self, recognize_image):
        super().__init__(recognize_image)    

 