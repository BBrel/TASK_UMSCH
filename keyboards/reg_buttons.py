from vkbottle import Keyboard, KeyboardButtonColor, Text, Location

confirmation = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Да!", payload={'registration': 'yes'}), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Нет :(", payload={'registration': 'no'}), color=KeyboardButtonColor.NEGATIVE)
).get_json()

geoposition = (
    Keyboard(one_time=True, inline=False)
    .add(Location(payload={'registration': 'place'}))
).get_json()
