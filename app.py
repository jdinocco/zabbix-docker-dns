import subprocess
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

def run_dig(server, url):
    try:
        # Ejecuta el comando dig, asegurándose de que la salida se maneje como texto
        command = f'dig @{server} {url} +noall +answer +stats | jc --dig'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # Si hay un error en la ejecución del comando, captura la salida de error
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, command, output=result.stdout)
        
        # Convierte la salida, que es texto, directamente a un objeto JSON
        data = json.loads(result.stdout)
        return data 
    except subprocess.CalledProcessError as e:
        return {'error': 'Command failed', 'details': e.output}
    except json.JSONDecodeError:
        return {'error': 'Failed to parse command output as JSON'}
    
def get_dns_servers():
    dns_servers = []
    try:
        with open('/tmp/resolv.conf', 'r') as file:
            for line in file:
                if line.startswith('nameserver'):
                    ip = line.split()[1]
                    if ip != '127.0.0.1':
                        dns_servers.append(ip)
                    else:
                        dns_servers.append('8.8.8.8')
            if not dns_servers:
                dns_servers.append('8.8.8.8')
    except FileNotFoundError:
        dns_servers.append('8.8.8.8')
    return dns_servers

@app.route('/dns_test')
def dns_test():
    server = request.args.get('server', '8.8.8.8')  # Default to 8.8.8.8 if no server is provided
    url = request.args.get('url', 'example.com')  # Default to example.com if no URL is provided
    results = run_dig(server, url)
    return jsonify(results)

@app.route('/dns_servers')
def dns_servers():
    servers = get_dns_servers()
    # Using list comprehension to create the list of dictionaries
    final_list = [{"{#DNS_SERVER}": dns_serv} for dns_serv in servers]
    # Directly creating the JSON structure expected by Zabbix and converting it to a JSON string
    return json.dumps({"data": final_list})
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

