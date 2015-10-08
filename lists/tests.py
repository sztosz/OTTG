from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from .models import Item, List
from .views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')

        self.assertEqual(response.content.decode(), expected_html)


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        to_do_list = List()
        to_do_list.save()
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.to_do_list = to_do_list
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.to_do_list = to_do_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, to_do_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item.text)
        self.assertEqual(second_saved_item.text, second_item.text)
        self.assertEqual(first_saved_item.to_do_list, to_do_list)
        self.assertEqual(second_saved_item.to_do_list, to_do_list)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        to_do_list = List.objects.create()
        Item.objects.create(text='item 1', to_do_list=to_do_list)
        Item.objects.create(text='item 2', to_do_list=to_do_list)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')


class NewListTest(TestCase):
    def test_home_page_can_save_a_POST_request(self):
        self.client.post('/lists/new', {'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_home_page_can_redirect_after_POST(self):
        response = self.client.post('/lists/new', {'item_text': 'A new list item'})

        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
