from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification

# Simulated register values: [123, 456] at address 0 and 1
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100),
    co=ModbusSequentialDataBlock(0, [0]*100),
    hr=ModbusSequentialDataBlock(0, [123, 456]),
    ir=ModbusSequentialDataBlock(0, [0]*100)
)
context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = "LocalTest"
identity.ProductCode = "LT"
identity.ProductName = "Local Test Modbus Server"
identity.ModelName = "ModelX"
identity.MajorMinorRevision = "1.0"

print("Starting Modbus slave server on localhost:5020...")
StartTcpServer(context, identity=identity, address=("localhost", 5020))
