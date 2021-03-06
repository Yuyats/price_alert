import uuid
import src.models.users.constants as UserConstants
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
from src.models.alerts.alert import Alert


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        this method verifies that an e-mail/password combo (as sent by the site form) is valid or not.
        Checks that the e-mail exists and that the password associated to that e-mail is correct.
        :param email:
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """

        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        if user_data is None:
            raise UserErrors.UserNotExistsError('your user does not exist.')

        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError('your password was wrong.')

        return True

    @staticmethod
    def register_user(email, password):
        """
        This method registers a user using email and password
        the password already comes hashed as sha-512

        :param email:
        :param password: sha-512 hashed
        :return: true if registered successfully, or False otherwise
        """

        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        if user_data is not None:
            # already registered
            raise UserErrors.UserAlreadyRegisteredError("Email is registered already")
        if not Utils.email_is_valid(email):
            # email is not valid form
            raise UserErrors.InvalidEmailError("E-mail not right format")

        User(email, Utils.hash_password(password)).save_to_db()

        return True


    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email': email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)
