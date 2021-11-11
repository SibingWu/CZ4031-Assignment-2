import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class basicWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Query')

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        self.title_lbl = QLabel("Query", self)
        self.title_lbl.setStyleSheet("QLabel{font-size: 18pt;}")
        grid_layout.addWidget(self.title_lbl, 0, 0)

        self.query_lbl = QLabel("Query: ", self)
        grid_layout.addWidget(self.query_lbl, 2, 0)

        self.query_ta = QPlainTextEdit(self)
        self.query_ta.setFixedHeight(300)
        self.query_ta.setPlaceholderText("Enter query here.")
        grid_layout.addWidget(self.query_ta, 3, 0, 1, 4)

        self.generate_button = QPushButton('Generate', self)
        self.generate_button.setFixedWidth(300)
        self.generate_button.clicked.connect(self.onclick_generate)
        grid_layout.addWidget(self.generate_button, 4, 0, 1, 2)

        self.anotate_lbl = QLabel("Anotated Query: ", self)
        grid_layout.addWidget(self.anotate_lbl, 5, 0)

        self.anotate_ta = QPlainTextEdit(self)
        self.anotate_ta.setFixedHeight(300)
        self.anotate_ta.setReadOnly(True)
        grid_layout.addWidget(self.anotate_ta, 6, 0, 1, 4)

    def onclick_generate(self):
        queryTxt = self.query_ta.toPlainText()
        dic = {
            "query": queryTxt,
            }
        data_json = json.dumps(dic)
    	#emit json
    	#get json
        result = json.loads(data_json)
        self.anotate_ta.setPlainText(result['query'])
        #self.anotate_ta.setPlainText(result['schema'])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowExample = basicWindow()
    windowExample.show()
    sys.exit(app.exec_())

'''
sql

Select r_name
From region
Where r_regionkey = 1

Select n_name, r_name
From region, nation
Where n_regionkey = r_regionkey

Select s_name
From supplier, nation
Where s_nationkey = n_nationkey
And acctbal > 100000

Select p_name, s_name
From part, supplier, partsupp
Where ps__suppkey = s_suppkey
And ps_partkey = p_partkey
And ps_availqty >1000
And acctbal > 100000
And p_size = 10


'''