import unittest

from myapp.views import check_cache, cache_response, IFSC_Hit_Tracking, IFSC_query, LeaderBoard, IFSC_Hit, URL_Hit

# Note-: Flask server needs to be running for these tests


class test_check_cache(unittest.TestCase):

    def test_cache(self):
        self.assertEqual(check_cache(7354), False)
        self.assertEqual(check_cache("7354"), False)
        self.assertEqual(check_cache(""), False)


class test_cache_response(unittest.TestCase):

    def test_cache_response(self):
        self.assertEqual(cache_response("142",{'error':"yes"}),False)
        self.assertEqual(cache_response("142",{'error':"yes"}),False)
        #self.assertEqual(cache_response("347",{'ifsc':'347','answer':"yes"}),True)

# class test_IFSC_Hit_Tracking(unittest.TestCase):

#     def test_IFSCHitTracking(self):
        
#         with self.assertRaises(ValueError):
#             IFSC_Hit_Tracking(1243).divide(10, 0)

#         self.assertEqual(IFSC_Hit_Tracking(1243),)        


class test_IFSC_query(unittest.TestCase):

    def test_IFSCquery(self):
        
        self.assertEqual((IFSC_query.get({},"",-1)).status_code,400)
        self.assertEqual((IFSC_query.get({},"","")).status_code,400)
        self.assertEqual((IFSC_query.get({},"",None)).status_code,400)

 

# class test_LeaderBoard(unittest.TestCase):

#     def test_leaderboard(self):

#         self.assertEqual((LeaderBoard.get(self,{'GET':{'sortorder': ['ASC'], 'fetchcount': ['6']}})).status_code,400)  


class test_IFSCHit(unittest.TestCase):

    def test_IFSCHit(self):

        self.assertEqual(IFSC_Hit().get({}).status_code,200)



class test_URLHit(unittest.TestCase):

    def test_URLHit(self):

        self.assertEqual(URL_Hit().get({}).status_code,200)


# ./manage.py test        