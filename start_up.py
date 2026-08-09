import pandas as pd 
import uuid 


def start_up() :
    
    df = [pd.read_json('feederProps.json', lines="true").to_dict(orient="dict")]
    
    print(df)
    try : 
        return df[0]["feederID"]
    except KeyError:

        print("inserting id") 
        df[0] ={"feederID" : "1234"}
    #         print(df["feederID"])
        pd.DataFrame(df,columns=['Info']).to_json("feederProps.json")
#         return df["values"]["feederID"] 
#     
#     return df["feederID"]
        
    
#     with open("./FeederInfo.txt", "r+") as f :
#         
#         if f.read() == "" :
#             f.write(uuid.uuid4().hex)
    
if __name__ == "__main__" :
    print(start_up())
