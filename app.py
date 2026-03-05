from flask import Flask
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "HEAD"])
def hello_world():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="https://sudor2spr.github.io/Documentation/assets/style.css">
    <title>SudoR2spr Repository</title>
    <link rel="icon" type="image/x-icon" href="https://raw.githubusercontent.com/SudoR2spr/SudoR2spr/main/assets/angel-op/Angel-ji.png">
</head>
<body>
    <div class="container" style="bg-dark text-red text-center py-3 mt-5">
        <a href="https://telegram.me/Opleech_WD" class="card">
            <p>
               ░█▀▀▄░▒█▄░▒█░▒█▀▀█░▒█▀▀▀░▒█░░░<br>
               ▒█▄▄█░▒█▒█▒█░▒█░▄▄░▒█▀▀▀░▒█░░░<br>
               ▒█░▒█░▒█░░▀█░▒█▄▄▀░▒█▄▄▄░▒█▄▄█<br>
               <br>
               <b>v3.0.0 - Fixed & Working</b>
            </p>
        </a>
    </div>
    <br/><br/><br/>
    <footer class="bg-dark text-white text-center py-3 mt-5">
        <center>
            <img loading="lazy" src="https://graph.org/file/548b8b73c35af202bfdac.png" width="60" height="60">
            Powered By 𝐖𝐎𝐎𝐃𝐜𝐫𝐚𝐟𝐭
            <img loading="lazy" src="https://graph.org/file/548b8b73c35af202bfdac.png" width="60" height="60">
            <div><p>© 2024 Text Leech Bot. All rights reserved.</p></div>
        </center>
    </footer>
</body>
</html>"""

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
