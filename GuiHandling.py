from chromeHandling import ChromeHandling
from stageDataHandling import StateDataHandling
import PySimpleGUI as sg
import threading
import psutil
import time
import os

class GuiHandling:

    def __init__(self):

        self.stageDataObj = StateDataHandling()
        self.stageList = self.stageDataObj.get_stage_list()
        self.rowList = self.stageDataObj.get_row(self.stageList[0])
        self.rowKeyList = self.stageDataObj.get_row_key()

        self.font = 'Helvetica'
        self.textSize = 15
        self.textColor = 'black'
        self.elementSize = (12, 1)
        self.buttonSize = (12, 2)
        self.radioElementSize = (5, 5)
        self.generalBackgroundColor = 'silver'
        self.inputBackgroundColor = 'white'
        self.defaultLink = 'https://ticketbox.vn/event/idecaf-ngay-xua-ngay-xua-34-87169?opm=tbox.edp.buybox.23'
        self.defaultLastName = 'Vũ'
        self.defaultFirstName = 'Quốc Sơn'
        self.defaultEmail = 'vuquocson1995@gmail.com'
        self.defaultPhone = '0979093748'
        self.defaultOutput = "- Your information wil be used to fulfil the requirement from ticketbox website.\n" \
                             "- Please type the very correct infor one by one.\n" \
                             "- Please select the according stage with the event.\n" \
                             "- Please select the prefer vip row and normal row.\n" \
                             "- Please be aware of that the tool isn't able to ensure 100% to buy ticket successfully.\n" \
                             "- Good luck."

        # url2 = "https://ticketbox.vn/event/kich-idecaf-thanh-xa-bach-xa-86983?opm=tbox.searchlistcategory.list.1"
        # url3 = "https://ticketbox.vn/event/idecaf-ngay-xua-ngay-xua-34-87169?opm=tbox.edp.buybox.23"

    def __get_selected_row(self, window, values: dict, rows: list):
        for row in rows:
            if values[row]:
                return window[row].Text
        return ""

    def __get_infor_column(self):
        link = [sg.Text("Link", font=(self.font, self.textSize), text_color=self.textColor, size=self.elementSize,
                        background_color=self.generalBackgroundColor),
                sg.InputText(self.defaultLink, font=(self.font, self.textSize),
                             background_color=self.inputBackgroundColor, key='-LINK-')]

        lastName = [
            sg.Text("Last Name", font=(self.font, self.textSize), text_color=self.textColor, size=self.elementSize,
                    background_color=self.generalBackgroundColor),
            sg.InputText(self.defaultLastName, font=(self.font, self.textSize),
                         background_color=self.inputBackgroundColor, key='-LAST-NAME-')]

        firstName = [
            sg.Text("First Name", font=(self.font, self.textSize), text_color=self.textColor, size=self.elementSize,
                    background_color=self.generalBackgroundColor),
            sg.InputText(self.defaultFirstName, font=(self.font, self.textSize),
                         background_color=self.inputBackgroundColor, key='-FIRST-NAME-')]

        email = [sg.Text("Email", font=(self.font, self.textSize), text_color=self.textColor, size=self.elementSize,
                         background_color=self.generalBackgroundColor),
                 sg.InputText(self.defaultEmail, font=(self.font, self.textSize),
                              background_color=self.inputBackgroundColor,
                              key='-EMAIL-')]

        phone = [
            sg.Text("Phone Number", font=(self.font, self.textSize), text_color=self.textColor, size=self.elementSize,
                    background_color=self.generalBackgroundColor),
            sg.InputText(self.defaultPhone, font=(self.font, self.textSize), background_color=self.inputBackgroundColor,
                         key='-PHONE-')]

        stage = [sg.Text("Stage", font=(self.font, self.textSize), text_color=self.textColor, size=self.elementSize,
                         background_color=self.generalBackgroundColor),
                 sg.Combo(values=self.stageList, size=(33, 4), font=(self.font, self.textSize),
                          background_color=self.inputBackgroundColor,
                          text_color=self.textColor, default_value=self.stageList[0],
                          enable_events=True, readonly=True, key='-STAGE-')]

        vipRow = [sg.Text("Vip Row", font=(self.font, self.textSize), text_color=self.textColor, size=self.elementSize,
                          background_color=self.generalBackgroundColor)]
        vipRow.extend(
            [sg.Radio(self.rowList['Vip'][i], 'vipRow', text_color=self.textColor, font=(self.font, self.textSize),
                      size=self.radioElementSize, background_color=self.generalBackgroundColor,
                      default=True, key=self.rowKeyList['Vip'][i]) for i in range(len(self.rowKeyList['Vip']))])

        normalRow = [
            sg.Text("Normal Row", size=self.elementSize, font=(self.font, self.textSize), text_color=self.textColor,
                    background_color=self.generalBackgroundColor)]
        normalRow.extend([sg.Radio(self.rowList['Normal'][i], 'normalRow', text_color=self.textColor,
                                   font=(self.font, self.textSize),
                                   size=self.radioElementSize, background_color=self.generalBackgroundColor,
                                   default=True, key=self.rowKeyList['Normal'][i]) for i in
                          range(len(self.rowKeyList['Normal']))])

        inforColumn = sg.Column([link, lastName, firstName, email, phone, stage, vipRow, normalRow],
                                background_color=self.generalBackgroundColor)
        return inforColumn

    def __get_showOutput_column(self):
        showOutput = [sg.Multiline(default_text=self.defaultOutput, font=(self.font, 14), text_color=self.textColor,
                                   size=(50, 12), background_color='white', autoscroll=True, expand_x=True,
                                   expand_y=True, enable_events=True,
                                   reroute_stderr=True, reroute_stdout=True, key='-OUTPUT-')]

        showOutputColumn = sg.Column([showOutput], background_color=self.generalBackgroundColor)

        return showOutputColumn

    def __get_title_column(self):
        title = [sg.Text("Please Enter Information", font=(self.font, 17), text_color=self.textColor,
                         background_color='lightgray')]
        titleColumn = sg.Column([title], background_color=self.generalBackgroundColor, justification='center')

        return titleColumn

    def __get_submit_column(self):
        submitButton = [sg.Button(button_text='Buy Tickets', size=self.buttonSize, font=(self.font, self.textSize), key='-SUBMIT-BUTTON-')]
        submitColumn = sg.Column([submitButton], background_color=self.generalBackgroundColor, justification='center')

        return submitColumn

    def __get_cancel_column(self):
        cancelButton = [sg.Button(button_text='Cancel', size=self.buttonSize, font=(self.font, self.textSize), key='-CANCEL-BUTTON-')]
        cancelColumn = sg.Column([cancelButton], background_color=self.generalBackgroundColor, justification='center')

        return cancelColumn

    def __get_stop_button(self):
        stopButton = [sg.Button(button_text='Stop', size=self.buttonSize, font=(self.font, self.textSize), disabled=True, key='-STOP-BUTTON-')]
        return stopButton

    def __get_stop_column(self):
        stopButton = self.__get_stop_button()
        stopColumn = sg.Column([stopButton], background_color=self.generalBackgroundColor, justification='center')

        return stopColumn

    def __buy_ticket(self, link: str, lastName: str, firstName: str, email: str, phone: str, stage: str, vipRow: str,
                     normalRow: str, stopButton):
        chromeHandlingObj = ChromeHandling()
        chromeHandlingObj.start(link, lastName, firstName, email, phone, stage, vipRow, normalRow, stopButton)

    def __GUI_ticket_box(self):

        titleColumn = self.__get_title_column()

        inforColumn = self.__get_infor_column()

        showOutputColumn = self.__get_showOutput_column()

        spaceLine = [sg.Text('', size=self.elementSize, font=(self.font, self.textSize), text_color=self.textColor,
                             background_color=self.generalBackgroundColor)]

        submitColumn = self.__get_submit_column()

        cancelColumn = self.__get_cancel_column()

        stopColumn = self.__get_stop_column()
        stopButton = self.__get_stop_button()

        layout = [
            [titleColumn],
            [inforColumn, showOutputColumn],
            spaceLine,
            [submitColumn, cancelColumn, stopColumn]
        ]

        window = sg.Window(title="Buy tickets from ticketbox.vn", layout=layout, grab_anywhere=True, resizable=True, finalize=True,
                           background_color=self.generalBackgroundColor)

        t_buy_ticket = None

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == '-CANCEL-BUTTON-':
                break
            elif event == '-STAGE-':
                rowList = self.stageDataObj.get_row(values['-STAGE-'])
                for i in range(len(self.rowKeyList['Vip'])):
                    window[self.rowKeyList['Vip'][i]].update(text=rowList['Vip'][i])
                    window[self.rowKeyList['Normal'][i]].update(text=rowList['Normal'][i])
            elif event == '-SUBMIT-BUTTON-':
                m_link = values['-LINK-']
                m_lastName = values['-LAST-NAME-']
                m_firstName = values['-FIRST-NAME-']
                m_email = values['-EMAIL-']
                m_phone = values['-PHONE-']
                m_stage = values['-STAGE-']
                m_vipRow = self.__get_selected_row(window, values, self.rowKeyList['Vip'])
                m_normalRow = self.__get_selected_row(window, values, self.rowKeyList['Normal'])

                t_buy_ticket = threading.Thread(target=self.__buy_ticket, args=(
                    m_link, m_lastName, m_firstName, m_email, m_phone, m_stage, m_vipRow, m_normalRow, window))
                t_buy_ticket.start()

                window['-SUBMIT-BUTTON-'].update(disabled=True)
                window['-CANCEL-BUTTON-'].update(disabled=True)
                window['-STOP-BUTTON-'].update(disabled=False)
                window['-OUTPUT-'].update("")
            elif event == '-STOP-BUTTON-':
                time.sleep(0.5)
                if t_buy_ticket and not t_buy_ticket.is_alive():
                    window['-SUBMIT-BUTTON-'].update(disabled=False)
                    window['-CANCEL-BUTTON-'].update(disabled=False)
                    window['-STOP-BUTTON-'].update(disabled=True)
                elif t_buy_ticket and t_buy_ticket.is_alive():
                    for proc in psutil.process_iter():
                        if 'chrome.exe' in proc.name():
                            print("Chrome process has been found out, start killing it.")
                            os.system("taskkill /f /im chrome.exe")

        if t_buy_ticket and t_buy_ticket.is_alive():
            t_buy_ticket.join()

        window.close()

    def start(self):
        self.__GUI_ticket_box()
