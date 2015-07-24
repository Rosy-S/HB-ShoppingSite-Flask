"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, url_for, escape, request
import jinja2

import model




app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = '1234abcdlkashfl'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melons = model.Melon.get_all()
    return render_template("all_melons.html",
                           melon_list=melons)


@app.route("/melon/<int:id>")
def show_melon(id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = model.Melon.get_by_id(id)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.
    #   - The cart is a list in session containing melons added

    melons = {}
    for value in session['cart']:     
        new_melon = model.Melon.get_by_id(value)
        print new_melon
        print melons
        if new_melon in melons: 
            melons[new_melon] += 1
        else: 
            print "KLSDNKLBSDLJBS"
            melons[new_melon] = 1

    melon_price = model.Melon.get_by_id(value)

    return render_template('cart.html',
                            melons=melons,
                            quantity=melons[new_melon],
                            price=melon_price)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    # TODO: Finish shopping cart functionality
    #   - use session variables to hold cart list

    if session.get('cart', None) == None:
        our_melon = model.Melon.get_by_id(id)
        session['cart'] = {id: our_melon.price, 'qty': 1}
    else: 
        session['cart'].append(id)
    print "**********************************"
    print session
    print "**********************************"
    return redirect('/cart')

@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    username = request.form.get("email")
    password = request.form.get("password")
    session['username'] = username
    return session['username']


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
