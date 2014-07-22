from wtforms.widgets import HTMLString, html_params

from jinja2 import escape
from flask import url_for

from mongoengine.fields import GridFSProxy, ImageGridFsProxy

from . import helpers


class MongoFileInput(object):
    """
        Renders a file input chooser field.
    """
    template = ('<div>'
                ' <i class="glyphicon glyphicon-file"></i>%(name)s %(size)dk (%(content_type)s)'
                ' <input type="checkbox" name="%(marker)s">Delete</input>'
                '</div>')

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)

        placeholder = ''
        if field.data and isinstance(field.data, GridFSProxy):
            data = field.data

            placeholder = self.template % {
                'name': escape(data.name),
                'content_type': escape(data.content_type),
                'size': data.length // 1024,
                'marker': '_%s-delete' % field.name
            }

        return HTMLString('%s<input %s>' % (placeholder,
                                            html_params(name=field.name,
                                                        type='file',
                                                        **kwargs)))


class MongoImageInput(object):
    """
        Renders a file input chooser field.
    """
    template = ('<li class="image-thumbnail">'
                ' <img src="%(thumb)s"/>'
                '</li>'
                '<li>'
                ' <input type="checkbox" name="%(marker)s">Apagar Imagem</input>'
                '</li>')

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)

        placeholder = ''
        if field.data and isinstance(field.data, ImageGridFsProxy):
            args = helpers.make_thumb_args(field.data)
            placeholder = self.template % {
                'thumb': url_for('.api_file_view', **args),
                'marker': '_%s-delete' % field.name
            }

        return HTMLString('<ul class="list-inline form-inline">%s<li><input %s></li></ul>' % (placeholder,
                                            html_params(name=field.name,
                                                        type='file',
                                                        **kwargs)))
