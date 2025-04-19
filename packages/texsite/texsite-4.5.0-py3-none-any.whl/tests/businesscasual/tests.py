from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase

from texsite.businesscasual.models import BusinessCasualPage


class BusinessCasualTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        try:
            self.page = BusinessCasualPage.objects.get(pk=2)
        except ObjectDoesNotExist:
            pass

        self.response = self.client.get('/business-casual-page/')


class BusinessCasualPageTest(BusinessCasualTestCase):
    fixtures = ['site.json', 'user.json', 'businesscasual.json']

    def test_business_casual_with_minimal_content_rendered(self):
        self.assertTemplateUsed(
            self.response, 'texsitebusinesscasual/business_casual_page.html'
        )
        self.assertInHTML(
            '<div class="brand">Texsite site</div>',
            str(self.response.content),
        )
        self.assertInHTML(
            '<div class="address-bar">Business Casual page</div>',
            str(self.response.content),
        )
