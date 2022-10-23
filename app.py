# import library/package pandas dan sci-kit learn
# memakai flask untuk membuat webnya
import pandas as pd
from flask import Flask, request, render_template
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

# inisialisasi flask
app = Flask(__name__)

# ambil data buys computer
ds = pd.read_csv('buys_computer.csv', usecols= ['age','income','student','creditrating','buyscomputer'])

# mengambil data tiap atribut
x = ds.iloc[:,:-1].values # atribut x (age, income, student, credit_rating)
y = ds.iloc[:,-1].values # atribut y (buys_computer)

# membuat encoder (mengubah string menjadi angka)
encoder = LabelEncoder()

# mengubah value tiap atribut menjadi angka
x[:,0] = encoder.fit_transform(x[:,0]) #age
x[:,1] = encoder.fit_transform(x[:,1]) #income
x[:,2] = encoder.fit_transform(x[:,2]) #student
x[:,3] = encoder.fit_transform(x[:,3]) #credit
y = encoder.fit_transform(y) # buy

# Membuat klasifikasi decision tree
model = DecisionTreeClassifier()

# train model
model.fit(x, y)

# tampilan index (halaman awal)
@app.route('/')
def index():
    # menampilkan template
    return render_template('index.html', predicted="?", age = "?", income = "?", student = "?", creditrating = "?")

# tampilan setelah button prediksi di klik
# diarahkan ke halaman /prediction
# data dikirimkan menggunakan method post
@app.route('/prediction', methods=['POST'])
def prediction():
    # mengambil data masukan user berdasarkan name form input
    age = int(request.form['age'])
    income = int(request.form['income'])
    student = int(request.form['student'])
    creditrating = int(request.form['creditrating'])
    
    # memprediksi masukan user berdasarkan model
    predicted = model.predict([[age, income, student, creditrating]])
    
    # mengubah angka encoder menjadi string
    # age
    if age == 0:
        age = "Young"
    elif age == 1:
        age = "Middle-Aged"
    elif age == 2:
        age = "Senior"
    # income
    if income == 0:
        income = "High"
    elif income == 1:
        income = "Medium"
    elif income == 2:
        income = "Low"
    # student
    student = "No" if student else "Yes"
    # credit
    creditrating = "Excellent" if creditrating else "Fair"

    # menampilkan template yang sama dengan membawa data hasil prediksi
    return render_template('index.html', predicted = "Yes" if predicted else "No", age = age, income = income, student = student, creditrating = creditrating)

# driver
if __name__ == '__main__':
    app.run(debug=True)