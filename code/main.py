import sys
import json
from PyQt5 import QtWidgets, QtCore
from screen import Ui_MainWindow

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.salvarJogo.clicked.connect(self.salvarJogo)
        self.ui.sair.clicked.connect(self.close)
        self.ui.carregarJogo.clicked.connect(self.carregarJogo)
        self.ui.novoJogo.clicked.connect(self.novoJogo)
        
    def clear(self):
        self.ui.lineNome.clear()
        self.ui.lineIdade.clear()
        self.ui.lineAltura.clear()
        self.ui.checkF.setChecked(False)
        self.ui.checkM.setChecked(False)
        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
        
    def novoJogo(self):
        self.clear()
        QtWidgets.QMessageBox.information(self, "Novo jogo", "Novo jogo iniciado!")
    
    def salvarJogo(self):
        
        data = {
            "nome" : self.ui.lineNome.text(),
            "idade" : self.ui.lineIdade.text(),
            "data_nascimento": self.ui.dateEdit.date().toString("yyyy-MM-dd"),
            "altura" : self.ui.lineAltura.text(),
            "sexo" : "Feminino" if self.ui.checkF.isChecked() else "Masculino" if self.ui.checkM.isChecked() else "Não informado"
        }

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Salvar jogo", "", "Arquivos JSON (*.json)")

        if file_path:
            try:
                #Verifica se o arquivo termina com '.json'
                if not file_path.endswith('.json'):
                    file_path += '.json'
                
                #Salva o arquivo JSON no local escolhido
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

                QtWidgets.QMessageBox.information(self, "Sucesso", "Jogo salvo com sucesso ")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erro", f"Erro ao salvar o jogo: {e}")
        else:
            QtWidgets.QMessageBox.warning(self, "Erro", "Nenhum arquivo selecionado ")

    def carregarJogo(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Carregar jogo", "", "Arquivos JSON (*.json)")
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    
                    data = json.load(file)
                    
                    self.ui.lineNome.setText(data.get("nome", ""))
                    self.ui.dateEdit.setDate(QtCore.QDate.fromString(data.get("data_nascimento", "2000-01-01"), "yyyy-MM-dd"))
                    self.ui.lineIdade.setText(data.get("idade", ""))
                    self.ui.lineAltura.setText(data.get("altura", ""))

                    if data.get("sexo") == "Feminino":
                        self.ui.checkF.setChecked(True)
                    elif data.get("sexo") == "Masculino":
                        self.ui.checkM.setChecked(True)
                    else:
                        self.ui.checkF.setChecked(False)
                        self.ui.checkM.setChecked(False)

                QtWidgets.QMessageBox.information(self, "Sucesso", "Jogo carregado com sucesso")

            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Erro", f"Erro ao carregar o jogo : {e}")
        else:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'Nenhum arquivo selecionado')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())