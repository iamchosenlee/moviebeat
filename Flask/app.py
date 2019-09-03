from flask import Flask,render_template,request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_sqlalchemy import SQLAlchemy
from models import NVquote,NVmovie,REALQUOTES,Subtitle,Subtitles2
import pickle, json, re


app = Flask(__name__)
app.config.update(
    FLASKADMIN_SWATCH='cerulean',
    #위의것은 admin 꾸미는 거
    SQLALCHEMY_DATABASE_URI='sqlite:///FINAL_MOVIEBEAT_DB.db'
)


movie_list = list() # parse 한 영화 제목 모음. index 하나씩 더해야야함.
with open('mov_nospace','rb') as f:
    movie_list=pickle.load(f)

with open('action10_coord','rb')as f:
    action_10=pickle.load(f)
with open('comedy10_coord','rb')as f:
    comedy_10=pickle.load(f)
with open('adventure10_coord','rb')as f:
    adventure_10=pickle.load(f)
with open('animation10_coord','rb')as f:
    animation_10=pickle.load(f)
with open('crime10_coord','rb')as f:
    crime_10=pickle.load(f)
with open('drama10_coord','rb')as f:
    drama_10=pickle.load(f)
with open('fantasy10_coord','rb')as f:
   fantasy_10 = pickle.load(f)
with open('mystery10_coord','rb')as f:
    mystery_10=pickle.load(f)
with open('romance10_coord','rb')as f:
    romance_10=pickle.load(f)
with open('SF10_coord','rb')as f:
    SF_10=pickle.load(f)
with open('thriller10_coord','rb')as f:
   thriller_10=pickle.load(f)


movie_eng_list = list() # 자막 제목 영어 리스트
with open('title_eng','rb') as f:
    movie_eng_list = pickle.load(f)


#여기서부터 각 장르병 인덱스 리스트를 만들거임
#######################################
act_list=list()
with open('actionList','rb') as f:
    act_list = pickle.load(f)

adv_list=list()
with open('adventureList','rb') as f:
    adv_list = pickle.load(f)

ani_list=list()
with open('animationList','rb') as f:
    ani_list = pickle.load(f)

com_list=list()
with open('comedyList','rb') as f:
    com_list = pickle.load(f)

cri_list=list()
with open('crimeList','rb') as f:
    cri_list = pickle.load(f)

dra_list=list()
with open('dramaList','rb') as f:
    dra_list = pickle.load(f)

fan_list=list()
with open('fantasyList','rb') as f:
    fan_list = pickle.load(f)

mys_list=list()
with open('mysteryList','rb') as f:
    mys_list = pickle.load(f)

rom_list=list()
with open('romanceList','rb') as f:
    rom_list = pickle.load(f)

sf_list=list()
with open('SFList','rb') as f:
    sf_list = pickle.load(f)

thr_list=list()
with open('thrillerList','rb') as f:
    thr_list = pickle.load(f)
#
# act_list = tot_list[0]
# act_list = [i-1 for i in act_list]
# com_list = tot_list[1]
# com_list = [i-1 for i in com_list]
# dra_list = tot_list[2]
# dra_list = [i-1 for i in dra_list]
# mel_list = tot_list[3]
# mel_list = [i-1 for i in mel_list]
# thr_list = tot_list[4]
# thr_list = [i-1 for i in thr_list]
# sf_list = tot_list[5]
# sf_list = [i-1 for i in sf_list]
# fan_list = tot_list[6]
# fan_list = [i-1 for i in fan_list]
# ani_list = tot_list[7]
# ani_list = [i-1 for i in ani_list]
# adv_list = tot_list[8]
# adv_list = [i-1 for i in adv_list]
# mys_list = tot_list[9]
# mys_ist = [i-1 for i in mys_list]
# cri_list = tot_list[10]
# cri_list = [i-1 for i in cri_list]
#######################################

with open('action_graph','rb')as f:
    action_main=pickle.load(f)
with open('comedy_graph','rb')as f:
    comedy_main=pickle.load(f)
with open('adventure_graph','rb')as f:
    adventure_main=pickle.load(f)
with open('animation_graph','rb')as f:
    animation_main=pickle.load(f)
with open('crime_graph','rb')as f:
    crime_main=pickle.load(f)
with open('drama_graph','rb')as f:
    drama_main=pickle.load(f)
with open('fantasy_graph','rb')as f:
   fantasy_main = pickle.load(f)
with open('mystery_graph','rb')as f:
    mystery_main=pickle.load(f)
with open('romance_graph','rb')as f:
    romance_main=pickle.load(f)
with open('SF_graph','rb')as f:
    SF_main=pickle.load(f)
with open('thriller_graph','rb')as f:
   thriller_main=pickle.load(f)




def convertmili(millis): # Millisecond to minutes.second
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))%24
    return ("%d:%d:%d" % (hours, minutes, seconds))

def keyword_match(keyword,movie_list):
    keyword = keyword.lower()
    mov_index=list()
    keyword = keyword.replace(" ", "")
    for i,_ in enumerate(movie_list):
        if keyword in _:
            mov_index.append(i+1)
    return mov_index

db=SQLAlchemy(app)
admin=Admin(app,name="Example: Simple Views")

class Mymodelview(ModelView):#이거하면 create를 못하게 한다.
    can_delete=False
    create_modal = True
admin.add_view(Mymodelview(NVmovie, db.session))

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/result', methods=['GET','POST']) # 메인 페이지에서 => 검색한다음에 나오는 화면입니다.
def result():
    a = request.form.get('d', None) # form 에서 받아옴
    mov_index = keyword_match(a,movie_list) # movie_list 에서 매치 시킴'
    if len(mov_index)==0:
        mov_index =keyword_match(a,movie_eng_list)
    keyword_list = list()
    poster_list = list()
    release_list = list()
    genre_list = list()
    country_list = list()
    score_list = list()
    for _ in mov_index:
        keyword_list.append(NVmovie.query.filter_by(id=_).first().title_kor)
        poster_list.append(NVmovie.query.filter_by(id=_).first().poster)
        release_list.append(NVmovie.query.filter_by(id=_).first().opendate)
        genre_list.append(NVmovie.query.filter_by(id=_).first().genre)
        country_list.append(NVmovie.query.filter_by(id=_).first().country)
        score_list.append(NVmovie.query.filter_by(id=_).first().score_net)

    poster_size = re.compile('type.+')
    poster_list = [re.sub(poster_size,'',_) for _ in poster_list]

    return render_template('searchresult.html', keyword = a, keywordlist = keyword_list,
                            poster_list = poster_list, release_list = release_list,
                            genre_list = genre_list, country_list = country_list,
                            score_list = score_list, mov_index = mov_index
                           )

@app.route('/personal',methods=['GET','POST'])
def coding():
    id = request.args.get('mov_index')
    mov_index = int(id) # Movie index 가지고
    #########################

    title = NVmovie.query.filter_by(id=id).first().title_kor
    #타이틀 가지고오는 부분

    movie = NVmovie.query.filter_by(id=id).first()
    runtime = int(movie.runtime.replace("분", ''))
    #런타임 가지고옴
    try:
        realquote = REALQUOTES.query.filter_by(movie_key=movie.id).all()
        quotes_tuple = [(int(_.start_time), _.lines, _.g_index) for _ in realquote]
        quotes_tuple.sort(key=lambda element: element[0])
        # rate = [round(_[0] / (runtime * 6000), 2) * 10 for _ in quotes_tuple]
        quote = [_[1] for _ in quotes_tuple]
        g_index = [_[2] for _ in quotes_tuple]
        # datetime = [convertmili(_[0]) for _ in quotes_tuple]

        sub = Subtitle.query.filter_by(movie_key=movie.id).all()
        real_sub = [_.lines for _ in sub]

        if len(real_sub)==0:
            sub = Subtitles2.query.filter_by(movie_key=movie.id).all()
            real_sub = [_.lines for _ in sub]

        sub_tuple = [(int(_.start_time), _.lines) for _ in sub]
        rate = [round(_[0] / (runtime * 6000), 2) * 10 for _ in sub_tuple]
        datetime = [convertmili(_[0]) for _ in sub_tuple]

        new_gindex= list()
        testing_list = list()

        for i in real_sub:
            if i in quote:
                testing_list.append(i)
                new_gindex.append(g_index[quote.index(i)])
            else:
                new_gindex.append(0)

        count = 0
        for j in quote:
            if j not in testing_list:
                print(j)


        poster = NVmovie.query.filter_by(id=mov_index).first().poster
        poster_size = re.compile('type.+')
        poster = re.sub(poster_size, '', poster)
        #포스터 리스트 가지고오는부분

        summary = NVmovie.query.filter_by(id=mov_index).first().summary
        #줄거리 가지고옴

        score_net = NVmovie.query.filter_by(id=mov_index).first().score_net
        #평점 가지고옴

        genre = NVmovie.query.filter_by(id=mov_index).first().genre
        #장르 가지고옴

        len_quotes = NVmovie.query.filter_by(id=mov_index).first().len_quotes
        #대사 개수 가지고옴.

        backcolor_list = list()
        color_list = list()
        width_list = list()

        for i in new_gindex:
            if i == 0:
                color_list.append('transparent')
                width_list.append(0)
                backcolor_list.append('transparent')
            else:
                color_list.append('rgba(255, 66, 84, 0.7)')
                backcolor_list.append('rgba(255, 66, 84, 0.1)')
                width_list.append(1 )
        alert = len(real_sub)

        return render_template("personal.html",mov_title=title,poster = poster,summary=summary,
                               score_net=score_net,genre=genre,len_quotes = len_quotes,
                               quotes=real_sub,level=new_gindex, datetime=datetime,
                               time=rate,color_list=color_list,width_list=width_list,backcolor_list=backcolor_list,alert=alert)
    except:
        return render_template('index.html')
#1
@app.route('/action',methods=['GET','POST'])
def action():
    poster_list = list()
    name_list = list()

    for i in NVmovie.query.all():
        poster_list.append(i.poster)
        name_list.append(i.title_kor)

    poster_size = re.compile('type.+')
    poster_list = [re.sub(poster_size, '', _) for _ in poster_list]
    return render_template('action.html',act_list=act_list, name_list=name_list,poster_list=poster_list,action_main=action_main,action_10=action_10)

#2
@app.route('/adventure', methods=['GET', 'POST'])
def adventure():
    poster_list = list()
    name_list = list()

    for i in NVmovie.query.all():
        poster_list.append(i.poster)
        name_list.append(i.title_kor)

    poster_size = re.compile('type.+')
    poster_list = [re.sub(poster_size, '', _) for _ in poster_list]
    return render_template('adventure.html',adv_list=adv_list, name_list=name_list,poster_list=poster_list,adventure_main=adventure_main,adventure_10=adventure_10)
#3
@app.route('/animation', methods=['GET', 'POST'])
def animation():
    poster_list = list()
    name_list = list()

    for i in NVmovie.query.all():
        poster_list.append(i.poster)
        name_list.append(i.title_kor)

    poster_size = re.compile('type.+')
    poster_list = [re.sub(poster_size, '', _) for _ in poster_list]
    return render_template('animation.html',ani_list=ani_list, name_list=name_list,poster_list=poster_list,animation_main=animation_main,animation_10=animation_10)
#4
@app.route('/comedy', methods=['GET', 'POST'])
def comedy():
    poster_list = list()
    name_list = list()

    for i in NVmovie.query.all():
        poster_list.append(i.poster)
        name_list.append(i.title_kor)

    poster_size = re.compile('type.+')
    poster_list = [re.sub(poster_size, '', _) for _ in poster_list]
    return render_template('comedy.html',com_list=com_list, name_list=name_list,poster_list=poster_list,comedy_main=comedy_main,comedy_10=comedy_10)
#5
@app.route('/crime', methods=['GET', 'POST'])
def crime():
    poster_list = list()
    name_list = list()

    for i in NVmovie.query.all():
        poster_list.append(i.poster)
        name_list.append(i.title_kor)

    poster_size = re.compile('type.+')
    poster_list = [re.sub(poster_size, '', _) for _ in poster_list]
    return render_template('crime.html',cri_list=cri_list, name_list=name_list,poster_list=poster_list,crime_main=crime_main,crime_10=crime_10)
#6
@app.route('/drama', methods=['GET', 'POST'])
def drama():
    poster_list = list()
    name_list = list()

    for i in NVmovie.query.all():
        poster_list.append(i.poster)
        name_list.append(i.title_kor)

    poster_size = re.compile('type.+')
    poster_list = [re.sub(poster_size, '', _) for _ in poster_list]
    return render_template('drama.html',dra_list=dra_list, name_list=name_list,poster_list=poster_list,drama_main=drama_main,drama_10=drama_10)
#7
@app.route('/fantasy', methods=['GET', 'POST'])
def fantasy():
    poster_list = list()
    name_list = list()

    for i in NVmovie.query.all():
        poster_list.append(i.poster)
        name_list.append(i.title_kor)

    poster_size = re.compile('type.+')
    poster_list = [re.sub(poster_size, '', _) for _ in poster_list]
    return render_template('fantasy.html',fan_list=fan_list, name_list=name_list,poster_list=poster_list,fantasy_main=fantasy_main,fantasy_10=fantasy_10)
#8
@app.route('/mystery', methods=['GET', 'POST'])
def mystery():
    poster_list = list()
    name_list = list()

    for i in NVmovie.query.all():
        poster_list.append(i.poster)
        name_list.append(i.title_kor)

    poster_size = re.compile('type.+')
    poster_list = [re.sub(poster_size, '', _) for _ in poster_list]
    return render_template('mystery.html',mys_list=mys_list, name_list=name_list,poster_list=poster_list,mystery_main=mystery_main,mystery_10=mystery_10)
#9
@app.route('/romance', methods=['GET', 'POST'])
def romance():
    poster_list = list()
    name_list = list()

    for i in NVmovie.query.all():
        poster_list.append(i.poster)
        name_list.append(i.title_kor)

    poster_size = re.compile('type.+')
    poster_list = [re.sub(poster_size, '', _) for _ in poster_list]
    return render_template('romance.html',rom_list=rom_list, name_list=name_list,poster_list=poster_list,romance_main=romance_main,romance_10=romance_10)
#10
@app.route('/sf', methods=['GET', 'POST'])
def sf():
    poster_list = list()
    name_list = list()

    for i in NVmovie.query.all():
        poster_list.append(i.poster)
        name_list.append(i.title_kor)

    poster_size = re.compile('type.+')
    poster_list = [re.sub(poster_size, '', _) for _ in poster_list]
    return render_template('sf.html',sf_list=sf_list, name_list=name_list,poster_list=poster_list,SF_main=SF_main,SF_10=SF_10)
#11
@app.route('/thriller', methods=['GET', 'POST'])
def thriller():
    poster_list = list()
    name_list = list()

    for i in NVmovie.query.all():
        poster_list.append(i.poster)
        name_list.append(i.title_kor)

    poster_size = re.compile('type.+')
    poster_list = [re.sub(poster_size, '', _) for _ in poster_list]
    return render_template('thriller.html',thr_list=thr_list, name_list=name_list,poster_list=poster_list,thriller_main=thriller_main,thriller_10=thriller_10)


@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

if __name__ == '__main__':
    app.run()