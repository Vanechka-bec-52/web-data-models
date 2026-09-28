from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Таблица базы данных для хранения данных о партнёрах
class Partner(db.Model):
    __tablename__ = "partners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    partner_type = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    address = db.Column(db.String(200), nullable=False)
    director_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    sales_volume = db.Column(db.Integer, nullable=False, default=0)
    discount = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    #Расчёт индивидуальной скидки для партнёра
    def calculate_discount(self):
        if self.sales_volume >= 300000:
            return 15
        elif self.sales_volume >= 50000:
            return 10
        elif self.sales_volume >= 10000:
            return 5
        else:
            return 0
        
    def __repr__(self):
        return f"Partner(id={self.id}, name={self.name})"