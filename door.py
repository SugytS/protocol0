class Door:
    def __init__(self, source_room, destination_room):
        self.source_room = source_room
        self.destination_room = destination_room
        self.is_locked = True

    def unlock(self):
        self.is_locked = False