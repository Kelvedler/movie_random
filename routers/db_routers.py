class AccountsRouter:
    app_labels = {'accounts', 'admin', 'auth', 'contenttypes', 'sessions', }
    db_route = 'users'

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.app_labels:
            return self.db_route
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.app_labels:
            return self.db_route
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.app_labels or \
        obj2._meta.app_label in self.app_labels:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.app_labels:
            return db == self.db_route
        return None


class MoviesRouter:
    app_labels = ['movies', 'staticfiles', ]
    db_route = 'movies'

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.app_labels:
            return self.db_route
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.app_labels:
            return self.db_route
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.app_labels or \
                obj2._meta.app_label in self.app_labels:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.app_labels:
            return db == self.db_route
        return None
