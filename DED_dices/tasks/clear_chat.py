from DED_dices.models import Message

message = Message.objects.all()
message.delete()