from flask import Flask, jsonify

app = Flask(__name__)

# In-memory health states used to simulate failures.
liveness_ok = True
readiness_ok = True


@app.route("/")
def home():
    return jsonify({
        "application": "Kubernetes Health Check Demo",
        "status": "Running"
    })


@app.route("/live")
def liveness():
    if not liveness_ok:
        return jsonify({"status": "Dead"}), 500
    return jsonify({"status": "Alive"}), 200


@app.route("/ready")
def readiness():
    if not readiness_ok:
        return jsonify({"status": "Not Ready"}), 500
    return jsonify({"status": "Ready"}), 200


@app.route("/fail-liveness")
def fail_liveness():
    global liveness_ok
    liveness_ok = False
    return jsonify({"message": "Liveness failure enabled"})


@app.route("/fail-readiness")
def fail_readiness():
    global readiness_ok
    readiness_ok = False
    return jsonify({"message": "Readiness failure enabled"})


@app.route("/recover")
def recover():
    global liveness_ok, readiness_ok
    liveness_ok = True
    readiness_ok = True
    return jsonify({"message": "Application recovered"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
