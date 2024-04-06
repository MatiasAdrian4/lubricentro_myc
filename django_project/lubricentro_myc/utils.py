from functools import wraps
from io import BytesIO
from unittest.mock import MagicMock, patch

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from lubricentro_myc.models.activity import Activity


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def mock_auth(func):
    @wraps(func)
    @patch(
        "lubricentro_myc.authentication.JWTAuthentication.authenticate",
        MagicMock(return_value=(MagicMock(), None)),
    )
    def wrapper(*args, **kwd):
        return func(*args, **kwd)

    return wrapper


def log_activity(request, type, title, description):
    # For unhandled exceptions the description field will be used to store the error's traceback
    # For info exceptions the description field will be used to store the request payload

    Activity.objects.create(
        user=request.user,
        request=f"{request.method} {request.get_full_path()}",
        type=type,
        title=title,
        description=description,
    )
