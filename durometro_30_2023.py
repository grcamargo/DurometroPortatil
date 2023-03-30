#!/usr/bin/python
import csv
import time
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
from picamera import PiCamera
from time import sleep
from hx711 import HX711  # import the class HX711
camera = PiCamera()
from datetime import date
import Adafruit_DHT

data_atual = date.today()
print(data_atual)
#GPIO.setmode(GPIO.BOARD)    
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  
#Define os pinos dos leds como saida
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)  
GPIO.setup(24, GPIO.IN) 
GPIO.output(17,0)
GPIO.output(27,0)
GPIO.output(22,0)

contador = 0

sensor = Adafruit_DHT.DHT22
pin = 25
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
 
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
                     
lcd_rs        = 26  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 11
lcd_backlight = 4

lcd_columns = 16
lcd_rows    = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows, lcd_backlight)
lcd.clear()
lcd.set_cursor(1,0)# Print a two line message
lcd.message('Durometro 4MA')
lcd.set_cursor(1,1)
message = 'PORTATIL!!!'   
lcd.message(message)
for i in range(lcd_columns-len(message)):
        time.sleep(0.1)
        lcd.move_right()
for i in range(lcd_columns-len(message)):
        time.sleep(0.2)
        lcd.move_left()
        time.sleep(1.0)

# Demo showing the cursor.
lcd.clear()
lcd.show_cursor(True)
lcd.message('PREPARANDO....')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,GPIO.HIGH)
time.sleep(1)
GPIO.output(17,GPIO.LOW)
time.sleep(1.0)

#-------Medição----------
try:
   
    hx = HX711(dout_pin=23, pd_sck_pin=18)
    # measure tare and save the value as offset for current channel
    # and gain selected. That means channel A and gain 128
    err = hx.zero()
    # check if successful
    if err:
        raise ValueError('Tare is unsuccessful.')

    reading = hx.get_raw_data_mean()
    if reading:  # always check if you get correct value or only False
        # now the value is close to 0
        print('Dados subtraídos por deslocamento, mas ainda não convertidos em unidades:  ',
              reading)
    else:
        print('invalid data', reading)

    # In order to calculate the conversion ratio to some units, in my case I want grams,
    # you must have known weight.
    #input('Coloque o peso conhecido na Durometro e, em seguida, pressione Enter:  ')
    reading = hx.get_data_mean()
    if reading:
        print('Valor médio de HX711 subtraído por deslocamento:', reading)
        known_weight_grams = 150  #input('Escreva quantos gramas foram e pressione Enter: ')
        time.sleep(1.0)
        try:
            value = float(known_weight_grams)
            print(value, 'grams')
        except ValueError:
            print('Inteiro esperado ou flutuador e eu tenho:',value) #known_weight_grams)

        # set scale ratio for particular channel and gain which is
        # used to calculate the conversion to units. Required argument is only
        # scale ratio. Without arguments 'channel' and 'gain_A' it sets
        # the ratio for current channel and gain.
        ratio = reading / value  # calculate the ratio for channel A and gain 128
        hx.set_scale_ratio(ratio)  # set ratio for current channel
        print('Ratio is set.')
    else:
        raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', reading)

    # Read data several times and return mean value
    # subtracted by offset and converted by scale ratio to
    # desired units. In my case in grams.
    print("Agora, vou ler os dados em loop infinito. Para sair, pressione 'CTRL + C'")
    #input('Pressione Enter para começar a ler')
    print('O peso atual na balança em Kilograma é:: ')
    time.sleep(1.0)       
except (KeyboardInterrupt, SystemExit):    #(KeyboardInterrupt, SystemExit):

    print('Bye :)')




while (1):
    
    print('iniciou')
    # Demo showing the blinking cursor.
    lcd.clear()
    lcd.blink(True)
    lcd.message('Instrumento')
    time.sleep(2.0)

    # Stop blinking and showing cursor.
    lcd.show_cursor(False)
    lcd.blink(False)


    # Demo scrolling message right/left.
    lcd.clear()
    message = 'PRONTO!!!'
    GPIO.output(17,GPIO.HIGH)

    lcd.message(message)
    for i in range(lcd_columns-len(message)):
        time.sleep(0.1)
        lcd.move_right()
    for i in range(lcd_columns-len(message)):
        time.sleep(0.1)
        lcd.move_left()
 
    while(1):
     
        #Verifica se o botao foi pressionado
        if GPIO.input(24) == True:
            #Incrementa a variavel contador
            contador = contador +1
            time.sleep(0.5)
            #Caso contador = 1, acende o led vermelho
            print(contador)
        if contador == 1:
            contador =  contador + 1
            GPIO.output(27, 1)
            lcd.clear()
            #lcd.blink(True)
            lcd.message('MEDINDO....')
            
            #-------Medição----------
            try:
                
                while True:
                    #carrega as variaveis para registro no arquivo
                    timestr = time.strftime("%d/%m/%Y")
                    data= timestr 
                    print(data)
                    
                    timestr = time.strftime("%H:%M:%S")
                    hora= timestr  
                    print (hora)
                    
                    carga=10
                    print(carga)
                    
                    valor= float(hx.get_weight_mean(15))
                    valor= "{:.1f}".format(valor)
                    print  (valor, 'K')
                    lcd.set_cursor(0,1)
                    lcd.message('VALOR :')
                    lcd.set_cursor(8,1)
                    lcd.message(valor)
                    lcd.message(' Kg')
                    
                    #temperatura=(temperature)
                    temperatura=float('{:.1f}'.format(temperature))
                    print(temperatura)
                    #umidade= (humidity)
                    umidade=float('{:.1f}'.format(humidity))
                    print(umidade)
                    
                    if GPIO.input(24) == True:
                        #Incrementa a variavel contador
                        contador = contador +1
                        time.sleep(0.5)
                   
                        with open('durometro.csv', mode='r') as csv_file:
                            csv_reader = csv.DictReader(csv_file)
                            line_count = 0
                            for row in csv_reader:
                                if line_count == 0:
                                    print(f'Column names are {", ".join(row)}')
                                    line_count += 1
                                    print(row)
                                    line_count += 1
                                    print(f'Processed {line_count} lines.')
                                    time.sleep(1.5)
                    #def writeCSV(data, hora, carga, valor, temperatura, umidade):
                        with open('durometro.csv', mode='a') as csv_file:
                            fieldnames = ['data','hora','pre-carga','valor','temperatura','umidade']
                            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                            writer.writerow({'data': data, 'hora': hora, 'pre-carga': carga, 'valor': valor, 'temperatura': temperatura, 'umidade': umidade})
 
                    if contador == 3:
                        GPIO.output(22, 1)
                        GPIO.output(27, 1)
                        lcd.clear()
                        lcd.message('PREPARE FOTO')  
                        contador = contador +1
                        break
                    
            except (KeyboardInterrupt, SystemExit):    #(KeyboardInterrupt, SystemExit):
   
                 print('Bye :)')
    
        
        if contador == 5 :
            GPIO.output(22, 1)
            GPIO.output(27, 1)
            lcd.clear()
            lcd.message('TIRAR FOTO ....')
            contador = contador +1
                    
        
        if contador == 6:
            GPIO.output(22, 1)
            GPIO.output(27, 0)
            lcd.clear()
            lcd.message('IMAGEM....')
            camera.start_preview()
            sleep(2)
            timestr = time.strftime("%d%m%Y%H%M%S") 
            camera.capture('/home/durometro/Desktop/fotos/imagem%s.jpg'% timestr)
            camera.stop_preview()
            contador = contador +1
                        
        if contador == 7:
            GPIO.output( 27, 0)
            GPIO.output( 22, 0)
            lcd.clear()
                        #lcd.blink(True)
            lcd.message('FINALIZADO!!!')
            for num in range(10):
                        # Se o número for igual a = 5, devemos parar o loop
                if num == 9:
                    GPIO.output(17,GPIO.LOW)
                break
                
        if contador == 8:
            contador = 0
            lcd.clear()
                        #lcd.blink(True)
            lcd.message('eoeoeo!!!')




