from flask import render_template

from application.forms import SearchForm
from application.models import DVD, Magazine
from application.tables import DVD_table, Mag_table


def dvd_library(dvd_items):

    search = SearchForm()

    dvd_table = DVD_table(dvd_items)

    if dvd_items:
        dvd_table.border = True

    return render_template("DVD_list.html", table=dvd_table, search=search)


def mag_library(mag_items):

    search = SearchForm()
    mag_table = Mag_table(mag_items)
    if mag_items:
        mag_table.border = True

    return render_template("MAG_list.html", table=mag_table, search=search)


def search_func(search):

    if search.data["dvd_search"] != "":
        if search.data["dvd_select"] == "Owner":
            dvd_items = (
                DVD.query.filter(DVD.owner_name.contains(search.data["dvd_search"]))
                .order_by(DVD.title)
                .all()
            )
        if search.data["dvd_select"] == "Title":
            dvd_items = (
                DVD.query.filter(DVD.title.contains(search.data["dvd_search"]))
                .order_by(DVD.title)
                .all()
            )

        search.data["dvd_search"] = ""
        search.data["mag_search"] = ""
        return dvd_library(dvd_items)

    if search.data["mag_search"] != "":
        if search.data["mag_select"] == "Owner":
            mag_items = (
                Magazine.query.filter(
                    Magazine.owner_name.contains(search.data["mag_search"])
                )
                .order_by(Magazine.title)
                .all()
            )
        if search.data["mag_select"] == "Title":
            mag_items = (
                Magazine.query.filter(
                    Magazine.title.contains(search.data["mag_search"])
                )
                .order_by(Magazine.title)
                .all()
            )

        search.data["dvd_search"] = ""
        search.data["mag_search"] = ""
        return mag_library(mag_items)
