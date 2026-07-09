from flask import Flask, render_template, request, redirect, session, url_for
app=Flask(__name__)
app.secret_key="supersecretkey"
artworks={
    1:{"name":"Dissolving Dream","price":1800,"image":"art1.jpg","artist":"Gill Bustamante","medium":"Oil"},
    2:{"name":"Daisy flowers - misty yellow","price":100,"image":"art2.jpg","artist":"Carol Ann Wood","medium":"Oil"},
    3:{"name":"Cockburn Street, Edinburgh Street","price":325,"image":"art3.jpg","artist":"Darren Carey","medium":"Watercolours"},
    4:{"name":"Austrian Winter", "price":225,"image":"art4.jpg","artist":"Darren Carey","medium":"Watercolours"},
    5:{"name":"Dissolving Dream","price":1800,"image":"art5.jpg","artist":"Gill Bustamante","medium":"Oil"},
    6:{"name":"Molten Sky","price":540,"image":"art6.jpg","artist":"Serguei Borodouline","medium":"Oil"},
    7:{"name":"Melancholy","price":490,"image":"art7.jpg","artist":"Serguei Borodouline","medium":"Oil"},
    8:{"name":"A Storm Brewing","price":550,"image":"art8.jpg","artist":"Anthony Edwards","medium":"Acrylic"},
    9:{"name":"The Grand Venice 2025","price":495,"image":"art9.jpg","artist":"Lesley Blackburn","medium":"Oil"},
    10:{"name":"Mimicry VI","price":1130,"image":"art10.jpg","artist":"Sonja Brzak","medium":"Oil"},
    11:{"name":"MELT WATER","price":290,"image":"art11.jpg","artist":"Serguei Borodouline","medium":"Oil"},
    12:{"name":"Sunset on the Ice","price":449,"image":"art12.jpg","artist":"Eugenia Gorbacheva","medium":"Watercolours"},
    13:{"name":"Romantic Evening Lake L 1","price":2180,"image":"art13.jpg","artist":"Peter Nottrott","medium":"Acrylic"},
    14:{"name":"Framed Colourful Flowers 1","price":100,"image":"art14.jpg","artist":"Carol Ann Wood"},
    15:{"name":"The Dolce Vita Life","price":10900,"image":"art15.jpg","artist":"Serguei Borodouline","medium":"Oil"},
    16:{"name":"Seaside Rendezvous","price":1390,"image":"art16.jpg","artist":"Peter Nottrott","medium":"Acrylic"},
    17:{"name":"March Breath","price":540,"image":"art17.jpg","artist":"Serguei Borodouline","medium":"Mixed Media"},
    18:{"name":"Apple Gin","price":100,"image":"art18.jpg","artist":"Fioana J Rose","medium":"Oil"},
    19:{"name":"Under the Veil","price":3300,"image":"art19.jpg","artist":"Simona Nedeva","medium":"Oil"},
    20:{"name":"Mexican Sunrise","price":700,"image":"art20.jpg","artist":"Faye Bardo","medium":"Oil"},
    21:{"name":"March Eve","price":390,"image":"art21.jpg","artist":"Serguei Borodouline","medium":"Acrylic"},
    22:{"name":"March","price":400,"image":"art22.jpg","artist":"Serguei Borodouline","medium":"Oil"},
    23:{"name":"PRIDE","price":980,"image":"art23.jpg","artist":"Emilia Milcheva","medium":"Oil"},
    24:{"name":"Four Stones, Four Stories","price":389,"image":"art24.jpg","artist":"Dharmishta Patel","medium":"Watercolours"},
    25:{"name":"Healing","price":340,"image":"art25.jpg","artist":"Christina Floricel"},
    26:{"name":"Red Energy L 8","price":1990,"image":"art26.jpg","artist":"Peter Nottrott"},
    27:{"name":"View From the Rocks","price":175,"image":"art27.jpg","artist":"Melanie Graham","medium":"Acrylic"},
}
def is_valid_password(password):
    if len(password)<8:
        return False
    has_upper=has_lower=has_digit=has_special=False
    for char in password:
        if char.isupper():
            has_upper=True
        elif char.islower():
            has_lower=True
        elif char.isdigit():
            has_digit=True
        elif not char.isalnum():
            has_special=True
    return has_upper and has_lower and has_digit and has_special

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html",artworks=artworks)

@app.route("/detail/<int:art_id>")
def detail(art_id):
    art=artworks.get(art_id)
    if art:
        return render_template("details.html",art=art)
    return "Artwork not found"

@app.route("/register",methods=["GET","POST"])
def register():
    message=''''''
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        if not is_valid_password(password):
            message=("Password must be at least 8 characters long and contain uppercase,lowercase,digit, and special character.")
        else:
            with open("users.txt","a") as f:
                f.write(f"{username},{password}\n")
            message="Registration Successful! You can now log in."
    return render_template("register.html",message=message)
    
@app.route("/login", methods=["GET","POST"])
def login():
    message=''''''
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        found=False
        try:
            with open("users.txt","r") as f:
             for line in f:
                saved_user,saved_pass=line.strip().split(",")
                if username==saved_user and password==saved_pass:
                    found=True
                    break
        except FileNotFoundError:
            pass
        if found:
            session["username"]=username
            message=f"Welcome, {username}!"
            return redirect(url_for("gallery"))
        else:
            message="invalid username or password."
    return render_template("login.html",message=message)
    
@app.route("/add_to_cart/<int:art_id>",methods=["POST"])
def add_to_cart(art_id):
    if "cart" not in session:
        session["cart"]=[]
    art=artworks.get(art_id)
    if art:
        session["cart"].append(art)
        session.modified=True
    return redirect(url_for("gallery"))

@app.route("/cart")
def view_cart():
    cart=session.get("cart",[])
    total=sum(item["price"] for item in cart)
    return render_template("cart.html",cart=cart,total=total)

@app.route("/remove_from_cart/<int:index>")
def remove_from_cart(index):
    cart=session.get("cart",[])
    if 0<= index< len(cart):
        cart.pop(index)
        session.modified=True
    return redirect(url_for("view_cart"))

@app.route("/place_order",methods=["POST"])
def place_order():
    name=request.form["fullname"]
    address=request.form["address"]
    contact=request.form["contact"]
    cart=session.get("cart",[])
    total=sum(item["price"] for item in cart)
    if cart:
        with open("orders.txt","a") as file:
            file.write(f"{name} | {address} | {contact} | Total: {total}\n")
            for item in cart:
                file.write(f"- {item['name']}: Rs {item['price']}\n")
            file.write("----------------------------------\n")
        session.pop("cart",None)
    return render_template("success.html",name=name,total=total)

if __name__=="__main__":
    app.run(debug=True)
