from __init__ import Session
from category import Category
from users import User
from games import Game 
from cart import Cart 
from __init__ import Base
from datetime import datetime
from sqlalchemy.exc import IntegrityError





import os 
from flask import Flask,render_template, request,redirect, url_for,flash,session



app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))
app.secret_key = 'ovo-je-moj-tajni-kljuc'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route("/")
def index ():
    return render_template('register.html') 


@app.route('/register', methods=['POST'])
def register_user():
    
    ime = request.form['ime']
    prezime = request.form['prezime']
    email = request.form['email']
    password = request.form['lozinka']
    
    user = User(ime=ime, prezime=prezime, email=email, password=password)
    Session.add(user)
    Session.commit()

    flash('Registracija uspjesna. ', 'success')
    return redirect(url_for('login'))



@app.route("/login")
def login ():
    return render_template('login.html')



@app.route('/loguser', methods=['GET', 'POST'])
def log_user():
   
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Session.query(User).filter_by(email=email, password=password).first()
       
        if user:
            session['user_name'] = user.ime
            session['user_id'] = user.ID_user
           
            return redirect(url_for('game'))
        else:
            flash('Pogrešan e-mail ili lozinka. Molimo pokušajte ponovno.', 'danger')
            return redirect(url_for('login'))
        
@app.route("/game")
def game ():
    user_id = session['user_id']  
    categories = Session.query(Category).all()
    games = Session.query(Game).all()
    users = Session.query(User).all()
    igre_u_kosarici = Session.query(Cart).filter_by(user_id=user_id).all()
    count_cart = len(igre_u_kosarici)
    return render_template('game.html', categories=categories, games=games,users=users,broj=count_cart)


@app.route('/logout')
def logout():
    
    session.pop('user_name', None)
   
    return redirect(url_for('login'))


@app.route("/categories")
def categories ():
    users = Session.query(User).all()
    user_id = session['user_id']  
    categories = Session.query(Category).all()
    igre_u_kosarici = Session.query(Cart).filter_by(user_id=user_id).all()
    count_cart = len(igre_u_kosarici)
    return render_template('categories.html', categories = categories,broj=count_cart, users=users)

@app.route('/dodaj-kategoriju', methods=['POST'])
def add_category():
    
    user_id = session['user_id']
    ime = request.form['ime']
    
    
    category = Category(ime=ime, user_id=user_id)
    Session.add(category)
    Session.commit()

   
    return redirect(url_for('categories'))



@app.route('/izbrisi_kategoriju/<int:ID_category>', methods=['POST'])
def izbrisi_kategoriju(ID_category):
    category = Session.query(Category).get(ID_category)
    
    Session.delete(category)
    Session.commit()  
        
    return redirect(url_for('categories'))
    



@app.route('/dodaj-igru', methods=['POST'])
def add_game():
    
    user_id = session['user_id']
    ime = request.form['ime']
    opis = request.form['opis']
    category_id = request.form['category_id']
    cijena = request.form['cijena']
    
    
    
    game = Game(ime=ime, user_id=user_id, opis=opis,category_id=category_id,cijena=cijena)
    Session.add(game)
    Session.commit()

   
    return redirect(url_for('game'))


@app.route('/izbrisi_igru/<int:ID_game>', methods=['POST'])
def izbrisi_igru(ID_game):
    game = Session.query(Game).get(ID_game)
    
    Session.delete(game)
    Session.commit()  
        
    return redirect(url_for('game'))
    

@app.route('/uredi_igru/<int:ID_game>')
def uredi_igru(ID_game):
    user_id = session['user_id']
    games = Session.query(Game).get(ID_game)
    categories = Session.query(Category).all()
    igre_u_kosarici = Session.query(Cart).filter_by(user_id=user_id).all()
    count_cart = len(igre_u_kosarici)
    return render_template('uredi_igru.html', games=games, categories=categories,broj=count_cart) 

@app.route('/update_igru/<int:ID_game>', methods=['POST'])
def update_igru(ID_game):
    game = Session.query(Game).get(ID_game)
    if game:
        
        game.ime = request.form.get('ime')
        game.opis = request.form.get('opis')
        game.cijena = request.form.get('cijena')
        game.category_id = request.form.get('category_id')
      
        Session.commit()
  
    return redirect(url_for('game'))


@app.route('/add_cart/<int:ID_game>', methods=['POST'])
def add_cart(ID_game):
    
    user_id = session['user_id']
    postoji = Session.query(Cart).filter_by(game_id=ID_game, user_id=user_id).first()
    if postoji:
        flash('Ne mozete dodati dva puta istu igru u kosaricu. ', 'danger')
        return redirect(url_for('game'))
    else:
        user_id = session['user_id']
        cart = Cart(game_id=ID_game, user_id=user_id)
        Session.add(cart)
        Session.commit()
    
    
    return redirect(url_for('game'))


@app.route("/cart")
def cart():
    game = Session.query(Game).all()
    user = Session.query(User).all()
    categories = Session.query(Category).all()
    user_id = session['user_id']   
    igre_u_kosarici = Session.query(Cart).filter_by(user_id=user_id).all()
    count_cart = len(igre_u_kosarici)
    return render_template('cart.html', cart=igre_u_kosarici, broj = count_cart,games=game, users=user,categories=categories)


@app.route('/remove_cart/<int:ID_cart>', methods=['POST'])
def remove_cart(ID_cart):
    cart = Session.query(Cart).get(ID_cart)
    
    Session.delete(cart)
    Session.commit()  
        
    return redirect(url_for('cart'))

@app.route("/search_game", methods=["GET"])
def search_game():
   
    user_id = session['user_id']   
    game_name = request.args.get("game_name")
    
    igre_u_kosarici = Session.query(Cart).filter_by(user_id=user_id).all()
    count_cart = len(igre_u_kosarici)
  
    games = Session.query(Game).filter(Game.ime.ilike(f"%{game_name}%")).all()

   
    return render_template("search.html", games=games, broj=count_cart)

app.debug = True

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=5000)