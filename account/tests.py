"""Тесты для приложения аккаунтов"""
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )

    def test_requires_auth(self):
        response = self.client.get(reverse('account'))
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_renders_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)


class AccountUpdatePasswordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='oldpass123'
        )

    def test_requires_auth(self):
        response = self.client.get(reverse('account_password'))
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_changes_password_successfully(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('account_update_password'), {
            'current_password': 'oldpass123',
            'password1': 'newpass456',
            'password2': 'newpass456',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass456'))

    def test_user_stays_logged_in_after_password_change(self):
        self.client.force_login(self.user)
        self.client.post(reverse('account_update_password'), {
            'current_password': 'oldpass123',
            'password1': 'newpass456',
            'password2': 'newpass456',
        })
        # session should still be valid — account page returns 200
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_wrong_current_password_shows_error(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('account_update_password'), {
            'current_password': 'wrongpass',
            'password1': 'newpass456',
            'password2': 'newpass456',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('answer', response.context)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('oldpass123'))

    def test_password_mismatch_shows_error(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('account_update_password'), {
            'current_password': 'oldpass123',
            'password1': 'newpass456',
            'password2': 'different789',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('answer', response.context)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('oldpass123'))


class AccountUpdateDataTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com',
            password='pass123', first_name='Old', last_name='Name',
        )

    def test_requires_auth(self):
        response = self.client.post(reverse('account_update_data'), {
            'first_name': 'New', 'last_name': 'Name', 'email': 'new@example.com'
        })
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_updates_name_and_email(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('account_update_data'), {
            'first_name': 'New',
            'last_name': 'Name',
            'email': 'newemail@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'New')
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_duplicate_email_shows_error(self):
        other = User.objects.create_user(
            username='other@example.com', email='other@example.com', password='pass123'
        )
        self.client.force_login(self.user)
        response = self.client.post(reverse('account_update_data'), {
            'first_name': 'New',
            'last_name': 'Name',
            'email': 'other@example.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('answer', response.context)

    def test_can_keep_own_email(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('account_update_data'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'u@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')


class AvatarViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )

    def test_avatar_update_requires_auth(self):
        avatar = SimpleUploadedFile('a.jpg', b'imgdata', content_type='image/jpeg')
        response = self.client.post(reverse('avatar_update'), {'avatar': avatar})
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_avatar_upload_redirects_to_account(self):
        self.client.force_login(self.user)
        avatar = SimpleUploadedFile('avatar.jpg', b'fake_image_data', content_type='image/jpeg')
        response = self.client.post(reverse('avatar_update'), {'avatar': avatar})
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(bool(self.user.avatar))

    def test_avatar_remove_requires_auth(self):
        response = self.client.post(reverse('avatar_remove'))
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_avatar_remove_clears_avatar(self):
        self.user.avatar = SimpleUploadedFile('av.jpg', b'data', content_type='image/jpeg')
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.post(reverse('avatar_remove'))
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertFalse(bool(self.user.avatar))


class AccountPricePasswordPagesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )

    def test_account_price_requires_auth(self):
        response = self.client.get(reverse('account_price'))
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_account_price_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account_price'))
        self.assertEqual(response.status_code, 200)

    def test_account_password_requires_auth(self):
        response = self.client.get(reverse('account_password'))
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_account_password_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account_password'))
        self.assertEqual(response.status_code, 200)
