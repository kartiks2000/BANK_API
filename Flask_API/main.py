from flask import Flask, jsonify, request
from flask import Response
from flask_restful import Api, Resource
import json, ast
from flask import jsonify
import bankdataclass
import bankcountclass
import queryclass
import operator
from datetime import datetime

import pandas

 
# ===================== * INITIATING FLASK APP * ================ #

# Initiating the app
app = Flask(__name__)
# creating an API object
api = Api(app)

# ===================== * INITIATING FLASK APP * ================ #








# =============================================================================#
# ===================== * DATA PROCESSING & FORMATTING START * ================ #
# =============================================================================#

# Importing excel data
sheet1 = pandas.read_excel('./sample2.xlsx')
sheet1 = sheet1.fillna('NA')


# Vairibale to store Bank Records 
# Bank Record FORMAT {"IFSC":JSON data}
bank_record = {}


# Formatting data
for row in range(sheet1.shape[0]):

    MICR_CODE_temp = sheet1["MICR CODE"][row]

    # If MICR_CODE_temp is a number
    if (type(MICR_CODE_temp)) == float:
        MICR_CODE_temp = int(MICR_CODE_temp)

    temp = bankdataclass.BankModel(sheet1["BANK"][row],sheet1["IFSC"][row], MICR_CODE_temp, sheet1["BRANCH"][row],sheet1["ADDRESS"][row] ,int(sheet1["STD CODE"][row]),int(sheet1["CONTACT"][row]), sheet1["CITY"][row] ,sheet1["DISTRICT"][row], sheet1["STATE"][row])

    # Storing data in a dictionary
    bank_record[temp.IFSC] = temp.__dict__


# Vairibale to store LeaderBoard 
leaderboard_dict = {}
# Vairibale to store sorted LeaderBoard Tuples
leaderboard_sorted = []

#Generating LeaderBoard
def gen_leader_board():
    global leaderboard_sorted
    for i,j in bank_record.items():

        temp = j

        # Bank already present in leader board
        if temp["BANK"] in leaderboard_dict:
           leaderboard_dict[temp["BANK"]] = leaderboard_dict[temp["BANK"]] + 1
        # Bank NOT present in leader board  
        else:
            leaderboard_dict[temp["BANK"]] = 1

    # Sorting leader board function        
    leaderboard_sorted = sorted(leaderboard_dict.items(),reverse=True, key=operator.itemgetter(1))




# Function call to generate LEADERBOARD
gen_leader_board()


# =============================================================================#
# ===================== * DATA PROCESSING & FORMATTING END * ================ #
# =============================================================================#



# Vairiable to store Search history
Search_History = []



# =============================================================================#
# ==================== * IFSC QUERY REQUEST START * ======================= #
# =============================================================================#

class IFSCquery(Resource):

    def get(self,ifsc_code):

        # Checking if IFSC code exists
        if ifsc_code in bank_record:

            # As the request is validated, hence it will be pushed to search history
            time_stamp = datetime.now()
            time_stamp_string = time_stamp.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            Search_History.insert(0,queryclass.QueryModel(ifsc_code,time_stamp_string).__dict__)
            #print("Search-History : ",Search_History)
            

            return {ifsc_code:bank_record[ifsc_code]}

        # IFSC code doesnt exixts
        else: 
            # return Response(
            #     "INVALID IFSC CODE",
            #     status=400,
            # )
            return {"error": "Sorry, INVALID IFSC code."}   

# =============================================================================#
# ==================== * IFSC QUERY REQUEST END * ======================= #
# =============================================================================#




# =============================================================================#
# ==================== * LEADERBOARD REQUEST START * ======================= #
# =============================================================================#
    
class  LeaderBoard(Resource):

    def get(self,order,val):
        #print(leaderboard_sorted)
        # If order == 'DESC' return "val" objects
        if order == 'DESC':
            if int(val)<=len(leaderboard_sorted):
                leader_response_dict = dict(leaderboard_sorted[:int(val)])
                return {"LeaderBoard":leader_response_dict}
            return {"message": "Sorry, Exceeding range."}

        # If order == 'ASC' return "val" objects    
        elif order == 'ASC':
            if int(val)<=len(leaderboard_sorted):
                leader_response_dict = dict(leaderboard_sorted[:-int(val)-1:-1])
                return {"LeaderBoard":leader_response_dict}
            return {"message": "Sorry, Exceeding range."}

# =============================================================================#
# ==================== * LEADERBOARD REQUEST END * ======================= #
# =============================================================================#




# =============================================================================#
# ==================== * SEARCH HISTORY REQUEST START * ======================= #
# =============================================================================#

class  SearchHistory(Resource):

    def get(self,order,val):

        # If val == 'all', order == "DESC"
        if val == "all" and order == "DESC":
            return {"History":Search_History}

        # If val == 'all', then val=total_enteries
        elif val == "all" and order == "ASC":
            return {"History":Search_History[::-1]}

        # If order == 'DESC', check if val<len(Search_History) 
        elif order == "DESC":
            if int(val)<=len(Search_History):
                return {"History":Search_History[:int(val)]}
            else:
                # return Response(
                #     "INVALID VALUE",
                #     status=400,
                # ) 
                return {"message": "Sorry, Exceeding range."}    

        # If order == 'ASC', check if val<len(Search_History)
        else:
            if int(val)<=len(Search_History):
                return {"History":Search_History[:-int(val)-1:-1]}
            else:
                # return Response(
                #     "INVALID VALUE",
                #     status=400,
                # )   
                return {"message": "Sorry, Exceeding range."}   

# =============================================================================#
# ==================== * SEARCH HISTORY REQUEST END * ======================= #
# =============================================================================#



# =============================================================================#
# ============================= * API ROUTES * =============================== #
# =============================================================================#

api.add_resource(IFSCquery, "/ifsc_query/<string:ifsc_code>")
api.add_resource(LeaderBoard, "/leaderboard/<string:order>/<int:val>")
api.add_resource(SearchHistory, "/searchhistory/<string:order>/<string:val>")

# =============================================================================#
# ============================= * API ROUTES * =============================== #
# =============================================================================#




# ===================== * SERVER * ======================= #

# Starts or server and app
# Please set "debug = False" for production environment
if __name__ == "__main__":
    app.run(debug=True)

# ===================== * SERVER * ======================= #    
