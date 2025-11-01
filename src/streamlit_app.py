import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px


st.title('Ames city house price prediction')
st.set_page_config(layout="wide")

ordinal = ['Overall Cond', 'MS SubClass', 'Overall Qual']

cat = {
    'MS SubClass':[
        '20 1-STORY 1946 & NEWER ALL STYLES',
        '30 1-STORY 1945 & OLDER',
        '40 1-STORY W/FINISHED ATTIC ALL AGES',
        '45 1-1/2 STORY - UNFINISHED ALL AGES',
        '50 1-1/2 STORY FINISHED ALL AGES',
        '60 2-STORY 1946 & NEWER',
        '70 2-STORY 1945 & OLDER',
        '75 2-1/2 STORY ALL AGES',
        '80 SPLIT OR MULTI-LEVEL',
        '85 SPLIT FOYER',
        '90 DUPLEX - ALL STYLES AND AGES',
        '120 1-STORY PUD (Planned Unit Development) - 1946 & NEWER',
        '150 1-1/2 STORY PUD - ALL AGES',
        '160 2-STORY PUD - 1946 & NEWER',
        '180 PUD - MULTILEVEL - INCL SPLIT LEV/FOYER',
        '190 2 FAMILY CONVERSION - ALL STYLES AND AGES'
    ],
    'Overall Qual':[
        '10 Very Excellent',
        '9 Excellent',
        '8 Very Good',
        '7 Good',
        '6 Above Average',
        '5 Average',
        '4 Below Average',
        '3 Fair',
        '2 Poor',
        '1 Very Poor'
        ],
    'MS Zoning': [
        'A Agriculture',
        'C Commercial',
        'FV Floating Village Residential',
        'I Industrial',
        'RH Residential High Density',
        'RL Residential Low Density',
        'RP Residential Low Density Park',
        'RM Residential Medium Density',
 ],
    'Lot Shape': [
        'Reg Regular', 
        'IR1 Slightly irregular',
        'IR2 Moderately Irregular',
        'IR3 Irregular',
        ],
    'Overall Cond':[
        '10 Very Excellent',
        '9 Excellent',
        '8 Very Good',
        '7 Good',
        '6 Above Average',
        '5 Average',
        '4 Below Average',
        '3 Fair',
        '2 Poor',
        '1 Very Poor'
    ],
'Land Contour':[
 'Lvl Near Flat/Level', 
 'Bnk Banked - Quick and significant rise from street grade to building',
 'HLS Hillside - Significant slope from side to side',
 'Low Depression'
 ],

'Lot Config': [
 'Inside Inside lot',
 'Corner Corner lot',
 'CulDSac Cul-de-sac',
 'FR2 Frontage on 2 sides of property',
 'FR3 Frontage on 3 sides of property'
 ],
'Condition 1':[
 'Artery Adjacent to arterial street',
 'Feedr Adjacent to feeder street ',
 'Norm Normal ',
 'RRNn Within 200\' of North-South Railroad',
 'RRAn Adjacent to North-South Railroad',
 'PosN Near positive off-site feature--park, greenbelt, etc.',
 'PosA Adjacent to postive off-site feature',
 'RRNe Within 200\' of East-West Railroad',
 'RRAe Adjacent to East-West Railroad'
 ],
'Bldg Type':[
 '1Fam Single-family Detached',
 '2FmCon Two-family Conversion; originally built as one-family dwelling',
 'Duplx Duplex',
 'TwnhsE Townhouse End Unit',
 'TwnhsI Townhouse Inside Unit'
 ],
'House Style':[
 '1Story One story',
 '1.5Fin One and one-half story: 2nd level finished',
 '1.5Unf One and one-half story: 2nd level unfinished',
 '2Story Two story',
 '2.5Fin Two and one-half story: 2nd level finished',
 '2.5Unf Two and one-half story: 2nd level unfinished',
 'SFoyer Split Foyer',
 'SLvl Split Level',
 ],
'Roof Style':[
 'Flat Flat',
 'Gable Gable',
 'Gambrel Gabrel (Barn)',
 'Hip Hip',
 'Mansard Mansard'
 'Shed Shed',
 ],
'Exterior 1st':[
 'AsbShng Asbestos Shingles',
 'AsphShn Asphalt Shingles',
 'BrkComm Brick Common',
 'BrkFace Brick Face',
 'CBlock Cinder Block',
 'CemntBd Cement Board',
 'HdBoard Hard Board',
 'ImStucc Imitation Stucco',
 'MetalSd Metal Siding',
 'Other Other',
 'Plywood Plywood',
 'PreCast PreCast',
 'Stone Stone',
 'Stucco Stucco',
 'VinylSd Vinyl Siding',
 'Wd Sdng Wood Siding',
 'WdShing Wood Shingles'
 ],
'Exterior 2nd':[
 'AsbShng Asbestos Shingles',
 'AsphShn Asphalt Shingles',
 'BrkComm Brick Common',
 'BrkFace Brick Face',
 'CBlock Cinder Block',
 'CemntBd Cement Board',
 'HdBoard Hard Board',
 'ImStucc Imitation Stucco',
 'MetalSd Metal Siding',
 'Other Other',
 'Plywood Plywood',
 'PreCast PreCast',
 'Stone Stone',
 'Stucco Stucco',
 'VinylSd Vinyl Siding',
 'Wd Sdng Wood Siding',
 'WdShing Wood Shingles'
 ],
'Exter Qual':[
 'Ex Excellent',
 'Gd Good',
 'TA Average/Typical',
 'Fa Fair',
 'Po Poor',
 ],
'Exter Cond':[
 'Ex Excellent',
 'Gd Good',
 'TA Average/Typical',
 'Fa Fair',
 'Po Poor'
 ],
'Foundation':[
 'BrkTil Brick & Tile',
 'CBlock Cinder Block',
 'PConc Poured Contrete',
 'Slab Slab',
 'Stone Stone',
 'Wood Wood',
 ],
'Bsmt Cond':[
 'Ex Excellent',
 'Gd Good',
 'TA Typical - slight dampness allowed',
 'Fa Fair - dampness or some cracking or settling',
 'Po Poor - Severe cracking, settling, or wetness',
 'NA No Basement'
 ],
'Heating QC':[
 'Ex Excellent',
 'Gd Good',
 'TA Average/Typical',
 'Fa Fair',
 'Po Poor'
 ],
'Central Air':[
 'N No',
 'Y Yes',
 ],
'Kitchen Qual':[
 'Ex Excellent',
 'Gd Good',
 'TA Typical/Average',
 'Fa Fair',
 'Po Poor',
 ],
'Garage Type':[
 '2Types More than one type of garage',
 'Attchd Attached to home',
 'Basment Basement Garage'
 'BuiltIn Built-In (Garage part of house - typically has room above garage)'
 'CarPort Car Port',
 'Detchd Detached from home',
 'NA No Garage'
 ],
'Garage Finish':[
 'Fin Finished',
 'RFn Rough Finished',
 'Unf Unfinished',
 'NA No Garage'
 ],
'Garage Qual':[
 'Ex Excellent',
 'Gd Good',
 'TA Typical/Average',
 'Fa Fair',
 'Po Poor',
 'NA No Garage'
 ]
    }

num = {         #min value, step, format
 'Gr Liv Area': [0, 1, "%i"],  
 'Lot Frontage': [0.0, 1.0, "%.3f"], 
 'Lot Area': [0, 1, "%i"], 
 'Year Built': [1864, 1, "%i"], 
 'Year Remod/Add': [1864, 1, "%i"], 
 'Total Bsmt SF': [0.0, 1.0, "%.3f"], 
 '2nd Flr SF': [0, 1, "%i"], 
 'Bsmt Full Bath': [0.0, 1.0, "%.3f"], 
 'Full Bath': [0, 1, "%i"], 
 'Half Bath': [0, 1, "%i"], 
 'Bedroom AbvGr': [0, 1, "%i"], 
 'TotRms AbvGrd': [0, 1, "%i"], 
 'Fireplaces': [0, 1, "%i"], 
 'Garage Area': [0.0, 1.0, "%.3f"], 
 'Wood Deck SF': [0, 1, "%i"], 
 'Open Porch SF': [0, 1, "%i"]
}

@st.cache_data
def load_expensive_data():
    with open('../data/X_test.pickle', 'rb') as f:
        x = pickle.load(f)
    with open('../data/y_test.pickle', 'rb') as f:
        y = pickle.load(f)
    with open('../models/clf_streamlit.pickle', 'rb') as f:
        clf = pickle.load(f) 
    with open('../models/mdl_streamlit.pickle', 'rb') as f:
        model = pickle.load(f)   
    return x, y, clf, model
    
x, y, clf, model = load_expensive_data()      

max_row = x.shape[0] - 1

line = st.slider("Select the object number from the test sample and click on the Update button", 
                    min_value=0, max_value=max_row, value=0, step=1)

def read_line(line): 
    
    x_row = x.iloc[line]

    for name in num:
        st.session_state[name] = x_row[name]

    for name in cat:
        x_ = str(x_row[name])
        items = cat[name]
        index = -1
        for i in range(len(items)):
            item = items[i]
            if x_ == item[ : item.find(' ')]:
                index = i
                break
        st.session_state[name] = index
    

if st.button('Update') or 'MS SubClass' not in st.session_state:
    read_line(line)


col1, col2, col3 = st.columns(3)

num_input = {}

with col1.container(border=True):
    st.subheader("Numerical attributes")
    for name in num:
        num_input[name] = st.number_input("Enter " + name + ":", 
#                        value=st.session_state[name], 
                        min_value = num[name][0],
                        step = num[name][1],
                        format = num[name][2],
                        key = name)    

cat_button = {}

with col2.container(border=True):
    st.subheader("Categorical attributes")
    for name in cat:
       
        cat_button[name] = st.selectbox("Select " + name + ":", cat[name])
                             #index = st.session_state[name]),
                         

with col3.container(border=True):
    st.subheader("Calculation results")
 
 
    if st.button("Estimate cost"):

        columns = list(num.keys()) + list(cat.keys())
        data = []
        for name in num:
            data.append(num_input[name])
        for name in cat:
            row = cat_button[name]
            #col3.write(name + ' ' + row)
            row = row[:row.find(' ')]
            if name in ordinal:
                data.append(int(row))
            else:
                data.append(row)

        X_test = pd.DataFrame(columns=columns,data=[data])
        
        #way = 'Pipeline'
        way = 'Soft Voting'

        y_class = clf.predict(X_test)
        probs = clf.predict_proba(X_test)
        probs = probs[0]
        y_pred = np.zeros(len(X_test))

        if way == 'Pipeline':
            x_row = X_test
            y_pred = model[y_class.item()].predict(x_row)[0]
        else:
            x_row = X_test
            pred0 = model[0].predict(x_row)[0]
            pred1 = model[1].predict(x_row)[0]
            pred2 = model[2].predict(x_row)[0]
            pred3 = model[3].predict(x_row)[0]
            y_pred = probs[0] * pred0 + probs[1] * pred1 + probs[2] * pred2 + probs[3] * pred3

        price = y_pred.item()
        st.write(f'Estimated cost: ${price*1000:,.0f}')
        
        df = pd.DataFrame({
        "Category": ["Economy", "Comfort", "Business", "Luxury"],
        "Probability": probs
        })

        # Создаём график
        fig = px.bar(df, x='Category', y="Probability", title="Probability of category membership")

        # Показываем в Streamlit
        st.plotly_chart(fig)
