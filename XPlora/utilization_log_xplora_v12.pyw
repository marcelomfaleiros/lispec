# -*- coding: utf-8 -*-
# revisão 19/04/2024

import os
from PyQt5 import QtWidgets, uic
import csv
import pandas as pd

class Report(QtWidgets.QWidget):
        
    '''
       
    ''' 

    file_header = ["Data", "Início", "Fim", "Tempo total (h)", "Temp. sala", 
                   "Humidade", "Usuário", "Status do usuário",
                   "Orientador", "Operador", "Natureza da amostra", 
                   "Número de amostras", "Descrição da amostra",
                   "Aquisição de espectro", "Sistema de Imageamento",
                   "Início laser", "Final laser", "Tempo laser (h)","Potência do laser", 
                   "Filtros", "Objetivas", "Calibração", "Forno Linkam",
                   "Temperatura inicial", "Temperatura final", "Observações",
                   "Problema no instrumento"]
    
    estat_method = ["Advisor", "User", "Sample nature", "Laser"]

    year_list = ["2024", "2025", "2026", "2027", "2028", "2029", "2030",
                "2031", "2032", "2033", "2034", "2035", "2036", "2037",
                "2038", "2039", "2040", "2041", "2042", "2043", "2044",
                "2045", "2046", "2047", "2048", "2049", "2050"]

    technicians_list = ["Milene Heloisa Martins", "Marcelo Meira Faleiros",
                        "Técnico Horiba"]

    months_list = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep",
                   "Oct", "Nov", "Dec"]
    
    coverage = ["Month", "Year", "Global"]
    
    data = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi('utilization_log_xplora_intrfc_v12.ui', self)

        self.save_pushButton.clicked.connect(self.save)
        self.report_pushButton.clicked.connect(self.report)
        self.cadastro_pushButton.clicked.connect(lambda: self.cadastro('add'))
        self.exclui_pushButton.clicked.connect(lambda: self.cadastro('exclui'))
        self.load_pushButton.clicked.connect(self.load_list)

        advisors_file = pd.read_csv('advisors_list.csv')
        self.advisors_list = list(advisors_file['Orientador'])
        self.advisor_comboBox.addItems(self.advisors_list)

        self.estat_method_comboBox.addItems(self.estat_method)
        self.abrangencia_comboBox.addItems(self.coverage)
        self.year_comboBox.addItems(self.year_list)
        self.month_comboBox.addItems(self.months_list)   

        self.load_list()     

    def load_list(self):
        #importar users_list   
        self.user_comboBox.clear()
        self.technician_comboBox.clear()

        users_file = pd.read_csv('users_list.csv')
        users_list = list(users_file['Usuarios'])

        self.user_comboBox.addItems(sorted(users_list))
        self.technician_comboBox.addItems(sorted(users_list)) 

    def write_data(self):
        date = self.calendarWidget.selectedDate().toString("dd/MM/yy")

        self.month = int(date[3:5])
        self.year = date[6:]
        
        user = self.user_comboBox.currentText()
        technician = self.technician_comboBox.currentText()
        advisor = self.advisor_comboBox.currentText()
       
        if self.ic_checkBox.isChecked():
           user_status = self.ic_checkBox.text()
        elif self.mestrado_checkBox.isChecked():
           user_status = self.mestrado_checkBox.text()
        elif self.doutorado_checkBox.isChecked():
           user_status = self.doutorado_checkBox.text()
        elif self.posdoc_checkBox.isChecked():
           user_status = self.posdoc_checkBox.text()
        elif self.pesquisador_checkBox.isChecked():
           user_status = self.pesquisador_checkBox.text()
        elif self.test_checkBox.isChecked():
           user_status = self.test_checkBox.text()
           advisor = "N/C"
        elif self.professor_checkBox.isChecked():
           user_status = self.professor_checkBox.text()
           advisor = "N/C"
        elif self.technician_checkBox.isChecked():
           user_status = self.technician_checkBox.text()
           advisor = "N/C"
        elif self.ca_checkBox.isChecked():
           user_status = self.ca_checkBox.text()
           advisor = "CA"
        elif self.treinamento_checkBox.isChecked():
           user_status = self.treinamento_checkBox.text()
           advisor = "N/C"
        else:
           user_status = "N/C" 

        ini_time = self.start_timeEdit.text()
        fin_time = self.stop_timeEdit.text()    
        if fin_time == "00:00":
           fin_time = "24:00"
        else:
           fin_time = fin_time

        hora_ini = int(ini_time[:2])
        hora_fin = int(fin_time[:2])
        min_ini = int(ini_time[3:])/60
        min_fin = int(fin_time[3:])/60
   
        horas = round((hora_fin + min_fin) - (hora_ini + min_ini), 1)
        total_time = str(horas)
        
        temp = self.temperature_lineEdit.text()
        humid = self.humidity_lineEdit.text()

        smpl_nature = []
        if self.powder_checkBox.isChecked():
           smpl_nature.append(self.powder_checkBox.text())
        if self.gel_checkBox.isChecked():
           smpl_nature.append(self.gel_checkBox.text())
        if self.piece_checkBox.isChecked():
           smpl_nature.append(self.piece_checkBox.text())
        if self.cachimbo_checkBox.isChecked():
           smpl_nature.append(self.cachimbo_checkBox.text())
        if self.al_checkBox.isChecked():
           smpl_nature.append(self.al_checkBox.text())
        if self.outra_amostra_checkBox.isChecked():
           smpl_nature.append(self.outra_amostra_textEdit.toPlainText())

        smpl_number = self.numero_amostras_lineEdit.text()

        smpl_description = self.description_plainTextEdit.toPlainText()

        spec_acq = []
        if self.pontoaponto_checkBox.isChecked():
           spec_acq.append(self.pontoaponto_checkBox.text())
        if self.binning_checkBox.isChecked():
           spec_acq.append(self.binning_checkBox.text())
        if self.espectro_autofocus_checkBox.isChecked():
           spec_acq.append(self.espectro_autofocus_checkBox.text())

        image_system = [] 
        if self.imagemxy_checkBox.isChecked():
           image_system.append(self.imagemxy_checkBox.text()) 
        if self.imagem_autofocus_checkBox.isChecked():
           image_system.append(self.imagem_autofocus_checkBox.text())
        if self.imagemxyz_checkBox.isChecked():
           image_system.append(self.imagemxyz_checkBox.text())
        if self.navmap_checkBox.isChecked():
           image_system.append(self.navmap_checkBox.text())
        if self.swift_checkBox.isChecked():
           image_system.append(self.swift_checkBox.text())
        if self.mosaico_checkBox.isChecked():
           image_system.append(self.mosaico_checkBox.text())

        ini_laser_time = self.laser_start_timeEdit.text()
        fin_laser_time = self.laser_stop_timeEdit.text()
        if fin_laser_time == "00:00":
           fin_laser_time = "24:00"
        else:
           fin_laser_time = fin_laser_time

        hora_laser_ini = int(ini_laser_time[:2])
        hora_laser_fin = int(fin_laser_time[:2])
        min_laser_ini = int(ini_laser_time[3:])/60
        min_laser_fin = int(fin_laser_time[3:])/60
        horas_laser = round((hora_laser_fin + min_laser_fin) - (hora_laser_ini + min_laser_ini), 1)
                       
        total_laser_time = str(horas_laser)

        laser_power = self.laser_power_lineEdit.text()

        filters = []
        if self.filtro01_checkBox.isChecked():
           filters.append(self.filtro01_checkBox.text())
        if self.filtro1_checkBox.isChecked():
           filters.append(self.filtro1_checkBox.text())
        if self.filtro10_checkBox.isChecked():
           filters.append(self.filtro10_checkBox.text())
        if self.filtro25_checkBox.isChecked():
           filters.append(self.filtro25_checkBox.text())
        if self.filtro50_checkBox.isChecked():
           filters.append(self.filtro50_checkBox.text())
        if self.filtro100_checkBox.isChecked():
           filters.append(self.filtro100_checkBox.text())

        objetivas = []
        if self.objetiva10x_checkBox.isChecked():
           objetivas.append(self.objetiva10x_checkBox.text())
        if self.objetiva50x_checkBox.isChecked():
           objetivas.append(self.objetiva50x_checkBox.text())
        if self.objetiva50xfluor_checkBox.isChecked():
           objetivas.append(self.objetiva50xfluor_checkBox.text())
        if self.objetiva100x_checkBox.isChecked():
           objetivas.append(self.objetiva100x_checkBox.text())

        cal = []
        if self.cal_si_checkBox.isChecked():
           cal.append(self.cal_si_checkBox.text())
        if self.cal_outro_checkBox.isChecked():
           cal.append(self.cal_outro_textEdit.toPlainText())

        if self.ts1500_checkBox.isChecked():
           linkam = self.ts1500_checkBox.text()
        elif self.thms600_checkBox.isChecked():
           linkam = self.thms600_checkBox.text()
        else:
           linkam = "N/C"

        Tstart = self.linkam_startT_lineEdit.text()
        Tstop = self.linkam_stopT_lineEdit.text()

        observations = self.observations_textEdit.toPlainText()   

        if self.inst_probl_checkBox.isChecked():
            problems = self.inst_probl_textEdit.toPlainText()  
        else:
           problems = "N/C"                      

        self.data = [date, ini_time, fin_time, total_time, temp, humid, user, 
                     user_status, advisor, technician, smpl_nature, smpl_number,
                     smpl_description, spec_acq, image_system, ini_laser_time,
                     fin_laser_time, total_laser_time, laser_power, filters, 
                     objetivas, cal, linkam, Tstart, Tstop, observations, problems]
              
    def save(self):
        self.write_data()
        month_file_label = self.months_list[self.month - 1] + self.year + '_data_log.csv'
        year_file_label = '20' + self.year + '_data_log.csv'
        global_file_label = 'data_log.csv'

        if os.path.exists(month_file_label):
            with open(month_file_label, 'a', newline='', encoding='utf8') as mf:
                write = csv.writer(mf)                
                write.writerow(self.data)       
        else:
            with open(month_file_label, 'a', newline='', encoding='utf8') as mf:
                write = csv.writer(mf)
                write.writerow(self.file_header)
                write.writerow(self.data)

        if os.path.exists(year_file_label):
            with open(year_file_label, 'a', newline='', encoding='utf8') as yf:
                write = csv.writer(yf)                
                write.writerow(self.data)       
        else:
            with open(year_file_label, 'a', newline='', encoding='utf8') as yf:
                write = csv.writer(yf)
                write.writerow(self.file_header)
                write.writerow(self.data)

        if os.path.exists(global_file_label):
            with open(global_file_label, 'a', newline='', encoding='utf8') as gf:
                write = csv.writer(gf)                
                write.writerow(self.data)       
        else:
            with open(global_file_label, 'a', newline='', encoding='utf8') as gf:
                write = csv.writer(gf)
                write.writerow(self.file_header)
                write.writerow(self.data)

        self.salvar_label.setText('OK - Arquivo salvo')

        '''with open('raw_data_log.txt', 'a') as tf:
            tf.write('\r')
            tf.write(str(self.data) + '\r')'''   

    def report(self): 
       #search parameters      
       search_method = self.estat_method_comboBox.currentText()
       coverage = self.abrangencia_comboBox.currentText()
       year = self.year_comboBox.currentText()
       month = self.month_comboBox.currentText() 

       #file to be opened
       if coverage == 'Global':
          file = 'data_log.csv'
       elif coverage == 'Year':
          file = year + '_data_log.csv'
       elif coverage == 'Month':
          file = month + year[2:] + '_data_log.csv'

       #read csv file
       data = pd.read_csv(file)

       if search_method == 'Laser':
          total_time = data['Tempo laser (h)'].sum()

          search_object = data['Orientador']    
          search_object = list(set(search_object))
          search_object = sorted(search_object)

          object_arr = ''

          for n in search_object:
             if n in self.advisors_list:
                array_orientador = data[data.Orientador == n]
                parcial_time = round(array_orientador['Tempo laser (h)'].sum(), 1)
                object_arr += n + ' ' + str(parcial_time) + '\n\n'  
                         
          self.report_label.setText('Total laser time: ' + str(round(total_time, 1)) + 'h\n\n' +
                                    object_arr)
      
       elif search_method == 'Advisor':
          total_time = data['Tempo total (h)'].sum()

          search_object = data['Orientador']       
          search_object = list(set(search_object))
          search_object = sorted(search_object)

          object_arr = ''

          for n in search_object:
             if n in self.advisors_list:
                array_orientador = data[data.Orientador == n]
                parcial_time = round(array_orientador['Tempo total (h)'].sum(), 1)
                object_arr += n + '     ' + str(parcial_time) + ' h \n\n'  
                
          self.report_label.setText('Total time: ' + str(round(total_time, 1)) + 'h\n\n' +
                                    object_arr)
          
    def cadastro(self, action=str):  
       user = self.user_lineEdit.text()
       if action == 'add':         
          user = [user] 
          with open('users_list.csv', 'a', newline='', encoding='utf8') as uf:
              write = csv.writer(uf)                
              write.writerow(user) 
       elif action == 'exclui':
          users = pd.read_csv('users_list.csv')
          users = users.drop(users[users.Usuarios == user].index)
          users.to_csv('users_list.csv', index=False)                                                       

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    tela = Report()
    tela.show()
    app.exec_()