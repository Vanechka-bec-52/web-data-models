from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import config
from models import db, Partner

app = Flask(__name__)
app.config.from_object(config.Config)
app.config['SECRET_KEY'] = 'your-secret-key-here'
db.init_app(app)

@app.route("/")
def index():
    partners = Partner.query.all()
    return render_template("index.html", partners=partners)

@app.route("/add_partner", methods=["GET", "POST"])
def add_partner():
    if request.method == "POST":
        try:
            # Проверка данных
            name = request.form["name"].strip()
            partner_type = request.form["partner_type"].strip()
            rating = int(request.form["rating"])
            address = request.form["address"].strip()
            director_name = request.form["director_name"].strip()
            phone = request.form["phone"].strip()
            email = request.form["email"].strip()
            sales_volume = int(request.form["sales_volume"])
            
            #Создание партнёра
            partner = Partner(
                name=name,
                partner_type=partner_type,
                rating=rating,
                address=address,
                director_name=director_name,
                phone=phone,
                email=email,
                sales_volume=sales_volume
            )
            
            #Расчёт скидки
            partner.discount = partner.calculate_discount()
            
            # Сохранение в базу данных
            db.session.add(partner)
            db.session.commit()
            
            flash("Партнёр успешно добавлен","success")
            return redirect(url_for("index"))
        
        except ValueError:
            flash ("Ошибка: некорректный формат числовых данных","error")
        except Exception as e:
            flash(f"Ошибка при добавлении партнёра: {str(e)}","error")
        return redirect(url_for("add_partner"))
    
    return render_template("add_partner.html")

@app.route("/edit_partner/<int:partner_id>", methods=["GET", "POST"])
def edit_partner(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    
    if request.method == "POST":
        try:
            #Обновление данных
            partner.name = request.form["name"].strip()
            partner.partner_type = request.form["partner_type"].strip()
            partner.rating = int(request.form["rating"])
            partner.address = request.form["address"].strip()
            partner.director_name = request.form["director_name"].strip()
            partner.phone = request.form["phone"].strip()
            partner.email = request.form["email"].strip()
            partner.sales_volume = int(request.form["sales_volume"])
            
            #Перерасчет скидки
            partner.discount = partner.calculate_discount()
            
            db.session.commit()
            
            flash("Данные партнера успешно обновлены", "success")
            return redirect(url_for("index"))
            
        except ValueError:
            flash("Ошибка: некорректный формат числовых данных", "error")
        except Exception as e:
            flash(f"Ошибка при редактировании партнера: {str(e)}", "error")
        return redirect(url_for("edit_partner", partner_id=partner_id))
    
    return render_template("edit_partner.html", partner=partner)

#Удаление партнёра
@app.route("/delete/<int:partner_id>")
def delete_partner(partner_id):
    try:
        partner = Partner.query.get_or_404(partner_id)
        db.session.delete(partner)
        db.session.commit()
        flash("Партнёр успешно удален","success")
    except Exception as e:
        flash(f"Ошибка при удалении партнёра :{str(e)}","error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)