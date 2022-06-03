# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
from urllib import response
import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for,
    jsonify,
)

# from flask_moment import Moment
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
from models import *

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#
def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale="en")


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    # data=[{
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "venues": [{
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "num_upcoming_shows": 0,
    #   }, {
    #     "id": 3,
    #     "name": "Park Square Live Music & Coffee",
    #     "num_upcoming_shows": 1,
    #   }]
    # }, {
    #   "city": "New York",
    #   "state": "NY",
    #   "venues": [{
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "num_upcoming_shows": 0,
    #   }]
    # }]
    # data=Venue.query.with_entities(Venue.id, Venue.name).group_by(Venue.city, Venue.state).all()
    result = Venue.query.all()
    index_city = {}
    data = []
    for res in result:
        if index_city.get(res.city, None):
            index = index_city[res.city]
            data[index]["venues"].append(res)
        else:
            index_city[res.city] = len(data)
            temp = {"city": res.city, "state": res.state, "venues": [res]}
            data.append(temp)
    print("data>>>", data)
    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    search_term = request.form["search_term"]
    print(">>>>>>>>>>>>>>>>>>", search_term)
    search_result = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()

    response = {}
    response["count"] = len(search_result)
    response["data"] = search_result

    print(">>>>>>>>>>>>>>>>>>", search_term, "<<<<<<<<", response)
    # response = {
    #     "count": 1,
    #     "data": [
    #         {
    #             "id": 2,
    #             "name": "The Dueling Pianos Bar",
    #             "num_upcoming_shows": 0,
    #         }
    #     ],
    # }
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/venues/<venue_id>")
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # data1={
    #   "id": 1,
    #   "name": "The Musical Hop",
    #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #   "address": "1015 Folsom Street",
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "phone": "123-123-1234",
    #   "website": "https://www.themusicalhop.com",
    #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #   "seeking_talent": True,
    #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #   "past_shows": [{
    #     "artist_id": 4,
    #     "artist_name": "Guns N Petals",
    #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #     "start_time": "2019-05-21T21:30:00.000Z"
    #   }],
    #   "upcoming_shows": [],
    #   "past_shows_count": 1,
    #   "upcoming_shows_count": 0,
    # }
    data = Venue.query.get(venue_id)
    # print("data>>>>", data)
    return render_template("pages/show_venue.html", venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    try:
        name = request.form["name"]
        city = request.form["city"]
        state = request.form["state"]
        address = request.form["address"]
        phone = request.form["phone"]
        image_link = request.form["image_link"]
        facebook_link = request.form["facebook_link"]
        genres = request.form.getlist("genres")
        seeking_talent = request.form.get("seeking_talent", default=False, type=bool)
        website_link = request.form["website_link"]
        seeking_description = request.form["seeking_description"]

        new_venue = Venue(
            name=name,
            city=city,
            state=state,
            address=address,
            phone=phone,
            image_link=image_link,
            facebook_link=facebook_link,
            genres=genres,
            website_link=website_link,
            seeking_talent=seeking_talent,
            seeking_description=seeking_description,
        )

        db.session.add(new_venue)
        db.session.commit()
        flash("Venue " + request.form["name"] + " was successfully listed!")
    except:
        # error = True
        db.session.rollback()
        # flash(
        #     "An error occurred. Venue "
        #     + request.get_json()["name"]
        #     + " could not be listed."
        # )
        print(sys.exc_info())
    finally:
        db.session.close()
    return redirect(url_for("venues"))
    # return render_template('pages/home.html')

    # on successful db insert, flash success

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    # TODO: replace with real data returned from querying the database
    # data=[{
    #   "id": 4,
    #   "name": "Guns N Petals",
    # }, {
    #   "id": 5,
    #   "name": "Matt Quevedo",
    # }, {
    #   "id": 6,
    #   "name": "The Wild Sax Band",
    # }]

    # data=Artist.query.with_entities(Artist.id, Artist.name).all()
    data = Artist.query.with_entities(Artist.id, Artist.name).all()
    # data=Artist.query.options(load_only('email', 'id')).all()
    print("data>>>", data)
    return render_template("pages/artists.html", artists=data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    search_term = request.form["search_term"]
    print(">>>>>>>>>>>>>>>>>>", search_term)
    search_result = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()

    response = {}
    response["count"] = len(search_result)
    response["data"] = search_result

    print(">>>>>>>>>>>>>>>>>>", search_term, "<<<<<<<<", response)
    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<artist_id>")
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    # data1={
    #   "id": 4,
    #   "name": "Guns N Petals",
    #   "genres": ["Rock n Roll"],
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "phone": "326-123-5000",
    #   "website": "https://www.gunsnpetalsband.com",
    #   "facebook_link": "https://www.facebook.com/GunsNPetals",
    #   "seeking_venue": True,
    #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #   "past_shows": [{
    #     "venue_id": 1,
    #     "venue_name": "The Musical Hop",
    #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #     "start_time": "2019-05-21T21:30:00.000Z"
    #   }],
    #   "upcoming_shows": [],
    #   "past_shows_count": 1,
    #   "upcoming_shows_count": 0,
    # }
    # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
    data = Artist.query.get(artist_id)
    print("data>>>>", data)
    return render_template("pages/show_artist.html", artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)

    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.image_link.data = artist.image_link
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link
    form.website_link.data = artist.website_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description

    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    try:
        artist = Artist.query.get(artist_id)

        name = request.form["name"]
        city = request.form["city"]
        state = request.form["state"]
        phone = request.form["phone"]
        image_link = request.form["image_link"]
        facebook_link = request.form["facebook_link"]
        genres = request.form.getlist("genres")
        seeking_venue = request.form.get("seeking_venue", default=False, type=bool)
        website_link = request.form["website_link"]
        seeking_description = request.form["seeking_description"]

        artist.name = name
        artist.city = city
        artist.state = state
        artist.phone = phone
        artist.image_link = image_link
        artist.facebook_link = facebook_link
        artist.genres = genres
        artist.seeking_venue = seeking_venue
        artist.website_link = website_link
        artist.seeking_description = seeking_description

        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/venues/<venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.genres.data = venue.genres
    form.image_link.data = venue.image_link
    form.facebook_link.data = venue.facebook_link
    form.website_link.data = venue.website_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description

    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    try:
        venue = Venue.query.get(venue_id)

        name = request.form["name"]
        city = request.form["city"]
        state = request.form["state"]
        address = request.form["address"]
        phone = request.form["phone"]
        image_link = request.form["image_link"]
        facebook_link = request.form["facebook_link"]
        genres = request.form.getlist("genres")
        seeking_talent = request.form.get("seeking_talent", default=False, type=bool)
        website_link = request.form["website_link"]
        seeking_description = request.form["seeking_description"]

        venue.name = name
        venue.city = city
        venue.state = state
        venue.phone = phone
        venue.address = address
        venue.image_link = image_link
        venue.facebook_link = facebook_link
        venue.genres = genres
        venue.seeking_talent = seeking_talent
        venue.website_link = website_link
        venue.seeking_description = seeking_description

        db.session.commit()
    except:
        print("except block>>>>>>>")
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return redirect(url_for("show_venue", venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        name = request.form["name"]
        city = request.form["city"]
        state = request.form["state"]
        phone = request.form["phone"]
        image_link = request.form["image_link"]
        facebook_link = request.form["facebook_link"]
        genres = request.form.getlist("genres")
        seeking_venue = request.form.get("seeking_venue", default=False, type=bool)
        website_link = request.form["website_link"]
        seeking_description = request.form["seeking_description"]

        new_artist = Artist(
            name=name,
            city=city,
            state=state,
            phone=phone,
            image_link=image_link,
            facebook_link=facebook_link,
            genres=genres,
            website_link=website_link,
            seeking_venue=seeking_venue,
            seeking_description=seeking_description,
        )

        print("sent in", new_artist)
        db.session.add(new_artist)
        db.session.commit()
        flash("Artist " + request.form["name"] + " was successfully listed!")
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return redirect(url_for("artists"))


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    data = [
        {
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "artist_id": 4,
            "artist_name": "Guns N Petals",
            "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            "start_time": "2019-05-21T21:30:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 5,
            "artist_name": "Matt Quevedo",
            "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
            "start_time": "2019-06-15T23:00:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-01T20:00:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-08T20:00:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-15T20:00:00.000Z",
        },
    ]
    # data = Show.query.join(Venue).join(Artist).all()
    # print(">>>>>>>>>>>>>>>>", data)
    return render_template("pages/shows.html", shows=data)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    # flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    # return render_template('pages/home.html')
    # form = ShowForm()
    # error = False
    try:
        artist_id = request.form["artist_id"]
        venue_id = request.form["venue_id"]
        start_time = request.form["start_time"]

        new_show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)

        print("sent in>>>>>>>", new_show)
        db.session.add(new_show)
        db.session.commit()
        flash("Show was successfully listed!")
    except:
        # error = True
        db.session.rollback()
        flash("An error occurred. Show could not be listed.")
        print(sys.exc_info())
    finally:
        db.session.close()
    return render_template("pages/home.html")

    # if not error:
    # flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # on successful db insert, flash success

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
