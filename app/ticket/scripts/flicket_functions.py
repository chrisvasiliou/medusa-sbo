#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime

from flask import flash, g
from app.models.users import User
from flask_user import current_user

from app import db
from app.ticket.models import FlicketPost, FlicketAction


def add_action(action=None, ticket=None, recipient=None):
    """
    :param action: string 'assign', 'unassign', 'close', 'claim', 'release'
    :param ticket: ticket object
    :param post: post object
    :param user: user object
    :return:
    """
    ticket_id = None
    post_id = None
    assigned = None
    claimed = None
    released = None
    closed = None
    opened = None


    if len(ticket.posts) == 0:
        ticket_id = ticket.id
    else:
        post_id = ticket.posts[len(ticket.posts)-1].id

    if action == 'assign':
        assigned = True

    if action == 'claim':
        claimed = True

    if action == 'release':
        released = True

    if action == 'close':
        closed = True
        ticket_id = ticket.id

    if action == 'reopen':
        opened = True
        ticket_id = ticket.id

    new_action = FlicketAction(
        ticket_id=ticket_id,
        post_id=post_id,
        assigned=assigned,
        claimed=claimed,
        released=released,
        closed=closed,
        opened=opened,
        user=current_user,
        recipient=recipient,
        date=datetime.datetime.now()
    )
    db.session.add(new_action)
    db.session.commit()


def is_ticket_closed(status):
    # check to see if topic is closed. ticket can't be edited once it's closed.
    if status == 'Closed':
        flash('Users can not edit closed tickets.')
        return True


def block_quoter(foo):
    """
    Indents input with '> '. Used for quoting text in posts.
    :param foo:
    :return:
    """

    foo = foo.strip()
    split_string = foo.split('\n')
    new_string = ''
    if len(split_string) > 0:
        for i in split_string:
            temp_string = '> ' + i
            new_string += temp_string
        return new_string
    else:
        return '> ' + foo
