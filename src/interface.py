import logging
import sys
import json
from PyQt5.QtWidgets import *

from preprocessing import Preprocessing


class basicWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.p = Preprocessing('localhost', '5432', 'postgres', 'postgres', '123456')

    def initUI(self):

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Query')

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        self.host_lbl = QLabel("Host: ", self)
        grid_layout.addWidget(self.host_lbl, 0, 0)
        self.host_tb = QLineEdit(self)
        self.host_tb.setFixedWidth(200)
        self.host_tb.setText("localhost")
        grid_layout.addWidget(self.host_tb, 0, 1)

        self.db_lbl = QLabel("Database", self)
        grid_layout.addWidget(self.db_lbl, 1, 0)
        self.db_tb = QLineEdit(self)
        self.db_tb.setFixedWidth(200)
        self.db_tb.setText("postgres")
        grid_layout.addWidget(self.db_tb, 1, 1)

        self.port_lbl = QLabel("Port: ", self)
        grid_layout.addWidget(self.port_lbl, 2, 0)
        self.port_tb = QLineEdit(self)
        self.port_tb.setFixedWidth(200)
        self.port_tb.setText("5432")
        grid_layout.addWidget(self.port_tb, 2, 1)

        self.user_lbl = QLabel("Username: ", self)
        grid_layout.addWidget(self.user_lbl, 3, 0)
        self.user_tb = QLineEdit(self)
        self.user_tb.setFixedWidth(200)
        self.user_tb.setText("postgres")
        grid_layout.addWidget(self.user_tb, 3, 1)

        self.pw_lbl = QLabel("Password: ", self)
        grid_layout.addWidget(self.pw_lbl, 4, 0)
        self.pw_tb = QLineEdit(self)
        self.pw_tb.setFixedWidth(200)
        self.pw_tb.setText("123456")
        self.pw_tb.setEchoMode(QLineEdit.Password)
        grid_layout.addWidget(self.pw_tb, 4, 1)

        self.connect_button = QPushButton('Connect to database', self)
        self.connect_button.setFixedWidth(400)
        self.connect_button.clicked.connect(self.onclick_connect)
        grid_layout.addWidget(self.connect_button, 5, 0, 1, 3)

        self.query_lbl = QLabel("Query: ", self)
        grid_layout.addWidget(self.query_lbl, 6, 0)

        self.query_ta = QPlainTextEdit(self)
        self.query_ta.setFixedHeight(300)
        self.query_ta.setPlaceholderText("Enter query here.")
        grid_layout.addWidget(self.query_ta, 7, 0, 1, 4)

        self.generate_button = QPushButton('Generate', self)
        self.generate_button.setFixedWidth(300)
        self.generate_button.clicked.connect(self.onclick_generate)
        grid_layout.addWidget(self.generate_button, 8, 0, 1, 2)

        self.anotate_lbl = QLabel("Annotated Query: ", self)
        grid_layout.addWidget(self.anotate_lbl, 9, 0)

        self.anotate_ta = QPlainTextEdit(self)
        self.anotate_ta.setFixedHeight(300)
        self.anotate_ta.setReadOnly(True)
        grid_layout.addWidget(self.anotate_ta, 10, 0, 1, 4)

    def onclick_connect(self):
        host = self.host_tb.text()
        database = self.db_tb.text()
        port = self.port_tb.text()
        username = self.user_tb.text()
        password = self.pw_tb.text()
        self.p = Preprocessing(host, port, database, username, password)


    def onclick_generate(self):
        queryTxt = self.query_ta.toPlainText()
        print(queryTxt)
        dic = {
            "query": queryTxt,
            }
        data_json = json.dumps(dic)
        # emit json
        annotation = self.get_annotation(queryTxt)
        self.anotate_ta.setPlainText(annotation)
        # get json
        # result = json.loads(data_json)
        # self.anotate_ta.setPlainText(result['query'])
        # self.anotate_ta.setPlainText(result['schema'])

    def get_annotation(self, queryTxt):
        try:
            parsed_plan = self.p.parse(queryTxt)
            annotation = self.p.annotate(parsed_plan)

            return annotation
        except Exception as e:
            logging.error(e)
            self.p.conn.rollback()
            return 'Invalid query input'

      
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
