import flask
import subprocess
from flask import abort, jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

processes = list()

@app.route('/')
def main():
    res = list()
    for i in range(len(processes)):
        res.append({
            "cmd": processes[i].args,
            "state": processes[i].poll()
        })
    return jsonify(res)

@app.route('/<int:ind>')
def describe(ind):
    if ind > len(processes)-1:
        abort(404)

    res = {
            "cmd": processes[ind].args,
            "state": processes[ind].poll(),
            "out": processes[ind].stdout.read().decode('utf-8')
    }
    
    return jsonify(res)

@app.route('/run', methods=["POST"])
def run():
    cmd = str(request.data.decode('utf-8'))
    p = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
    processes.append(p)
    return jsonify({ "index": len(processes)-1})

@app.route('/kill/<int:ind>')
def kill(ind):
    if ind > len(processes)-1:
        abort(404)
    
    processes[ind].terminate()

    res = {
            "cmd": processes[ind].args,
            "state": processes[ind].poll()
    }
    return jsonify(res)


app.run()