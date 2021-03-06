# -*- coding: utf-8 -*-
"""Model unit tests"""
from datetime import datetime

from strength_log.models import SquatPersonalRecord


class TestUser:
    """ User tests"""

    def test_new_user(self, new_user):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check email, password, authenticated
        """
        assert new_user.email == "ryan.sheppard@gmail.com"
        assert new_user.hashed_password != "strengthlog"
        assert new_user.authenticated == False

    def test_created_at_defaults_to_datetime(self, new_user):
        assert bool(new_user.created_at)
        assert isinstance(new_user.created_at, datetime)

    def test_setting_password(self, new_user):
        """
        GIVEN an existing User
        WHEN the password for the user is set
        THEN check the password is stored correctly and not as plaintext
        """
        new_user.set_password("MyNewPassword")
        assert new_user.hashed_password != "MyNewPassword"
        assert new_user.is_correct_password("MyNewPassword")
        assert not new_user.is_correct_password("MyNewPassword2")
        assert not new_user.is_correct_password("FlaskIsAwesome")

    def test_user_id(self, new_user):
        """
        GIVEN an existing User
        WHEN the ID of the user is defined to a value
        THEN check the user ID returns a string (and not an integer) as needed by Flask-WTF
        """
        new_user.id = 17
        assert isinstance(new_user.get_id(), str)
        assert not isinstance(new_user.get_id(), int)
        assert new_user.get_id() == "17"


class TestPersonalRecords:
    def test_new_squat_records(self):
        """
        Given a SquatPersonalRecord Model
        When a new SquatPersonalRecord is created
        Then check one, two, three, four, five
        """
        squat_personal_records = SquatPersonalRecord(
            one_rep=315, two_reps=305, three_reps=295, four_reps=285, five_reps=275,
        )
        assert squat_personal_records.one_rep == 315
        assert squat_personal_records.two_reps == 305
        assert squat_personal_records.three_reps == 295
        assert squat_personal_records.four_reps == 285
        assert squat_personal_records.five_reps == 275
