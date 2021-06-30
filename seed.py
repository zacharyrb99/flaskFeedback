from re import U
from models import db, User, Feedback
from app import app

#create tables
db.drop_all()
db.create_all()

zach = User(username='zacharyrb99', password='Zb112099', email='zacharyrb99@live.com', first_name='Zach', last_name='Boudreaux')
mariah = User(username='mariah0118', password='Bowser0118!', email='mariahmckaye2000@gmail.com', first_name='Mariah', last_name='Rick')
laura = User(username='lauraeb71', password='lauraeb71', email='lauraeb71@hotmail.com', first_name='Laura', last_name='Boudreaux')
byron = User(username='byronjb66', password='byronjb66', email='byronjb66@hotmail.com', first_name='Byron', last_name='Boudreaux')

f1 = Feedback(title='Feedback1', content='Hello this is the first post', username='zacharyrb99')
f2 = Feedback(title='Feedback2', content='Hello this is the second post', username='mariah0118')
f3 = Feedback(title='Feedback3', content='Hello this is the third post', username='lauraeb71')
f4 = Feedback(title='Feedback4', content='Hello this is the fourth post', username='byronjb66')

u_list = [zach, mariah, laura, byron]
f_list = [f1, f2, f3, f4]

db.session.add_all(u_list)
db.session.commit()

db.session.add_all(f_list)
db.session.commit()