# Feilmeldinger og løsninger

## 1. Skrivefeil i SQLAlchemy — `db.Colum` og `db.text`

**Feilmelding:**
```
sqlalchemy.exc.ArgumentError: 'SchemaItem' object, such as a 'Column' or a 'Constraint' expected,
got <function text at 0x000002E6BD48EF00>
```

**Feil kode:**
```python
class Sections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Colum(db.text, nullable=True)
    topics = db.relationship('Topics', backref='section', lazy=True, cascade='all, delete-orphan')
```

**Problemer:**
- `db.Colum` → skal være `db.Column`
- `db.text` → datatyper må ha stor forbokstav: `db.Text`

**Fikset kode:**
```python
description = db.Column(db.Text, nullable=True)
```

---

## 2. Feil syntaks med `[]` og `()` i SQLAlchemy og Flask forms

**Feil kode:**
```python
@app.route('/index', methods=['GET', 'POST'])
@admin_required
def login():
    if request.method == 'POST':
        user = User.query.filter_by[username=request.form('username')].first()
```

**Problem:**
- Når man jobber med SQLAlchemy brukes `()`
- Når man jobber med form brukes `[]`

**Fikset kode:**
```python
user = User.query.filter_by(username=request.form['username']).first()
```

---

## 3. `SyntaxError` — `=` brukt i stedet for nøkkelord-argument

**Feilmelding:**
```
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

**Årsak:** Feil syntaks inne i `filter_by[]` (se feil nr. 2 over).

---

## 4. Feil logikk og manglende `''` rundt strenger

**Feil kode:**
```python
if request.method == 'POST':
    user = User.query.filter_by(username=request.form['username']).first()
    if user or check_password_hash(password_hash=request.form[password]).first()
```

**Problemer:**
- Glemte å sette `''` rundt `'password'` i `request.form[password]`
- Feil logikk: skrev `if user or check_password_hash` — skal være `if not user or not check_password_hash`
- Fikk feilmelding fordi den ikke fant noen tabell med `password_hash` — måtte spesifisere at den var på `user`-objektet: `user.password_hash`
- Hadde `.first()` på slutten — det kan man ikke ha når det ikke er en query

**Fikset kode:**
```python
if not user or not check_password_hash(user.password_hash, request.form['password']):
```