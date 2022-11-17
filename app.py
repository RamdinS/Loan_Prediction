import config
from project_app.utils import LoanPrediction
from flask import Flask,request,jsonify,render_template,url_for

app = Flask(__name__) #creates the Flask instance. __name__ is the name of the current Python module. The app needs to know where it's located to set up some paths, and __name__ is a convenient way to tell it that.

#Home API
@app.route('/')
def home():
#    return "Welcome to Home Page"
    return render_template('index.html')

#Prediction API
@app.route('/result_prediction')
def result_prediction():
    input_data = request.get_json()
    Gender=str(input_data['Gender'])
    Married=str(input_data['Married'])
    Dependents=str(input_data['Dependents'])
    Education=str(input_data['Education'])
    Self_Employed=str(input_data['Self_Employed'])
    ApplicantIncome=int(input_data['ApplicantIncome'])
    CoapplicantIncome=float(input_data['CoapplicantIncome'])
    LoanAmount=float(input_data['LoanAmount'])
    Loan_Amount_Term=float(input_data['Loan_Amount_Term'])
    Credit_History=float(input_data['Credit_History'])
    Property_Area=str(input_data['Property_Area'])

    loan = LoanPrediction(Gender,Married,Dependents,Education,Self_Employed,ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History,Property_Area)
    result = loan.loan_pred()

    return jsonify({"Result":f"The prediction for loan approval is :{result}"})


# take input from web
@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method == 'POST':
        Gender=str(request.form['Gender'])
        Married=str(request.form['Married'])
        Dependents=str(request.form['Dependents'])
        Education=str(request.form['Education'])
        Self_Employed=str(request.form['Self_Employed'])
        ApplicantIncome=int(request.form['ApplicantIncome'])
        CoapplicantIncome=float(request.form['CoapplicantIncome'])
        LoanAmount=float(request.form['LoanAmount'])
        Loan_Amount_Term=float(request.form['Loan_Amount_Term'])
        Credit_History=float(request.form['Credit_History'])
        Property_Area=str(request.form['Property_Area'])

    loan = LoanPrediction(Gender,Married,Dependents,Education,Self_Employed,ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History,Property_Area)
    result = loan.loan_pred()

    # return jsonify({"Result":f"The prediction for loan approval is :{result}"})
    return render_template('pred.html', data=result)


if __name__ == '__main__':
    app.run()