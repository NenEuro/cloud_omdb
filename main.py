from flask import Flask, render_template, request
import json
from urllib.request import urlopen

app = Flask(__name__)

api_url="http://www.omdbapi.com/?t="
api_key="&apikey=insert_your_key"

def get_movie_details(details_in_json):
    parsed_json = json.loads(details_in_json)
    print(parsed_json)
    if 'Error' in parsed_json.keys():
        return [parsed_json['Error']],""
    result=[]
    result.append('Title: '+parsed_json['Title'])
    result.append('Year: '+parsed_json['Year'])
    ratings='Ratings: '
    for rating in parsed_json['Ratings']:
        ratings+=rating['Value']+'['+rating['Source']+']; '
    result.append(ratings)
    if 'Poster' in parsed_json.keys():
        poster_url=parsed_json['Poster']
    else:
        poster_url=""
    return result,poster_url

@app.route('/', methods=['GET','POST'])
def root():
    title, poster_url, errors, details = '', '', [], []
    if request.method == "POST":
        try:
            title = request.form['movie_title'].replace(" ", "+")
            with urlopen(api_url + str(title) + api_key) as res:
                res_tuple = get_movie_details(res.read())
                details = res_tuple[0]
                poster_url= res_tuple[1]
        except Exception as e:
            errors.append(
               str(e) 
            )
    return render_template('index.html', errors=errors, details=details, poster=poster_url)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
