import pytest
from d4k_ms_ui.pagination import Pagination

def test_pagination_initialization():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': ''
    }
    pagination = Pagination(results, '/test')
    
    assert pagination.page == 1
    assert pagination.page_size == 10
    assert pagination.item_count == 25
    assert pagination.page_count == 3
    assert pagination.base_url == '/test'
    assert pagination.filter == ''

def test_pagination_with_partial_page():
    results = {
        'page': '1',
        'size': '10',
        'count': '22',  # This should still result in 3 pages
        'filter': ''
    }
    pagination = Pagination(results, '/test')
    assert pagination.page_count == 3

def test_link_generation():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': 'test'
    }
    pagination = Pagination(results, '/test')
    
    expected = '/test?page=2&size=10&filter=test'
    assert pagination.link(2) == expected

def test_link_generation_params():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': 'test'
    }
    pagination = Pagination(results, '/test', **{'params': {'sort': 'desc', 'category': 'books'}})
    
    expected = '/test?page=2&size=10&filter=test&sort=desc&category=books'
    assert pagination.link(2) == expected

def test_filter_disabled():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': ''
    }
    params = {'disable_filter': True}
    pagination = Pagination(results, '/test', **params)
    assert pagination.disable_filter == True
    assert pagination.filter_disabled() == 'disabled'
    assert pagination.filter_text() == 'Search disabled!'

def test_filter_enabled():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': ''
    }
    params = {'disable_filter': False}
    pagination = Pagination(results, '/test', **params)
    assert pagination.disable_filter == False
    assert pagination.filter_disabled() == ''
    assert pagination.filter_text() == 'Begin typing to search ...'

def test_autofocus():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': 'test'
    }
    pagination = Pagination(results, '/test')
    
    assert pagination.autofocus() == 'autofocus'
    
    results['filter'] = ''
    pagination = Pagination(results, '/test')
    assert pagination.autofocus() == ''

def test_page_info_structure():
    results = {
        'page': '2',
        'size': '10',
        'count': '30',
        'filter': ''
    }
    pagination = Pagination(results, '/test')
    pages = pagination.pages
    
    # Check first and last elements (prev and next arrows)
    assert pages[0]['text'] == '&laquo;'
    assert pages[-1]['text'] == '&raquo;'
    
    # Check current page is marked active
    current_page = next(page for page in pages if page['active'] == 'active')
    assert current_page['text'] == '2'

def test_base_link_methods():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': 'test'
    }
    pagination = Pagination(results, '/test')
    
    assert pagination.base_link(2, 20) == '/test?page=2&size=20'
    assert pagination.base_link_with_filter(2, 20) == '/test?page=2&size=20&filter=test' 

def test_base_link_methods_params():
    results = {
        'page': '1',
        'size': '10',
        'count': '25',
        'filter': 'test'
    }
    pagination = Pagination(results, '/test', **{'params': {'sort': 'desc', 'category': 'books'}})
    
    assert pagination.base_link(2, 20) == '/test?page=2&size=20&sort=desc&category=books'
    assert pagination.base_link_with_filter(2, 20) == '/test?page=2&size=20&filter=test&sort=desc&category=books' 

def test_pages():
    results = {
        'page': '10',
        'size': '10',
        'count': '200',
        'filter': ''
    }
    pagination = Pagination(results, '/test')
    
    assert pagination.build_page_info() == [
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=9&size=10&filter=',
            'text': '&laquo;',
        },
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=1&size=10&filter=',
            'text': '1',
        },
        {
            'active': '',
            'disabled': 'disabled',
            'link': '',
            'text': '...',
        },
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=7&size=10&filter=',
            'text': '7',
        },
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=8&size=10&filter=',
            'text': '8',
        },
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=9&size=10&filter=',
            'text': '9',
        },
        {
            'active': 'active',
            'disabled': '',
            'link': '/test?page=10&size=10&filter=',
            'text': '10',
        },
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=11&size=10&filter=',
            'text': '11',
        },
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=12&size=10&filter=',
            'text': '12',
        },
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=13&size=10&filter=',
            'text': '13',
        },
        {
            'active': '',
            'disabled': 'disabled',
            'link': '',
            'text': '...',
        },
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=20&size=10&filter=',
            'text': '20',
        },
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=11&size=10&filter=',
            'text': '&raquo;',
        },
    ]

def test_last_page():
    results = {
        'page': '20',
        'size': '10',
        'count': '200',
        'filter': ''
    }
    pagination = Pagination(results, '/test')
    
    assert pagination.build_page_info() == [
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=19&size=10&filter=',
            'text': '&laquo;',
        },
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=1&size=10&filter=',
            'text': '1',
        },
        {
            'active': '',
            'disabled': 'disabled',
            'link': '',
            'text': '...',
        },
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=17&size=10&filter=',
            'text': '17',
        },
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=18&size=10&filter=',
            'text': '18',
        },
        {
            'active': '',
            'disabled': '',
            'link': '/test?page=19&size=10&filter=',
            'text': '19',
        },
        {
            'active': 'active',
            'disabled': '',
            'link': '/test?page=20&size=10&filter=',
            'text': '20',
        },
        {
            'active': '',
            'disabled': 'disabled',
            'link': '/test?page=21&size=10&filter=',
            'text': '&raquo;',
        },
    ]
    