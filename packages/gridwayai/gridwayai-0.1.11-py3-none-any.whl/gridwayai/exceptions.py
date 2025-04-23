class GridwayAIError(Exception):
    pass

class AuthenticationError(GridwayAIError):
    pass

class RateLimitError(GridwayAIError):
    pass

class APIError(GridwayAIError):
    pass
