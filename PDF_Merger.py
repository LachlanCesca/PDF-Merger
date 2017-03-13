import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyPDF2


class PDF_Merger(QWidget):

    def __init__(self, parent = None):
        super(PDF_Merger, self).__init__(parent)
        
        # Variables
        self.file_list = []
        self.file_filter = "PDF files (*.pdf)"
        self.total_pages = 0
        
        # Window properties
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("PDF File Merger")

        # Header label
        self.le = QLabel("Choose files to merge:")	
        layout.addWidget(self.le)
            
        
        header = QHBoxLayout()
        
        # Open file dialog
        self.btn_select = QPushButton("Select PDF")
        self.btn_select.clicked.connect(self.open_file)		
        header.addWidget(self.btn_select)
        
        # Remove item button
        self.btn_remove = QPushButton("Remove PDF")
        self.btn_remove.clicked.connect(self.remove_pdf)		
        header.addWidget(self.btn_remove)

        layout.addLayout(header)
        
        # List widget for storign files
        self.contents = QListWidget()
        #self.contents.setDragDropMode(QAbstractItemView.InternalMove) #Allows ordering
        layout.addWidget(self.contents)
        
        footer = QHBoxLayout()
        
        # Number of pages label
        self.l_pages = QLabel("Total number of pages: "+str(self.total_pages))	
        footer.addWidget(self.l_pages)

        self.btn_merge = QPushButton("Merge pdf's")
        self.btn_merge.clicked.connect(self.save_file)
        footer.addWidget(self.btn_merge)
        
        layout.addLayout(footer)

        
    def remove_pdf(self):
        selected = self.contents.currentItem()
        if selected is not None:
            index = self.contents.row(selected)
            self.total_pages -= self.num_pages(self.file_list[index])
            self.file_list.pop(index)
            self.contents.takeItem(index)
            self.l_pages.setText("Total number of pages: "+str(self.total_pages))
        
        
        
    def open_file(self):
        if(len(self.file_list)>0):
            f = str(self.file_list[-1])
            directory = f[:f.rfind('/')]
        else:
            directory = 'c:\\'
        
        pdf_dialog = QFileDialog()
        pdf_dialog.setFileMode(QFileDialog.ExistingFiles)
        
        f_paths = pdf_dialog.getOpenFileNamesAndFilter(self, 'Open file', 
        directory,self.file_filter)
        for f_path in f_paths[0]:
            f = str(f_path)
            print f
            if f[-4:] == '.pdf':
                self.update_page(f)

    def update_page(self, f_path):      
        f_path = str(f_path)
        f_name = f_path[f_path.rfind("\\")+1:]
        
        f_pages = self.num_pages(f_path)
        self.total_pages += f_pages
        
        self.file_list.append(f_path)
        
        if(f_pages > 1):
            list_string = "{}     [{} Pages]".format(f_name,f_pages)
        else:
            list_string = "{}     [{} Page]".format(f_name,f_pages)
        QListWidgetItem(list_string,self.contents)
        self.l_pages.setText("Total number of pages: "+str(self.total_pages))
        
        
    def save_file(self):
        save_name = QFileDialog.getSaveFileName(self, "Save file", 
        "c:\\", self.file_filter)
        if save_name != "":
            self.merge_pdfs(save_name)

    def merge_pdfs(self,save_name):
        pdfs_in = [open(name,'rb') for name in self.file_list]
        pdfs_reader = [PyPDF2.PdfFileReader(pdf_in) for pdf_in in pdfs_in]
        pdf_writer = PyPDF2.PdfFileWriter()

        for pdf_reader in pdfs_reader:
            for pagenum in range(pdf_reader.numPages):
                page = pdf_reader.getPage(pagenum)
                pdf_writer.addPage(page)

        pdf_out = open(save_name, 'wb')
        pdf_writer.write(pdf_out)
        pdf_out.close()

        for pdf_in in pdfs_in:
            pdf_in.close()
				
                
    def num_pages(self,file_path):
        pdf = open(file_path,'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf)
        num_pages = pdf_reader.numPages
        pdf.close()
        return num_pages
        
def main():
    app = QApplication(sys.argv)
    ex = PDF_Merger()

    ex.show()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
    main()
