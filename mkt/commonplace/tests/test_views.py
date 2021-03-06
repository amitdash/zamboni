from django.conf import settings

import mock
from nose import SkipTest
from nose.tools import eq_

import amo.tests
from amo.utils import reverse


class TestCommonplace(amo.tests.TestCase):

    def test_fireplace(self):
        res = self.client.get('/server.html')
        self.assertTemplateUsed(res, 'commonplace/index.html')
        self.assertEquals(res.context['repo'], 'fireplace')

    def test_commbadge(self):
        res = self.client.get('/comm/')
        self.assertTemplateUsed(res, 'commonplace/index.html')
        self.assertEquals(res.context['repo'], 'commbadge')

    def test_rocketfuel(self):
        res = self.client.get('/curation/')
        self.assertTemplateUsed(res, 'commonplace/index.html')
        self.assertEquals(res.context['repo'], 'rocketfuel')

    def test_fireplace_persona_js_not_included_on_firefox_os(self):
        # Temporarily enabling include.js shim (bug 992334).
        raise SkipTest

        for url in ('/server.html?mccs=blah',
                    '/server.html?mcc=blah&mnc=blah',
                    '/server.html?nativepersona=true'):
            res = self.client.get(url)
            self.assertNotContains(res, 'login.persona.org/include.js')

    def test_fireplace_persona_js_is_included_elsewhere(self):
        for url in ('/server.html', '/server.html?mcc=blah'):
            res = self.client.get(url)
            self.assertContains(res, 'login.persona.org/include.js" async')

    def test_rocketfuel_persona_js_is_included(self):
        for url in ('/curation/', '/curation/?nativepersona=true'):
            res = self.client.get(url)
            self.assertContains(res, 'login.persona.org/include.js" defer')


class TestAppcacheManifest(amo.tests.TestCase):

    def test_no_repo(self):
        if 'fireplace' not in settings.COMMONPLACE_REPOS_APPCACHED:
            raise SkipTest

        res = self.client.get(reverse('commonplace.appcache'))
        eq_(res.status_code, 404)

    def test_bad_repo(self):
        if 'fireplace' not in settings.COMMONPLACE_REPOS_APPCACHED:
            raise SkipTest

        res = self.client.get(reverse('commonplace.appcache'),
                              {'repo': 'rocketfuel'})
        eq_(res.status_code, 404)

    @mock.patch('mkt.commonplace.views.get_build_id', new=lambda x: 'p00p')
    @mock.patch('mkt.commonplace.views.get_imgurls')
    def test_good_repo(self, get_imgurls_mock):
        if 'fireplace' not in settings.COMMONPLACE_REPOS_APPCACHED:
            raise SkipTest

        img = '/media/img/icons/eggs/h1.gif'
        get_imgurls_mock.return_value = [img]
        res = self.client.get(reverse('commonplace.appcache'),
                              {'repo': 'fireplace'})
        eq_(res.status_code, 200)
        assert '# BUILD_ID p00p' in res.content
        img = img.replace('/media/', '/media/fireplace/')
        assert img + '\n' in res.content
