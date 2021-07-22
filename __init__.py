from mycroft import MycroftSkill, intent_file_handler


class OcTranspoBusTimes(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('times.bus.transpo.oc.intent')
    def handle_times_bus_transpo_oc(self, message):
        self.speak_dialog('times.bus.transpo.oc')


def create_skill():
    return OcTranspoBusTimes()

