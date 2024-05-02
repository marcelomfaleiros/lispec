# -*- coding: utf-8 -*-
# revisão 19/04/2024

import os
from PyQt5 import QtWidgets as qtw
from utilization_log_t64000_intrfc import Ui_Form
import csv
import pandas as pd
from time import sleep

class Report(qtw.QWidget, Ui_Form):
        
    '''
       
    ''' 
    
    file_header = ["Data", "Início", "Fim", "Tempo total (h)", "Temp. sala (ºC)", 
                   "Humidade (%)", "Usuário", "Status do usuário",
                   "Orientador", "Operador", "Natureza da amostra", 
                   "Número de amostras", "Descrição da amostra",
                   "Modos de aquisição", "Sistema de Imageamento",
                   "Início 785", "Final 785", "Tempo 785 (h)","Potência 785 (mW)",
                   "Início 633", "Final 633", "Tempo 633 (h)","Potência 633 (mW)",
                   "Início 532", "Final 532", "Tempo 532 (h)","Potência 532 (mW)", 
                   "Filtros", "Objetivas", "Calibração", "Forno Linkam",
                   "Temperatura inicial", "Temperatura final", "Observações",
                   "Problema no instrumento"]
    
    estat_method = ["Orientador", "Usuário", "Natureza da amostra", "Laser"]

    year_list = ["2024", "2025", "2026", "2027", "2028", "2029", "2030",
                "2031", "2032", "2033", "2034", "2035", "2036", "2037",
                "2038", "2039", "2040", "2041", "2042", "2043", "2044",
                "2045", "2046", "2047", "2048", "2049", "2050"]

    technicians_list = ["Milene Heloisa Martins", "Marcelo Meira Faleiros",
                        "Técnico Horiba"]

    months_list = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep",
                   "Oct", "Nov", "Dec"]
    
    coverage = ["Mensal", "Anual", "Global"]
    
    data = []
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("Relatório de Utilização")
        self.setupUi(self)      

        self.save_pushButton.clicked.connect(self.save)
        self.report_pushButton.clicked.connect(self.report)
        self.cadastro_pushButton.clicked.connect(lambda: self.cadastro('add'))
        self.exclui_pushButton.clicked.connect(lambda: self.cadastro('exclui'))
        self.load_pushButton.clicked.connect(self.load_lists)

        advisors_file = pd.read_csv('advisors_list.csv')
        self.advisors_list = list(advisors_file['Orientador'])
        self.advisor_comboBox.addItems(self.advisors_list)

        self.estat_method_comboBox.addItems(self.estat_method)
        self.abrangencia_comboBox.addItems(self.coverage)
        self.year_comboBox.addItems(self.year_list)
        self.month_comboBox.addItems(self.months_list)

        self.load_lists()

    def load_lists(self):
        #importar lists
        self.user_comboBox.clear()
        self.technician_comboBox.clear()
        
        users_file = pd.read_csv('t64000_users_list.csv')
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
           advisor = "N/C"
        elif self.treinamento_checkBox.isChecked():
           user_status = self.treinamento_checkBox.text()
           advisor = "N/C"
        else:
           user_status = "N/C" 

        ini_time = self.start_timeEdit.text()
        fin_time = self.stop_timeEdit.text()         
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

        acq_modes = []
        if self.microscope_checkBox.isChecked():
           acq_modes.append(self.microscope_checkBox.text())
        if self.macro_checkBox.isChecked():
           acq_modes.append(self.macro_checkBox.text())
        if self.single_checkBox.isChecked():
           acq_modes.append(self.single_checkBox.text())
        if self.triple_checkBox.isChecked():
           acq_modes.append(self.triple_checkBox.text())

        image_system = [] 
        if self.imagemxy_checkBox.isChecked():
           image_system.append(self.imagemxy_checkBox.text()) 
        if self.imagem_autofocus_checkBox.isChecked():
           image_system.append(self.imagem_autofocus_checkBox.text())
        if self.imagemxyz_checkBox.isChecked():
           image_system.append(self.imagemxyz_checkBox.text())        
        if self.swift_checkBox.isChecked():
           image_system.append(self.swift_checkBox.text())
        
        l785_start_time = self.l785_start_timeEdit.text()
        l785_stop_time = self.l785_stop_timeEdit.text()

        ini_l785_time = self.l785_start_timeEdit.text()
        fin_l785_time = self.l785_stop_timeEdit.text()

        hora_l785_ini = int(ini_l785_time[:2])
        hora_l785_fin = int(fin_l785_time[:2])
        min_l785_ini = int(ini_l785_time[3:])/60
        min_l785_fin = int(fin_l785_time[3:])/60
        horas_l785 = round((hora_l785_fin + min_l785_fin) - (hora_l785_ini + min_l785_ini), 1)
                       
        total_l785_time = str(horas_l785)

        l785_power = self.l785_power_lineEdit.text()

        l633_start_time = self.l633_start_timeEdit.text()
        l633_stop_time = self.l633_stop_timeEdit.text()

        ini_l633_time = self.l633_start_timeEdit.text()
        fin_l633_time = self.l633_stop_timeEdit.text()

        hora_l633_ini = int(ini_l633_time[:2])
        hora_l633_fin = int(fin_l633_time[:2])
        min_l633_ini = int(ini_l633_time[3:])/60
        min_l633_fin = int(fin_l633_time[3:])/60
        horas_l633 = round((hora_l633_fin + min_l633_fin) - (hora_l633_ini + min_l633_ini), 1)
                       
        total_l633_time = str(horas_l633)

        l633_power = self.l633_power_lineEdit.text()

        l532_start_time = self.l532_start_timeEdit.text()
        l532_stop_time = self.l532_stop_timeEdit.text()

        ini_l532_time = self.l532_start_timeEdit.text()
        fin_l532_time = self.l532_stop_timeEdit.text()

        hora_l532_ini = int(ini_l532_time[:2])
        hora_l532_fin = int(fin_l532_time[:2])
        min_l532_ini = int(ini_l532_time[3:])/60
        min_l532_fin = int(fin_l532_time[3:])/60
        horas_l532 = round((hora_l532_fin + min_l532_fin) - (hora_l532_ini + min_l532_ini), 1)
                       
        total_l532_time = str(horas_l532)

        l532_power = self.l532_power_lineEdit.text()

        filters = []
        if self.filtro01_checkBox.isChecked():
           filters.append(self.filtro01_checkBox.text())
        if self.filtro1_checkBox.isChecked():
           filters.append(self.filtro1_checkBox.text())
        if self.filtro5_checkBox.isChecked():
           filters.append(self.filtro5_checkBox.text())
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
        if self.objetiva50xlwd_checkBox.isChecked():
           objetivas.append(self.objetiva50xfluor_checkBox.text())
        if self.objetiva50xfluor_checkBox.isChecked():
           objetivas.append(self.objetiva50xlwd_checkBox.text())
        if self.objetiva100x_checkBox.isChecked():
           objetivas.append(self.objetiva100x_checkBox.text())
        if self.objetiva100xlwd_checkBox.isChecked():
           objetivas.append(self.objetiva100xlwd_checkBox.text())

        cal = []
        if self.align_checkBox.isChecked():
           cal.append(self.align_checkBox.text())
        if self.cal_checkBox.isChecked():
           cal.append(self.cal_checkBox.text())
        if self.cal_si_checkBox.isChecked():
           cal.append(self.cal_si_checkBox.text())
        if self.cal_outro_checkBox.isChecked():
           cal.append(self.cal_outro_textEdit.toPlainText())

        #linkam.append(self.linkam_startT_lineEdit.text() + ' - ' + self.linkam_stopT_lineEdit.text())
        linkam = self.gases_lineEdit.text()

        Tstart = self.linkam_startT_lineEdit.text()
        Tstop = self.linkam_stopT_lineEdit.text()

        observations = self.observations_textEdit.toPlainText()   

        if self.inst_probl_checkBox.isChecked():
           problems = self.inst_probl_textEdit.toPlainText()  
        else:
           problems = "N/C"                      

        self.data = [date, ini_time, fin_time, total_time, temp, humid, user, 
                     user_status, advisor, technician, smpl_nature, smpl_number,
                     smpl_description, acq_modes, image_system, l785_start_time,
                     l785_stop_time, total_l785_time, l785_power, l633_start_time,
                     l633_stop_time, total_l633_time, l633_power, l532_start_time,
                     l532_stop_time, total_l532_time, l532_power, filters, 
                     objetivas, cal, linkam, Tstart, Tstop, observations, problems]
              
    def save(self):
        self.write_data()
        month_file_label = 'T64000 - ' + self.months_list[self.month - 1] + self.year + '_data_log.csv'
        year_file_label = 'T64000 - ' + '20' + self.year + '_data_log.csv'
        global_file_label = 'T64000 - ' + 'data_log.csv'

        if os.path.exists(month_file_label):
            with open(month_file_label, 'a', newline='', encoding='utf8') as mf:
                write = csv.writer(mf)                
                write.writerow(self.data)       
        else:
            with open(month_file_label, 'a', newline='', encoding='utf8') as mf:
                write = csv.writer(mf)
                write.writerow(self.file_header)
                write.writerow("")
                write.writerow(self.data)

        if os.path.exists(year_file_label):
            with open(year_file_label, 'a', newline='', encoding='utf8') as yf:
                write = csv.writer(yf)                
                write.writerow(self.data)       
        else:
            with open(year_file_label, 'a', newline='', encoding='utf8') as yf:
                write = csv.writer(yf)
                write.writerow(self.file_header)
                write.writerow("")
                write.writerow(self.data)

        if os.path.exists(global_file_label):
            with open(global_file_label, 'a', newline='', encoding='utf8') as gf:
                write = csv.writer(gf)                
                write.writerow(self.data)       
        else:
            with open(global_file_label, 'a', newline='', encoding='utf8') as gf:
                write = csv.writer(gf)
                write.writerow(self.file_header)
                write.writerow("")
                write.writerow(self.data)

        for i in range(10000):
           self.salvar_label.setText('OK - Arquivo salvo!')
        self.salvar_label.setText('')
           

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
          file = 'T64000 - data_log.csv'
       elif coverage == 'Anual':
          file = 'T64000 - ' + year + '_data_log.csv'
       elif coverage == 'Mensal':
          file = 'T64000 - ' + month + year[2:] + '_data_log.csv'

       #read csv file
       data = pd.read_csv(file)

       if search_method == 'Laser':
          total_time_785 = data['Tempo 785 (h)'].sum()
          total_time_633 = data['Tempo 633 (h)'].sum()
          total_time_532 = data['Tempo 532 (h)'].sum()

          search_object = data['Orientador']    
          search_object = list(set(search_object))
          search_object = sorted(search_object)

          object_str_785 = ''
          object_str_633 = ''
          object_str_532 = ''

          for n in search_object:
             if n in self.advisors_list:
                array_orientador = data[data.Orientador == n]
                parcial_time_785 = round(array_orientador['Tempo 785 (h)'].sum(), 1)
                parcial_time_633 = round(array_orientador['Tempo 633 (h)'].sum(), 1)
                parcial_time_532 = round(array_orientador['Tempo 532 (h)'].sum(), 1)
                object_str_785 += n + ' ' + str(parcial_time_785) + '\n' 
                object_str_633 += n + ' ' + str(parcial_time_633) + '\n'
                object_str_532 += n + ' ' + str(parcial_time_532) + '\n'
                         
          self.report_label.setText('Tempo 785 nm total: ' + str(round(total_time_785, 1)) + 'h\n\n' +
                                    object_str_785 + '\n' +
                                    'Tempo 633 nm total: ' + str(round(total_time_633, 1)) + 'h\n\n' +
                                    object_str_633 + '\n' +
                                    'Tempo 532 nm total: ' + str(round(total_time_532, 1)) + 'h\n\n' +
                                    object_str_532)
      
       elif search_method == 'Orientador':
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
                
          self.report_label.setText('Tempo total: ' + str(round(total_time, 1)) + 'h\n\n' +
                                    object_arr)
          
    def cadastro(self, action=str):  
       user = self.user_lineEdit.text()
       if action == 'add':         
          user = [user] 
          with open('t64000_users_list.csv', 'a', newline='', encoding='utf8') as uf:
              write = csv.writer(uf)                
              write.writerow(user) 
       elif action == 'exclui':
          users = pd.read_csv('t64000_users_list.csv')
          users = users.drop(users[users.Usuarios == user].index)
          users.to_csv('t64000_users_list.csv', index=False)                                                       

if __name__ == '__main__':
    app = qtw.QApplication([])
    tela = Report()
    tela.show()
    app.exec_()