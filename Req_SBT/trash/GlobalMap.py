

class GlobalMap:
    # ƴװ���ֵ乹��ȫ�ֱ���  ���map  ������������ɾ�Ĳ�
    map = {}

    def set_map(self, key, value):
        if(isinstance(value,dict)):
            value = json.dumps(value)
        self.map[key] = value


    def set(self, **keys):
        try:
            for key_, value_ in keys.items():
                self.map[key_] = str(value_)
                log.debug(key_+":"+str(value_))
        except BaseException as msg:
            log.error(msg)
            raise msg

    def del_map(self, key):
        try:
            del self.map[key]
            return self.map
        except KeyError:
            log.error("key:'" + str(key) + "'  ������")


    def get(self,*args):
        try:
            dic = {}
            for key in args:
                if len(args)==1:
                    dic = self.map[key]
                    log.debug(key+":"+str(dic))
                elif len(args)==1 and args[0]=='all':
                    dic = self.map
                else:
                    dic[key]=self.map[key]
            return dic
        except KeyError:
            log.warning("key:'" + str(key) + "'  ������")
            return 'Null_'
