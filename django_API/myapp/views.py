from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import authentication, permissions
from rest_framework import status

import requests

import json




# =============================================================================#
# ====================== * CACHING MECHANISM START * ========================= #
# =============================================================================#

# All the cached queries
# Format {"IFSC": result}
cachedqueries = {}

# Checking if Query is cached
def check_cache(ifsc):
    if cachedqueries.get(ifsc) is not None:
        return cachedqueries[ifsc]
    return False

# Caching the response for a IFSC_Query request
def cache_response(ifsc,result):
    # cache only if recieved succesful response
    if 'error' not in result.keys():
        cachedqueries[ifsc] = result[ifsc]
        return True

    # Response unsuccessful (INVALID ifsc code)    
    else:
        return False 

# =============================================================================#
# ======================= * CACHING MECHANISM END * ========================= #
# =============================================================================#






# =============================================================================#
# =================== * TRACKING IFSC HIT COUNT START * ======================= #
# =============================================================================#

# Tracking IFSC hits count
# Format {"IFSC": COUNT}
IFSC_hit_count = {}

# IFSC Hit tracking function
def IFSC_Hit_Tracking(ifsc):
    if IFSC_hit_count.get(ifsc) is not None: # Already called erlier
        IFSC_hit_count[ifsc] = IFSC_hit_count[ifsc] + 1
    else:                               # Called first time
        IFSC_hit_count[ifsc] = 1

# =============================================================================#
# ====================== * TRACKING IFSC HIT COUNT END * ====================== #
# =============================================================================#






# =============================================================================#
# ==================== * TRACKING URL HIT COUNT START * ======================= #
# =============================================================================#

# Tracking URL hits count
URL_hit_count = {"IFSC_QUERY": 0, "LEADER_BOARD": 0, "SEARCH_HISTORY": 0}

# =============================================================================#
# ==================== * TRACKING URL HIT COUNT END * ====================== #
# =============================================================================#







# =============================================================================#
# ==================== * IFSC QUERY REQUEST START * ======================= #
# =============================================================================#

class IFSC_query(APIView):

    def get(self, request, format=None,ifsc = "-1"):

        # Checking if request is VALID
        # ifsc should not be NULL or -1 or ""
        if ifsc == "-1" or ifsc == None or ifsc == '':
            return Response("INVALID IFSC", status=400)


        # Check if required query is already Cached
        cache_res = check_cache(ifsc)
        if cache_res:

            # If ----VALID REQUEST ONLY---- then track URL hit
            URL_hit_count["IFSC_QUERY"] = URL_hit_count["IFSC_QUERY"] + 1
            # If ----VALID REQUEST ONLY---- then track IFSC hit
            IFSC_Hit_Tracking(ifsc)
            print("------------------- cached_Response_delivered-------------------")
            #print(cache_res["IFSC"])
            return Response(cache_res)

        # If not cached send request to flask api and cache the response and send it to the user
        # sending req to flask api and recieving response
        res = requests.get("http://127.0.0.1:5000/ifsc_query/"+ifsc)       
        res_dict_format = json.loads(res.content)

        # Caching response recieved
        flag = cache_response(ifsc,res_dict_format) 

        # Returning response to the user
        # If recieved Valid response
        if flag:

            # If ----VALID REQUEST ONLY---- then track URL hit
            URL_hit_count["IFSC_QUERY"] = URL_hit_count["IFSC_QUERY"] + 1

            # If ----VALID REQUEST ONLY---- then track IFSC hit
            IFSC_Hit_Tracking(ifsc)
            return Response(res_dict_format[ifsc])

        # If recieved Invalid response    
        else:
            return Response(
                "INVALID IFSC CODE",
                status=400,
            )    
        
# =============================================================================#
# ==================== * IFSC QUERY REQUEST END * ======================= #
# =============================================================================#







# =============================================================================#
# ==================== * LEADERBOARD REQUEST START * ======================= #
# =============================================================================#

class LeaderBoard(APIView):
    
    def get(self, request):

        # Fetching Query parameters
        #/<str:sortorder>/<str:fetchcount>
        print(request.GET)
        if 'sortorder' in request.GET:
            sortorder = request.query_params['sortorder']
        else:
            sortorder = "DESC"  

        if 'fetchcount' in request.GET:
            fetchcount = request.query_params['fetchcount']
        else:
             fetchcount = "10"   

        # Checking if request is VALID
        # If fetchcount is not a number
        if not(fetchcount.isnumeric()):
            return Response("INVALID parameters passed", status=400)

        # Checking if request is VALID
        # (sortorder == 'DESC' OR sortorder == 'ASC')  AND 1 <= fetchcount <= 225
        if sortorder == "DESC" or sortorder == "ASC":
            if 1 <= int(fetchcount) <= 225:

                # Tracking URL hits
                URL_hit_count["LEADER_BOARD"] = URL_hit_count["LEADER_BOARD"]+1
        
                # Sending request to flask api and returning the response
                res = requests.get("http://127.0.0.1:5000/leaderboard/"+sortorder+"/"+str(fetchcount))
                res_dict_format = json.loads(res.content)
                return Response(res_dict_format["LeaderBoard"])


        return Response("INVALID parameters passed", status=400)
        
# =============================================================================#
# ======================= * LEADERBOARD REQUEST END * ========================= #
# =============================================================================#






# =============================================================================#
# ==================== * SEARCH HISTORY REQUEST START * ======================= #
# =============================================================================#

class SearchHistory(APIView):
    
    def get(self, request, sortorder="ASC",fetchcount="all"):

        # Fetching Query parameters
        #<str:sortorder>/<str:fetchcount>
        if 'sortorder' in request.GET:
            sortorder = request.query_params['sortorder']
        else:
            sortorder = "ASC"  

        if 'fetchcount' in request.GET:
            fetchcount = request.query_params['fetchcount']
        else:
             fetchcount = "all"

        # Checking if request is VALID
        if (sortorder == "DESC" or sortorder == "ASC"):

            # If fetchcount.isalpha()==True AND fetchcount!="all", return error
            if fetchcount.isalpha()==True and fetchcount!="all":
                return Response("INVALID parameters passed", status=400)

            if fetchcount == "all":

                # Tracking URL hits
                URL_hit_count["SEARCH_HISTORY"] = URL_hit_count["SEARCH_HISTORY"] + 1

                # Sending request to flask api and returning the response
                res = requests.get("http://127.0.0.1:5000/searchhistory/"+ sortorder + "/" + fetchcount)
                res_dict_format = json.loads(res.content)

                return Response(res_dict_format["History"]) 
                
            elif 1 <= int(fetchcount) <= 1000: 

                # Tracking URL hits
                URL_hit_count["SEARCH_HISTORY"] = URL_hit_count["SEARCH_HISTORY"] + 1

                # Sending request to flask api and returning the response
                res = requests.get("http://127.0.0.1:5000/searchhistory/"+ sortorder + "/" + fetchcount)
                res_dict_format = json.loads(res.content)

                return Response(res_dict_format["History"])  

            else:
                return Response("INVALID parameters passed", status=400)                      

        return Response("INVALID parameters passed", status=400)

# =============================================================================#
# ==================== * SEARCH HISTORY REQUEST END * ======================= #
# =============================================================================#






# =============================================================================#
# ======================= * IFSC HIT REQUEST START * ========================== #
# =============================================================================#

class IFSC_Hit(APIView):

    def get(self, request):
        return Response(IFSC_hit_count)

# =============================================================================#
# ======================= * IFSC HIT REQUEST END * ========================= #
# =============================================================================#






# =============================================================================#
# ======================= * URL HIT REQUEST START * ========================== #
# =============================================================================#

class URL_Hit(APIView):

    def get(self, request):
        return Response(URL_hit_count)     

# =============================================================================#
# ======================= * URL HIT REQUEST END * ========================== #
#==============================================================================#           
