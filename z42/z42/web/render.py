#coding:utf-8
import _env
from os.path import join
from z42.config import DEBUG
import os




from hmako.lookup import TemplateLookup
RENDER_PATH = [join(_env.PREFIX, 'html')]

template_lookup = TemplateLookup(
    directories=tuple(RENDER_PATH),
    disable_unicode=True,
    encoding_errors='ignore',
    default_filters=['str', 'h'],
    filesystem_checks=DEBUG,
    input_encoding='utf-8',
    output_encoding='',
    module_directory=join(_env.PREFIX, '_html'),
)

def render(htm, **kwds):
    #print htm,"!"*11
    mytemplate = template_lookup.get_template(htm)
    return mytemplate.render(**kwds)

if __name__ == '__main__':
    render('test.html', name='abc')
