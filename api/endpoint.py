from flask import jsonify


class EndPoint:
    def __init__(self, app):
        self.app = app
        selfPath = self.path()
        docPath = selfPath + '/doc'
        print("will register endpoint", selfPath, " of type ", type(self))
        app.add_url_rule(selfPath, view_func=self.wrap_function, methods=[self.method()], endpoint=selfPath)
        print("will register endpoint", docPath, " as doc of type ", type(self))
        app.add_url_rule(docPath, view_func=self.get_documentation, methods=['GET'], endpoint=docPath)

    def method(self):
        return 'GET'

    def path(self):
        raise NotImplementedError("Subclasses must implement this method")

    def wrap_function(self):
        try:
            print("calling endpoint", self.path())
            return self.function()
        except Exception as e:
            print("error in endpoint", self.path(), ":", e)

            raise e

    def function(self):
        raise NotImplementedError("Subclasses must implement this method")

    def doc(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_documentation(self):
        method_doc = {}
        try:
            method_doc = self.doc()
        except Exception as e:
            method_doc = 'no documentation available'

        full_doc = {
            'method': self.method(),
            'path': self.path(),
            'doc': method_doc,
        }
        if 'parameters' in method_doc:
            full_doc['parameters'] = method_doc['parameters']
        return jsonify(full_doc)


class BadRequest(Exception):
    pass
