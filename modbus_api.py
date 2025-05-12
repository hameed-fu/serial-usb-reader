from flask import Flask, request, jsonify
from pymodbus.client.sync import ModbusTcpClient

app = Flask(__name__)

MODBUS_HOST = "localhost"
MODBUS_PORT = 5020

@app.route('/read-register', methods=['GET'])
def read_register():
    address = int(request.args.get('address', 0))
    count = int(request.args.get('count', 1))

    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
    if not client.connect():
        return jsonify({"error": "Connection failed"}), 500

    result = client.read_holding_registers(address, count, unit=1)
    client.close()

    if result.isError():
        return jsonify({"error": "Read failed"}), 500

    return jsonify({"data": result.registers})

if __name__ == '__main__':
    print("Flask Modbus API running at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)
