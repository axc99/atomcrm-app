from flask_babel import _
from flaskr import db
import enum
from datetime import datetime, date
from sqlalchemy import Integer, Enum, Column


# Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    index = db.Column(db.Integer, default=0, nullable=False)

    parent_task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='SET NULL'), nullable=True)
    veokit_installation_id = db.Column(db.Integer, nullable=False, index=True)

    # Set tasks
    def set_subtasks(self, tasks):
        i = 0
        removed_task_ids = []
        exist_tasks = db.session.execute("""
                    SELECT
                        t.id
                    FROM
                        public.task AS t
                    WHERE
                        t.parent_task_id = :parent_task_id""", {
            'parent_task_id': self.id
        })
        for exist_task in exist_tasks:
            removed_task_ids.append(exist_task['id'])

        for task in tasks:
            if task.get('name'):
                if task.get('id'):
                    # Update exist task
                    exist_task = Task.query \
                        .filter_by(id=task['id'],
                                   parent_task_id=self.id) \
                        .first()
                    exist_task.index = i
                    exist_task.name = task['name']

                    removed_task_ids.remove(exist_task.id)
                else:
                    # Create task
                    new_task = Task()
                    new_task.index = i
                    new_task.name = task['name']
                    new_task.parent_task_id = self.id
                    new_task.veokit_installation_id = self.veokit_installation_id

                    db.session.add(new_task)
            i += 1

        if len(removed_task_ids) > 0:
            Task.query \
                .filter(Task.id.in_(removed_task_ids, )) \
                .delete(synchronize_session=False)

        db.session.commit()

    # Get tasks
    def get_subtasks(self, lead_id=None):
        tasks = db.session.execute("""
            SELECT
                t.*,
                (
                    CASE
                        WHEN :lead_id is not NULL THEN (SELECT COUNT(*) FROM public.lead_completed_task as lct WHERE lct.task_id = t.id AND lct.lead_id = :lead_id) != 0
                        ELSE false
                    END
                ) AS completed
            FROM
                public.task AS t
            WHERE
                t.parent_task_id = :parent_task_id
            ORDER BY
                t.index""", {
            'parent_task_id': self.id,
            'lead_id': lead_id
        })

        return tasks
