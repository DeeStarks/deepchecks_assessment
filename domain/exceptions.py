class InvalidAlertType(Exception):
    def __init__(self, alert_type):
        self.alert_type = alert_type
        super().__init__(f"Invalid alert type: {alert_type}")


class InvalidInteractionType(Exception):
    def __init__(self, interaction_type):
        self.interaction_type = interaction_type
        super().__init__(f"Invalid interaction type: {interaction_type}")


class NotFound(Exception):
    def __init__(self, entity):
        self.entity = entity
        super().__init__(f"{entity} not found")
