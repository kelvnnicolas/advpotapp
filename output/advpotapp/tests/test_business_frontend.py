import re
from django.test import TestCase, override_settings
from django.urls import reverse
from advpot.identity.models import User
from advpot.intake.models import Contact, Demand, BusinessAuthority
from advpot.cases.models import Case


@override_settings(DEBUG=True)
class BusinessFrontendTests(TestCase):
    pages = {'index': '/business/', 'team': '/business/equipe/', 'flows': '/business/fluxos/', 'subscription': '/business/assinatura/', 'integrations': '/business/integracoes/', 'settings': '/business/configuracoes/', 'contract': '/contratar/', 'return': '/contratar/retorno/'}

    def setUp(self):
        self.account = User.objects.create_user(username='business.ficticio')

    def test_business_requires_login_but_local_contract_is_public(self):
        for name, route in self.pages.items():
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200 if name in {'contract', 'return'} else 302)

    def test_named_routes_render_preview_and_do_not_mutate_domain(self):
        self.client.force_login(self.account)
        before = self.counts()
        for name, route in self.pages.items():
            self.assertEqual(reverse(f'business:{name}'), route)
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Prévia Business')
            self.assertContains(response, 'nenhuma cobrança')
        self.assertEqual(self.counts(), before)

    def counts(self):
        return tuple(model.objects.count() for model in [User, Contact, Demand, Case, BusinessAuthority])

    def test_mutations_are_not_available_in_frontend_checkpoint(self):
        self.client.force_login(self.account)
        before = self.counts()
        for route in self.pages.values():
            for method in ['post', 'put', 'delete']:
                self.assertEqual(getattr(self.client, method)(route).status_code, 405)
        self.assertEqual(self.counts(), before)

    @override_settings(DEBUG=False)
    def test_production_hides_all_preview_pages(self):
        self.client.force_login(self.account)
        for route in self.pages.values():
            self.assertEqual(self.client.get(route).status_code, 404)
        self.assertNotContains(self.client.get('/meu-trabalho/'), 'business/')

    def test_unknown_scenario_cannot_be_rendered_as_paid(self):
        self.client.force_login(self.account)
        for route in self.pages.values():
            self.assertEqual(self.client.get(route, {'scenario': 'payment-confirmed-by-client'}).status_code, 404)
        for scenario in ['active', 'pending', 'expired', 'cancelled']:
            response = self.client.get('/business/assinatura/', {'scenario': scenario})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['preview']['subscription']['access_state'], scenario)

    def test_preview_contract_never_invents_commercial_values_or_google_connection(self):
        from advpot.business_frontend.contracts import get_preview
        preview = get_preview('active')
        self.assertEqual(preview['schema_version'], 'advpot.business.frontend.v1')
        self.assertTrue(preview['is_preview'])
        for field in ['amount_minor', 'currency', 'interval', 'seats_included']:
            self.assertIsNone(preview['plan'][field])
        self.assertEqual(preview['workspace']['status'], 'disconnected')
        preview['business']['name'] = 'Mutação do chamador'
        self.assertNotEqual(get_preview('active')['business']['name'], 'Mutação do chamador')

    def test_static_preview_has_no_forms_that_submit_without_javascript(self):
        self.client.force_login(self.account)
        for route in ['/business/equipe/', '/business/fluxos/', '/business/configuracoes/', '/contratar/']:
            response = self.client.get(route)
            self.assertContains(response, 'data-preview-form')
            self.assertContains(response, 'type="button"')
            forms = re.findall(r'<form[^>]*data-preview-form[\s\S]*?</form>', response.content.decode())
            self.assertTrue(forms)
            for form in forms:
                self.assertNotIn('type="submit"', form)
                self.assertIn('<fieldset disabled', form)

    def test_checkout_return_links_preserve_the_origin_scenario(self):
        self.client.force_login(self.account)
        for scenario in ['active', 'pending', 'expired', 'cancelled']:
            response = self.client.get('/contratar/retorno/', {'scenario': scenario})
            panel = re.search(r'<section class="business-return">([\s\S]*?)</section>', response.content.decode()).group(1)
            self.assertIn(f'href="/business/assinatura/?scenario={scenario}"', panel)
            self.assertIn(f'href="/contratar/?scenario={scenario}"', panel)
