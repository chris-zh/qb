import time
from . import db
from datetime import datetime


class Overtime(db.Model):
    __bind_key__ = 'tpdev'
    __tablename__ = 'ebao_leave'
    apply_id = db.Column(db.Integer, primary_key=True, default=str(time.time()))
    apply_name = db.Column(db.String(64))
    apply_reason = db.Column(db.String(64))
    current_version = db.Column(db.String(64))
    week_number = db.Column(db.String(64))
    apply_date = db.Column(db.DateTime(), default=datetime.utcnow())
    overtime_date = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self):
        # return '<apply_id %r apply_name %r apply_reason %r>' % self.apply_id, self.apply_name, self.apply_reason
        return u'<Record: {0},{1},{2},{3},{4}>'.format(self.apply_id, self.apply_name, self.apply_reason,
                                                       self.current_version, self.week_number)


#new = Overtime(apply_name='test', apply_reason='test', current_version='3.91', week_number='9')