from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "app": "SiteWatch",
        "status": "running",
        "message": "Website monitoring backend is working!"
    })


@app.route("/api/check")
def check_website():
    url = request.args.get("url", "").strip()

    if not url.startswith(("https://", "http://")):
        return jsonify({
            "error": "Enter a valid URL starting with http:// or https://"
        }), 400

    start_time = time.perf_counter()

    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=False,
            stream=True
        )

        elapsed = round(
            (time.perf_counter() - start_time) * 1000, 2
        )

        result = {
            "website": url,
            "status": (
                "online"
                if 200 <= response.status_code < 400
                else "error"
            ),
            "http_status": response.status_code,
            "response_time_ms": elapsed
        }

        response.close()
        return jsonify(result)

    except requests.RequestException:
        return jsonify({
            "website": url,
            "status": "unreachable"
        }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)