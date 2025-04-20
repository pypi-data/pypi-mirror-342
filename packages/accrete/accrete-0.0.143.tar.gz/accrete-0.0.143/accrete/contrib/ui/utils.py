import ast
import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from . import OobContext
from .context import BaseContext, ModalContext
from accrete.utils import render_templates


def modal_response(
    request: HttpRequest,
    template: str,
    context: ModalContext | dict,
    update: bool = False
) -> HttpResponse:

    if isinstance(context, ModalContext):
        context = context.dict()
    res = render(request, template, context)
    if update:
        res.headers['HX-Retarget'] = f'#{context["modal_id"]}'
        res.headers['HX-Reswap'] = 'outerHTML'
        return res
    res.headers['HX-Retarget'] = 'body'
    res.headers['HX-Reswap'] = 'beforeend'
    return res


def detail_response(
    request: HttpRequest,
    header_template: str = None,
    content_template: str = None,
    context: BaseContext | dict = None,
    extra_content: str | None = None
) -> HttpResponse:
    if isinstance(context, BaseContext):
        context = context.dict()
    templates = [
        ('ui/message.html', context)
    ]
    if header_template:
        templates.append(('ui/oob.html', OobContext(
            template=header_template,
            swap='innerHTML:#content-right-header',
            extra=context
        ).dict()))
    if content_template:
        templates.append(('ui/oob.html', OobContext(
            template=content_template,
            swap='innerHTML:#content-right',
            extra=context
        ).dict()))
    content = render_templates(templates, request=request)
    if extra_content:
        content += extra_content
    res = HttpResponse(content=content)
    add_trigger(res, 'activate-content-right')
    return res


def search_select_response(queryset) -> HttpResponse:
    return HttpResponse(render_to_string(
        'ui/widgets/model_search_select_options.html',
        {'options': queryset}
    ))


def add_trigger(
    response: HttpResponse,
    trigger: dict | str,
    header: str = 'HX-Trigger'
) -> HttpResponse:
    if isinstance(trigger, str):
        trigger = {trigger: ''}
    res_trigger = response.headers.get(header)
    if not res_trigger:
        response.headers[header] = json.dumps(trigger)
        return response
    try:
        res_trigger = ast.literal_eval(response.headers.get(header, '{}'))
    except SyntaxError:
        res_trigger = {response.headers[header]: ''}
    res_trigger.update(trigger)
    response.headers[header] = json.dumps(res_trigger)
    return response
