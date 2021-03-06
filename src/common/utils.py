from passlib.handlers.pbkdf2 import pbkdf2_sha512
import re


class Utils(object):
    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')

        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        """

        :param password:
        :return:
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password user sent matches that of the database
        The database password is encrypted more than the user's password at this stage.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if password match, False otherwise
        """

        return pbkdf2_sha512.verify(password, hashed_password)
