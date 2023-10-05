import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/credits'),
        ('get_html', '/sources'),
        ('get_html', '/sources/Kondic2019.snippet.html'),
        ('get_html', '/languages'),
        ('get_html', '/languages/Alotepec'),
        ('get_dt', '/languages?iSortingCols=1&iSortCol_0=0'),
        ('get_html', '/parameters'),
        ('get_html', '/parameters/8_i'),
        ('get_html', '/contributors'),
        ('get_html', '/contributions'),
        ('get_html', '/valuesets'),
        ('get_html', '/values/Alotepec-1_one-1'),
        ('get_dt', '/parameters?sSearch_0=right'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)

