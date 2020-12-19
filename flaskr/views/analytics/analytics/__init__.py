import enum
import dukpy
from flask_babel import _
from datetime import datetime, timedelta

from flaskr import db
from flaskr.models.lead import Lead
from flaskr.views.view import View, get_method, method_with_vars
from flaskr.models.status import Status, get_hex_by_color

compiled_methods = {
    'onChangePeriodType': get_method('methods/onChangePeriodType'),
    'onChangePeriod': get_method('methods/onChangePeriod')
}


# Page: Analytics
class Analytics(View):
    def __init__(self):
        self.meta = {
            'name': _('v_analytics_meta_name')
        }
        self.statuses = []
        self.rows = []
        self.period = []
        self.period_type = None
        self.data = []
        self.count_by_dates = None

    def before(self, params, request_data):
        self.period_type = params['periodType'] if params.get('periodType') else 'currentMonth'

        dates = None
        today_date = datetime.today()

        if self.period_type == 'currentMonth':
            dates = [today_date.replace(day=1), today_date]
        elif self.period_type == 'prevMonth':
            last_day_of_prev_month = today_date.today().replace(day=1) - timedelta(days=1)
            dates = [today_date.replace(day=1) - timedelta(days=last_day_of_prev_month.day), last_day_of_prev_month]
        elif self.period_type == 'last30d':
            dates = [today_date - timedelta(days=30), today_date]
        elif self.period_type == 'last3m':
            dates = [today_date - timedelta(days=90), today_date]
        elif self.period_type == 'last6m':
            dates = [today_date - timedelta(days=180), today_date]
        elif self.period_type == 'custom':
            dates = [datetime.strptime(params['periodFrom'], '%Y.%m.%d') if params.get('periodFrom') else today_date - timedelta(days=30),
                     datetime.strptime(params['periodTo'], '%Y.%m.%d') if params.get('periodTo') else today_date]
        elif self.period_type == 'allTime':
            first_added_lead = Lead.query \
                .filter_by(nepkit_installation_id=request_data['installation_id']) \
                .order_by(Lead.add_date.asc()) \
                .first()
            dates = [first_added_lead.add_date, today_date]

        if dates:
            self.period = [dates[0].strftime('%Y.%m.%d'), dates[1].strftime('%Y.%m.%d')]

            select_raw_items = []

            dates_delta = dates[1] - dates[0]
            for i in range(dates_delta.days + 1):
                if i > 2000:
                    break

                day = dates[0] + timedelta(days=i)
                date = day.strftime('%Y.%m.%d')
                self.data.append({
                    'date': date,
                    'leadCount': 100
                })
                select_raw_items.append('(SELECT COUNT(*) FROM public.lead AS l WHERE l.add_date::date = \'{}\' AND '
                                        'l.archived = false) AS "lead_count_on_{}"'.format(date, date))
            count_by_dates_result = db.session\
                .execute("""
                    SELECT
                        (
                            SELECT COUNT(*) 
                            FROM public.lead AS l 
                            WHERE 
                                (l.add_date::date >= :period_from AND l.add_date::date <= :period_to) AND 
                                l.archived = false
                        ) AS lead_count,
                        {}
                    FROM
                        public.status AS s
                    WHERE
                        s.nepkit_installation_id = :nepkit_installation_id
                    ORDER BY
                        s.index ASC
                    LIMIT 1 OFFSET 0""".format(','.join(select_raw_items)), {
                    'nepkit_installation_id': request_data['installation_id'],
                    'period_from': self.period[0],
                    'period_to': self.period[1]
                })
            self.count_by_dates = [r for r in count_by_dates_result][0]

            for i, row in enumerate(self.data):
                self.data[i]['leadCount'] = self.count_by_dates['lead_count_on_{}'.format(row['date'])]
        else:
            self.period = []

    def get_header(self, params, request_data):
        return {
            'title': self.meta.get('name'),
            'actions': [
                {
                    '_com': 'Field.Select',
                    'key': 'periodType',
                    'onChange': 'onChangePeriodType',
                    'value': self.period_type,
                    'options': [
                        {'value': 'currentMonth', 'label': _('v_analytics_header_periodType_currentMonth')},
                        {'value': 'prevMonth', 'label': _('v_analytics_header_periodType_previousMonth')},
                        {'value': 'last30d', 'label': _('v_analytics_header_periodType_last30days')},
                        {'value': 'last3m', 'label': _('v_analytics_header_periodType_last3months')},
                        {'value': 'last6m', 'label': _('v_analytics_header_periodType_last6months')},
                        {'value': 'allTime', 'label': _('v_analytics_header_periodType_allTime')},
                        {'value': 'custom', 'label': _('v_analytics_header_periodType_customPeriod')}
                    ]
                },
                {
                    '_com': 'Field.DatePicker',
                    'key': 'period',
                    'onChange': 'onChangePeriod',
                    'range': True,
                    'format': 'YYYY.MM.DD',
                    'disabled': self.period_type != 'custom',
                    'value': self.period
                }
            ]
        }

    def get_schema(self, params, request_data):
        return [
            {
                '_com': 'Statistics',
                'rows': [
                    {
                        'title': _('v_analytics_statistics_allLeads'),
                        'value': self.count_by_dates['lead_count'],
                        'span': 2
                    }
                ]
            },
            {
                '_com': 'Chart',
                'title': _('v_analytics_statistics_statisticsByDay'),
                'type': 'line',
                'data': self.data,
                'params': {
                    'padding': 'auto',
                    'xField': 'date',
                    'yField': 'leadCount',
                    'smooth': True,
                    'xAxis': {
                        'type': 'timeCat',
                        'tickCount': 5
                    },
                    # 'tooltip': {
                    #     'showTitle': False
                    # },
                    'label': {
                        'title': 'TITLE!'
                    }
                }
            }
        ]

    def get_methods(self, params, request_data):
        methods = compiled_methods.copy()

        methods['onChangePeriodType'] = method_with_vars(methods['onChangePeriodType'])
        methods['onChangePeriod'] = method_with_vars(methods['onChangePeriod'], {'PERIOD_TYPE': params.get('periodType')})

        return methods
