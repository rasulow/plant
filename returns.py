class Returns:
    UPDATED                        = {"status" : "Successfully updated!"}
    DELETED                        = {"status" : "Successfully deleted!"}
    ACTIVATED                      = {"status" : "Activated!"}
    DISACTIVATED                   = {"status" : "Disactivated!"}
    
    def object(obj):
        return {"error" : False, "body" : obj}
    
    def id(obj):
        return {"error" : False, "body" : {"INSERTED_ID" : obj}}