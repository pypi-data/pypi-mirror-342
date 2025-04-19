class EditAction:
    def __init__(self, pk, form, fields, service):
        self.form = form
        self.fields = fields
        self.service = service
        self.pk = pk

    def _update_obj(self, obj):
        for field in self.fields:
            try:
                setattr(obj, field , getattr(self.form[field], "data"))
            except Exception as e:
                raise e
            else:
                try:
                    self.service.update(obj)
                except Exception as e:
                    raise e
        return obj

    def _update_form(self, obj):
        for field in self.fields:
            try:
                setattr(getattr(self.form, field), "data", getattr(obj,field))
            except Exception as e:
                raise e
        return self.form

    def update(self):
        obj = self.service.get_one_by_id(self.pk)
        try:
            self._update_obj(obj)
        except Exception as e:
            raise e
        else:
            return True

    @property
    def edit_form(self):
        obj = self.service.get_one_by_id(self.pk)
        return self._update_form(obj)