"""Содержит тесты ядра системы"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import ShortedUrl, Qr
from core.utils import generate_short_url, create_shorted_url

User = get_user_model()


class GenerateShortUrlTest(TestCase):
    def test_returns_correct_length(self):
        code = generate_short_url()
        self.assertEqual(len(code), 6)

    def test_returns_alphanumeric(self):
        code = generate_short_url()
        self.assertTrue(code.isalnum())

    def test_returns_unique_codes(self):
        codes = {generate_short_url() for _ in range(50)}
        self.assertEqual(len(codes), 50)


class CreateShortedUrlTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='pass123',
        )

    def test_creates_for_authenticated_user(self):
        url = create_shorted_url(self.user, 'http://example.com')
        self.assertEqual(url.author, self.user)
        self.assertEqual(url.original_url, 'http://example.com')

    def test_creates_anonymous(self):
        anon = self.client.get('/').wsgi_request.user
        url = create_shorted_url(anon, 'http://example.com')
        self.assertIsNone(url.author)

    def test_saved_to_db(self):
        url = create_shorted_url(self.user, 'http://example.com')
        self.assertTrue(ShortedUrl.objects.filter(pk=url.pk).exists())


class IndexViewTest(TestCase):
    def test_redirects_to_linker(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('linker'), fetch_redirect_response=False)


class LinkerViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )
        self.short = ShortedUrl.objects.create(
            author=self.user,
            original_url='http://example.com',
            short_url='abc123',
        )

    def test_renders_empty(self):
        response = self.client.get(reverse('linker'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['url'])

    def test_renders_with_valid_code(self):
        response = self.client.get(reverse('linker_with_url', args=['abc123']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['url'], self.short)

    def test_404_for_missing_code(self):
        response = self.client.get(reverse('linker_with_url', args=['xxxxxx']))
        self.assertEqual(response.status_code, 404)


class GenerateUrlViewTest(TestCase):
    def test_post_valid_url_creates_and_redirects(self):
        response = self.client.post(reverse('generate_url'), {'url': 'http://example.com'})
        self.assertEqual(ShortedUrl.objects.filter(original_url='http://example.com').count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_post_javascript_scheme_rejected(self):
        response = self.client.post(reverse('generate_url'), {'url': 'javascript:alert(1)'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ShortedUrl.objects.count(), 0)

    def test_post_no_scheme_rejected(self):
        response = self.client.post(reverse('generate_url'), {'url': 'example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ShortedUrl.objects.count(), 0)

    def test_get_redirects(self):
        response = self.client.get(reverse('generate_url'))
        self.assertEqual(response.status_code, 302)


class GenerateQrViewTest(TestCase):
    def test_post_valid_url_creates_qr_entry(self):
        response = self.client.post(reverse('generate_qr'), {'url': 'http://example.com'})
        self.assertEqual(response.status_code, 302)
        qs = ShortedUrl.objects.filter(original_url='http://example.com', is_only_qr=True)
        self.assertEqual(qs.count(), 1)

    def test_post_ftp_scheme_rejected(self):
        response = self.client.post(reverse('generate_qr'), {'url': 'ftp://bad.example'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ShortedUrl.objects.count(), 0)

    def test_get_redirects(self):
        response = self.client.get(reverse('generate_qr'))
        self.assertEqual(response.status_code, 302)


class FavoriteUrlsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )
        ShortedUrl.objects.create(
            author=self.user, original_url='http://fav.example.com',
            short_url='fav001', is_favorite=True,
        )
        ShortedUrl.objects.create(
            author=self.user, original_url='http://nonfav.example.com',
            short_url='nfv001', is_favorite=False,
        )

    def test_requires_auth(self):
        response = self.client.get(reverse('favorite_urls'))
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_returns_only_favorites(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('favorite_urls'))
        self.assertEqual(response.status_code, 200)
        urls = list(response.context['urls'])
        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0].short_url, 'fav001')


class HistoryUrlsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )
        ShortedUrl.objects.create(
            author=self.user, original_url='http://example.com', short_url='his001',
        )

    def test_requires_auth(self):
        response = self.client.get(reverse('history_urls'))
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_returns_history(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('history_urls'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('urls_by_dates', response.context)

    def test_invalid_date_does_not_crash(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('history_urls'), {'date': 'not-a-date'})
        self.assertEqual(response.status_code, 200)


class FavoriteQrsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )

    def test_requires_auth(self):
        response = self.client.get(reverse('favorite_qrs'))
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_renders_for_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('favorite_qrs'))
        self.assertEqual(response.status_code, 200)


class HistoryQrsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )

    def test_requires_auth(self):
        response = self.client.get(reverse('history_qrs'))
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_invalid_date_does_not_crash(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('history_qrs'), {'date': 'bad-date'})
        self.assertEqual(response.status_code, 200)


class MakeUrlFavoriteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )
        self.short = ShortedUrl.objects.create(
            author=self.user, original_url='http://example.com', short_url='mkfav1',
        )

    def test_requires_auth(self):
        response = self.client.post(
            reverse('make_url_favorite'), {'url': 'mkfav1', 'title': 'My Link'}
        )
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_marks_as_favorite(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse('make_url_favorite'), {'url': 'mkfav1', 'title': 'My Link'}
        )
        self.short.refresh_from_db()
        self.assertTrue(self.short.is_favorite)
        self.assertEqual(self.short.title, 'My Link')

    def test_get_redirects_to_linker(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('make_url_favorite'))
        self.assertEqual(response.status_code, 302)


class RemoveUrlFavoriteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )
        self.short = ShortedUrl.objects.create(
            author=self.user, original_url='http://example.com',
            short_url='rmfav1', is_favorite=True,
        )

    def test_requires_auth(self):
        response = self.client.post(reverse('remove_url_favorite'), {'url': 'rmfav1'})
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)

    def test_removes_favorite(self):
        self.client.force_login(self.user)
        self.client.post(reverse('remove_url_favorite'), {'url': 'rmfav1'})
        self.short.refresh_from_db()
        self.assertFalse(self.short.is_favorite)


class DeleteUrlViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )
        self.short = ShortedUrl.objects.create(
            author=self.user, original_url='http://example.com',
            short_url='del001', is_favorite=True,
        )

    def test_removes_from_favorites(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse('delete_url_title'), {'url': 'del001'},
            HTTP_REFERER='http://testserver/urls/favorite',
        )
        self.short.refresh_from_db()
        self.assertFalse(self.short.is_favorite)

    def test_no_referer_does_not_crash(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_url_title'), {'url': 'del001'})
        self.assertEqual(response.status_code, 302)


class UpdateUrlTitleViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )
        self.short = ShortedUrl.objects.create(
            author=self.user, original_url='http://example.com', short_url='ttl001',
        )

    def test_updates_title(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse('update_url_title'), {'url': 'ttl001', 'title': 'New Title'},
            HTTP_REFERER='http://testserver/',
        )
        self.short.refresh_from_db()
        self.assertEqual(self.short.title, 'New Title')

    def test_no_referer_does_not_crash(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('update_url_title'), {'url': 'ttl001', 'title': 'Title'},
        )
        self.assertEqual(response.status_code, 302)


class RedirectToUrlViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )
        self.short = ShortedUrl.objects.create(
            author=self.user, original_url='http://example.com', short_url='redir1',
        )

    def test_returns_js_redirect_page(self):
        response = self.client.get(f'/{self.short.short_url}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Redirecting', response.content)

    def test_404_for_missing_code(self):
        response = self.client.get('/xxxxxx')
        self.assertEqual(response.status_code, 404)


class PricePrivacyViewTest(TestCase):
    def test_price_renders(self):
        response = self.client.get(reverse('price'))
        self.assertEqual(response.status_code, 200)

    def test_privacy_renders(self):
        response = self.client.get(reverse('privacy'))
        self.assertEqual(response.status_code, 200)


class XssProtectionTest(TestCase):
    """redirect_with_js must not embed raw URLs into HTML output."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='u@example.com', email='u@example.com', password='pass123'
        )

    def test_xss_payload_not_rendered_raw(self):
        malicious = ShortedUrl.objects.create(
            author=self.user,
            original_url='http://x.com/</script><script>alert(1)</script>',
            short_url='xss001',
        )
        response = self.client.get(f'/{malicious.short_url}')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'<script>alert(1)</script>', response.content)
