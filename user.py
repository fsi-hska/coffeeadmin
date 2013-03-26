class User():
    def __init__(self, id, auth, active, admin):
        self.id = id
        self.auth = auth
        self.active = active
        self.admin = admin

    def is_authenticated(self):
        return self.auth

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.admin

    def get_id(self):
        return self.id

class AnonymousUser(User):
    def __init__(self):
        User.__init__(self, '', False, False, False)

def get(payment, id):
    pass