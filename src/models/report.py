class Report:
    name: str
    title: str
    body: str
    date: str
    publish: bool

    def __init__(self, name: str, title: str, body: str, date: str, publish: bool) -> None:
        self.name = name
        self.title = title
        self.body = body
        self.date = date
        self.publish = publish
