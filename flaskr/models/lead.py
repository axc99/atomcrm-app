from flaskr import db
from datetime import datetime, date
from flaskr.models.tag import Tag
from flaskr.models.field import Field


# Lead
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    add_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    upd_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    archived = db.Column(db.Boolean, default=False, nullable=False)

    veokit_installation_id = db.Column(db.Integer, nullable=False, index=True)
    veokit_user_id = db.Column(db.Integer, nullable=False, index=True)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id', ondelete='SET NULL'), nullable=False)

    # UTM marks
    utm_source = db.Column(db.String(500))
    utm_medium = db.Column(db.String(500))
    utm_campaign = db.Column(db.String(500))
    utm_term = db.Column(db.String(500))
    utm_content = db.Column(db.String(500))

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
                db.session.add(tag)
                db.session.commit()

                # Add tag to lead
                new_lead_tag = LeadTag()
                new_lead_tag.tag_id = tag.id
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
                .filter_by(id=lead_field['fieldId'],
                           veokit_installation_id=self.veokit_installation_id) \
                .first()

            if field:
                new_lead_field = LeadField()
                new_lead_field.field_id = field.id
                new_lead_field.lead_id = self.id
                new_lead_field.value = lead_field['value']

                db.session.add(new_lead_field)

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
                f.as_title AS field_as_title,
                f.primary AS field_primary,
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
                'field_as_title': field.field_as_title,
                'field_primary': field.field_primary,
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
