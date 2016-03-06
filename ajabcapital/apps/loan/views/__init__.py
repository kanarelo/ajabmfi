from .accounting import *
from .accounts import *
from .config import *
from .products import *
from .transactions import *

@login_required
def dashboard(request):
	return TemplateResponse(request, "loan/dashboard.html", {
	})