class User():
    def __init__(self, id, auth, active, admin, user = None):
        self.id = id
        self.auth = auth
        self.active = active
        self.admin = admin
        self.user = user

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
        User.__init__(self, '', False, False, False, None)

def paymentUserToWebUser(payment_user):
    if payment_user is None:
        return None
    return User(payment_user.id, True, True, True, payment_user)

def get(payment, id):
    payment_user = payment.getUserById(int(id))
    return paymentUserToWebUser(payment_user)

def validate(payment, username, password):
    payment_user = payment.getUserWithLogin(username, password)
    return paymentUserToWebUser(payment_user)