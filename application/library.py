"""
    Logged-in pages :
                index
                library
                add_dvd
                add_mag
                borrow_dvd
                borrow_mag
                return_dvd
                return_mag
                lent_list
                borrowed_list
                rules
                changes
"""
from datetime import datetime

from flask import current_app as app
from flask import url_for, render_template, redirect, request
from flask_login import current_user
from flask_login import login_required

from application.forms import AddDvdForm, AddMagForm, SearchForm
from application.functions import search_func
from application.models import DVD, Magazine, db
from application.tables import DVD_table, Mag_table


@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("library"))
    return render_template("index.html")


@app.route("/library", methods=["GET", "POST"])
@login_required
def library():

    search = SearchForm()
    if request.method == "POST":
        return search_func(search)

    dvd_items = DVD.query.order_by(DVD.title).all()
    dvd_table = DVD_table(dvd_items)
    dvd_table.border = True
    mag_items = Magazine.query.order_by(Magazine.title).all()
    mag_table = Mag_table(mag_items)
    mag_table.border = True

    return render_template(
        "list.html", mag_table=mag_table, dvd_table=dvd_table, search=search
    )


@app.route("/add_dvd", methods=["GET", "POST"])
@login_required
def add_dvd():

    dvd_items = DVD.query.filter_by(owner_id=current_user.id).order_by(DVD.title).all()
    dvd_table = DVD_table(dvd_items)
    dvd_table.border = True

    form = AddDvdForm()

    if request.method == "POST":
        if form.validate_on_submit():
            dvd = DVD(
                title=form.title.data,
                rating=form.rating.data,
                format_dvd=form.format_dvd.data,
                format_bluray=form.format_bluray.data,
                format_4k=form.format_4k.data,
                owner_id=current_user.id,
                owner_name=current_user.name,
            )
            db.session.add(dvd)
            db.session.commit()
            return redirect(url_for("add_dvd"))

    return render_template("add_dvd.html", form=form, table=dvd_table)


@app.route("/add_mag", methods=["GET", "POST"])
@login_required
def add_mag():

    mag_items = (
        Magazine.query.filter_by(owner_id=current_user.id)
        .order_by(Magazine.title)
        .all()
    )
    mag_table = Mag_table(mag_items)
    mag_table.border = True

    form = AddMagForm()

    if request.method == "POST":
        if form.submit.data:
            if form.validate_on_submit():
                mag = Magazine(
                    title=form.title.data,
                    owner_id=current_user.id,
                    owner_name=current_user.name,
                )
                db.session.add(mag)
                db.session.commit()
                #                db.session.close()
                return redirect(url_for("add_mag"))

    return render_template("add_mag.html", form=form, table=mag_table)


@app.route("/borrow_dvd/<int:id>", methods=["GET", "POST"])
@login_required
def borrow_dvd(id):

    dvd_items = DVD.query.filter_by(id=id).first()
    if dvd_items.borrower_id == None:
        dvd_items.date_borrowed = datetime.now()
        dvd_items.borrower_id = current_user.id
        dvd_items.borrower_name = current_user.name
        db.session.commit()

    return redirect(url_for("library"))


@app.route("/borrow_mag/<int:id>", methods=["GET", "POST"])
@login_required
def borrow_mag(id):

    mag_items = Magazine.query.filter_by(id=id).first()
    if mag_items.borrower_id == None:
        mag_items.date_borrowed = datetime.now()
        mag_items.borrower_id = current_user.id
        mag_items.borrower_name = current_user.name
        db.session.commit()
    #        db.session.close()

    return redirect(url_for("library"))


@app.route("/return_dvd/<int:id>", methods=["GET", "POST"])
@login_required
def return_dvd(id):

    dvd_items = DVD.query.filter_by(id=id).first()
    if dvd_items.owner_id == current_user.id:
        dvd_items.date_borrowed = None
        dvd_items.borrower_id = None
        dvd_items.borrower_name = ""
        db.session.commit()
    #        db.session.close()

    return redirect(url_for("library"))


@app.route("/return_mag/<int:id>", methods=["GET", "POST"])
@login_required
def return_mag(id):

    mag_items = Magazine.query.filter_by(id=id).first()
    if mag_items.owner_id == current_user.id:
        mag_items.date_borrowed = None
        mag_items.borrower_id = None
        mag_items.borrower_name = ""
        db.session.commit()
    #        db.session.close()

    return redirect(url_for("library"))


@app.route("/lent_list", methods=["GET", "POST"])
@login_required
def lent_list():

    search = SearchForm()
    if request.method == "POST":
        return search_func(search)

    dvd_items = DVD.query.filter(
        DVD.owner_id == current_user.id, DVD.borrower_id != None
    ).all()
    dvd_table = DVD_table(dvd_items)
    dvd_table.border = True
    mag_items = Magazine.query.filter(
        Magazine.owner_id == current_user.id, Magazine.borrower_id != None
    ).all()
    mag_table = Mag_table(mag_items)
    mag_table.border = True
    return render_template(
        "list.html", mag_table=mag_table, dvd_table=dvd_table, search=search
    )


@app.route("/borrowed_list", methods=["GET", "POST"])
@login_required
def borrowed_list():

    search = SearchForm()
    if request.method == "POST":
        return search_func(search)

    dvd_items = DVD.query.filter(DVD.borrower_id == current_user.id).all()
    dvd_table = DVD_table(dvd_items)
    dvd_table.border = True
    mag_items = Magazine.query.filter(Magazine.borrower_id == current_user.id).all()
    mag_table = Mag_table(mag_items)
    mag_table.border = True
    return render_template(
        "list.html", mag_table=mag_table, dvd_table=dvd_table, search=search
    )


@app.route("/rules", methods=["GET"])
def rules():

    return render_template("rules.html")


@app.route("/changes", methods=["GET"])
def changes():

    return render_template("changes.html")
