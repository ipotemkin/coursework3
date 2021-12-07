class BasicService:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, did: int):
        return self.dao.get_one(did)

    def create(self, new_obj_d: dict):
        return self.dao.create(new_obj_d)

    def update(self, new_obj_d: dict, did: int):
        return self.dao.update(new_obj_d, did)

    def part_update(self):
        pass

    def delete(self, did: int):
        self.dao.delete(did)

    def get_all_by_filter(self, *args, **kwargs):
        return self.dao.get_all_by_filter(*args, **kwargs)
