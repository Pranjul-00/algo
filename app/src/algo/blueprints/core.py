from flask import Blueprint, render_template, request, flash, redirect, url_for

bp = Blueprint('core', __name__)

@bp.route('/')
def home():
    """Renders the main landing page."""
    return render_template('home.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Forward to auth.login for both GET and POST."""
    from algo.blueprints.auth import login as auth_login
    return auth_login()

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Forward to auth.register for both GET and POST."""
    from algo.blueprints.auth import register as auth_register
    return auth_register()

@bp.route('/about')
def about():
    """Renders the about us page."""
    return render_template('about.html')

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Render the contact page and handle form submission"""
    if request.method == 'POST':
        # Logic to handle contact form submission will be moved here
        flash('Thank you for your message. We will get back to you shortly.', 'success')
        return redirect(url_for('core.contact'))
    return render_template('contact.html')

@bp.route("/thanks", methods=["GET", "POST"])
def thanks():
    if request.method == "POST":
        return redirect(url_for("core.home"))
    return render_template("thanks.html")

@bp.route("/recommendations")
def recommendations():
    return render_template("recommendations.html")
