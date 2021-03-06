from app import app, db, mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_user import current_user
from app.models import Asset, Site, AssetPoint, AssetType, Algorithm, FunctionalDescriptor, FunctionalDescriptorCategory, PointType, InbuildingsAsset, Result, EmailTemplate, Email, User, Role, Alarm, LoggedEntity, LogTimeValue
from app.ict.models import ITasset
from app.ticket.models import FlicketPriority, FlicketCategory, FlicketStatus, TicketComponent, TicketResolution
from app.models.ITP import Deliverable_type, Location
from flask_mail import Message
from flask import render_template, url_for
from flask_security.utils import hash_password, send_mail
from flask_security.confirmable import generate_confirmation_link
from app.models.ITP import ITC_group, Secondary_location

# configuration of views for Admin page
# some columns (eg results) are excluded, since it tries to load and display >10,000 entries and crashes the page
# default sort column is needed on views that have enough entries to use pagination

admin = Admin(app)

# all views should be subclasses of this
class ProtectedView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class FunctionalDescriptorView(ProtectedView):
    pass

class AssetView(ProtectedView):
	form_excluded_columns = ['results']

class AssetPointView(ProtectedView):
    column_filters = (Asset.name, PointType.name)
    column_searchable_list = ('name', Asset.name)
    column_default_sort = ('asset_id')
    form_excluded_columns = ['results']

class PointTypeView(ProtectedView):
    form_excluded_columns = ['algorithms']

# lock the algorithm models from being edited - these are automatically generated from the code
class AlgorithmView(ProtectedView):
    form_excluded_columns = ['results']
    can_view_details = True
    column_details_list = ['name', 'descr', 'point_types', 'functions']

class InbuildingsAssetView(ProtectedView):
    column_default_sort = 'id'

class ResultView(ProtectedView):
    column_default_sort = ('id', True)

class SiteView(ProtectedView):
    form_excluded_columns = ['issue_history']
    can_view_details = True

class AssetTypeView(ProtectedView):
    pass

class EmailTemplateView(ProtectedView):
    pass

class EmailView(ProtectedView):
    pass

class UserView(ProtectedView):
    column_exclude_list = ('password', 'last_login_ip', 'last_login_at', 'current_login_ip', 'current_login_at', 'login_count')
    form_create_rules = ('first_name', 'last_name','email', 'company', 'roles', 'sites', 'active', 'authenticated')
    #create_template='create_user.html'
    column_filters = ('first_name', 'last_name', 'roles.name', 'sites.name', 'projects')
    column_editable_list = ['first_name', 'last_name']
    form_excluded_columns = ['Deliverable_ITC', 'password', 'last_login_ip', 'last_login_at', 'current_login_ip', 'current_login_at', 'login_count',
        'confirmed_at', 'ticket_modified_id', 'ticket_assigned_id', 'ticket_resolve_id', 'ticket_start_id', 'password_change_date', 'password_active', 'projects']
    can_view_details = True
    can_delete = False

    def after_model_change(self, form, model, is_created):
        if model.active == 1:
            print('account is active')
        else:
            print('account needs to be activated')

        #Randomly generate temp user pw and send to email
        if len(model.password) == 0:
            import string
            import random
            def pw_gen(size=10, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
                return ''.join(random.choice(chars) for _ in range(size))

            password = pw_gen()
            model.password = password
            confirmation_link, token = generate_confirmation_link(model)
            from app.templates.security import email
            msg = Message("Medusa Temp Password",
                        recipients=[model.email])
            msg.body = "Your temporary password is: " + password + "\n\nPlease click on the following confirmation link " + confirmation_link
            mail.send(msg)
            from flask_security.changeable import change_user_password
            model.password = hash_password(password)
            db.session.commit()

class RoleView(ProtectedView):
    pass

class AlarmView(ProtectedView):
     column_display_pk = True

class LoggedEntityView(ProtectedView):
     column_display_pk = True

class LogTimeValueView(ProtectedView):
     column_display_pk = True

class DeliverableTypeView(ProtectedView):
    column_display_pk = True

class LocationView(ProtectedView):
    column_display_pk = True

class SecondaryLocationView(ProtectedView):
    column_list = ('name', 'location', 'deliverable')

class ITassetView(ProtectedView):
    pass

class TicketPriorityView(ProtectedView):
    pass

class TicketCategoryView(ProtectedView):
    pass

class TicketStatusView(ProtectedView):
    pass

class TicketComponentView(ProtectedView):
    pass

class TicketResolutionView(ProtectedView):
    pass

class ITCGroup(ProtectedView):
    pass

# attach the model views to the admin page
admin.add_view(SiteView(Site, db.session))
admin.add_view(AssetTypeView(AssetType, db.session))
admin.add_view(FunctionalDescriptorView(FunctionalDescriptor, db.session))
admin.add_view(AssetView(Asset, db.session))
admin.add_view(AssetPointView(AssetPoint, db.session))
admin.add_view(PointTypeView(PointType, db.session))
admin.add_view(AlgorithmView(Algorithm, db.session))
admin.add_view(ResultView(Result, db.session))
admin.add_view(InbuildingsAssetView(InbuildingsAsset, db.session))
admin.add_view(EmailTemplateView(EmailTemplate, db.session))
admin.add_view(EmailView(Email, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(RoleView(Role, db.session))
admin.add_view(ProtectedView(FunctionalDescriptorCategory, db.session))
admin.add_view(AlarmView(Alarm, db.session))
admin.add_view(LoggedEntityView(LoggedEntity, db.session))
admin.add_view(LogTimeValueView(LogTimeValue, db.session))
admin.add_view(DeliverableTypeView(Deliverable_type, db.session))
admin.add_view(LocationView(Location, db.session))
admin.add_view(SecondaryLocationView(Secondary_location, db.session))
admin.add_view(ITassetView(ITasset, db.session))
admin.add_view(TicketPriorityView(FlicketPriority, db.session))
admin.add_view(TicketCategoryView(FlicketCategory, db.session))
admin.add_view(TicketStatusView(FlicketStatus, db.session))
admin.add_view(TicketComponentView(TicketComponent, db.session))
admin.add_view(TicketResolutionView(TicketResolution, db.session))
admin.add_view(ITCGroup(ITC_group, db.session))
