import json
import os
import bs4
import requests
import sys
#from control.control import Control
#from curses.ascii import controlnames
from mainwindow_ui import Ui_MainWindow
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QApplication, QMainWindow

basedir = os.path.dirname(__file__)

tick = QImage(os.path.join(basedir, "tick.png"))
datafile = os.path.join(basedir,"config", "isin.json")



class FondiModel(QAbstractTableModel):
    '''
    COLUMNS = [
        ("isin", "ISIN"),
        ("desc", "Description"),
        ("qta", "Quantity"),
        ("investment", "Investment"),
    ]
    '''
    def __init__(self,json_data=None):
        super().__init__()
        self.json_data = json_data or {}

    def rowCount(self, parent=None):
        return len(self._fondi)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            row = self._fondi[index.row()]

            key = self.COLUMNS[index.column()][0]

            if key == "desc":
                return row.get("desc", row.get("Desc", ""))

            return row.get(key)

        return None



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = FondiModel()
        self.load()
        # l=len(self.todoFondi["fondi"])
        # print(l)
        # self.model = FondiModel(self.todoFondi)


        self.todoView.setModel(self.model)
        #self.addButton.pressed.connect(self.add)
        #self.deleteButton.pressed.connect(self.delete)
        #self.completeButton.pressed.connect(self.complete)
        #self.getFounds = Fondi()

    def add(self):
        """
        Add an item to our todo list, getting the text from the
        QLineEdit .todoEdit and then clearing it.
        """
        text = self.todoEdit.text()
        # Remove whitespace from the ends of the string.
        text = text.strip()
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.model.todos.append((False, text))
            # Trigger refresh.
            self.model.layoutChanged.emit()
            # Empty the input
            self.todoEdit.setText("")
            self.save()

    def delete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            # Indexes is a single-item list in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
            self.save()

    def complete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            # .dataChanged takes top-left and bottom right, which
            # are equal for a single selection.
            self.model.dataChanged.emit(index, index)
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
            self.save()

    def load(self):
        try:
            with open(datafile, "r", encoding="utf-8") as f:
                self.model.json_data = json.load(f)
                #print(self.model.json_data)
        except FileNotFoundError:
            print("Il file non esiste.")

        except json.JSONDecodeError:
            print("Il file non contiene un JSON valido.")

        except Exception as e:
            print(f"Errore imprevisto: {e}")


    def save(self):
        with open(datafile, "w") as f:
            json.dump(self.model.todos, f)

class Fondi:
    def __init__(self,nameFile):
        self

    def help():
        sys.stdout.write("""Usage :-
        $ ./getFunds [Arg1: filename.txt] [optional Arg] [Arg2: outputFileName.csv]

        Optional Argument:  -ft   , gets data from https://markets.ft.com
                            -br   , gets data from https://www.boursorama.com default

        $ ./getFunds --help or -h		# Show usage

        Example: $ ./getFunds.py fundcodes.txt -ft funds_ft.csv
                 $ ./getFunds.py fundcodes.txt funds_br.csv\n""")
        exit()

    def getfunds(self):
        try:
            data = json.load(open(self.nameFile, "r"+"w"))
        except Exception as IOError:
            print("Open file error")
            exit

        # for i in range( len(data["fondi"])):
        # isinCode = data["fondi"][i]["isin"]
        # investment = data["fondi"][i]["investment"]
        # prezzoAttuale = data["fondi"][i][]

        # if len(sys.argv) > 1:
        #     file_name = sys.argv[1]
        #     output_file_name = sys.argv[-1]
        # else:
        #     file_name = "isin.txt"
        #     output_file_name = "isin.csv"

        # with open(file_name, 'r') as file:
        #     fund_codes = file.readlines()

        # print("Getting ISIN codes from file...")
        # isin_codes=[i.strip() for i in fund_codes]

        # if sys.argv[-2] =='-ft':
        #     url = 'https://markets.ft.com/data/funds/tearsheet/summary?s='
        # else:
        url = 'https://www.boursorama.com/bourse/opcvm/cours/'

        # print(isin_codes)
        name_list = []
        price_list = []
        date_list = []
        guadagno = 0.0
        # print("Getting Prices...\nPlease Wait")
        for i in range(len(data["fondi"])):
            isinCode = data["fondi"][i]["isin"]
            res = requests.get(url + isinCode, headers={'User-Agent': 'Mozilla/5.0'})
            # Checking for Bad download
            try:
                res.raise_for_status()
            except Exception as exc:
                print("There was a problem: %s" % (exc))

            # making soup
            soup_res = bs4.BeautifulSoup(res.text, 'html.parser')
            try:
                # if sys.argv[-2] =='-ft':
                #     name = soup_res.find('h1', {'class':'mod-tearsheet-overview__header__name mod-tearsheet-overview__header__name--large'})
                #     price = soup_res.find('span',{'class':'mod-ui-data-list__value'})
                #     name_list.append(name.text)
                #     price_list.append(price.text.replace(',', ''))
                # else:
                name = soup_res.find('a', {'class': 'c-faceplate__company-link'})
                price = soup_res.find('span', {'class': 'c-instrument c-instrument--last'})
                name_list.append(name.text.strip())
                price_list.append(''.join(price.text.split()))
                f_Price = float(price.text.replace(",", "."))
                prezzoAttuale = (float)(data["fondi"][i]["qta"]) * f_Price
                guadagno += prezzoAttuale - (float)(data["fondi"][i]["investment"])
            except:
                name_list.append('NA')
                price_list.append('NA')
                continue

        print("Totale Guadagno Attuale", guadagno)
        #     date_list.append(datetime.datetime.now())

        # with open(output_file_name, 'w', encoding='utf-8') as f:
        #     print('Saving File as', output_file_name)
        #     for code, name, price, dateNow in zip(isin_codes, name_list, price_list,date_list):
        #         f.write(code + ", " + name + ", " + price + ", " + str(dateNow.day) + "/" +str(dateNow.month) + "/" + str(dateNow.year) + "\n")

   # def main():
        # control = Control()
        # if len(sys.argv)==1 or sys.argv[1]== '--help' or sys.argv[1]=='-h' or len(sys.argv)>4:
        #     help()
        # else:
        #getFunds()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
