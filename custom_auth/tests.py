"""Тесты модуля авторизации"""
from datetime import timedelta

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from custom_auth.models import PasswordResetCode

User = get_user_model()


class PasswordResetCodeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )

    def test_not_expired_when_fresh(self):
        code = PasswordResetCode.objects.create(user=self.user, code='1234')
        self.assertFalse(code.is_expired())

    def test_expired_when_old(self):
        code = PasswordResetCode.objects.create(user=self.user, code='5678')
        code.created_at = timezone.now() - timedelta(minutes=15)
        code.save()
        self.assertTrue(code.is_expired())


class RegistrationViewTest(TestCase):
    def test_get_renders_form(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)

    def test_post_valid_creates_user_and_redirects(self):
        response = self.client.post(reverse('registration'), {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'securepass1',
            'passwordAnother': 'securepass1',
        })
        self.assertTrue(User.objects.filter(email='john@example.com').exists())
        self.assertEqual(response.status_code, 302)

    def test_post_password_mismatch_shows_error(self):
        response = self.client.post(reverse('registration'), {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'pass1',
            'passwordAnother': 'pass2',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)
        self.assertFalse(User.objects.filter(email='john@example.com').exists())

    def test_post_duplicate_email_shows_error(self):
        User.objects.create_user(
            username='john@example.com', email='john@example.com', password='existing'
        )
        response = self.client.post(reverse('registration'), {
            'firstName': 'Jane',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'newpass1',
            'passwordAnother': 'newpass1',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user@example.com', email='user@example.com', password='correctpass'
        )

    def test_get_renders_form(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_post_valid_credentials_redirects(self):
        response = self.client.post(reverse('login'), {
            'email': 'user@example.com',
            'password': 'correctpass',
        })
        self.assertEqual(response.status_code, 302)

    def test_post_invalid_credentials_shows_error(self):
        response = self.client.post(reverse('login'), {
            'email': 'user@example.com',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_post_unknown_email_shows_error(self):
        response = self.client.post(reverse('login'), {
            'email': 'nobody@example.com',
            'password': 'anypass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class PasswordResetRequestViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user@example.com', email='user@example.com', password='pass123'
        )

    def test_get_renders_form(self):
        response = self.client.get(reverse('password_reset_request'))
        self.assertEqual(response.status_code, 200)

    def test_post_valid_email_creates_code(self):
        response = self.client.post(reverse('password_reset_request'), {
            'email': 'user@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PasswordResetCode.objects.filter(user=self.user).exists())

    def test_post_unknown_email_shows_error(self):
        response = self.client.post(reverse('password_reset_request'), {
            'email': 'nobody@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_post_replaces_existing_code(self):
        PasswordResetCode.objects.create(user=self.user, code='0000')
        self.client.post(reverse('password_reset_request'), {'email': 'user@example.com'})
        self.assertEqual(PasswordResetCode.objects.filter(user=self.user).count(), 1)


class PasswordResetVerifyViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user@example.com', email='user@example.com', password='pass123'
        )
        self.code = PasswordResetCode.objects.create(user=self.user, code='4321')

    def test_get_renders_form(self):
        response = self.client.get(reverse('password_reset_verify'))
        self.assertEqual(response.status_code, 200)

    def test_post_valid_code_redirects_to_confirm(self):
        response = self.client.post(reverse('password_reset_verify'), {'code': '4321'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('password/reset/confirm', response['Location'])

    def test_post_invalid_code_returns_400(self):
        response = self.client.post(reverse('password_reset_verify'), {'code': '9999'})
        self.assertEqual(response.status_code, 400)

    def test_post_expired_code_returns_400(self):
        self.code.created_at = timezone.now() - timedelta(minutes=15)
        self.code.save()
        response = self.client.post(reverse('password_reset_verify'), {'code': '4321'})
        self.assertEqual(response.status_code, 400)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class PasswordResetConfirmViewTest(TestCase):
    """password_reset_confirm is an AJAX endpoint: GET → 404, POST → 200 text."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='user@example.com', email='user@example.com', password='pass123'
        )
        self.code = PasswordResetCode.objects.create(user=self.user, code='7777')

    def test_get_returns_404(self):
        response = self.client.get(
            reverse('password_reset_confirm', kwargs={'code': '7777'})
        )
        self.assertEqual(response.status_code, 404)

    def test_get_invalid_code_returns_404(self):
        response = self.client.get(
            reverse('password_reset_confirm', kwargs={'code': '0000'})
        )
        self.assertEqual(response.status_code, 404)

    def test_post_resets_password_and_deletes_code(self):
        old_password_hash = self.user.password
        response = self.client.post(
            reverse('password_reset_confirm', kwargs={'code': '7777'})
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.password, old_password_hash)
        self.assertFalse(PasswordResetCode.objects.filter(code='7777').exists())

    def test_post_invalid_code_returns_404(self):
        response = self.client.post(
            reverse('password_reset_confirm', kwargs={'code': '0000'})
        )
        self.assertEqual(response.status_code, 404)
