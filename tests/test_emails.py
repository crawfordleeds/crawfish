from django.conf import settings
from django.core import mail
from django.test import TestCase, override_settings

from crawfish.emails import send_mail


class EmailsTests(TestCase):
    @override_settings(SERVER_EMAIL="help@crawfordleeds.com")
    def test_message__with_from_email(self):
        """Test sending an email with a from_email"""
        to_email = "crawford@crawfordleeds.com"
        from_email = "na@crawfordleeds.com"
        template_id = "d-73e65fa7b1cd4593a52eaab4d1f9a609"
        data = {"crawford@crawfordleeds.com": {"first_name": "Test First Name"}}
        resp = send_mail(
            to_email=to_email, from_email=from_email, template_id=template_id, data=data
        )

        expected_data = {"help@crawfordleeds.com": {"first_name": "Test First Name"}}
        self.assertTrue(resp)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].template_id, template_id)
        self.assertEqual(mail.outbox[0].merge_data, expected_data)
        self.assertEqual(mail.outbox[0].to, [settings.SERVER_EMAIL])
        self.assertEqual(mail.outbox[0].from_email, from_email)

    @override_settings(SERVER_EMAIL="help@crawfordleeds.com")
    def test_message_not_in_production(self):
        """ "
        Test the 'to' address gets set to the server email outside of a production app context where
        the server email is a str
        """
        to_email = "crawford@crawfordleeds.com"
        template_id = "d-73e65fa7b1cd4593a52eaab4d1f9a609"
        data = {"crawford@crawfordleeds.com": {"first_name": "Test First Name"}}
        resp = send_mail(to_email=to_email, template_id=template_id, data=data)

        expected_data = {"help@crawfordleeds.com": {"first_name": "Test First Name"}}
        self.assertTrue(resp)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].template_id, template_id)
        self.assertEqual(mail.outbox[0].merge_data, expected_data)
        self.assertEqual(mail.outbox[0].to, [settings.SERVER_EMAIL])

    @override_settings()
    def test_message__no_app_environment(self):
        """
        Test sending a message where the environment does not have the APP_ENVIRONMENT setting configured.py
        This should act as if in production
        """
        del settings.APP_ENVIRONMENT
        to_email = "crawford@crawfordleeds.com"
        template_id = "d-73e65fa7b1cd4593a52eaab4d1f9a609"
        data = {"crawford@crawfordleeds.com": {"first_name": "Test First Name"}}
        resp = send_mail(to_email=to_email, template_id=template_id, data=data)

        self.assertTrue(resp)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].template_id, template_id)
        self.assertEqual(mail.outbox[0].merge_data, data)
        self.assertEqual(mail.outbox[0].to, [to_email])

    @override_settings(SERVER_EMAIL="help@crawfordleeds.com")
    def test_message_not_in_production__to_list(self):
        """
        Test the send mail method where the to_email contains a list of emails,
        thus, each to email should be individually overridden to the server email
        """
        to_email = ["crawford@crawfordleeds.com", "someoneelse@crawfordleeds.com"]
        template_id = "d-73e65fa7b1cd4593a52eaab4d1f9a609"

        data = {
            "crawford@crawfordleeds.com": {"first_name": "Test First Name 0"},
            "someoneelse@crawfordleeds.com": {"first_name": "Test First Name 1"},
        }

        resp = send_mail(to_email=to_email, template_id=template_id, data=data)
        self.assertEqual(resp, 2)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].template_id, template_id)
        self.assertEqual(
            mail.outbox[0].merge_data,
            {settings.SERVER_EMAIL: {"first_name": "Test First Name 0"}},
        )
        self.assertEqual(mail.outbox[0].to, [settings.SERVER_EMAIL])
        self.assertEqual(mail.outbox[1].template_id, template_id)
        self.assertEqual(
            mail.outbox[1].merge_data,
            {settings.SERVER_EMAIL: {"first_name": "Test First Name 1"}},
        )
        self.assertEqual(mail.outbox[1].to, [settings.SERVER_EMAIL])

    @override_settings(
        SERVER_EMAIL="help@crawfordleeds.com", APP_ENVIRONMENT="production"
    )
    def test_message_in_production__to_list(self):
        """
        Test the send mail method where the to_email contains a list of emails,
        thus, each to email should be individually overridden to the server email
        """
        to_email = ["crawford@crawfordleeds.com", "someoneelse@crawfordleeds.com"]
        template_id = "d-73e65fa7b1cd4593a52eaab4d1f9a609"

        data = {
            "crawford@crawfordleeds.com": {"first_name": "Test First Name 0"},
            "someoneelse@crawfordleeds.com": {"first_name": "Test First Name 1"},
        }

        resp = send_mail(to_email=to_email, template_id=template_id, data=data)
        self.assertEqual(resp, 2)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].template_id, template_id)
        self.assertEqual(
            mail.outbox[0].merge_data,
            {"crawford@crawfordleeds.com": {"first_name": "Test First Name 0"}},
        )
        self.assertEqual(mail.outbox[0].to, ["crawford@crawfordleeds.com"])
        self.assertEqual(mail.outbox[1].template_id, template_id)
        self.assertEqual(
            mail.outbox[1].merge_data,
            {"someoneelse@crawfordleeds.com": {"first_name": "Test First Name 1"}},
        )
        self.assertEqual(mail.outbox[1].to, ["someoneelse@crawfordleeds.com"])

    @override_settings(APP_ENVIRONMENT="production")  # "fake" a production environment
    def test_message_in_production(self):
        """Override the settings and test the message is sent when the app is in production"""

        # We don't need to enable sandbox mode in testing because django automatically saves every outgoing
        # email in django.core.mail.outbox.
        # Reference: https://timonweb.com/tutorials/testing-email-in-django/
        # If we had to, this is how we enable enable sandbox mode from esp_extra
        # https://anymail.readthedocs.io/en/stable/esps/sendgrid/#esp-extra-support
        # esp_extra = {"mail_settings": {"sandbox_mode": {"enable": True}}}

        to_email = "crawford@crawfordleeds.com"
        template_id = "d-73e65fa7b1cd4593a52eaab4d1f9a609"
        data = {"crawford@crawfordleeds.com": {"first_name": "Test First Name"}}
        resp = send_mail(to_email=to_email, template_id=template_id, data=data)

        self.assertTrue(resp)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].template_id, template_id)
        self.assertEqual(mail.outbox[0].merge_data, data)
        self.assertEqual(mail.outbox[0].to, [to_email])
