import asyncio
import time
import random
from pymodbus.server.async_io import StartAsyncTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# Datablock con indirizzi simulati
max_address = 0x6300
holding_registers = [0] * (max_address)

store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, holding_registers),
)
context = ModbusServerContext(slaves=store, single=True)

async def increment_active_energy():
    while True:
        # Incremento energia attiva totale e per fase
        active_energy_total = store.getValues(3, 0x5000 + 3, count=1)[0]
        active_energy_l1 = store.getValues(3, 0x5460 + 3, count=1)[0]
        active_energy_l2 = store.getValues(3, 0x5464 + 3, count=1)[0]
        active_energy_l3 = store.getValues(3, 0x5468 + 3, count=1)[0]

        set_register(0x5000, 4, active_energy_total + random.randrange(0, 4)*100) 	        #- Energia attiva totale
        set_register(0x5460, 4, active_energy_l1 + random.randrange(0, 4)*100)		    #- Energia attiva L1
        set_register(0x5464, 4, active_energy_l2 + random.randrange(0, 4)*100)		    #- Energia attiva L2
        set_register(0x5468, 4, active_energy_l3 + random.randrange(0, 4)*100)		    #- Energia attiva L3

        print("Energia attiva incrementata")

        # Attesa 15 minuti (900 secondi)
        await asyncio.sleep(1800)

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
set_register(0x5460, 4, 1000)		    #- Energia attiva L1 8,5 kWh
set_register(0x5464, 4, 900)		    #- Energia attiva L2 8,5 kWh
set_register(0x5468, 4, 900)		    #- Energia attiva L3 8,5 kWh
set_register(0x5484, 4, 200)		    #- Energia reattiva L1 1,5 kWh
set_register(0x5488, 4, 150)		    #- Energia reattiva L2 1,5 kWh
set_register(0x548C, 4, 300)		    #- Energia reattiva L3 1,5 kWh
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
set_register(0x5B0E, 2, 1000)	    	#- Corrente di sistema 10,00 A
set_register(0x5B10, 2, 744)	    	#- Corrente L1  7,44 A
set_register(0x5B12, 2, 903)	    	#- Corrente L2  9,03 A
set_register(0x5B14, 2, 1355)	    	#- Corrente L3  13,55 A
set_register(0x5B16, 2, 822)	    	#- Corrente N   8,22 A

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
set_register(0x5B33, 1, 288)	    	#- Angolo potenza totale -28,8°
set_register(0x5B34, 1, 32)	    	    #- Angolo potenza L1 -3,2
set_register(0x5B35, 1, 285)	    	#- Angolo potenza L2 -28,5°
set_register(0x5B36, 1, 427)	    	#- Angolo potenza L3 -42,7°
set_register(0x5B37, 1, 0)	    	    #- Angolo V1 0,0°
set_register(0x5B38, 1, 1195)	    	#- Angolo V2 119,5°
set_register(0x5B39, 1, 2400)		    #- Angolo V3 -120,0°
set_register(0x5B3D, 1, 3580)		        #- Angolo I1 -3,2°
set_register(0x5B3E, 1, 909)		    #- Angolo I2 90,9°
set_register(0x5B3F, 1, 1978)		    #- Angolo I3 -162,7°
set_register(0x5B40, 1, 852)		    #- Fattore potenza totale 0,852
set_register(0x5B41, 1, 989)		    #- Fattore potenza L1 0,989
set_register(0x5B42, 1, 848)		    #- Fattore potenza L2 0,848
set_register(0x5B43, 1, 724)		    #- Fattore potenza L3 0,724
set_register(0x5B44, 1, 1)		        #- Quadrante totale 1
set_register(0x5B45, 1, 1)		        #- Quadrante L1 1
set_register(0x5B46, 1, 1)		        #- Quadrante L2 1
set_register(0x5B47, 1, 1)		        #- Quadrante L3 1
set_register(0x5B48, 1, 876)		    #- Cosphi totale 0,876 °
set_register(0x5B49, 1, 998)		    #- Cosphi L1 0,998 °
set_register(0x5B4A, 1, 878)		    #- Cosphi L2 0,878 °
set_register(0x5B4B, 1, 735)		    #- Cosphi L3 0,735 °

# Registri Voltage THD
set_register(0x5D00, 1, 137)	    	# Voltage THD L1
set_register(0x5D01, 1, 200)	    	# Voltage THD L1 2°
set_register(0x5D02, 1, 300)	    	# Voltage THD L1 3°
set_register(0x5D03, 1, 400)	    	# Voltage THD L1 4°
set_register(0x5D04, 1, 500)	    	# Voltage THD L1 5°
set_register(0x5D05, 1, 600)	    	# Voltage THD L1 6°
set_register(0x5D06, 1, 700)	    	# Voltage THD L1 7°
set_register(0x5D07, 1, 600)	    	# Voltage THD L1 8°
set_register(0x5D08, 1, 700)	    	# Voltage THD L1 9°
set_register(0x5D80, 1, 262)	    	# Voltage THD L2
set_register(0x5D81, 1, 900)	    	# Voltage THD L2 2°
set_register(0x5D82, 1, 300)	    	# Voltage THD L2 3°
set_register(0x5D83, 1, 400)	    	# Voltage THD L2 4°
set_register(0x5D84, 1, 300)	    	# Voltage THD L2 5°
set_register(0x5D85, 1, 600)	    	# Voltage THD L2 6°
set_register(0x5D86, 1, 100)	    	# Voltage THD L2 7°
set_register(0x5D87, 1, 600)	    	# Voltage THD L2 8°
set_register(0x5D88, 1, 100)	    	# Voltage THD L2 9°
set_register(0x5E00, 1, 160)	    	# Voltage THD L3
set_register(0x5E01, 1, 500)	    	# Voltage THD L3 2°
set_register(0x5E02, 1, 900)	    	# Voltage THD L3 3°
set_register(0x5E03, 1, 200)	    	# Voltage THD L3 4°
set_register(0x5E04, 1, 100)	    	# Voltage THD L3 5°
set_register(0x5E05, 1, 100)	    	# Voltage THD L3 6°
set_register(0x5E06, 1, 400)	    	# Voltage THD L3 7°
set_register(0x5E07, 1, 100)	    	# Voltage THD L3 8°
set_register(0x5E08, 1, 400)	    	# Voltage THD L3 9°
set_register(0x5E80, 1, 500)	    	# Voltage THD L1-L2
set_register(0x5E81, 1, 600)	    	# Voltage THD L1-L2 2°
set_register(0x5E82, 1, 400)	    	# Voltage THD L1-L2 3°
set_register(0x5E83, 1, 900)	    	# Voltage THD L1-L2 4°
set_register(0x5E84, 1, 300)	    	# Voltage THD L1-L2 5°
set_register(0x5E85, 1, 500)	    	# Voltage THD L1-L2 6°
set_register(0x5E86, 1, 300)	    	# Voltage THD L1-L2 7°
set_register(0x5E87, 1, 500)	    	# Voltage THD L1-L2 8°
set_register(0x5E88, 1, 300)	    	# Voltage THD L1-L2 9°
set_register(0x5F00, 1, 400)	    	# Voltage THD L3-L2
set_register(0x5F01, 1, 200)	    	# Voltage THD L3-L2 2°
set_register(0x5F02, 1, 300)	    	# Voltage THD L3-L2 3°
set_register(0x5F03, 1, 200)	    	# Voltage THD L3-L2 4°
set_register(0x5F04, 1, 500)	    	# Voltage THD L3-L2 5°
set_register(0x5F05, 1, 300)	    	# Voltage THD L3-L2 6°
set_register(0x5F06, 1, 500)	    	# Voltage THD L3-L2 7°
set_register(0x5F07, 1, 300)	    	# Voltage THD L3-L2 8°
set_register(0x5F08, 1, 500)	    	# Voltage THD L3-L2 9°
set_register(0x5F80, 1, 300)	    	# Voltage THD L1-L3
set_register(0x5F81, 1, 700)	    	# Voltage THD L1-L3 2°
set_register(0x5F82, 1, 300)	    	# Voltage THD L1-L3 3°
set_register(0x5F83, 1, 400)	    	# Voltage THD L1-L3 4°
set_register(0x5F84, 1, 700)	    	# Voltage THD L1-L3 5°
set_register(0x5F85, 1, 400)	    	# Voltage THD L1-L3 6°
set_register(0x5F86, 1, 100)	    	# Voltage THD L1-L3 7°
set_register(0x5F87, 1, 400)	    	# Voltage THD L1-L3 8°
set_register(0x5F88, 1, 100)	    	# Voltage THD L1-L3 9°

# Registri Current THD
set_register(0x6000, 1, 1)	    	# Current THD L1
set_register(0x6001, 1, 1)	    	# Current THD L1 2°
set_register(0x6002, 1, 106)	    # Current THD L1 3°
set_register(0x6003, 1, 1)	    	# Current THD L1 4°
set_register(0x6004, 1, 26)	    	# Current THD L1 5°
set_register(0x6005, 1, 0)	    	# Current THD L1 6°
set_register(0x6006, 1, 37)	    	# Current THD L1 7°
set_register(0x6007, 1, 0)	    	# Current THD L1 8°
set_register(0x6008, 1, 37)	    	# Current THD L1 9°
set_register(0x6080, 1, 262)	    # Current THD L2
set_register(0x6081, 1, 1)	    	# Current THD L2 2°
set_register(0x6082, 1, 200)	    # Current THD L2 3°
set_register(0x6083, 1, 0)	    	# Current THD L2 4°
set_register(0x6084, 1, 68)	    	# Current THD L2 5°
set_register(0x6085, 1, 1)	    	# Current THD L2 6°
set_register(0x6086, 1, 154)	    # Current THD L2 7°
set_register(0x6087, 1, 1)	    	# Current THD L2 8°
set_register(0x6088, 1, 154)	    # Current THD L2 9°
set_register(0x6100, 1, 160)	    # Current THD L3
set_register(0x6101, 1, 0)	    	# Current THD L3 2°
set_register(0x6102, 1, 188)	    # Current THD L3 3°
set_register(0x6103, 1, 1)	    	# Current THD L3 4°
set_register(0x6104, 1, 140)	    # Current THD L3 5°
set_register(0x6105, 1, 1)	    	# Current THD L3 6°
set_register(0x6106, 1, 100)	    # Current THD L3 7°
set_register(0x6107, 1, 1)	    	# Current THD L3 8°
set_register(0x6108, 1, 100)	    # Current THD L3 9°
set_register(0x6180, 1, 617)	    # Current THD N
set_register(0x6181, 1, 0)	    	# Current THD N 2°
set_register(0x6182, 1, 588)	    # Current THD N 3°
set_register(0x6183, 1, 0)	    	# Current THD N 4°
set_register(0x6184, 1, 105)	    # Current THD N 5°
set_register(0x6185, 1, 1)	    	# Current THD N 6°
set_register(0x6186, 1, 128)	    # Current THD N 7°
set_register(0x6187, 1, 1)	    	# Current THD N 8°
set_register(0x6188, 1, 128)	    # Current THD N 9°

# Registri Sbilanci
set_register(0x6200, 2, 100)	    	# Sbilancio tensioni concatenate
set_register(0x6202, 2, 100)	    	# Sbilancio tensioni stellate
set_register(0x6204, 2, 100)	    	# sbilancio correnti

async def main():
    print("Registri inizializzati.")
    print("Avvio Modbus TCP Slave...")

    # Task parallelo
    asyncio.create_task(increment_active_energy())

    # Server async (CORRETTO)
    await StartAsyncTcpServer(
        context=context,
        address=("0.0.0.0", 502)
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nArresto server Modbus...")
