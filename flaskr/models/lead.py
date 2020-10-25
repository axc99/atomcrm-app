import enum
from flask_babel import _
from flask import request
from flaskr import db
from datetime import datetime, timedelta
from flaskr.models.tag import Tag
from flaskr.models.field import Field
import random
import string
from sqlalchemy import Enum


# Lead
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # User friendly ID (for API, search)
    uid = db.Column(db.String(8))

    add_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    upd_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    amount = db.Column(db.Float, nullable=True)

    archived = db.Column(db.Boolean, default=False, nullable=False)

    veokit_installation_id = db.Column(db.Integer, nullable=False, index=True)
    veokit_user_id = db.Column(db.Integer, nullable=True, index=True)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id', ondelete='SET NULL'), nullable=False)

    # UTM marks
    utm_source = db.Column(db.String(500))
    utm_medium = db.Column(db.String(500))
    utm_campaign = db.Column(db.String(500))
    utm_term = db.Column(db.String(500))
    utm_content = db.Column(db.String(500))

    # Get unique uid
    @staticmethod
    def get_uid():
        uid = Lead.generate_uid()

        is_not_unique = Lead.query.filter_by(uid=uid).count() >= 1
        if is_not_unique:
            return Lead.get_uid()

        return uid

    # Generate uid
    @staticmethod
    def generate_uid():
        return ''.join(random.choice('ABCD' + string.digits) for _ in range(8))

    # Set tags
    def set_tags(self, tags, new_lead=False):
        if not new_lead:
            # Delete all lead tags
            LeadTag.query \
                .filter_by(lead_id=self.id) \
                .delete()

        for tag_name in tags:
            # Search tag by name
            exist_tag = Tag.query \
                .filter_by(name=tag_name,
                           veokit_installation_id=self.veokit_installation_id) \
                .first()

            # If tag with such name already exist
            if not exist_tag:
                # Create tag
                new_tag = Tag()
                new_tag.name = tag_name
                new_tag.veokit_installation_id = self.veokit_installation_id
                db.session.add(new_tag)
                db.session.commit()

                # Add tag to lead
                new_lead_tag = LeadTag()
                new_lead_tag.tag_id = new_tag.id
                new_lead_tag.lead_id = self.id

                db.session.add(new_lead_tag)
            else:
                # Add tag to lead
                new_lead_tag = LeadTag()
                new_lead_tag.tag_id = exist_tag.id
                new_lead_tag.lead_id = self.id

                db.session.add(new_lead_tag)

        db.session.commit()

    # Set fields
    def set_fields(self, fields, new_lead=False):
        if not new_lead:
            # Delete lead fields
            LeadField.query \
                .filter_by(lead_id=self.id) \
                .delete()

        for lead_field in fields:
            field = Field.query \
                .filter_by(id=lead_field['field_id'],
                           veokit_installation_id=self.veokit_installation_id) \
                .first()

            if field:
                new_lead_field = LeadField()
                new_lead_field.field_id = field.id
                new_lead_field.lead_id = self.id
                new_lead_field.value = lead_field.get('value')

                db.session.add(new_lead_field)
            else:
                print('Unknown field #{}'.format(lead_field['field_id']))

        db.session.commit()

    # Get fields
    @staticmethod
    def get_fields(lead_id, for_api=False):
        res_fields = []

        fields = db.session.execute("""
            SELECT
                lf.field_id,
                lf.value,
                f.value_type AS field_value_type,
                f.board_visibility AS field_board_visibility,
                f.name AS field_name
            FROM
                public.lead_field AS lf
            LEFT JOIN
                public.field as f ON f.id = lf.field_id
            WHERE
                lf.lead_id = :lead_id
            ORDER BY
                f.id ASC""", {
            'lead_id': lead_id
        })
        for field in fields:
            res_fields.append({
                                  'field_id': field.field_id,
                                  'field_name': field.field_name,
                                  'value': field.value
                              } if for_api else {
                'field_id': field.field_id,
                'value': field.value,
                'field_board_visibility': field.field_board_visibility,
                'field_value_type': field.field_value_type
            })

        return res_fields

    # Get tags
    @staticmethod
    def get_tags(lead_id, for_api=False):
        res_tags = []

        tags = db.session.execute("""
            SELECT
                lt.tag_id,
                t.name AS tag_name
            FROM
                public.lead_tag AS lt
            LEFT JOIN
                public.tag as t ON t.id = lt.tag_id
            WHERE
                lt.lead_id = :lead_id
            ORDER BY
                t.name ASC""", {
            'lead_id': lead_id
        })
        for tag in tags:
            res_tags.append(tag.tag_name)

        return res_tags

    @staticmethod
    def get_regular_date(src_date):
        data = request.get_json()
        timezone_offset = data['timezoneOffset'] if data else 0

        date_obj = datetime.strptime(src_date, '%Y-%m-%d %H:%M:%S')
        [date, time] = src_date.split(' ')
        [year, month, day] = date.split('-')
        [hours, minutes, seconds] = time.split(':')

        months = {
            '01': _('m_lead_getRegularDate_jan'),
            '02': _('m_lead_getRegularDate_feb'),
            '03': _('m_lead_getRegularDate_mar'),
            '04': _('m_lead_getRegularDate_apr'),
            '05': _('m_lead_getRegularDate_may'),
            '06': _('m_lead_getRegularDate_jun'),
            '07': _('m_lead_getRegularDate_jul'),
            '08': _('m_lead_getRegularDate_aug'),
            '09': _('m_lead_getRegularDate_sep'),
            '10': _('m_lead_getRegularDate_oct'),
            '11': _('m_lead_getRegularDate_nov'),
            '12': _('m_lead_getRegularDate_dec')
        }
        month_str = months[month]

        if date_obj.date() >= datetime.today().date():
            return _('m_lead_getRegularDate_today', hours=hours, minutes=minutes)
        elif date_obj.date() == datetime.today().date() - timedelta(days=1):
            return _('m_lead_getRegularDate_yesterday', hours=hours, minutes=minutes)
        else:
            if date_obj.year == datetime.today().year:
                return _('m_lead_getRegularDate_date', day=day, month=month_str, hours=hours, minutes=minutes)
            elif date_obj.year == datetime.today().year:
                return _('m_lead_getRegularDate_dateWithYear', day=day, month=month_str, year=year, hours=hours,
                         minutes=minutes)

        return date

    # Filter leads
    @staticmethod
    def get_with_filter(installation_id, status_id, search, offset, limit, filter):
        search = search.strip() if search else None
        search_exp = 'true'
        join_exp = ''
        search_value = None

        if search:
            if search.startswith('uid='):
                search_exp = 'l.uid = :search_value'
                search_value = search.split('=').pop(1)
            # elif search.startswith('archived=true') or search.startswith('archived=1'):
            #     search_exp = "l.archived = TRUE"
            # elif search.startswith('utm_source=') or search.startswith('utmSource='):
            #     search_exp = 'l.utm_source LIKE :search_value'
            # elif search.startswith('utm_medium=') or search.startswith('utmMedium='):
            #     search_exp = 'l.utm_medium LIKE :search_value'
            # elif search.startswith('utm_campaign=') or search.startswith('utmCampaign='):
            #     search_exp = 'l.utm_campaign LIKE :search_value'
            # elif search.startswith('utm_term=') or search.startswith('utmTerm='):
            #     search_exp = 'l.utm_term LIKE :search_value'
            # elif search.startswith('utm_content=') or search.startswith('utmContent='):
            #     search_exp = 'l.utm_content LIKE :search_value'
            else:
                search_value = '%' + search.lower() + '%'
                search_exp = """(lf.value != '' AND LOWER(lf.value) LIKE :search_value) OR 
                                (LOWER(t.name) LIKE :search_value)"""

                join_exp = """
                    LEFT JOIN 
                        public.lead_field AS lf ON lf.lead_id = l.id
                    LEFT JOIN 
                        public.lead_tag AS lt ON lt.lead_id = l.id
                    LEFT JOIN 
                        public.tag AS t ON t.id = lt.tag_id"""

        return db.session.execute("""  
            SELECT 
                l.*,
                COUNT(*) OVER () AS total,
                SUM(l.amount) OVER () AS amount_sum
            FROM 
                public.lead AS l
            {}
            WHERE
                l.veokit_installation_id = :installation_id AND
                l.status_id = :status_id AND
                l.archived = :archived AND
                (:utm_source is null OR l.utm_source = :utm_source) AND
                (:utm_medium is null OR l.utm_medium = :utm_medium) AND
                (:utm_campaign is null OR l.utm_campaign = :utm_campaign) AND
                (:utm_term is null OR l.utm_term = :utm_term) AND
                (:utm_content is null OR l.utm_content = :utm_content) AND
                (:period_from is null OR l.add_date > :period_from) AND 
                (:period_to is null OR l.add_date < :period_to) AND 
                ({})
            GROUP BY
                l.id
            ORDER BY 
                l.add_date DESC
            OFFSET 
                :offset
            LIMIT
                :limit""".format(join_exp, search_exp), {
            'offset': 0 if offset is None else offset,
            'limit': 10 if limit is None else limit,
            'installation_id': installation_id,
            'status_id': status_id,
            'search_exp': search_exp,
            'search_value': search_value if search_value else None,
            'archived': filter['archived'] if filter.get('archived') else False,
            'utm_source': filter.get('utm_source'),
            'utm_medium': filter.get('utm_medium'),
            'utm_campaign': filter.get('utm_campaign'),
            'utm_term': filter.get('utm_term'),
            'utm_content': filter.get('utm_content'),
            'period_from': "{} 00:00:00".format(filter['period_from']) if filter.get('period_from') else None,
            'period_to': "{} 23:59:59".format(filter['period_to']) if filter.get('period_to') else None
        })


# Lead field
class LeadField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(1000), nullable=True)

    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id', ondelete='CASCADE'), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('field.id', ondelete='CASCADE'), nullable=False)


# Lead tag
class LeadTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id', ondelete='CASCADE'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), nullable=False)


# Lead action type
class LeadActionType(enum.Enum):
    create_lead = 1
    update_lead = 2
    update_lead_status = 3
    archive_lead = 4
    restore_lead = 5


# Lead action
class LeadAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(Enum(LeadActionType), nullable=False)

    # Update task status
    old_status_id = db.Column(db.Integer, db.ForeignKey('status.id', ondelete='CASCADE'), nullable=True)
    new_status_id = db.Column(db.Integer, db.ForeignKey('status.id', ondelete='CASCADE'), nullable=True)

    log_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    veokit_user_id = db.Column(db.Integer, nullable=True, index=True)
    # extension_id = db.Column(db.Integer, nullable=True, index=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id', ondelete='CASCADE'), nullable=False)

    @staticmethod
    def get_item_data(action):
        types_date = {
            'create_lead': {
                'color': 'green',
                'title': _('m_lead_leadAction_getItemData_createLead',
                           new_status_name=action['new_status_name'] if action['new_status_name'] else '...')
                # 'Create lead in {}'.format()
            },
            'update_lead': {
                'color': 'blue',
                'title': _('m_lead_leadAction_getItemData_updateLead'),
                # 'title': 'Update lead'
            },
            'update_lead_status': {
                'color': 'blue',
                'title': _('m_lead_leadAction_getItemData_updateLeadStatus',
                           old_status_name=action['old_status_name'] if action['old_status_name'] else '...',
                           new_status_name=action['new_status_name'] if action['new_status_name'] else '...')
                # 'title': 'Change status from {} to {}'.format(
                #     action['old_status_name'] if action['old_status_name'] else '...',
                #     action['new_status_name'] if action['new_status_name'] else '...')
            },
            'archive_lead': {
                'color': 'red',
                'title': _('m_lead_leadAction_getItemData_archiveLead')  # 'Archive lead'
            },
            'restore_lead': {
                'color': 'green',
                'title': _('m_lead_leadAction_getItemData_restoreLead')  # 'Restore lead'
            }
        }

        return types_date[action.type]
