import os
import re
from django.test import TestCase
from django.conf import settings
from django.urls import reverse


class GamefolioTemplateTests(TestCase):
    def get_template(self, path_to_template):
        """
        Helper function to return the string representation of a template file.
        """
        with open(path_to_template, 'r') as f:
            template_str = f.read()
        return template_str

    def test_base_template_exists(self):
        """
        Tests whether the base template exists.
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'gamefolio_app', 'base.html')
        self.assertTrue(os.path.exists(template_base_path), "Base template does not exist.")

    def test_profile_template(self):
        """
        Test whether the profile template exists and renders correctly.
        """
        response = self.client.get(reverse('gamefolio_app:profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gamefolio_app/profile.html')

    def test_template_title_blocks(self):
        """
        Test whether the title blocks in each template are the expected values.
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'gamefolio_app')
        mappings = {
            reverse('gamefolio_app:index'): {'title_pattern': r'<title>(\s*|\n*)Gamefolio(\s*|\n*)-(\s*|\n*)Home(\s*|\n*)</title>',
                                             'template_filename': 'index.html'},
            reverse('gamefolio_app:list_profiles'): {'title_pattern': r'<title>(\s*|\n*)Gamefolio(\s*|\n*)-(\s*|\n*)User Profiles(\s*|\n*)</title>',
                                                      'template_filename': 'list_profiles.html'},
            reverse('gamefolio_app:profile', kwargs={'username': 'testuser'}): {'title_pattern': r'<title>(\s*|\n*)Gamefolio(\s*|\n*)-(\s*|\n*)Profile for testuser(\s*|\n*)</title>',
                                                                                 'template_filename': 'profile.html'},
            reverse('gamefolio_app:base'): {'title_pattern': r'<title>(\s*|\n*)Gamefolio(\s*|\n*)-(\s*|\n*)User Profiles(\s*|\n*)</title>',
                                                      'template_filename': 'base.html'},
        }

        for url in mappings.keys():
            title_pattern = mappings[url]['title_pattern']
            template_filename = mappings[url]['template_filename']
            block_title_pattern = mappings[url]['block_title_pattern']

            request = self.client.get(url)
            content = request.content.decode('utf-8')
            template_str = self.get_template(os.path.join(template_base_path, template_filename))

            self.assertTrue(re.search(title_pattern, content), f"Title pattern not found in {url}")
            self.assertTrue(re.search(block_title_pattern, template_str), f"There is no template block, are you using template inheritance correctly?")