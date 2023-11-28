from vkbottle import Keyboard, KeyboardButtonColor, Text

main_keyboard = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Погода", payload={'command': 'weather'}))
    .add(Text("Афиша", payload={'command': 'afisha'}))
    .row()
    .add(Text("Пробки", payload={'command': 'trafjam'}))
    .add(Text("Валюта", payload={'command': 'money'}))
    .row()
    .add(Text("Изменить город", payload={'command': 'delete'}), KeyboardButtonColor.NEGATIVE)
).get_json()

dayweek = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Сегодня", payload={'dayweek': 'today'}), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Завтра", payload={'dayweek': 'tomorrow'}))
    .row()
    .add(Text("Передумал. В меню!", payload={'menu': 'menu'}))
).get_json()
