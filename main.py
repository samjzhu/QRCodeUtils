import socket
import pyqrcode
import pyclip
import cv2
import PySimpleGUI as sg


def QRGen(data, fname):
    qrObj = pyqrcode.create(data, error='Q')
    if fname:
        qrObj.png(fname)
    return qrObj


def getMyLocalIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def wifiQR(T, ssid, p):
    data = f'WIFI:T:{T};S:{ssid};P:{p};;'
    QRGen(data, 'wifi.png')


def wifiQR2(T, S, P):
    data = f'WIFI:T:{T};S:{S};P:{P};;'
    return pyqrcode.create(data, error='H')


def pasteToQR():
    data = pyclip.paste()
    return pyqrcode.create(data, error='Q')


def test():

    qr = wifiQR2('WPA2', 'TP-Link_DC79', '123498765')
    print(qr.terminal())
    qr.svg("wifi.svg", scale=5)
    qr.png("wifi.png")

    qr = wifiQR2('WPA2', 'TP-Link_DC79_5G', '123498765')
    print(qr.terminal())
    qr.svg("wifi5g.svg", scale=5)
    qr.png("wifi5g.png")

    img = cv2.imread("wifi5g.png")
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(img)
    # if there is a QR code
    # print the data
    if vertices_array is not None:
        print("QRCode data:")
        print(data)
    else:
        print("There was some error")


def utility_simpleGUI():
    sg.theme('DarkAmber')  # Keep things interesting for your users

    tab_layout_wifi = [
        [sg.T('Generate QR code for WIFI access')],
        [sg.Text('Authentication Type'),
         sg.Combo(['WPA2', 'WEP', 'WPA'], key='T', default_value='WPA2')],
        [sg.Text('SSID'),
         sg.InputText('YourSSID', key='ssid')],
        [sg.Text('Passcode'),
         sg.InputText('YourPassCode', key='P')],
        [sg.Button('Generate WIFI QRCode')]]

    tab_layout_input = [[sg.T('Generate QR code for given input')],
                        [sg.InputText(key='myText')],
                        [sg.Button('Generate QRCode')]]

    tab_layout_clipboard = [[sg.T('Generate QR code for content currently in clipboard')],
                            [sg.Button('QRCode of Clipboard')]]

    tab_layout_local_url = [
        [sg.T('Generate QR code for WIFI access')],
        [sg.Text('Protocol'), sg.InputText(key='myProtocol')],
        [sg.Text('LAN IP'), sg.InputText(getMyLocalIP(), key='myLocalIP')],
        [sg.Text('port'), sg.InputText(key='myPort')],
        [sg.Text('appPath'), sg.InputText(key='myPath')],
        [sg.Button('Local URL')]]

    layout = [
        [sg.TabGroup([[sg.Tab('Text to QR', tab_layout_input),
                       sg.Tab('Clipboard to QR', tab_layout_clipboard),
                       sg.Tab('QR for Wifi', tab_layout_wifi),
                       sg.Tab('QR local URL', tab_layout_local_url)]
                      ]
                     )
         ],
        [sg.Exit()]
    ]

    window = sg.Window('WiFi QRCode Generator', layout)

    while True:  # The Event Loop
        event, values = window.read()
        print(event, values)
        if event == 'Generate QRCode':
            my_text = values['myText']
            qr = pyqrcode.create(my_text, error='H')
            print(qr.data)
            qr.show()
        if event == 'Generate WIFI QRCode':
            T = values['T']
            ssid = values['ssid']
            p = values['P']
            qr = wifiQR2(T, ssid, p)
            qr.show()
        if event == 'QRCode of Clipboard':
            qr = pasteToQR()
            print(qr.data)
            qr.show()
        if event == 'Local URL':
            t = f"{values['myProtocol']}://{values['myLocalIP']}:{values['myPort']}/{values['myPath']}"
            qr = pyqrcode.create(t, error='H')
            print(qr.data)
            qr.show()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break


# test()
utility_simpleGUI()
