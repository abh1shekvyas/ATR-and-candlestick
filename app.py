# from flask import Flask, render_template, request
# import pandas as pd 
# from datetime import datetime
# import numpy as np
# import plotly.graph_objects as go

# app = Flask(__name__)

# @app.route("/")

# def home():
#     start_date = request.args.get('start_date')
#     print(start_date)


#     end_date = request.args.get('end_date')
#     print(end_date)

    
#     data = pd.read_csv("C:/Users/dell/Desktop/FF assignment/graph atr/CL Data.csv",index_col = 'Timestamp')
#     data['Timestamp'] = data.index
#     data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%m/%d/%Y')
#     data['Timestamp'] = data['Timestamp'].dt.strftime('%Y-%m-%d')

#     data['H_CP'] = (abs(data['High']-data['Close'].shift(1)))
#     data['H_L']= (data['High']-data['Low'])
#     data['L_CP'] = (abs(data['Low']-data['Close'].shift(1)))
#     data['TR'] = np.max(data[['H_CP', 'H_L', 'L_CP']], axis = 1)
#     data['ATR'] = data['TR'].rolling(14).mean()
#     data['MSD'] = data['Close'].rolling(window=14).std()
#     #data['TR'][0:14].mean()

#     data = data.iloc[13:,:]
#     atr1 = data['ATR'][0]
#     atr_final = [atr1]
#     prev_atr = 0

#     for i in range(1,len(data)):
#         new_atr = (atr1*(14-1) + data['TR'][i])/14
#         atr_final.append(new_atr)
#         atr1 = new_atr

#     data['final_ATR'] = atr_final
#     print(data.head())
            
#     if start_date and end_date:
#         data = data[(data['Timestamp'] >= start_date) & (data['Timestamp'] <= end_date)]
        
#     labels = data['Timestamp'].tolist()
#     print(labels)
#     values = data['final_ATR'].tolist()
    
#     return render_template("index.html", labels=labels, values=values)





from flask import Flask, render_template, request
import pandas as pd 
import numpy as np
import plotly.graph_objects as go

app = Flask(__name__)

@app.route("/")
def home():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    data = pd.read_csv("C:/Users/dell/Desktop/FF assignment/graph atr/CL Data.csv",index_col = 'Timestamp')
    data['Timestamp'] = pd.to_datetime(data.index, format='%m/%d/%Y')
    data['Timestamp'] = data['Timestamp'].dt.strftime('%Y-%m-%d')
    data['H_CP'] = (abs(data['High']-data['Close'].shift(1)))
    data['H_L']= (data['High']-data['Low'])
    data['L_CP'] = (abs(data['Low']-data['Close'].shift(1)))
    data['TR'] = np.max(data[['H_CP', 'H_L', 'L_CP']], axis = 1)
    data['ATR'] = data['TR'].rolling(14).mean()
    data['MSD'] = data['Close'].rolling(window=14).std()

    data = data.iloc[13:,:]
    atr1 = data['ATR'][0]
    atr_final = [atr1]
    prev_atr = 0

    for i in range(1,len(data)):
        new_atr = (atr1*(14-1) + data['TR'][i])/14
        atr_final.append(new_atr)
        atr1 = new_atr

    data['final_ATR'] = atr_final

    if start_date and end_date:
        data = data[(data['Timestamp'] >= start_date) & (data['Timestamp'] <= end_date)]
            
    labels = data['Timestamp'].tolist()
    values = data['final_ATR'].tolist() # use final_ATR instead of ATR
    print(labels[1:15])
    print(values[1:15])
    candlestick = go.Figure(data=[go.Candlestick(x=data.index,
                            open=data['Open'],
                            high=data['High'],
                            low=data['Low'],
                            close=data['Close'])]) 
    candlestick.update_layout(xaxis_rangeslider_visible=False)
    candlestick_html = candlestick.to_html(full_html=False)
    
    return render_template("index.html", labels=labels, values=values, candlestick=candlestick_html)
