# -*- coding: utf-8 -*-
# revisão 19/04/2024

import os
from PyQt5 import QtWidgets as qtw
from utilization_log_fluorolog3_intrfc import Ui_Form
import csv
import pandas as pd
from time import sleep

class Report(qtw.QWidget, Ui_Form):
        
    '''
       
    ''' 
    
    file_header = ["Data", "Início", "Fim", "Tempo total (h)", "Temp. sala", 
                   "Humidade", "Usuário", "Status do usuário",
                   "Orientador", "Operador", "Natureza da amostra", 
                   "Número de amostras", "Descrição da amostra",
                   "Porta-amostras", "Análises res. no tempo",
                   "Fontes de excitação"
                   "Início Exc.", "Final Exc.", "Tempo Exc (h)","Potência Exc.", 
                   "Filtros", "Detectores", "Calibração", "Acessórios",
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

        self.users_file = pd.read_csv('fluorolog3_users_list.csv')
        self.users_list = list(self.users_file['Usuarios'])

        self.user_comboBox.addItems(sorted(self.users_list))
        self.technician_comboBox.addItems(sorted(self.users_list)) 
        
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
        if self.piece_checkBox.isChecked():
           smpl_nature.append(self.piece_checkBox.text())
        if self.liquido_checkBox.isChecked():
           smpl_nature.append(self.cachimbo_checkBox.text())

        smpl_number = self.numero_amostras_lineEdit.text()

        smpl_description = self.description_plainTextEdit.toPlainText()

        smpl_holders = []
        if self.cubeta_checkBox.isChecked():
           smpl_holders.append(self.cubeta_checkBox.text())
        if self.cela_checkBox.isChecked():
           smpl_holders.append(self.cela_checkBox.text())
        if self.tubo_checkBox.isChecked():
           smpl_holders.append(self.tubo_checkBox.text())
        if self.suporte_checkBox.isChecked():
           smpl_holders.append(self.suporte_checkBox.text())
        if self.platina_checkBox.isChecked():
           smpl_holders.append(self.platina_checkBox.text())
        if self.othersmpl_checkBox.isChecked():
           smpl_holders.append(self.other_smpl_lineEdit.text())

        time_resolved_analy = [] 
        if self.xetcspc_checkBox.isChecked():
           time_resolved_analy.append(self.xetcspc_checkBox.text()) 
        if self.xefosfor_checkBox_checkBox.isChecked():
           time_resolved_analy.append(self.xefosfor_checkBox.text())
        if self.nanoled_checkBox.isChecked():
           time_resolved_analy.append(self.nanoled_lineEdit.text())        
        if self.spectraled_checkBox.isChecked():
           time_resolved_analy.append(self.spectraled_lineEdit.text())
        if self.laser_checkBox.isChecked():
           time_resolved_analy.append(self.laser_lineEdit.text())
        if self.otheranaly_checkBox.isChecked():
           time_resolved_analy.append(self.otheranaly_lineEdit.text())

        ini_fonte_time = self.fonte_start_timeEdit.text()
        fin_fonte_time = self.fonte_stop_timeEdit.text()

        hora_fonte_ini = int(ini_fonte_time[:2])
        hora_fonte_fin = int(fin_fonte_time[:2])
        min_fonte_ini = int(ini_fonte_time[3:])/60
        min_fonte_fin = int(fin_fonte_time[3:])/60
        horas_fonte = round((hora_fonte_fin + min_fonte_fin) - (hora_fonte_ini + min_fonte_ini), 1)
                       
        total_fonte_time = str(horas_fonte)

        laser_power = self.laser_power_lineEdit.text()

        filters = self.filtro_lineEdit.text()

        detectors = []
        if self.pmt_uvvis_checkBox.isChecked():
           detectors.append(self.pmt_uvvis_checkBox.text())
        if self.pmt_nir_checkBox.isChecked():
           detectors.append(self.pmt_nir_checkBox.text())
        if self.ccd_checkBox.isChecked():
           detectors.append(self.ccd_checkBox.text())

        cal = []
        if self.exc_checkBox.isChecked():
           cal.append(self.exc_checkBox.text())
        if self.emi_checkBox.isChecked():
           cal.append(self.emis_lineEdit.text())
        if self.ccd_grade_checkBox.isChecked():
           cal.append(self.ccd_grade_lineEdit.text())

        accessories = []

        if self.esf_integ_liquid_checkBox.isChecked():
           linkam.append(self.esf_integ_liquid_checkBox.text())
        if self.esf_int_solid_checkBox.isChecked():
           linkam.append(self.esf_int_solid_lineEdit.text())
        if self.dewar_checkBox.isChecked():
           linkam.append(self.dewar_checkBox.text())
        if self.fibra_checkBox.isChecked():
           linkam.append(self.fibra_checkBox.text())
        if self.polarizer_checkBox.isChecked():
           linkam.append(self.polarizer_checkBox.text())
        if self.mfc_checkBox.isChecked():
           linkam.append(self.mfc_checkBox.text())
        if self.banho_term_checkBox.isChecked():
           linkam.append(self.banho_term_checkBox.text())
        if self.n2_checkBox.isChecked():
           linkam.append(self.n2_checkBox.text())
           linkam.append(self.temp_criost_lineEdit.text())
        if self.he_checkBox.isChecked():
           linkam.append(self.he_checkBox.text())
           linkam.append(self.temp_criost_lineEdit.text())
        linkam.append(self.peltier_temp_lineEdit.text())
        if self.fibra_checkBox.isChecked():
           linkam.append(self.fibra_checkBox.text())
        if self.polarizer_checkBox.isChecked():
           linkam.append(self.polarizer_checkBox.text())
        if self.mfc_checkBox.isChecked():
           linkam.append(self.mfc_checkBox.text())

        Tstart = self.linkam_startT_lineEdit.text()
        Tstop = self.linkam_stopT_lineEdit.text()

        observations = self.observations_textEdit.toPlainText()   

        if self.inst_probl_checkBox.isChecked():
           problems = self.inst_probl_textEdit.toPlainText()  
        else:
           problems = "N/C"                      

        self.data = [date, ini_time, fin_time, total_time, temp, humid, user, 
                     user_status, advisor, technician, smpl_nature, smpl_number,
                     smpl_description, smpl_holders, time_resolved_analy, ini_fonte_time,
                     fin_fonte_time, total_fonte_time, laser_power, filters, 
                     detectors, cal, linkam, Tstart, Tstop, observations, problems]
              
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

        self.salvar_label.setText('OK - Arquivo salvo!')

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
                         
          self.report_label.setText('Tempo laser total: ' + str(round(total_time, 1)) + 'h\n\n' +
                                    object_arr)
      
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
          with open('fluorolog3_users_list.csv', 'a', newline='', encoding='utf8') as uf:
              write = csv.writer(uf)                
              write.writerow(user) 
       elif action == 'exclui':
          users = pd.read_csv('fluorolog3_users_list.csv')
          users = users.drop(users[users.Usuarios == user].index)
          users.to_csv('fluorolog3_users_list.csv', index=False)                                                       

if __name__ == '__main__':
    app = qtw.QApplication([])
    tela = Report()
    tela.show()
    app.exec_()