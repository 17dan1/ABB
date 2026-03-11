from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification

# Datablock con indirizzi simulati
max_address = 0x6300
holding_registers = [0] * (max_address)

store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, holding_registers),
)
context = ModbusServerContext(slaves=store, single=True)

# ==============================
# Assegnazione valori iniziali
# Attenzione utilizzo solo il registro LSB a 16 bit,
# quindii valori simulati non possono eccedere 65535
# ==============================

def set_register(addr, size, value):
    store.setValues(3, addr + (size-1), [value])  # 3 = Holding Register

# Registri energia
set_register(0x5000, 4, 1000) 	        #- Energia attiva totale 10,0 kWh
set_register(0x500C, 4, 900)	        #- Energia reattiva totale 9,0 kvarh
set_register(0x5018, 4, 1100)	    	#- Energia apparente totale 11,0 kVAh
set_register(0x5460, 4, 850)		    #- Energia attiva L1 8,5 kWh
set_register(0x5464, 4, 850)		    #- Energia attiva L2 8,5 kWh
set_register(0x5468, 4, 850)		    #- Energia attiva L3 8,5 kWh
set_register(0x5484, 4, 150)		    #- Energia reattiva L1 1,5 kWh
set_register(0x5488, 4, 150)		    #- Energia reattiva L2 1,5 kWh
set_register(0x548C, 4, 150)		    #- Energia reattiva L3 1,5 kWh
set_register(0x54A8, 4, 1500)		    #- Energia apparente L1 15,0 kWh
set_register(0x54AC, 4, 1500)		    #- Energia apparente L2 15,0 kWh
set_register(0x54B0, 4, 1500)		    #- Energia apparente L3 15,0 kWh

# Registri tensione
set_register(0x5B00, 2, 2300)	    	#- Tensione di sistema 230,0V
set_register(0x5B02, 2, 2310)	    	#- Tensione L1-N 231,0 V
set_register(0x5B04, 2, 2320)	    	#- Tensione L2-N 232,0 V
set_register(0x5B06, 2, 2330)	    	#- Tensione L3-N 233,0 V
set_register(0x5B08, 2, 4010)	    	#- Tensione L1-L2 401,0 V
set_register(0x5B0A, 2, 4020)	    	#- Tensione L3-L2 402,0 V
set_register(0x5B0C, 2, 4030)	    	#- Tensione L1-L3 403,0 V

# Registri corrente
set_register(0x5B0E, 2, 10000)	    	#- Corrente di sistema 100,0 A
set_register(0x5B10, 2, 10100)	    	#- Corrente L1  101,0 A
set_register(0x5B12, 2, 10200)	    	#- Corrente L2  102,0 A
set_register(0x5B14, 2, 10300)	    	#- Corrente L3  103,0 A
set_register(0x5B16, 2, 200)	    	#- Corrente N   2,0 A

# Registri potenza
set_register(0x5B1A, 2, 13000)	        #- Potenza attiva totale 13000,0 W
set_register(0x5B1C, 2, 11000)	        #- Potenza attiva L1 1100,0 W
set_register(0x5B1E, 2, 12000)	        #- Potenza attiva L2 1200,0 W
set_register(0x5B20, 2, 13000)	        #- Potenza attiva L3 1300,0 W
set_register(0x5B22, 2, 15000)	        #- Potenza reattiva totale 1500,0 VAr
set_register(0x5B24, 2, 51000)	        #- Potenza reattiva L1 510,0 VAr
set_register(0x5B26, 2, 52000)	        #- Potenza reattiva L2 520,0 VAr
set_register(0x5B28, 2, 53000)	        #- Potenza reattiva L3 530,0 VAr
set_register(0x5B2A, 2, 20000)	        #- Potenza apparente totale 20000,0 VA
set_register(0x5B2C, 2, 21000)	        #- Potenza apparente L1 2100,0 VA
set_register(0x5B2E, 2, 22000)	        #- Potenza apparente L2 2200,0 VA
set_register(0x5B30, 2, 23000)	        #- Potenza apparente L3 2300,0 VA

# Registro frequenza
set_register(0x5B32, 1, 5000)	        #- Frequenza 50,00 Hz

# Registri fattori potenza
set_register(0x5B33, 1, 100)	    	#- Angolo potenza totale 10,0°
set_register(0x5B34, 1, 110)	    	#- Angolo potenza L1 11,0°
set_register(0x5B35, 1, 120)	    	#- Angolo potenza L2 12,0°
set_register(0x5B36, 1, 130)	    	#- Angolo potenza L3 13,0°
set_register(0x5B37, 1, 100)	    	#- Angolo V1 10,0°
set_register(0x5B38, 1, 1300)	    	#- Angolo V2 130,0°
set_register(0x5B39, 1, 2500)		    #- Angolo V3 250,0°
set_register(0x5B3D, 1, 50)		        #- Angolo I1 5,0°
set_register(0x5B3E, 1, 1250)		    #- Angolo I2 125,0°
set_register(0x5B3F, 1, 2450)		    #- Angolo I3 245,0°
set_register(0x5B40, 1, 900)		    #- Fattore potenza totale 0,9
set_register(0x5B41, 1, 900)		    #- Fattore potenza L1 0,9
set_register(0x5B42, 1, 900)		    #- Fattore potenza L2 0,9
set_register(0x5B43, 1, 900)		    #- Fattore potenza L3 0,9
set_register(0x5B44, 1, 1)		        #- Quadrante totale 1
set_register(0x5B45, 1, 2)		        #- Quadrante L1 2
set_register(0x5B46, 1, 3)		        #- Quadrante L2 3
set_register(0x5B47, 1, 4)		        #- Quadrante L3 4
set_register(0x5B48, 1, 900)		    #- Cosphi totale 0,9 °
set_register(0x5B49, 1, 900)		    #- Cosphi L1 0,9 °
set_register(0x5B4A, 1, 900)		    #- Cosphi L2 0,9 °
set_register(0x5B4B, 1, 900)		    #- Cosphi L3 0,9 °

# Registri Voltage THD
set_register(0x5D00, 1, 100)	    	# Voltage THD L1
set_register(0x5D01, 1, 100)	    	# Voltage THD L1 2°
set_register(0x5D02, 1, 100)	    	# Voltage THD L1 3°
set_register(0x5D03, 1, 100)	    	# Voltage THD L1 4°
set_register(0x5D04, 1, 100)	    	# Voltage THD L1 5°
set_register(0x5D05, 1, 100)	    	# Voltage THD L1 6°
set_register(0x5D06, 1, 100)	    	# Voltage THD L1 7°
set_register(0x5D80, 1, 100)	    	# Voltage THD L2
set_register(0x5D81, 1, 100)	    	# Voltage THD L2 2°
set_register(0x5D82, 1, 100)	    	# Voltage THD L2 3°
set_register(0x5D83, 1, 100)	    	# Voltage THD L2 4°
set_register(0x5D84, 1, 100)	    	# Voltage THD L2 5°
set_register(0x5D85, 1, 100)	    	# Voltage THD L2 6°
set_register(0x5D86, 1, 100)	    	# Voltage THD L2 7°
set_register(0x5E00, 1, 100)	    	# Voltage THD L3
set_register(0x5E01, 1, 100)	    	# Voltage THD L3 2°
set_register(0x5E02, 1, 100)	    	# Voltage THD L3 3°
set_register(0x5E03, 1, 100)	    	# Voltage THD L3 4°
set_register(0x5E04, 1, 100)	    	# Voltage THD L3 5°
set_register(0x5E05, 1, 100)	    	# Voltage THD L3 6°
set_register(0x5E06, 1, 100)	    	# Voltage THD L3 7°
set_register(0x5E80, 1, 100)	    	# Voltage THD L1-L2
set_register(0x5E81, 1, 100)	    	# Voltage THD L1-L2 2°
set_register(0x5E82, 1, 100)	    	# Voltage THD L1-L2 3°
set_register(0x5E83, 1, 100)	    	# Voltage THD L1-L2 4°
set_register(0x5E84, 1, 100)	    	# Voltage THD L1-L2 5°
set_register(0x5E85, 1, 100)	    	# Voltage THD L1-L2 6°
set_register(0x5E86, 1, 100)	    	# Voltage THD L1-L2 7°
set_register(0x5F00, 1, 100)	    	# Voltage THD L3-L2
set_register(0x5F01, 1, 100)	    	# Voltage THD L3-L2 2°
set_register(0x5F02, 1, 100)	    	# Voltage THD L3-L2 3°
set_register(0x5F03, 1, 100)	    	# Voltage THD L3-L2 4°
set_register(0x5F04, 1, 100)	    	# Voltage THD L3-L2 5°
set_register(0x5F05, 1, 100)	    	# Voltage THD L3-L2 6°
set_register(0x5F06, 1, 100)	    	# Voltage THD L3-L2 7°
set_register(0x5F80, 1, 100)	    	# Voltage THD L1-L3
set_register(0x5F81, 1, 100)	    	# Voltage THD L1-L3 2°
set_register(0x5F82, 1, 100)	    	# Voltage THD L1-L3 3°
set_register(0x5F83, 1, 100)	    	# Voltage THD L1-L3 4°
set_register(0x5F84, 1, 100)	    	# Voltage THD L1-L3 5°
set_register(0x5F85, 1, 100)	    	# Voltage THD L1-L3 6°
set_register(0x5F86, 1, 100)	    	# Voltage THD L1-L3 7°

# Registri Current THD
set_register(0x6000, 1, 100)	    	# Current THD L1
set_register(0x6001, 1, 100)	    	# Current THD L1 2°
set_register(0x6002, 1, 100)	    	# Current THD L1 3°
set_register(0x6003, 1, 100)	    	# Current THD L1 4°
set_register(0x6004, 1, 100)	    	# Current THD L1 5°
set_register(0x6005, 1, 100)	    	# Current THD L1 6°
set_register(0x6006, 1, 100)	    	# Current THD L1 7°
set_register(0x6080, 1, 100)	    	# Current THD L2
set_register(0x6081, 1, 100)	    	# Current THD L2 2°
set_register(0x6082, 1, 100)	    	# Current THD L2 3°
set_register(0x6083, 1, 100)	    	# Current THD L2 4°
set_register(0x6084, 1, 100)	    	# Current THD L2 5°
set_register(0x6085, 1, 100)	    	# Current THD L2 6°
set_register(0x6086, 1, 100)	    	# Current THD L2 7°
set_register(0x6100, 1, 100)	    	# Current THD L3
set_register(0x6101, 1, 100)	    	# Current THD L3 2°
set_register(0x6102, 1, 100)	    	# Current THD L3 3°
set_register(0x6103, 1, 100)	    	# Current THD L3 4°
set_register(0x6104, 1, 100)	    	# Current THD L3 5°
set_register(0x6105, 1, 100)	    	# Current THD L3 6°
set_register(0x6106, 1, 100)	    	# Current THD L3 7°
set_register(0x6180, 1, 100)	    	# Current THD N
set_register(0x6181, 1, 100)	    	# Current THD N 2°
set_register(0x6182, 1, 100)	    	# Current THD N 3°
set_register(0x6183, 1, 100)	    	# Current THD N 4°
set_register(0x6184, 1, 100)	    	# Current THD N 5°
set_register(0x6185, 1, 100)	    	# Current THD N 6°
set_register(0x6186, 1, 100)	    	# Current THD N 7°

# Registri Sbilanci
set_register(0x6200, 2, 100)	    	# Sbilancio tensioni concatenate
set_register(0x6202, 2, 100)	    	# Sbilancio tensioni stellate
set_register(0x6204, 2, 100)	    	# sbilancio correnti


print("Registri inizializzati.")

try:
    print("Avvio Modbus TCP Slave su porta 502...")
    StartTcpServer(
        context=context,
        address=("0.0.0.0", 502)
    )

except KeyboardInterrupt:
    print("\nArresto server Modbus...")
