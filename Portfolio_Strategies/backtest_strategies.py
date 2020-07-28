import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import mplfinance as mpf
from finta import TA
from pylab import rcParams
from yahoo_fin import stock_info as si
import talib
import ta

pd.set_option('display.max_columns', None)

# define stock and time range 
stock = input('Enter a stock ticker: ')

num_of_years = input('Enter number of years: ')
num_of_years = float(num_of_years)
start = dt.date.today() - dt.timedelta(days = int(365.25*num_of_years))
end = dt.datetime.now()

current_price = round(si.get_live_price(stock), 2)
df = yf.download(stock,start, end, interval='1d')

signals = ['Moving Average', 'Relative Strength Index', 'Bollinger Bands', 'MACD', 'Commodity Channel Index', 'Extended Market Calculator']
change = []
num_of_trades = []
last_sell = []
last_buy = []
average_gain = []
average_loss = []
max_return = []
max_loss = []
gain_loss = []
battling_avg  = []

for signal in signals:
    if signal.lower() == 'moving average':
        print ('-'*60)
        print ('Simple Moving Average: ')
        # Let's calulate Simple Moving Average(SMA)
        short_sma= 20
        long_sma = 50
        SMAs=[short_sma, long_sma]
        
        for i in SMAs:
            df["SMA_"+str(i)]= df.iloc[:,4].rolling(window=i).mean()
        
        position=0 # 1 means we have already entered poistion, 0 means not already entered
        counter=0
        percentChange=[]   # empty list to collect %changes 
        for i in df.index:
            SMA_short=df['SMA_20']
            SMA_long =df['SMA_50']
            close=df['Adj Close'][i]
            
            if(SMA_short[i] > SMA_long[i]):

                if(position==0):
                    buyP=close   #buy price
                    position=1   # turn position

                
            elif(SMA_short[i] < SMA_long[i]):

                if(position==1):   # have a poistion in down trend
                    position=0     # selling position
                    sellP=close    # sell price
    
                    perc=(sellP/buyP-1)*100
                    percentChange.append(perc)
            if(counter==df["Adj Close"].count()-1 and position==1):
                position=0
                sellP=close

                perc=(sellP/buyP-1)*100
                percentChange.append(perc)
        
            counter+=1
        
        gains=0
        numGains=0
        losses=0
        numLosses=0
        totReturn=1
        for i in percentChange:
            if(i>0):
                gains+=i
                numGains+=1
            else:
                losses+=i
                numLosses+=1
            totReturn = totReturn*((i/100)+1)
        totReturn=round((totReturn-1)*100,2)
        print("These statistics are from "+str(start)+" up till now with "+str(numGains+numLosses)+" trades:")
        print("SMAs used: "+str(SMAs))
        print("Total return over "+str(numGains+numLosses)+ " trades: "+ str(totReturn)+"%")
        
        if (numGains>0):
            avgGain=gains/numGains
            maxReturn= str(max(percentChange))
        else:
            avgGain=0
            maxReturn=np.nan
        
        if(numLosses>0):
            avgLoss=losses/numLosses
            maxLoss=str(min(percentChange))
            ratioRR=str(-avgGain/avgLoss)  # risk-reward ratio
        else:
            avgLoss=0
            maxLoss=np.nan
            ratioRR='inf'
        
        df['PC'] = df['Close'].pct_change()
        hold = round(df['PC'].sum() * 100, 2)
        print ("Total return for a B&H strategy: " + str(hold)+'%')
        print("Average Gain: "+ str(round(avgGain, 2)))
        print("Average Loss: "+ str(round(avgLoss, 2)))
        print("Max Return: "+ str(maxReturn))
        print("Max Loss: "+ str(maxLoss))
        print("Gain/loss ratio: "+ str(ratioRR))
        
        if(numGains>0 or numLosses>0):
            batAvg=numGains/(numGains+numLosses)
        else:
            batAvg=0
        print("Batting Avg: "+ str(batAvg))
        change.append(totReturn)
        trades = numGains+numLosses
        num_of_trades.append(trades)
        last_sell.append(sellP)
        last_buy.append(buyP)
        average_gain.append(avgGain)
        average_loss.append(avgLoss)
        max_return.append(float(maxReturn))
        max_loss.append(float(maxLoss))
        gain_loss.append(float(ratioRR))
        battling_avg.append(batAvg)

    elif signal.lower() == 'relative strength index':
        print ('-'*60)
        print ('Relative Strength Index: ')
        
        df["RSI"] = talib.RSI(df["Close"])
        values = df["RSI"].tail(14)
        value = values.mean()
        
        position=0 # 1 means we have already entered poistion, 0 means not already entered
        counter=0
        percentChange=[]   # empty list to collect %changes 
        for i in df.index:
            rsi=df['RSI']
            close=df['Adj Close'][i]
            
            if(rsi[i] <= 30):
                if(position==0):
                    buyP=close   #buy price
                    position=1   # turn position

                
            elif(rsi[i] >= 70):

                if(position==1):   # have a position in down trend
                    position=0     # selling position
                    sellP=close    # sell price
    
                    perc=(sellP/buyP-1)*100
                    percentChange.append(perc)
            if(counter==df["Adj Close"].count()-1 and position==1):
                position=0
                sellP=close

                perc=(sellP/buyP-1)*100
                percentChange.append(perc)
        
            counter+=1

        gains=0
        numGains=0
        losses=0
        numLosses=0
        totReturn=1
        for i in percentChange:
            if(i>0):
                gains+=i
                numGains+=1
            else:
                losses+=i
                numLosses+=1
            totReturn = totReturn*((i/100)+1)
        totReturn=round((totReturn-1)*100,2)
        print("These statistics are from "+str(start)+" up till now with "+str(numGains+numLosses)+" trades:")
        print("Total return over "+str(numGains+numLosses)+ " trades: "+ str(totReturn)+"%")
        
        if (numGains>0):
            avgGain=gains/numGains
            maxReturn= str(max(percentChange))
        else:
            avgGain=0
            maxReturn=np.nan
        
        if(numLosses>0):
            avgLoss=losses/numLosses
            maxLoss=str(min(percentChange))
            ratioRR=str(-avgGain/avgLoss)  # risk-reward ratio
        else:
            avgLoss=0
            maxLoss=np.nan
            ratioRR='inf'
        
        df['PC'] = df['Close'].pct_change()
        hold = round(df['PC'].sum() * 100, 2)
        print ("Total return for a B&H strategy: " + str(hold)+'%')
        print("Average Gain: "+ str(round(avgGain, 2)))
        print("Average Loss: "+ str(round(avgLoss, 2)))
        print("Max Return: "+ str(maxReturn))
        print("Max Loss: "+ str(maxLoss))
        print("Gain/loss ratio: "+ str(ratioRR))
        
        if(numGains>0 or numLosses>0):
            batAvg=numGains/(numGains+numLosses)
        else:
            batAvg=0
        print("Batting Avg: "+ str(batAvg))
        change.append(totReturn)
        trades = numGains+numLosses
        num_of_trades.append(trades)
        last_sell.append(sellP)
        last_buy.append(buyP)
        average_gain.append(avgGain)
        average_loss.append(avgLoss)
        max_return.append(float(maxReturn))
        max_loss.append(float(maxLoss))
        gain_loss.append(float(ratioRR))
        battling_avg.append(batAvg)

    elif signal.lower() == 'bollinger bands':  
        print ('-'*60)
        print ('Bollinger Bands: ')
        
        position=0 # 1 means we have already entered poistion, 0 means not already entered
        counter=0
        percentChange=[]   # empty list to collect %changes 
        df['upper_band'], df['middle_band'], df['lower_band'] = talib.BBANDS(df['Adj Close'], timeperiod =20)
        for i in df.index:
            BBAND_upper =df['upper_band']
            BBAND_lower =df['lower_band']
            close_price = df['Adj Close']
            close=df['Adj Close'][i]
            
            if(BBAND_lower[i] > close_price[i]):
                if(position==0):
                    buyP=close   #buy price
                    position=1   # turn position

            elif(BBAND_upper[i] < close_price[i]):
                if(position==1):   # have a poistion in down trend
                    position=0     # selling position
                    sellP=close    # sell price
    
                    perc=(sellP/buyP-1)*100
                    percentChange.append(perc)
            if(counter==df["Adj Close"].count()-1 and position==1):
                position=0
                sellP=close

                perc=(sellP/buyP-1)*100
                percentChange.append(perc)
        
            counter+=1

        gains=0
        numGains=0
        losses=0
        numLosses=0
        totReturn=1
        for i in percentChange:
            if(i>0):
                gains+=i
                numGains+=1
            else:
                losses+=i
                numLosses+=1
            totReturn = totReturn*((i/100)+1)
        totReturn=round((totReturn-1)*100,2)
        print("These statistics are from "+str(start)+" up till now with "+str(numGains+numLosses)+" trades:")
        print("Total return over "+str(numGains+numLosses)+ " trades: "+ str(totReturn)+"%")
        
        if (numGains>0):
            avgGain=gains/numGains
            maxReturn= str(max(percentChange))
        else:
            avgGain=0
            maxReturn=np.nan
        
        if(numLosses>0):
            avgLoss=losses/numLosses
            maxLoss=str(min(percentChange))
            ratioRR=str(-avgGain/avgLoss)  # risk-reward ratio
        else:
            avgLoss=0
            maxLoss=np.nan
            ratioRR='inf'
        
        df['PC'] = df['Close'].pct_change()
        hold = round(df['PC'].sum() * 100, 2)
        print ("Total return for a B&H strategy: " + str(hold)+'%')
        print("Average Gain: "+ str(round(avgGain, 2)))
        print("Average Loss: "+ str(round(avgLoss, 2)))
        print("Max Return: "+ str(maxReturn))
        print("Max Loss: "+ str(maxLoss))
        print("Gain/loss ratio: "+ str(ratioRR))
        
        if(numGains>0 or numLosses>0):
            batAvg=numGains/(numGains+numLosses)
        else:
            batAvg=0
        print("Batting Avg: "+ str(batAvg))
        change.append(totReturn)
        trades = numGains+numLosses
        num_of_trades.append(trades)
        last_sell.append(sellP)
        last_buy.append(buyP)
        average_gain.append(avgGain)
        average_loss.append(avgLoss)
        max_return.append(float(maxReturn))
        max_loss.append(float(maxLoss))
        gain_loss.append(float(ratioRR))
        battling_avg.append(batAvg)
        
    elif signal.lower() == 'macd':
        print ('-'*60)
        print ('MACD: ')
        
        position=0 # 1 means we have already entered poistion, 0 means not already entered
        counter=0
        percentChange=[]   # empty list to collect %changes 
        df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(df['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        for i in df.index:
            macd = df['macd']
            macdsignal = df['macdsignal']
            close=df['Adj Close'][i]
            
            if(macd[i] > macdsignal[i]):
                if(position==0):
                    buyP=close   #buy price
                    position=1   # turn position

                
            elif(macd[i] < macdsignal[i]):

                if(position==1):   # have a poistion in down trend
                    position=0     # selling position
                    sellP=close    # sell price
    
                    perc=(sellP/buyP-1)*100
                    percentChange.append(perc)
            if(counter==df["Adj Close"].count()-1 and position==1):
                position=0
                sellP=close

                perc=(sellP/buyP-1)*100
                percentChange.append(perc)
        
            counter+=1

        gains=0
        numGains=0
        losses=0
        numLosses=0
        totReturn=1
        for i in percentChange:
            if(i>0):
                gains+=i
                numGains+=1
            else:
                losses+=i
                numLosses+=1
            totReturn = totReturn*((i/100)+1)
        totReturn=round((totReturn-1)*100,2)
        print("These statistics are from "+str(start)+" up till now with "+str(numGains+numLosses)+" trades:")
        print("Total return over "+str(numGains+numLosses)+ " trades: "+ str(totReturn)+"%")
        
        if (numGains>0):
            avgGain=gains/numGains
            maxReturn= str(max(percentChange))
        else:
            avgGain=0
            maxReturn=np.nan
        
        if(numLosses>0):
            avgLoss=losses/numLosses
            maxLoss=str(min(percentChange))
            ratioRR=str(-avgGain/avgLoss)  # risk-reward ratio
        else:
            avgLoss=0
            maxLoss=np.nan
            ratioRR='inf'
        
        df['PC'] = df['Close'].pct_change()
        hold = round(df['PC'].sum() * 100, 2)
        print ("Total return for a B&H strategy: " + str(hold)+'%')
        print("Average Gain: "+ str(round(avgGain, 2)))
        print("Average Loss: "+ str(round(avgLoss, 2)))
        print("Max Return: "+ str(maxReturn))
        print("Max Loss: "+ str(maxLoss))
        print("Gain/loss ratio: "+ str(ratioRR))
        
        if(numGains>0 or numLosses>0):
            batAvg=numGains/(numGains+numLosses)
        else:
            batAvg=0
        print("Batting Avg: "+ str(batAvg))
        change.append(totReturn)
        trades = numGains+numLosses
        num_of_trades.append(trades)
        last_sell.append(sellP)
        last_buy.append(buyP)
        average_gain.append(avgGain)
        average_loss.append(avgLoss)
        max_return.append(float(maxReturn))
        max_loss.append(float(maxLoss))
        gain_loss.append(float(ratioRR))
        battling_avg.append(batAvg)
    
    elif signal.lower() == 'commodity channel index':
        print ('-'*60)
        print ('Commodity Channel Index: ')
        
        position=0 # 1 means we have already entered poistion, 0 means not already entered
        counter=0
        percentChange=[]   # empty list to collect %changes 
        cci = talib.CCI(df['High'], df['Low'], df['Close'], timeperiod=14)
        for i in df.index:
            cci = cci
            close=df['Adj Close'][i]
            
            if(cci[i] > 0):

                if(position==0):
                    buyP=close   #buy price
                    position=1   # turn position

                
            elif(cci[i] < 0):

                if(position==1):   # have a poistion in down trend
                    position=0     # selling position
                    sellP=close    # sell price
    
                    perc=(sellP/buyP-1)*100
                    percentChange.append(perc)
            if(counter==df["Adj Close"].count()-1 and position==1):
                position=0
                sellP=close

                perc=(sellP/buyP-1)*100
                percentChange.append(perc)
        
            counter+=1

        gains=0
        numGains=0
        losses=0
        numLosses=0
        totReturn=1
        for i in percentChange:
            if(i>0):
                gains+=i
                numGains+=1
            else:
                losses+=i
                numLosses+=1
            totReturn = totReturn*((i/100)+1)
        totReturn=round((totReturn-1)*100,2)
        
        print("These statistics are from "+str(start)+" up till now with "+str(numGains+numLosses)+" trades:")
        print("Total return over "+str(numGains+numLosses)+ " trades: "+ str(totReturn)+"%")
        
        if (numGains>0):
            avgGain=gains/numGains
            maxReturn= str(max(percentChange))
        else:
            avgGain=0
            maxReturn=np.nan
        
        if(numLosses>0):
            avgLoss=losses/numLosses
            maxLoss=str(min(percentChange))
            ratioRR=str(-avgGain/avgLoss)  # risk-reward ratio
        else:
            avgLoss=0
            maxLoss=np.nan
            ratioRR='inf'
        
        df['PC'] = df['Close'].pct_change()
        hold = round(df['PC'].sum() * 100, 2)
        print ("Total return for a B&H strategy: " + str(hold)+'%')
        print("Average Gain: "+ str(round(avgGain, 2)))
        print("Average Loss: "+ str(round(avgLoss, 2)))
        print("Max Return: "+ str(maxReturn))
        print("Max Loss: "+ str(maxLoss))
        print("Gain/loss ratio: "+ str(ratioRR))
        
        if(numGains>0 or numLosses>0):
            batAvg=numGains/(numGains+numLosses)
        else:
            batAvg=0
        print("Batting Avg: "+ str(batAvg))
        change.append(totReturn)
        trades = numGains+numLosses
        num_of_trades.append(trades)
        last_sell.append(sellP)
        last_buy.append(buyP)
        average_gain.append(avgGain)
        average_loss.append(avgLoss)
        max_return.append(float(maxReturn))
        max_loss.append(float(maxLoss))
        gain_loss.append(float(ratioRR))
        battling_avg.append(batAvg)

    if signal.lower() == 'extended market calculator':
        #Asks for stock ticker
        sma = 50
        limit = 10
        
        #calculates sma and creates a column in the dfframe
        df['SMA'+str(sma)] = df.iloc[:,4].rolling(window=sma).mean() 
        df['PC'] = ((df["Adj Close"]/df['SMA'+str(sma)])-1)*100
        
        position=0 # 1 means we have already entered poistion, 0 means not already entered
        counter=0
        percentChange=[]   # empty list to collect %changes 
        
        n = -1
        for i in df.index:
            n = n + 1 
            mean =df["PC"].mean()
            stdev=df["PC"].std()
            current=df["PC"][n]
            close=df['Adj Close'][i]
            
            if(current < -2*stdev+mean):
                if(position==0):
                    buyP=close   #buy price
                    position=1   # turn position
                
            elif(current > 2*stdev+mean):
                if(position==1):   # have a poistion in down trend
                    position=0     # selling position
                    sellP=close    # sell price
    
                    perc=(sellP/buyP-1)*100
                    percentChange.append(perc)
            if(counter==df["Adj Close"].count()-1 and position==1):
                position=0
                sellP=close

                perc=(sellP/buyP-1)*100
                percentChange.append(perc)
        
            counter+=1
        
        gains=0
        numGains=0
        losses=0
        numLosses=0
        totReturn=1
        for i in percentChange:
            if(i>0):
                gains+=i
                numGains+=1
            else:
                losses+=i
                numLosses+=1
            totReturn = totReturn*((i/100)+1)
        totReturn=round((totReturn-1)*100,2)
        print("These statistics are from "+str(start)+" up till now with "+str(numGains+numLosses)+" trades:")
        print("Total return over "+str(numGains+numLosses)+ " trades: "+ str(totReturn)+"%")
        
        if (numGains>0):
            avgGain=gains/numGains
            maxReturn= str(max(percentChange))
        else:
            avgGain=0
            maxReturn=np.nan
        
        if(numLosses>0):
            avgLoss=losses/numLosses
            maxLoss=str(min(percentChange))
            ratioRR=str(-avgGain/avgLoss)  # risk-reward ratio
        else:
            avgLoss=0
            maxLoss=np.nan
            ratioRR='inf'
        
        df['PC'] = df['Close'].pct_change()
        hold = round(df['PC'].sum() * 100, 2)
        print ("Total return for a B&H strategy: " + str(hold)+'%')
        print("Average Gain: "+ str(round(avgGain, 2)))
        print("Average Loss: "+ str(round(avgLoss, 2)))
        print("Max Return: "+ str(maxReturn))
        print("Max Loss: "+ str(maxLoss))
        print("Gain/loss ratio: "+ str(ratioRR))
        
        if(numGains>0 or numLosses>0):
            batAvg=numGains/(numGains+numLosses)
        else:
            batAvg=0
        print("Batting Avg: "+ str(batAvg))
        change.append(totReturn)
        trades = numGains+numLosses
        num_of_trades.append(trades)
        last_sell.append(sellP)
        last_buy.append(buyP)
        average_gain.append(avgGain)
        average_loss.append(avgLoss)
        max_return.append(float(maxReturn))
        max_loss.append(float(maxLoss))
        gain_loss.append(float(ratioRR))
        battling_avg.append(batAvg)
        
prices = df['Adj Close'].tolist()
first_price = prices[0]

new_col = [current_price, current_price, current_price, current_price, current_price, current_price]

if hold > 0:
    holding = [['Buy and Hold', hold, 1, first_price, np.nan, hold, np.nan, hold, np.nan, np.inf, 1]]
else:
    holding = [['Buy and Hold', hold, 1, first_price, np.nan, np.nan, hold, np.nan, hold, 0, 0]]

dataframe = pd.DataFrame(list(zip(signals, change, num_of_trades, last_buy, last_sell, average_gain, average_loss, max_return, max_loss, gain_loss, battling_avg)), columns =['Strategy', 'Total Return' ,'Number of Trades', 'Last Buy', 'Last Sell' ,'Average Gain', 'Average Loss', 'Max Return', 'Max Loss', 'Gain/Loss Ratio', 'Battling Avg.'])
dataframe = dataframe.append(pd.DataFrame(holding, columns =['Strategy', 'Total Return' ,'Number of Trades', 'Last Buy', 'Last Sell', 'Average Gain', 'Average Loss', 'Max Return', 'Max Loss', 'Gain/Loss Ratio', 'Battling Avg.']),ignore_index=True)
dataframe = dataframe.set_index('Strategy')
dataframe = dataframe.sort_values('Total Return', ascending=False)
dataframe = dataframe.round(2)
print ('\nFull Statistics: ')
print (dataframe)
print ('\nCurrent Price: ' + str(current_price))