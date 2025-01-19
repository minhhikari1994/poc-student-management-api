class Result:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data

    def to_json(self):
        return dict(
            success=self.success,
            message=self.message,
            data=self.data
        )
    
    @classmethod
    def success(cls, message, data=None):
        return cls(success=True, message=message, data=data)
    
    
    @classmethod
    def error(cls, message, data=None):
        return cls(success=False, message=message, data=data)

