from flask import Flask, render_template
from flask import request

import requests
import config
import webbrowser

from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('page_1.html')

@app.route('/creator', methods=['POST'])
def creator(): #this part gets data ready for insertion
    variables = request.get_json()
    #getting out each individual component
    name = variables['name']
    vege = variables['vege']
    vega = variables['vega']
    pro = variables['pro']
    carb = variables['carb']
    fat = variables['fat']
    alc = variables['alc']
    bal = variables['bal']
    Tre = variables['Tre']
    Pea = variables['Pea']
    lowCal = variables['lowCal']
    highCal = variables['highCal']
    maxItems = variables['maxItems']
    recipeNumber = variables['recipeNumber']
    
    commandparts = [name,vege,vega,pro,carb,fat,alc,bal,Tre,Pea,lowCal,highCal,maxItems,recipeNumber]
    reqString = "https://api.edamam.com/search?q="+name+"&app_id="+config.APPID+"&app_key="+config.APPKEY+"&calories="+str(lowCal)+"-"+str(highCal)+"&ingr="+str(maxItems)
    # LOT OF IF STATEMENTS
    if (vege==1):
        reqString = reqString + "&health="+"vegetarian"
    if (vega==1):
        reqString = reqString + "&health="+"vegan"    
    if (pro==1):
        reqString = reqString + "&diet="+"high-protein"
    if (carb==1):
        reqString = reqString + "&diet="+"low-carb"
    if (fat==1):
        reqString = reqString + "&diet="+"low-fat"
    if (alc==1):
        reqString = reqString + "&health="+"alcohol-free"
    if (bal==1):
        reqString = reqString + "&diet="+"balanced"
    if (Tre==1):
        reqString = reqString + "&health="+"tree-nut-free"
    if (Pea==1):
        reqString = reqString + "&health="+"peanut-free"
    #end of  long ifs
    print(reqString)
    a = requests.get(reqString)
    dat = a.json()
    procedure=""
    label=""
    ingredients=[]
    imgurl=""
    nextlabel="final recipe reached"
    #commandparts
    print(['hits'])        
    procedure = dat['hits'][int(recipeNumber)]['recipe']['url']
    label = dat['hits'][int(recipeNumber)]['recipe']['label']#: addefd t look good
    imgurl = dat['hits'][int(recipeNumber)]['recipe']['image']
    print(len(dat['hits']))
    print(recipeNumber)
    if (len(dat['hits'])-1> recipeNumber+1): #if next label is valid
        nextlabel = dat['hits'][int(recipeNumber)+1]['recipe']['label']
    else:
        nextlabel = "final recipe reached"
        
    for j in dat['hits'][int(recipeNumber)]['recipe']['ingredients']:
        ingredients.append(j['text'])

    return render_template('flask1.html', ingredients = ingredients, imgurl=imgurl, procedure=procedure, commandparts=commandparts, label=label, nextlabel = nextlabel)
    
    
    

    
if __name__ == '__main__':
    app.run(debug=True) #get rid of debug mode when ur done