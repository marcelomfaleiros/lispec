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
                   "Porta-amostras", "Análises res. no tempo",
                   "Início Xe", "Final Xe", "Tempo Xe (h)","Potência Xe", 
                   "Laser 1", "Início Laser 1", "Final Laser 1", 
                   "Tempo Laser 1 (h)","Potência Laser 1",
                   "Laser 2", "Início Laser 2", "Final Laser 2", 
                   "Tempo Laser 2 (h)","Potência Laser 2",
                   "Laser 3", "Início Laser 3", "Final Laser 3", 
                   "Tempo Laser 3 (h)","Potência Laser 3",
                   "Filtros", "Detectores", "Calibração", 
                   "Esfera de integração", "Acessórios", "Criostato", 
                   "Peltier", "Nanoled", "Linkam aquecimento",
                   "Linkam N2", "Observações", "Problema no instrumento"]
    
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

        uic.loadUi('utilization_log_fluorolog3_intrfc_v11.ui', self)

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

        users_file = pd.read_csv('fluorolog3_users_list.csv')
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
           smpl_nature.append(self.liquido_checkBox.text())

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
        if self.xefosfor_checkBox.isChecked():
           time_resolved_analy.append(self.xefosfor_checkBox.text())
        if self.nanoled_checkBox.isChecked():
           time_resolved_analy.append("Nanoled: " + self.nanoled_lineEdit.text())        
        if self.spectraled_checkBox.isChecked():
           time_resolved_analy.append("Spectraled: " + self.spectraled_lineEdit.text())
        if self.laser_checkBox.isChecked():
           time_resolved_analy.append("Laser: " + self.laser_lineEdit.text())
        if self.otheranaly_checkBox.isChecked():
           time_resolved_analy.append(self.otheranaly_lineEdit.text())
        
        if self.xecont_checkBox.isChecked():
           xe_power = self.xe_power_lineEdit.text() 

           ini_xe_time = self.fonte_start_timeEdit.text()
           fin_xe_time = self.fonte_stop_timeEdit.text()

           hora_xe_ini = int(ini_xe_time[:2])
           hora_xe_fin = int(fin_xe_time[:2])
           min_xe_ini = int(ini_xe_time[3:])/60
           min_xe_fin = int(fin_xe_time[3:])/60
           horas_xe = round((hora_xe_fin + min_xe_fin) - 
                            (hora_xe_ini + min_xe_ini), 1)
                       
           total_xe_time = str(horas_xe)
        else:
           ini_xe_time = ""
           fin_xe_time = ""
           total_xe_time = ""
           xe_power = ""

        if self.exc_laser1_checkBox.isChecked():
           laser1 = self.exc_laser1_lineEdit.text() 
        
           laser1_power = self.laser1_power_lineEdit.text()
           
           ini_laser1_time = self.exc_laser1_ini_timeEdit.text()
           fin_laser1_time = self.exc_laser1_fin_timeEdit.text()

           hora_laser1_ini = int(ini_laser1_time[:2])
           hora_laser1_fin = int(fin_laser1_time[:2])
           min_laser1_ini = int(ini_laser1_time[3:])/60
           min_laser1_fin = int(fin_laser1_time[3:])/60
           horas_laser1 = round((hora_laser1_fin + min_laser1_fin) - 
                                (hora_laser1_ini + min_laser1_ini), 1)
                       
           total_laser1_time = str(horas_laser1)
        else:
           laser1 = ""
           ini_laser1_time = ""
           fin_laser1_time = ""
           total_laser1_time = ""
           laser1_power = ""

        if self.exc_laser2_checkBox.isChecked():
           laser2 = self.exc_laser2_lineEdit.text() 
        
           laser2_power = self.laser2_power_lineEdit.text()
           
           ini_laser2_time = self.exc_laser2_ini_timeEdit.text()
           fin_laser2_time = self.exc_laser2_fin_timeEdit.text()

           hora_laser2_ini = int(ini_laser2_time[:2])
           hora_laser2_fin = int(fin_laser2_time[:2])
           min_laser2_ini = int(ini_laser2_time[3:])/60
           min_laser2_fin = int(fin_laser2_time[3:])/60
           horas_laser2 = round((hora_laser2_fin + min_laser2_fin) - 
                                (hora_laser2_ini + min_laser2_ini), 1)
                       
           total_laser2_time = str(horas_laser2)
        else:
           laser2 = ""
           ini_laser2_time = ""
           fin_laser2_time = ""
           total_laser2_time = ""
           laser2_power = ""
         
        if self.exc_laser3_checkBox.isChecked():
           laser3 = self.exc_laser3_lineEdit.text() 
        
           laser3_power = self.laser3_power_lineEdit.text()
           
           ini_laser3_time = self.exc_laser3_ini_timeEdit.text()
           fin_laser3_time = self.exc_laser3_fin_timeEdit.text()

           hora_laser3_ini = int(ini_laser3_time[:2])
           hora_laser3_fin = int(fin_laser3_time[:2])
           min_laser3_ini = int(ini_laser3_time[3:])/60
           min_laser3_fin = int(fin_laser3_time[3:])/60
           horas_laser3 = round((hora_laser3_fin + min_laser3_fin) - 
                                (hora_laser3_ini + min_laser3_ini), 1)
                       
           total_laser3_time = str(horas_laser3)
        else:
           laser3 = ""
           ini_laser3_time = ""
           fin_laser3_time = ""
           total_laser3_time = ""
           laser3_power = ""

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
           cal.append("mono emis: " + self.emis_lineEdit.text())
        if self.ccd_grade_checkBox.isChecked():
           cal.append("CCD: " + self.ccd_grade_lineEdit.text())

        int_sphere = []
        if self.esf_integ_liquid_checkBox.isChecked():
           int_sphere.append(self.esf_integ_liquid_checkBox.text())
        if self.esf_int_solid_checkBox.isChecked():
           int_sphere.append(self.esf_int_solid_lineEdit.text() + " " + self.esf_int_solid_lineEdit.text())

        accessories = []        
        if self.dewar_checkBox.isChecked():
           accessories.append(self.dewar_checkBox.text())
        if self.fibra_checkBox.isChecked():
           accessories.append(self.fibra_checkBox.text())
        if self.polarizer_checkBox.isChecked():
           accessories.append(self.polarizer_checkBox.text())
        if self.mfc_checkBox.isChecked():
           accessories.append(self.mfc_checkBox.text())
        if self.banho_term_checkBox.isChecked():
           accessories.append(self.banho_term_checkBox.text())

        cryostat = []
        if self.n2_checkBox.isChecked():
           cryostat.append(self.n2_checkBox.text())
           cryostat.append(self.temp_criost_lineEdit.text())
        if self.he_checkBox.isChecked():
           cryostat.append(self.he_checkBox.text())
           cryostat.append(self.temp_criost_lineEdit.text())
        
        peltier = self.peltier_temp_lineEdit.text()

        if self.nanoled_sc_checkBox.isChecked():
           nanoled = self.nanoled_sc_checkBox.text()
        elif self.nanoled_cc_checkBox.isChecked():
           nanoled = self.nanoled_cc_checkBox.text()
        else:
           nanoled = ""

        linkam_heat = []
        if self.linkam_aquec_checkBox.isChecked():
           linkam_heat.append(self.linkam_temp_lineEdit.text())
        if self.linkam_banho_checkBox.isChecked():
           linkam_heat.append(self.linkam_banho_checkBox.text())

        linkam_n2 = []
        if self.linkam_n2_checkBox.isChecked():
           linkam_n2.append(self.linkam_n2_temp_lineEdit.text())
        if self.linkam_n2_banho_checkBox.isChecked():
           linkam_n2.append(self.linkam_n2_banho_checkBox.text())

        observations = self.observations_textEdit.toPlainText()   

        if self.inst_probl_checkBox.isChecked():
           problems = self.inst_probl_textEdit.toPlainText()  
        else:
           problems = "N/C"                      

        self.data = [date, ini_time, fin_time, total_time, temp, 
                     humid, user, user_status, 
                     advisor, technician, smpl_nature, 
                     smpl_number, smpl_description, 
                     smpl_holders, time_resolved_analy, 
                     ini_xe_time, fin_xe_time, total_xe_time, xe_power,
                     laser1, ini_laser1_time, fin_laser1_time, 
                     total_laser1_time, laser1_power,
                     laser2, ini_laser2_time, fin_laser2_time, 
                     total_laser2_time, laser2_power, 
                     laser3, ini_laser3_time, fin_laser3_time, 
                     total_laser3_time, laser3_power, 
                     filters, detectors, cal, 
                     int_sphere, accessories, cryostat, 
                     peltier, nanoled, linkam_heat, 
                     linkam_n2, observations, problems]
                     
    def save(self):
        self.write_data()
        month_file_label = 'Fluorolog3 - ' + self.months_list[self.month - 1] + self.year + '_data_log.csv'
        year_file_label = 'Fluorolog3 - ' + '20' + self.year + '_data_log.csv'
        global_file_label = 'Fluorolog3 - ' + 'data_log.csv'

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
          file = 'Fluorolog3 - data_log.csv'
       elif coverage == 'Year':
          file = 'Fluorolog3 - ' + year + '_data_log.csv'
       elif coverage == 'Month':
          file = 'Fluorolog3 - ' + month + year[2:] + '_data_log.csv'

       #read csv file
       data = pd.read_csv(file)

       if search_method == 'Fonte de excitação':
          total_time = data['Tempo Exc (h)'].sum()

          search_object = data['Advisor']    
          search_object = list(set(search_object))
          search_object = sorted(search_object)

          object_arr = ''

          for n in search_object:
             if n in self.advisors_list:
                array_orientador = data[data.Orientador == n]
                parcial_time = round(array_orientador['Tempo Exc (h)'].sum(), 1)
                object_arr += n + ' ' + str(parcial_time) + '\n\n'  
                         
          self.report_label.setText('Tempo Exc (h): ' + str(round(total_time, 1)) + 'h\n\n' +
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
    app = QtWidgets.QApplication([])
    tela = Report()
    tela.show()
    app.exec_()