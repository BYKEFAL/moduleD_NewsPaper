# Пример:
# class SimpleMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # код, выполняемый до формирования ответа (или другого middleware)

#         response = self.get_response(request)

#         # код, выполняемый после формирования запроса (или нижнего слоя)

#         return response


# код ничего не делат, лишний слой, просто для проверки работоспособности при подключении в Settings > middleweare.
class MobileOrFullMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if 'Mobile' in user_agent:
            # пользователь зашел с мобильного устройства
            prefix = "mobile/"
        else:
            # пользователь зашел с ПК
            prefix = "full/"
        # response.template_name = prefix + response.template_name
        return response
