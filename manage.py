from flask_script import Manager, Server, Shell, Command
from flask_migrate import Migrate, MigrateCommand
from grattitude import app, db
from sqlalchemy import and_, or_, not_
from grattitude.models.user import User
import time


class ScheduleIntros(Command):
    'A command to run Application Intros'
    def run(self):
        """Run scheduled job."""
        print('Finding Unintroduced Users...')
        unintroduced_users = User.query.filter_by(introduced=False).all()
        if not len(unintroduced_users):
            print('Nobody to be introduced to ...  =[')
        for user in unintroduced_users: 
            print('Users:', user, " is getting an introduction!")
            user.make_introduction()
        print('Done!')

class ScheduleGrattitude(Command):
    'A command to run Grattitude Reminders'
    def run(self):
        """Run scheduled job."""
        print('Finding opted in and welcomed Users...')
        introduced_opedin_users = User.query.filter_by(introduced=True).filter_by(opted_in=True).all()
        if not len(introduced_opedin_users):
            print('Nobody to ask grattitude of ...  =[')
        for user in introduced_opedin_users: 
            print('Users:', user, " is getting asked! =D")
            user.ask_grattitude()
        print('Done!')

def make_shell_context():
    return dict(app=app, db=db, User=User)


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('runserver', Server(host='0.0.0.0', port=80))
manager.add_command('db', MigrateCommand)
manager.add_command('intros', ScheduleIntros)
manager.add_command('reminders', ScheduleGrattitude)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
