from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__, template_folder="templates")
import pandas as pd
import cx_Oracle 
import os
path = os.getcwd()

@app.route('/', methods = ['GET', 'POST'])

def upload_page():
    if request.method == 'POST':
        date = request.form.get('date', False)
        card_1 = request.form.get('type_1', False)
        card_2 = request.form.get('type_2', False)
        mcc  = request.form.get('mcc', False)
        bank = request.form.get('bank', False)
        merchant = request.form.get('merchant', False)
        
        dsn_tns = cx_Oracle.makedsn('YOUR_ORACLE_DNS', 
        							'PORT', 
        							service_name='YOUR_SERVICE_NAME')

        conn = cx_Oracle.connect(user=r'YOUR_USERNAME', 
        						 password='YOUR_PASSWORD', 
        						 dsn=dsn_tns) 
        c = conn.cursor()



        query1 = ''' 
                select /*+parallel(20)*/
                        t1.*
                    from table1 t1
                    where 1=1
                      and t1.date >= date\'''' + (date if date else '2022-01-01') + ''''
                      and t1.date < sysdate
                      and t1.mcc like \'''' + (mcc if mcc else '%') + '''')
                      and upper(t1.merchant_name_f) like upper('%'''+(merchant if merchant else '%')+'''%')
                	  and type_card IN (\'''' + (card_1 if card_1 else ' ') + '''',
                                 \'''' + (card_2 if card_2 else ' ') + '''')
                	  and ACQUIRER_NAME LIKE upper('%''' +(bank if bank else '%')+ '''%')
             '''

        df = pd.read_sql(query1, con=conn) # Query Execution
        
        df.to_excel(path + '/static/Detalization.xlsx') # Output file
        
        with open('readme.txt', 'w') as f:
            f.write(query1) # How the final SQL Script Looks like, for debugging purposes
        
        return render_template('index.html', 
                                      date = date,
                                      card_1 = card_1,
                                      card_2 = card_2,
                                      mcc  = mcc,
                                      bank = bank,
                                      merchant = merchant)

    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0')
