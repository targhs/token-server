from .models import Token


def ExpireTokensMiddleware(get_response):
    def middleware(request):
        Token.objects.delete_expired()
        Token.objects.unassign_allocated_tokens()
        response = get_response(request)

        return response

    return middleware