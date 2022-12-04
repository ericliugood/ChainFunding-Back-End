from rest_framework.response import Response
from rest_framework import status


def success(response={}):
    response.update({"response": "True"})
    return Response(response, status=status.HTTP_200_OK)


def err(message):
    return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


def notfound(message):
    return Response({"notfound": message}, status=status.HTTP_404_NOT_FOUND)
