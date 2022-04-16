import pytest
import pytest_check
import requests
from dataload import *


@pytest.mark.usefixtures("setup")
class Test_api:

    lst_dataids = []
    lst_actualresponse = []
    lst_actualresponse2 = []
    lst_expectedresponse1 = []

    def test_postData(self, get_data):


        print("Total user count before adding is", get_usercount())
        adddata_response = requests.post(self.url, params={'access-token': self.key},json=addinfo(get_data["name"],get_data["gender"],get_data["status"]),headers=self.header,)
        assert adddata_response.status_code == 200

        print("User has been added successfully")

        adddata_json_response = adddata_response.json()
        data_id = adddata_json_response['data']['id']
        Test_api.lst_dataids.append(data_id)
       # print(Test_api.lst_dataids)

        print("Total user count after adding user "+f'{data_id}'+" is", get_usercount())

    def test_postData_negative(self):
        print("Negative scenario1 for POST request. Posting incomplete json format")
        print("Total user count before adding is", get_usercount())
        adddata_response = requests.post(self.url, params={'access-token': self.key},json={"name":"Manohar Kale","gender": "male","status": "active"},headers=self.header,)

        pytest_check.equal(adddata_response.json()["code"], 200)
        #print(adddata_response.json())
        #print(adddata_response.json()["data"]["message"])
        for data in adddata_response.json()["data"]:
            message = data["message"]

        assert message == "can't be blank"
        print(message)
        print("User has not been added")

        print("Negative scenario2 for POST request. Posting with invalid access token")
        print("Total user count before adding is", get_usercount())
        adddata_response = requests.post(self.url, params={'access-token': 'a2608d81deefb9d45d2ddef0f4365dc82deca66c52a74c8896ee9a20f2140'},
                                         json={"id":123,  "name":"Ramesh Damle","email":"Ramesh_Kale@temp.com","gender": "male","status": "inactive"},
                                         headers=self.header, )

        pytest_check.equal(adddata_response.json()["code"], 200)
        assert adddata_response.json()["data"]["message"] == "Authentication failed"

        #print(adddata_response.json())

        print(adddata_response.json()["data"]["message"])

        print("User has not been added")

    def test_getData(self):

        #print(Test_api.lst_dataids)

        for data_id in Test_api.lst_dataids:
            response = requests.get(self.url, params={'access-token': self.key,"id":data_id},)
            json_response = response.json()
            assert response.status_code == 200
            print("User information for id "+f'{data_id}'+" has been retrieved successfully")
            Test_api.lst_actualresponse.append(json_response["data"])

        #print(Test_api.lst_actualresponse[0][0])

        for i in range (0,len(Test_api.lst_actualresponse)):
            Test_api.lst_actualresponse2.append(Test_api.lst_actualresponse[i][0])
        #print(Test_api.lst_actualresponse2)

        for item in Test_api.lst_actualresponse2:
            item.pop("id")
       # print(Test_api.lst_actualresponse2)

    def test_getresponse(self, get_data):

        expected_info = getexpectedres(get_data["name"], get_data["gender"], get_data["status"])

        Test_api.lst_expectedresponse1.append(expected_info)
        # print(Test_api.lst_expectedresponse1)
        # print(Test_api.lst_actualresponse2)



    def test_testresponse(self):

        assert Test_api.lst_actualresponse2 == Test_api.lst_expectedresponse1
        print("Actual and expected response content is matching")


    def test_putData(self):

        lst_params = [{"id":Test_api.lst_dataids[0],  "name":"Ramesh Damle","email":"Ramesh_Kale@temp.com","gender": "male","status": "inactive"}, {"id":Test_api.lst_dataids[1],"name":"Hemalata Malini","email":"Hema_Malini@temp.com","gender": "female","status": "active"}, {"id":Test_api.lst_dataids[2],"name":"Vaishavi Bramhe","email":"Vishnu_Bramhe@temp.com","gender": "female","status": "active"}, {"id":Test_api.lst_dataids[3],"name":"Anushka Rangan","email":"Anushka_Sharma@temp.com","gender": "female","status": "active"},{"id":Test_api.lst_dataids[4],"name":"Steve Austin","email":"Steve_Austin@temp.com","gender": "male","status": "inactive"},]
        for param in lst_params:
            editdata_response = requests.put(self.url+f'{param["id"]}', params={'access-token': self.key},json=editstatus(param["name"],param["gender"],param["status"]),headers=self.header, )
            #print(editdata_response.json()["data"])
            #print(param)
            assert editdata_response.status_code == 200
            print("User information for id "+f'{param["id"]}'+" has been modified successfully")
            assert param == editdata_response.json()["data"]
            print("Actual and expected response content after modification is matching")


    def test_putData_negative(self):

        print("Negative scenario3 for PUT / edit request. Posting with invalid user id.")

        #lst_params = [{"id":Test_api.lst_dataids[0],  "name":"Ramesh Damle","email":"Ramesh_Kale@temp.com","gender": "male","status": "inactive"}, {"id":Test_api.lst_dataids[1],"name":"Hemalata Malini","email":"Hema_Malini@temp.com","gender": "female","status": "active"}, {"id":Test_api.lst_dataids[2],"name":"Vaishavi Bramhe","email":"Vishnu_Bramhe@temp.com","gender": "female","status": "active"}, {"id":Test_api.lst_dataids[3],"name":"Anushka Rangan","email":"Anushka_Sharma@temp.com","gender": "female","status": "active"},{"id":Test_api.lst_dataids[4],"name":"Steve Austin","email":"Steve_Austin@temp.com","gender": "male","status": "inactive"},]
        editdata_response = requests.put(self.url+"123000", params={'access-token': self.key},json={"name":"Ramesh Damle","email":"Ramesh_Kale@temp.com","gender": "male","status": "inactive"},headers=self.header,)
        pytest_check.equal(editdata_response.json()["code"], 200)

        assert editdata_response.json()["data"]["message"] == "Resource not found"
        print(editdata_response.json()["data"]["message"])
        print("User information has not been modified")

        print("Negative scenario4 for PUT / edit request. Posting with invalid access code.")

        #lst_params = [{"id":Test_api.lst_dataids[0],  "name":"Ramesh Damle","email":"Ramesh_Kale@temp.com","gender": "male","status": "inactive"}, {"id":Test_api.lst_dataids[1],"name":"Hemalata Malini","email":"Hema_Malini@temp.com","gender": "female","status": "active"}, {"id":Test_api.lst_dataids[2],"name":"Vaishavi Bramhe","email":"Vishnu_Bramhe@temp.com","gender": "female","status": "active"}, {"id":Test_api.lst_dataids[3],"name":"Anushka Rangan","email":"Anushka_Sharma@temp.com","gender": "female","status": "active"},{"id":Test_api.lst_dataids[4],"name":"Steve Austin","email":"Steve_Austin@temp.com","gender": "male","status": "inactive"},]
        editdata_response = requests.put(self.url+f'{Test_api.lst_dataids[0]}', params={'access-token': 'a2608d81deefb9d45d2ddef0f436'},json={"name":"Ramesh Damle","email":"Ramesh_Kale@temp.com","gender": "male","status": "inactive"},headers=self.header,)
        code = editdata_response.json()["code"]
        pytest_check.equal(code, 200)

        assert editdata_response.json()["data"]["message"] == "Resource not found"
        print(editdata_response.json()["data"]["message"])
        print("User information has not been modified")




    def test_deleteData_negative(self):

        print("Negative scenario5 for delete request. Posting with invalid access code.")

        #lst_params = [{"id":Test_api.lst_dataids[0],  "name":"Ramesh Damle","gender": "male","status": "inactive"}, {"id":Test_api.lst_dataids[1],"name":"Hemalata Malini","gender": "female","status": "active"}, {"id":Test_api.lst_dataids[2],"name":"Vaishavi Bramhe","gender": "female","status": "active"}, {"id":Test_api.lst_dataids[3],"name":"Anushka Rangan","gender": "female","status": "active"},{"id":Test_api.lst_dataids[4],"name":"Steve Austin","gender": "male","status": "inactive"},]
        deletedata_response = requests.delete(self.url+f'{Test_api.lst_dataids[0]}', params={'access-token': 'a2608d81deefb9d45d2ddef0f436'},headers=self.header, )

        pytest_check.equal(deletedata_response.json()["code"], 200)
        assert deletedata_response.json()["code"] == 404
        assert deletedata_response.json()["data"]["message"] == "Resource not found"
        print(deletedata_response.json()["data"]["message"])
        print("User information has not been deleted")



    def test_deleteData(self):

        #lst_params = [{"id":Test_api.lst_dataids[0],  "name":"Ramesh Damle","gender": "male","status": "inactive"}, {"id":Test_api.lst_dataids[1],"name":"Hemalata Malini","gender": "female","status": "active"}, {"id":Test_api.lst_dataids[2],"name":"Vaishavi Bramhe","gender": "female","status": "active"}, {"id":Test_api.lst_dataids[3],"name":"Anushka Rangan","gender": "female","status": "active"},{"id":Test_api.lst_dataids[4],"name":"Steve Austin","gender": "male","status": "inactive"},]
        for id in Test_api.lst_dataids:
            deletedata_response = requests.delete(self.url+f'{id}', params={'access-token': self.key},headers=self.header, )
            print(deletedata_response.json())
            assert deletedata_response.status_code == 200
            print("User information for id "+f'{id}'+" has been deleted successfully")

    def test_getData_negative(self):

        print("Negative scenario6 for Get request. Trying to retrieve user data by id after data got deleted.")

        for data_id in Test_api.lst_dataids:
            response = requests.get(self.url, params={'access-token': self.key,"id":data_id},)
            json_response = response.json()
            pytest_check.greater(json_response["meta"]["pagination"]["total"],0)
            print(json_response)
            print("User information for id "+f'{data_id}'+" has not retrieved successfully")


    @pytest.fixture(params=[{"name":"Ramesh Kale","gender": "male","status": "active"}, {"name":"Hema Malini","gender": "female","status": "active"}, {"name":"Vishnu Bramhe","gender": "male","status": "active"}, {"name":"Anushka Sharma","gender": "female","status": "inactive"},{"name":"Steve Austin","gender": "male","status": "active"},])
    def get_data(self, request):
        return request.param








