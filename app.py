from flask import Flask, render_template, request
import qrcode
import json
import base64
import io

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_qr():
    student_data = {
        "student_id": request.form["student_id"],
        "name": request.form["name"],
        "gender": request.form["gender"],
        "dob": request.form["dob"],
        "mobile": request.form["mobile"],
        "email": request.form["email"],
        "branch": request.form["branch"],
        "course": request.form["course"]
    }

    json_data = json.dumps(student_data)
    encoded_data = base64.urlsafe_b64encode(json_data.encode()).decode()

    qr_url = request.host_url + "view?data=" + encoded_data
    qr = qrcode.make(qr_url)

    img_buffer = io.BytesIO()
    qr.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    qr_base64 = base64.b64encode(img_buffer.getvalue()).decode()

    return render_template("qr.html", qr_code=qr_base64)


@app.route("/view")
def view_data():
    encoded_data = request.args.get("data")

    decoded_json = base64.urlsafe_b64decode(encoded_data).decode()
    student_data = json.loads(decoded_json)

    return render_template("view.html", student=student_data)


if __name__ == "__main__":
    app.run(debug=True)