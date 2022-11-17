import config
import json
import pickle
import numpy as np


class LoanPrediction():
    def __init__(self,Gender,Married,Dependents,Education,Self_Employed,ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History,Property_Area):
        self.Gender = "Gender_"+Gender
        self.Married = "Married_"+Married
        self.Dependents = Dependents
        self.Education = "Education_"+Education
        self.Self_Employed = "Self_Employed_"+Self_Employed
        self.ApplicantIncome = ApplicantIncome
        self.CoapplicantIncome = CoapplicantIncome
        self.LoanAmount = LoanAmount
        self.Loan_Amount_Term = Loan_Amount_Term
        self.Credit_History = Credit_History
        self.Property_Area = "Property_Area_"+Property_Area

    def load_model(self):
        with open(config.MODEL_FILE_PATH,'rb') as f:
            self.model = pickle.load(f)

        with open(config.ENCODER_FILE_PATH,'r') as f:
            self.enc = json.load(f)

    def loan_pred(self):
        self.load_model()
        test_arr = np.zeros(len(self.enc['columns']))

        #Conversion of categorical to numericals columns
        self.Dependents = self.enc['Dependents'][self.Dependents]

        #Conversion of categorical encoding columns
        Gender_index = self.enc['columns'].index(self.Gender)
        Married_index = self.enc['columns'].index(self.Married)
        Dependents = "Dependents_"+str(self.Dependents)
        Dependents_index = self.enc['columns'].index(Dependents)
        Education_index = self.enc['columns'].index(self.Education)
        Self_Employed_index = self.enc['columns'].index(self.Self_Employed)
        Property_Area_index = self.enc['columns'].index(self.Property_Area)

        #Creating New columns
        Total_Income = self.ApplicantIncome + self.CoapplicantIncome
        Total_Income_log = np.log(Total_Income)
        LoanAmount_log = np.log(self.LoanAmount)
        EMI = self.LoanAmount/self.Loan_Amount_Term
        Balance_Income = Total_Income - (EMI * 1000)

        test_arr[0] = self.Credit_History #Credit_History
        test_arr[1] = LoanAmount_log #LoanAmount_log
        test_arr[Gender_index] = 1 #Gender
        test_arr[Married_index] = 1 #Married
        test_arr[Dependents_index] = 1 #Dependents
        test_arr[Education_index] = 1 #Education
        test_arr[Self_Employed_index] = 1 #Self_Employed
        test_arr[Property_Area_index] = 1 #Property_Area
        test_arr[17] = Total_Income_log #Total_Income_log
        test_arr[18] = EMI #EMI
        test_arr[19] = Balance_Income #Balance_Income

        prediction = self.model.predict([test_arr])[0]
        prediction = self.enc['target'][str(prediction)]

        return prediction