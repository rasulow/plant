class Returns:
    UPDATED                        = {"status" : "Успешно обновлено!"}
    DELETED                        = {"status" : "Успешно удалено!"}
    ACTIVATED                      = {"status" : "Активировано!"}
    DISACTIVATED                   = {"status" : "Отключено!"}
    update                         = {"msg"    : "Обновлено!"}
    delete                         = {"msg"    : "Удалено!"}
    
    def object(obj):
        return {"error" : False, "body" : obj}
    
    def id(obj):
        return {"error" : False, "body" : {"INSERTED_ID" : obj}}