import datetime

from app import db
from app.models.users import User

# define field sizes. max are used for forms and database. min just for forms.
field_size = {
    'title_min_length': 3,
    'title_max_length': 128,
    'content_min_length': 5,
    'content_max_length': 5000,
    'status_min_length': 3,
    'status_max_length': 20,
    'department_min_length': 3,
    'department_max_length': 30,
    'category_min_length': 3,
    'category_max_length': 30,
    'filename_min_length': 3,
    'filename_max_length': 128,
    'priority_min_length': 3,
    'priority_max_length': 12
}


class FlicketStatus(db.Model):
    __tablename__ = 'flicket_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(field_size['status_max_length']))

class TicketComponent(db.Model):
    __tablename__ = 'ticket_component'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(field_size['status_max_length']))


class FlicketDepartment(db.Model):
    __tablename__ = 'flicket_department'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(field_size['department_max_length']))

    categories = db.relationship('FlicketCategory', back_populates='department')

    # make the default sort order the department name
    __mapper_args__ = {
        "order_by": department.asc()
    }


class FlicketCategory(db.Model):
    __tablename__ = 'flicket_category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(field_size['category_max_length']))

    department_id = db.Column(db.Integer, db.ForeignKey(FlicketDepartment.id))
    department = db.relationship(FlicketDepartment, back_populates='categories')

    # make the default sort order the category name
    __mapper_args__ = {
        "order_by": category.asc()
    }


class FlicketPriority(db.Model):
    __tablename__ = 'flicket_priorities'

    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.String(field_size['priority_max_length']))

class TicketResolution(db.Model):
    __tablename__ = 'ticket_resolution'

    id = db.Column(db.Integer, primary_key=True)
    resolution = db.Column(db.String(field_size['status_max_length']))


class FlicketTicket(db.Model):
    __tablename__ = 'flicket_topic'

    id = db.Column(db.Integer, primary_key=True)
    ticket_name = db.Column(db.String(field_size['title_max_length']), index=True)
    description = db.Column(db.String(field_size['content_max_length']))

    date_added = db.Column(db.DateTime())
    date_due = db.Column(db.DateTime())

    started_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User, foreign_keys='FlicketTicket.started_id')

    category_id = db.Column(db.Integer, db.ForeignKey(FlicketCategory.id))
    category = db.relationship(FlicketCategory)

    component_id = db.Column(db.Integer, db.ForeignKey(TicketComponent.id))
    component = db.relationship(TicketComponent)

    ticket_priority_id = db.Column(db.Integer, db.ForeignKey(FlicketPriority.id))
    ticket_priority = db.relationship(FlicketPriority)

    assigned_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned = db.relationship(User, foreign_keys='FlicketTicket.assigned_id')

    #cc_list = db.Column(db.Integer)

    date_resolved = db.Column(db.DateTime())
    resolved_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    resolved_by = db.relationship(User, foreign_keys='FlicketTicket.resolved_by_id')
    resolution_id = db.Column(db.Integer, db.ForeignKey(TicketResolution.id), nullable=True)
    resolution = db.relationship(TicketResolution)

    status_id = db.Column(db.Integer, db.ForeignKey(FlicketStatus.id))
    current_status = db.relationship(FlicketStatus)

    # site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    site_id = db.Column('site_id', db.Integer, db.ForeignKey('site.ID'), nullable=False)

    # facility = db.Column(db.String(field_size['title_max_length']))
    project_id = db.Column('project_id', db.Integer, db.ForeignKey('project.id'), nullable=True)

    date_modified = db.Column(db.DateTime())
    modified_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    modified = db.relationship(User, foreign_keys='FlicketTicket.modified_id')

    posts = db.relationship("FlicketPost", back_populates="ticket")

    # find all the images associated with the topic
    uploads = db.relationship('FlicketUploads',
                              primaryjoin="and_(FlicketTicket.id == FlicketUploads.topic_id)")

    # finds all the users who are subscribed to the ticket.
    subscribers = db.relationship('FlicketSubscription', order_by='FlicketSubscription.user_def')

    # finds all the actions associated with the post
    actions = db.relationship('FlicketAction', primaryjoin="and_(FlicketTicket.id == FlicketAction.ticket_id)")

    # reports

    @property
    def num_replies(self):
        n_replies = FlicketPost.query.filter_by(ticket_id=self.id).count()
        return n_replies

    @property
    def id_zfill(self):
        return str(self.id).zfill(5)

    def is_subscribed(self, user):
        for s in self.subscribers:
            if s.user == user:
                return True
        return False

    def get_subscriber_emails(self):
        """
        Function to return a list of email addresses of subscribed users.
        :return:
        """
        emails = list()
        for user in self.subscribers:
            emails.append(user.user.email)

        return emails


class FlicketPost(db.Model):
    __tablename__ = 'flicket_post'

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    ticket = db.relationship(FlicketTicket, back_populates='posts')

    content = db.Column(db.String(field_size['content_max_length']))

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, foreign_keys='FlicketPost.user_id')

    date_added = db.Column(db.DateTime())
    date_modified = db.Column(db.DateTime())

    modified_id = db.Column(db.Integer, db.ForeignKey(User.id))
    modified = db.relationship(User, foreign_keys='FlicketPost.modified_id')

    # finds all the images associated with the post
    uploads = db.relationship('FlicketUploads',
                              primaryjoin="and_(FlicketPost.id == FlicketUploads.posts_id)")

    # finds all the actions associated with the post
    actions = db.relationship('FlicketAction',
                              primaryjoin="and_(FlicketPost.id == FlicketAction.post_id)")


class FlicketUploads(db.Model):
    __tablename__ = 'flicket_uploads'

    id = db.Column(db.Integer, primary_key=True)

    posts_id = db.Column(db.Integer, db.ForeignKey(FlicketPost.id))
    post = db.relationship(FlicketPost)

    topic_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    topic = db.relationship(FlicketTicket)

    filename = db.Column(db.String(field_size['filename_max_length']))
    original_filename = db.Column(db.String(field_size['filename_max_length']))


class FlicketHistory(db.Model):
    __tablename__ = 'flicket_history'

    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey(FlicketPost.id))
    post = db.relationship(FlicketPost)

    topic_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    topic = db.relationship(FlicketTicket)

    date_modified = db.Column(db.DateTime())

    original_content = db.Column(db.String(field_size['content_max_length']))

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class FlicketSubscription(db.Model):
    __tablename__ = 'flicket_ticket_subscription'

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    ticket = db.relationship(FlicketTicket)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

    user_def = db.deferred(db.select([User.email]).where(User.id == user_id))

    def __repr__(self):
        return '<Class FlicketSubscription: ticket_id={}, user_id={}>'


class FlicketAction(db.Model):
    """
    SQL table that stores the action history of a ticket.
    For example, if a user claims a ticket that action is stored here.
    The action is associated with either the ticket_id (if no posts) or post_id (of
    lastest post). The reason for this is displaying within the ticket view.
    """
    __tablename__ = 'flicket_ticket_action'

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    ticket = db.relationship(FlicketTicket)

    post_id = db.Column(db.Integer, db.ForeignKey(FlicketPost.id))
    post = db.relationship(FlicketPost)

    assigned = db.Column(db.Boolean)
    claimed = db.Column(db.Boolean)
    released = db.Column(db.Boolean)
    closed = db.Column(db.Boolean)
    opened = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, foreign_keys=[user_id])

    recipient_id = db.Column(db.Integer, db.ForeignKey(User.id))
    recipient = db.relationship(User, foreign_keys=[recipient_id])

    date = db.Column(db.DateTime)

    def output_action(self):
        """
        Method used in ticket view to show what action has taken place in ticket.
        :return:
        """

        _date = self.date.strftime('%d-%m-%Y %H:%M')

        if self.assigned:
            return 'Ticket assigned to <a href="mailto:{1}">{0}</a> by <a href="mailto:{3}">{2}</a> | {4}'.format(
                self.recipient.first_name, self.recipient.email, self.user.first_name, self.user.email, _date)

        if self.claimed:
            return 'Ticked claimed by <a href="mailto:{}">{}</a>  | {}'.format(self.user.email, self.user.first_name, _date)

        if self.released:
            return 'Ticket released by <a href="mailto:{}">{}</a> | {}'.format(self.user.email, self.user.first_name, _date)

        if self.closed:
            return 'Ticked closed by <a href="mailto:{}">{}</a> | {}'.format(self.user.email, self.user.first_name, _date)

        if self.opened:
            return 'Ticked opened by <a href="mailto:{}">{}</a> | {}'.format(self.user.email, self.user.first_name, _date)

    def __repr__(self):

        return ('<Class FlicketAction: ticket_id={}, post_id={}, assigned={}, unassigned={}, claimed={},'
                'released={}, closed={}, opened={}, user_id={}, recipient_id={}, date={}>').format(self.ticket_id,
                                                                                                   self.post_id,
                                                                                                   self.assigned,
                                                                                                   self.unassigned,
                                                                                                   self.claimed,
                                                                                                   self.released,
                                                                                                   self.closed,
                                                                                                   self.opened,
                                                                                                   self.user_id,
                                                                                                   self.recipient_id,
                                                                                                   self.date)
