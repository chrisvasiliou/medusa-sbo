#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime
import decimal
import json

from flask import request
from flask_login import login_required

from app import app
from app.ticket.models import (FlicketCategory, FlicketDepartment, FlicketTicket, FlicketPost, FlicketStatus)
from app.models.users import User


# todo currently unused
def alchemy_encoder(obj):
    """
    JSON encoder function for SQLAlchemy special cases.
    Taken from: http://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/
    """
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


# json api to display departments
@app.route('/department', methods=['GET', 'POST'])
def api_departments():

    departments = FlicketDepartment.query.all()
    my_list = []
    for d in departments:
        sub_dict = {
            'id': d.id,
            'department': d.department,
        }
        my_list.append(sub_dict)

    json_dump = json.dumps(my_list)

    return json_dump


# json api to display categories
#@flicket_api_bp.route(app.config['FLICKET_API'] + 'category/<int:id>/', methods=['GET', 'POST'])
@app.route('/category')
def api_categories(id=None):

    categories = FlicketCategory.query
    if id:
        categories = categories.filter_by(department_id=id)

    my_list = []
    for c in categories:
        sub_dict = {
            'id': c.id,
            'category': c.category,
        }
        my_list.append(sub_dict)

    json_dump = json.dumps(my_list)

    return json_dump


# json api to get statuses from db
@app.route('/statuses', methods=['GET', 'POST'])
def api_statuses():
    statuses = FlicketStatus.query.all()

    my_list = []
    for s in statuses:
        sub_dict = {
            'id': s.id,
            'status': s.status,
        }
        my_list.append(sub_dict)

    json_dump = json.dumps(my_list)

    return json_dump


# json api to display tickets
# todo probably won't use this unitl I understand how to implement my pagination understanding
@app.route('/tickets/other')
def api_tickets(page=1):

    # get request arguments from the url
    status = request.args.get('status')
    department = request.args.get('department')
    category = request.args.get('category')
    content = request.args.get('content')
    user_id = request.args.get('user_id')

    tickets = FlicketTicket.query
    if status:
        tickets = tickets.filter(FlicketTicket.current_status.has(FlicketStatus.status == status))
    if category:
        tickets = tickets.filter(FlicketTicket.category.has(FlicketCategory.category == category))
    if department:
        department_filter = FlicketDepartment.query.filter_by(department=department).first()
        tickets = tickets.filter(FlicketTicket.category.has(FlicketCategory.department == department_filter))
    if user_id:
        tickets = tickets.filter_by(assigned_id=int(user_id))

    if content:

        f1 = FlicketTicket.title.ilike('%' + content + '%')
        f2 = FlicketTicket.content.ilike('%' + content + '%')
        f3 = FlicketTicket.posts.any(FlicketPost.content.ilike('%' + content + '%'))
        tickets = tickets.filter(f1 | f2 | f3)

    tickets = tickets.order_by(FlicketTicket.id.desc())

    tickets = tickets.paginate(page, app.config['posts_per_page'])

    my_list = []
    for t in tickets.items:

        assigned = '-'

        if t.assigned_id:
            assigned = t.assigned.username

        sub_dict = {
            'id': t.id,
            'number': t.id_zfill,
            'title': t.title,
            'submitted_by': t.user.username,
            'priority': t.ticket_priority.priority,
            'date': t.date_added.strftime('%d/%m/%Y'),
            'replies': t.num_replies,
            'department': t.category.department.department,
            'category': t.category.category,
            'status': t.current_status.status,
            'assigned': assigned,
        }
        my_list.append(sub_dict)

    json_dump = json.dumps(my_list)

    return json_dump
