Feil meldinger:

``` python
class Sections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Colum(db.text, nullable=True)   
    topics = db.relationship('Topics', backref='section', lazy=True, cascade='all, delete-orphan')
    
```

Her hadde jeg skrevet db.Colum og db.text.
Det er db.Column for det første.
FOR det andre må man gi datatyper med stor forbokstav som `db.Text` ellers aksepteres den ikke som datatype.

---

```python
@app.route('/index', methods=['GET', 'POST'])
@admin_required
def login():
    if request.method == 'POST':
        user = User.query.filter_by[username=request.form('username')].first()
```

Her hadde jeg feil syntax med [] og ().  
Når man jobber med Sqlalchemy er det ().
Når man jobber med form er det []

---

```python
@app.route('/index', methods=['GET', 'POST'])
@admin_required
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user or check_password_hash(password_hash=request.form[password]).first()
````
Når jeg sammenlikner eller gir noe et navn så glemmer jeg ofte ¨sette ''.
Jeg hadde også feil logik. Jeg skrev `if user or check_password_hash.`
Det skal egentlig være `if not user or not check_password_hash`

Fikk feilmelding fordi den ikke fant noe tabel med passordhash fordi jeg ikke definerte hvor den var.
Fix: ' if not user or not check_password_hash(user.password_hash, password_hash=request.form['password']).first():'