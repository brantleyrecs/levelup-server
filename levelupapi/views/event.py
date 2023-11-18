"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer

class EventView(ViewSet):
  
  def retrieve(self, request, pk):
    
    try:
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    except Event.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
  
  def list(self, request):
    
    event = Event.objects.all()
    
    game = request.query_params.get('game', None)
    if game is not None:
      event = event.filter(game_id=game)
      
    serializer = EventSerializer(event, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    organizer = Gamer.objects.get(uid=request.data["userId"])
    game = Game.objects.get(pk=request.data["game"])
    
    event = Event.objects.create(
      description=request.data["description"],
      date=request.data["date"],
      time=request.data["time"],
      game=game,
      organizer=organizer,
    )
    serializer = EventSerializer(event)
    return Response(serializer.data)
  
  def update(self, request, pk):
    event = Event.objects.get(pk=pk)
    event.description = request.data["description"]
    event.date = request.data["date"]
    event.time = request.data["time"]
    
    game = Game.objects.get(pk=request.data["game"])
    event.game = game
    
    organizer = Gamer.objects.get(pk=request.data["userId"])
    event.organizer = organizer
    
    event.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    event = Event.objects.get(pk=pk)
    event.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    
  
class EventSerializer(serializers.ModelSerializer):
    
  class Meta:
    model = Event
    fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
    depth = 1
