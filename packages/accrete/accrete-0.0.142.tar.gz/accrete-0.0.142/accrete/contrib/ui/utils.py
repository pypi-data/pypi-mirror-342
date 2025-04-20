import ast
import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

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
    header_template: str,
    content_template: str,
    context: BaseContext | dict,
    extra_content: str | None = None
) -> HttpResponse:
    if isinstance(context, BaseContext):
        context = context.dict()
    content = render_templates([
        ('ui/message.html', context),
        ('ui/oob.html', OobContext(
            template=header_template,
            swap='innerHTML:#content-right-header',
            extra=context
        ).dict()),
        ('ui/oob.html', OobContext(
            template=content_template,
            swap='innerHTML:#content-right',
            extra=context
        ).dict())
    ], request=request)
    if extra_content:
        content += extra_content
    res = HttpResponse(content=content)
    add_trigger(res, 'activate-content-right')
    return res


def add_trigger(
    response: [HttpResponse],
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
