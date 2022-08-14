from django.shortcuts import render, redirect
from .models import stock
from .forms import stockform
from django.contrib import messages
#from alpha_vantage.timeseries import TimeSeries

# Create your views here.

def home(request):
    import requests
    import json 
    # pandas
    if request.method == "POST":
        sticker = request.POST['sticker']
        #pk_579e8f74c64b4b9086a6f2d84b4ed3b1
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(sticker) +"/quote?token=pk_579e8f74c64b4b9086a6f2d84b4ed3b1")
        apis = requests.get("https://cloud.iexapis.com/stable/tops?token=pk_579e8f74c64b4b9086a6f2d84b4ed3b1&symbols="+ (sticker) +"")
        #alph = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+ (sticker) +"&interval=5min&apikey=G44QM5V1IHBG6RP8")
        # a = 'G44QM5V1IHBG6RP8'
        # ts = TimeSeries(key=a, output_format='pandas')
        # data = ts.get_intraday(sticker, interval="15min")
        try:
            api = json.loads(api_request.content)
            apid = json.loads(apis.content) 
            #alpha = json.loads(alph.content) 
            # d = pandas.DataFrame.from_dict(alpha, orient='index')
        except Exception as e:
            api = "Error..."
        return render (request, 'home.html', {'api':api, 'apid':apid})
    else:
        return render (request, 'home.html', {'sticker':"enter the sticker symbol above"})

def about(request):
    return render (request, 'about.html')

def addstock(request):
    import requests
    import json 
    if request.method == "POST":
        form = stockform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added"))
            return redirect('/addstock/')
    else:
        sticker = stock.objects.all()
         
        output = []

        for sticker_item in sticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(sticker_item) +"/quote?token=pk_579e8f74c64b4b9086a6f2d84b4ed3b1")
            try:
                api = json.loads(api_request.content)
                
                output.append(api)
                #output.append(apid)
            except Exception as e:
                api = "Error..."

        return render (request, 'addstock.html', {'sticker':sticker,'output':output})

def delete(request, id):
    fm = stock.objects.get(pk=id)
    fm.delete()
    messages.success(request, ('Stock has been deleted successfully'))
    return redirect ('/addstock/' )

def delete_stock(request):
    sticker = stock.objects.all()
    return render (request, 'delete.html', {'sticker':sticker})