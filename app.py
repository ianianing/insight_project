import numpy as np
from flask import Flask, request, render_template
import pickle
import pandas as pd
from scipy.spatial import distance

app = Flask(__name__)
sneaker = pickle.load(open('/home/ianyin/桌面/Insight_Project/sneaker.pkl', 'rb'))

######################routes#################################################################

@app.route('/')
def sneaker_invest():
    return render_template('sneaker_invest.html')

@app.route('/sneaker',methods=['POST'])
def sneaker_predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [x for x in request.form.values()]
    final_features = [np.array(int_features)]

    #predicted result
    prediction = sneaker.predict(final_features)
    prob = sneaker.predict_proba(final_features)
    prob1 = prob[0][1]
    prob0 = prob[0][0]

    if prediction ==1:
        output = "THIS SNEAKER IS A PRPOFITABLE 1 MONTH INVESTMENT, LET'S MAKE SOME $$$ ({0:.0%} Chance) ".format(prob1)
    else:
        output = "THIS SNEAKER IS NOT PROFITABLE 1 MONTH INVESTMENT. DONT INVEST! ({0:.0%} Chance)".format(prob0)

    df = pd.read_csv('/home/ianyin/PycharmProjects/Flask_Blog/flaskblog/ml/combine.csv').drop('Unnamed: 0', axis=1)
    #convert input from string to float
    lst = [float(i) for i in int_features]
    # define function to find closest sneaker

    def closestSneaker(aList):
        model = aList[0]
        size = aList[-1]

        # dataset with matching shoe model and size
        select = df[(df['model_encode'] == model) & (df['size'] == size)]
        select = select.sort_values(by='release_date', ascending=False).reset_index(drop=True)
        select['distance'] = np.nan

        # calculate distance for selected feaure
        feature_select = ['collab', 'classic', 'limited_release', 'GS']
        df_fs = select[feature_select]
        b = aList[1:5]

        # calculate all euclidean distance
        for i in range(len(select)):
            a = df_fs.loc[i].values
            dst = distance.euclidean(a, b)
            select.loc[i, 'distance'] = dst

        # find closest sneaker
        closest_index = select['distance'].idxmin()
        closest_sneaker = select.iloc[closest_index]

        name_closest = closest_sneaker['name']
        link_closest = closest_sneaker['link']
        image_closest = closest_sneaker['image']
        return1month_closest = closest_sneaker['return_1month']

        return (name_closest, link_closest, image_closest, return1month_closest)

    # get closest sneaker
    name,link,image,return1month= closestSneaker(lst)
    return1month = "1 Month Return: ({0:.0%})".format(return1month)

    return render_template('back.html', prediction_text='{}'.format(output),closest_sneaker='{}'.format(name),
                           image_closest='{}'.format(image),link_closest='{}'.format(link),return_1month='{}'.format(return1month))


if __name__ == "__main__":
    app.run(debug=True)