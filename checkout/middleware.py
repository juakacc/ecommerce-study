from .models import CarItem

def cart_item_middleware(get_response):
    def middleware(request):
        session_key = request.session.session_key
        response = get_response(request)
        if session_key != request.session.session_key and request.session.session_key:
            CarItem.objects.filter(cart_key=session_key).update(
                cart_key=request.session.session_key
            )
        return response
    return middleware
