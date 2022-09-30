from flask import Flask, render_template, redirect,request, send_file
import firebase_admin
from firebase_admin import credentials,auth,firestore, storage
import hashlib

# firebase init
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'storageBucket': 'da-sharing.appspot.com'})
db = firestore.client()
app = Flask(__name__)

email = ""
@app.route('/')
def index():
    return redirect('/signup')

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup-post", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    password = request.form.get("password")
    display_name = request.form.get("username")
    hash_object = hashlib.sha512((email + password).encode())
    uid = hash_object.hexdigest()
    try:
        user = auth.create_user(uid = uid, display_name = display_name, email = email, password = password)
        return redirect("/login")
    except:
        return "User already exists."
    

@app.route("/login-post", methods=["POST"])
def login_post():
    emailid = request.form.get("email")
    password = request.form.get("password")
    try: 
        user = auth.get_user_by_email(emailid)
        hash_object = hashlib.sha512((emailid + password).encode())
        uid = hash_object.hexdigest()
        if uid == user.uid:
            global email
            email = emailid
            return redirect("/upload")
        return "Wrong password."
    except:
        return "User does not exist."


@app.route("/upload")
def upload():
    return render_template("upload.html", email = email)

@app.route("/upload-post", methods=["POST"])
def upload_post():
    title = request.form.get("title")
    title = title.replace(" ", "-")
    f = request.files["file"]
    filename = f.filename
    filename = filename.replace(" ", "-")
    filename = title + "-" + filename
    file_path = "public/{fname}".format(fname = filename)
    f.save(file_path)
    bucket = storage.bucket() # storage bucket
    blob = bucket.blob(file_path)
    blob.upload_from_filename(file_path)
    blob.make_public()
    
    data = {
        "title": title,
        "filename": filename,
        "email": email,
        "link" : blob.public_url
    }
    db.collection("files").add(data)
    return redirect("/upload")

@app.route("/myfiles")
def myfiles():
    docs = db.collection("files").where("email", "==", email).stream()
    data = [doc.to_dict() for doc in docs]
    return render_template("myfiles.html", files = data, email = email)

@app.route("/search")
def search_get():
    return render_template("search.html", email = email)

@app.route("/search", methods=["POST"])
def search_post():
    query = request.form.get("search")
    docs = db.collection("files").stream()
    data = [doc.to_dict() for doc in docs if query in doc.to_dict()["filename"]]
    return render_template("search.html", files = data , email = email)


if __name__ == "__main__":
    app.run()