from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, Column
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from datetime import timedelta
from flask_mail import Mail, Message


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Setting the configuration options for the SQLAlchemy instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Lamsaa.db')
app.config['JWT_SECRET_KEY'] = 'top-secret'
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '1800fa5aa0c9b3'
app.config['MAIL_PASSWORD'] = '8923ce288e5626'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Creating a SQLAlchemy instance
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)


# CREATING THE DATABASE
@app.cli.command('db_creation')
def db_creation():
    db.create_all()
    print('database is created')


@app.cli.command('db_dropping')
def db_dropping():
    db.drop_all()
    print('database dropped')

# SEEDING THE DATABASE
@app.cli.command('db_seeding')
def db_seeding():
    client1 = Client(contact_name='Mohamed Ali lasmer', client_email='alilasmer@gmail.com',
                     client_password='medali123000',
                     phone_number='21456987', address='la marsa sidi daoued ')
    client2 = Client(contact_name='nada dalai', client_email='nadadalai@gmail.com', client_password='dalai923000',
                     phone_number='91785623',
                     address='Mourouj 6')
    client3 = Client(contact_name='Amine litim', client_email='aminelitim@gmail.com', client_password='aminefejfej00',
                     phone_number='91799712',
                     address='tatouine')

    db.session.add(client1)
    db.session.add(client2)
    db.session.add(client3)

    # Create some Seller instances and add them to the database
    seller1 = Seller(name='jalila ben yeder', seller_email='jalilabydr@gmail.com', seller_password='jalila123456',
                     seller_phone_number='92793826',
                     seller_address='gafsa redaif',
                     description='I sell handmade Tunisian carpets and pillows inspired from the amazigh culture',
                     number_of_products=20)
    seller2 = Seller(name='soltana ferjani', seller_email='soltanaferjani@gmail.com', seller_password='soltana789123',
                     seller_phone_number='99874521',
                     seller_address='nabeul mrezga',
                     description='I sell handmade aesthetic home items inspired from nabeul culture ',
                     number_of_products=15)
    seller3 = Seller(name='Ayoubbelarbi', seller_email='ayoubbelarbi@gmail.com', seller_password='belaarbibinflow124',
                     seller_phone_number='21445233',
                     seller_address='douz tunisia',
                     description='I sell handmade sewed baskets ', number_of_products=23)

    db.session.add(seller1)
    db.session.add(seller2)
    db.session.add(seller3)

    # Create some Product instances and add them to the database
    product1 = Product(name='Margoum', price=50.0,
                       description='This is a handmade craft margoum inspired by amazigh culture ',
                       size='Medium', weight=1.5, condition='new',
                       image_url='https://www.google.com/search?q=margoum&rlz=1C1CHBF_frTN954TN954&sxsrf=ALiCzsYb9eqQYTtdEJYOW0XHKnsMud9hpg:1671839911329&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiG0qSA-ZD8AhVuU6QEHR85AB8Q_AUoAXoECAEQAw&biw=1536&bih=664&dpr=1.25#imgrc=cNbR9U8CW1a0dM',
                       category='crafts')
    product2 = Product(name='olive wooden candle holder', price=30.0,
                       description='This a good quality olive wooden candle holder crafted by tunisian artisan',
                       size='medium', weight=0.5, condition='new',
                       image_url='https://atelierauboiszen.fr/en/products/lot-3-porte-bougies-en-bois-dolivier',
                       category='olive wood')
    product3 = Product(name='handmade basket', price=25.0,
                       description='This a good quality handmade basket for your kids toys',
                       size='medium', weight=0.2, condition='new',
                       image_url='https://www.urbankissed.com/all-categories/living-and-gifts/homeware/storage-boxes-and-baskets-en/sisal-basket-practical-weave-sunshine/',
                       category='baskets')

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)

    # Create some Review instances and add them to the database
    review1 = Review(reviewer_name='amine ferjani', review_text='This is a great product!',
                     rating=5.0)
    review2 = Review(reviewer_name='Eya briki',
                     review_text='I love this product , such a very good quality!', rating=4.5)
    review3 = Review(reviewer_name='montassar ben massoud',
                     review_text='it is a good quality product but I did not like much the color ', rating=3)

    db.session.add(review1)
    db.session.add(review2)
    db.session.add(review3)
    db.session.commit()
    print('database seeded')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/first_msg')
def first_msg():
    return jsonify(message='welcome lamsa marketplace clients.'), 200


@app.route('/handle_not_found')
def handle_not_found():
    return jsonify(message='error not found , we could not find this resource'), 404


@app.route('/URL_parameters')
def URL_parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 14:
        return jsonify(message="sorry " + name + ", you are not allowed to sell or buy"), 401
    else:
        return jsonify(message="welcome to lamsa marketplace" + name + ", you can sell or buy")

#CRUD Endpoints and Methods
@app.route('/products', methods=['GET'])
def products():
    products_list = Product.query.all()
    result = products_schema.dump(products_list)
    return jsonify(result)


@app.route('/registration', methods=['POST'])
def registration():
    seller_email = request.form['seller_email']
    test = Seller.query.filter_by(seller_email=seller_email).first()
    if test:
        return jsonify(message='the email already exist!!!'), 409
    else:
        name = request.form['name']
        seller_password = request.form['seller_password']
        seller_phone_number = request.form['seller_phone_number']
        seller_address = request.form['seller_address']
        description = request.form['description']
        number_of_products = request.form['number_of_products']
        seller = Seller(name=name, seller_email=seller_email, seller_password=seller_password,
                        seller_phone_number=seller_phone_number, seller_address=seller_address, description=description,
                        number_of_products=number_of_products)
        db.session.add(seller)
        db.session.commit()
        return jsonify(message="User is successfully created."), 201


@app.route('/registration_client', methods=['POST'])
def registration_client():
    client_email = request.form['client_email']
    test = Client.query.filter_by(client_email=client_email).first()
    if test:
        return jsonify(message='the email already exist!!!'), 409
    else:
        contact_name = request.form['contact_name']
        client_password = request.form['client_password']
        phone_number = request.form['phone_number']
        address = request.form['address']
        client = Client(contact_name=contact_name, client_email=client_email, client_password=client_password,
                        phone_number=phone_number, address=address)
        db.session.add(client)
        db.session.commit()
        return jsonify(message="Client is successfully created."), 201


@app.route('/login_seller', methods=['POST'])
def login_seller():
    if request.is_json:
        seller_email = request.json['seller_email']
        seller_password = request.json['seller_password']
    else:
        seller_email = request.form['seller_email']
        seller_password = request.form['seller_password']

    test = Seller.query.filter_by(seller_email=seller_email, seller_password=seller_password).first()
    if test:
        # Set the expiration time to 30 minutes
        expires = timedelta(minutes=30)
        access_token = create_access_token(identity=seller_email, expires_delta=expires)
        return jsonify(message="login done successfully", access_token=access_token, expires_in=expires.total_seconds())
    else:
        return jsonify(message="wrong email or password please enter the correct ones"), 401


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        client_email = request.json['client_email']
        client_password = request.json['client_password']
    else:
        client_email = request.form['client_email']
        client_password = request.form['client_password']

    test = Client.query.filter_by(client_email=client_email, client_password=client_password).first()
    if test:
        # Set the expiration time to 30 minutes
        expires = timedelta(minutes=30)
        access_token = create_access_token(identity=client_email, expires_delta=expires)
        return jsonify(message="login done successfully dear client", access_token=access_token,
                       expires_in=expires.total_seconds())
    else:
        return jsonify(message="wrong email or password please enter the correct ones")


@app.route('/retrieving_password/<string:seller_email>', methods=['GET'])
def retrieving_password(seller_email: str):
    seller = Seller.query.filter_by(seller_email=seller_email).first()
    if seller:
        message = Message("your password is" + seller.seller_password,
                          sender="mohamedaminferjani923@gmail.com",
                          recipients=[seller_email])
        mail.send(message)
        return jsonify(message="password is sent to " + seller_email)
    else:
        return jsonify(message="this email does not exist sorry !!")



@app.route('/product_details/<int:product_id>', methods=["GET"])
def product_details(product_id: int):
    product = Product.query.filter_by(product_id=product_id).first()
    if product:
        result = product_schema.dump(product)
        return jsonify(result)
    else:
        return jsonify(message="This product does not exist we are sorrry"), 404


@app.route('/adding_product', methods=['POST'])
@jwt_required()
def adding_product():
    name = request.form['name']
    test = Product.query.filter_by(name=name).first()
    if test:
        return jsonify(message="there exist a product by this name ! "), 409
    else:
        price = request.form['price']
        description = request.form['description']
        size = request.form['size']
        weight = request.form['weight ']
        condition = request.form['condition']
        image_url = request.form['image_url']
        category = request.form['category']

        new_product = Product(name=name, price=price, description=description, size=size, weight=weight,
                              condition=condition, image_url=image_url, category=category)
        db.session.add(new_product)
        db.session.commit()
        return jsonify(message=" a new product successfully added"), 201


@app.route('/updating_product', methods=['PUT'])
@jwt_required()
def updating_product():
    product_id = int(request.form['product_id'])
    product = Product.query.filter_by(product_id=product_id).first()
    if product:
        product.name = request.form['name']
        product.price = request.form['price']
        product.description = request.form['description']
        product.size = request.form['size']
        product.weight = request.form['weight']
        product.condition = request.form['condition']
        product.image_url = request.form['image_url']
        product.category = request.form['category']
        db.session.commit()
        return jsonify(message='product successfully updated'), 202
    else:
        return jsonify(message='the product you are trying to update does not exist'), 404


@app.route('/remove_product/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_product(product_id: int):
    product = Product.query.filter_by(product_id=product_id).first()
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify(message=" product has been successfully deleted"), 202
    else:
        return jsonify(message="this product does not exit sorry"), 404


# database models
class Client(db.Model):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    contact_name = Column(String(255))
    client_email = Column(String(255), nullable=False)
    client_password = Column(String(225))
    phone_number = Column(String(255))
    address = Column(String(255))


class Seller(db.Model):
    __tablename__ = 'sellers'
    seller_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    seller_email = Column(String(255), nullable=False)
    seller_password = Column(String)
    seller_phone_number = Column(String(255))
    seller_address = Column(String(255))
    description = Column(String(255))
    number_of_products = Column(Integer)


class Product(db.Model):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(255))
    size = Column(String(255))
    weight = Column(Float)
    condition = Column(String(255))
    image_url = Column(String(255))
    category = Column(String(255))


class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = Column(Integer, primary_key=True)
    reviewer_name = Column(String(255), nullable=False)
    review_text = Column(String(255), nullable=False)
    rating = Column(Float, nullable=False)


class ClientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'contact_name', 'email', 'phone_number', 'address')


class SellerSchema(ma.Schema):
    class Meta:
        fields = ('seller_id', 'name', 'email', 'phone_number', 'address', 'description', 'number_of_products')


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('product_id', 'name', 'price', 'description', 'size', 'weight', 'condition', 'image_url', 'category')
        fields = ('product_id', 'name', 'price', 'description', 'size', 'weight', 'condition', 'image_url', 'category')


class ReviewSchema(ma.Schema):
    class Meta:
        fields = ('review_id', 'reviewer_name', 'review_text', 'rating')


client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

seller_schema = SellerSchema()
sellers_schema = SellerSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

if __name__ == '__main__':
    app.run()
