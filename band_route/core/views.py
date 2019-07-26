from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import CityListSerializer
from .tasks import City, fastest_route


class FastestRouteAPIView(APIView):
    """Find fastest route"""

    permission_classes = (AllowAny,)
    serializer_class = CityListSerializer

    def post(self, request):
        """Method to handle incoming list of coordinates(cities)
         in order to return fastest route to view all cities"""

        cities = request.data.get("cities", {})
        cities_list = [
            City(x=tuple(d.values())[0], y=tuple(d.values())[1])
            for d in cities
        ]
        best_route = fastest_route(
            routes=cities_list,
            num_routes=100,
            elite_size=20,
            swap_rate=0.01,
            generations=50,
        )

        serializer = CityListSerializer(best_route, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
