import firebase_admin
from firebase_admin import credentials,auth,firestore, storage
import hashlib


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'storageBucket': 'da-sharing.appspot.com'})
db = firestore.client()


email = "keerthi@gmail.com"
docs = db.collection("files").where("email", "==", email).stream()
data = []
x = 1
for doc in docs:
            dict_ = doc.to_dict()
            dict_["id"] = x
            data.append(dict_)
            x+=1
print(data)


###db.collection("users").add(current_data)

"""
file_path = "text_docs/sample_text_file.txt"
bucket = storage.bucket() # storage bucket
blob = bucket.blob(file_path)
blob.upload_from_filename(file_path)


email = input("Enter your email: ")
password = input("Enter your password: ")
display_name = input("Enter your display name: ")


hash_object = hashlib.sha512((display_name).encode())
uid = hash_object.hexdigest()


user = auth.create_user(uid = uid, display_name = display_name, email = email, password = password)
print(user.uid)
#firebase_admin._auth_utils.UidAlreadyExistsError:
"""


