from jinja2 import Environment, PackageLoader

_templates = Environment(loader=PackageLoader('intercom', 'templates'))


def accept(timeout_seconds, phone_number):
    template = _templates.get_template('accept.xml')
    return template.render(
        timeout_seconds=timeout_seconds,
        phone_number=phone_number)


def grant(grant_digits):
    template = _templates.get_template('grant.xml')
    return template.render(grant_digits=grant_digits)


def reject():
    template = _templates.get_template('reject.xml')
    return template.render()
