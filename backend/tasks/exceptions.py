from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Chama a resposta padrão do DRF para capturar a maioria dos erros
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "status_code": response.status_code,
            "error": True,
            "details": response.data
        }
        
        # Se for erro de validação (400 Bad Request), padroniza a mensagem principal
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_data["message"] = "Dados inválidos fornecidos."
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_data["message"] = "Não autorizado. Token inválido ou expirado."
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_data["message"] = "Recurso não encontrado."
        else:
            custom_data["message"] = "Ocorreu um erro ao processar a requisição."

        response.data = custom_data

    else:
        # Trata erros não capturados pelo DRF (Erros 500 do servidor)
        return Response(
            {
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error": True,
                "message": "Erro interno no servidor. Tente novamente mais tarde.",
                "details": str(exc)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response