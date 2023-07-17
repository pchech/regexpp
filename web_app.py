from flask import Flask,request
from flask_cors import CORS
import pymorphy2
import re
app = Flask(__name__)
cors = CORS(app, resources={r"/makeRegexp": {"origins": ""}})


@app.route('/makeRegexp',methods=['POST'])
def reqMakeRegexp():
    #keywords = request.form.get('keywords')
    request_data = request.get_json()
    return makeRegxp(request_data['keywords'])


def makeRegxp(str_to_convert):
    #print(str_to_convert)
    no_moprh = re.compile("'.*'")
    morph = pymorphy2.MorphAnalyzer()
    try:
        total = []
        for part in str_to_convert.split("|"):
            reg = []
            for tok in part.strip().split(" "):
                rezl = []
                rez = ""
                if not no_moprh.match(tok):
                    # print(tok)
                    p = morph.parse(tok)[0]     
                    gen = ""
                    for pi in p.lexeme:
                        # print(pi)
                        if pi.word == tok.lower():
                            gen = pi.tag.gender
                    for pi in p.lexeme:
                        if (pi.tag.gender == gen or pi.tag.number == "plur") and pi.word not in rezl:
                            # print(pi.tag.gender)
                            rezl.append(pi.word)
                            # rez=rez+"|"+pi.word
                else:
                    rezl.append(tok.replace("'",""))
                rez = "\\b(" + '|'.join(rezl) + ")\\b"
                reg.append(rez)
                # print(rez)
            total.append("(" + " ".join(reg) + ")")
        #print("|".join(total))
        return "|".join(total)
    except:
        #print(str_to_convert)
        return "|".join(total)


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)