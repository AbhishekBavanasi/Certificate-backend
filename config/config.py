from collections import defaultdict
from email.policy import default


class CertificateEntity:
    def __init__(self) -> None:
        self.dict = defaultdict(list)

    def add_item(self,phone,filename):
        self.dict[phone] = [filename,False]
    
    def update_item(self,phone):
        for i in self.dict:
            if i == phone and self.dict[i][1] == False:
                self.dict[i][1] = True

    def get_item(self):
        return self.dict

    def get_updated_item(self,phone):
        for i in self.dict:
            if i == phone:
                return self.dict[i]
    def get_path(self,phone):
        for i in self.dict:
            if i == phone:
                return self.dict[i][0]
