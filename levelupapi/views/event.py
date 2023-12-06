"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer, EventGamer

class EventView(ViewSet):
  
  def retrieve(self, request, pk):
    
    try:
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    except Event.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
  
  def list(self, request):
    
    events = Event.objects.all()
    
    # game = request.query_params.get('game', None)
    # if game is not None:
    #   event = event.filter(game_id=game)
    
    uid = request.META['HTTP_AUTHORIZATION']
    gamer = Gamer.objects.get(uid=uid)

    for event in events:
    # Check to see if there is a row in the Event Games table that has the passed in gamer and event
      event.joined = len(EventGamer.objects.filter(
        gamer=gamer, event=event)) > 0

    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    gamer = Gamer.objects.get(uid=request.data["organizer"])
    game = Game.objects.get(pk=request.data["game"])
    
    event = Event.objects.create(
      description=request.data["description"],
      date=request.data["date"],
      time=request.data["time"],
      game=game,
      organizer=gamer,
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
    
    organizer = Gamer.objects.get(uid=request.data["userId"])
    event.organizer = organizer
    
    event.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    event = Event.objects.get(pk=pk)
    event.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  @action(methods=['post'], detail=True)
  def signup(self, request, pk):
      """Post request for a user to sign up for an event"""
      gamer = Gamer.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
      # gamer = Gamer.objects.get(uid=request.data["userId"])
      event = Event.objects.get(pk=pk)
      EventGamer.objects.create(
          gamer=gamer,
          event=event
      )
      return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
  @action(methods=['delete'], detail=True)
  def leave(self, request, pk):
    """user leaving an event"""
    gamer = Gamer.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
    # gamer = Gamer.objects.get(uid=request.data["userId"])
    event = Event.objects.get(pk=pk)
    attendee = EventGamer.objects.get(
      gamer=gamer,
      event=event
    )
    attendee.delete()
    return Response({'message': 'Gamer left'}, status=status.HTTP_204_NO_CONTENT)
      
  
class EventSerializer(serializers.ModelSerializer):
    
  class Meta:
    model = Event
    fields = ('id', 'game', 'description', 'date', 'time', 'organizer', 'joined')
    depth = 1
