from tuya import Tuya
import time


devicePIR = 'eb4b796e16a9d377cfvnqb'
deviceSwicth = 'eb9fd4d13d3fd60f6fbgpa'
tuya = Tuya()
tuya.get_token()

# commands = {"commands":[{"code": "switch_1", "value":False}]}
# tuya.sent_commands(deviceSwicth, commands)
while True:
  try:
    pir_data = tuya.get_device_info(devicePIR)
    if(pir_data['success']):
      if(pir_data['result']['status'][0]['value'] == 'pir'):
        print(pir_data['result']['status'][0])
        print('pir loop')
        commands = {"commands":[{"code": "switch_1", "value":True}]}
        tuya.sent_commands(deviceSwicth, commands)
      else:
        print(pir_data['result']['status'][0])
        print('none loop')
        commands = {"commands":[{"code": "switch_1" ,"value":False}]}
        tuya.sent_commands(deviceSwicth, commands)
  except:
    print('Error!')

  time.sleep(5)
