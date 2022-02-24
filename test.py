import requests

BASE = "http://127.0.0.1:5000/"

# --------------------Test API endpoint /device--------------------


# test 1 bad request --------------------
response = requests.get(
    BASE + "device/1",
)
try:
    returned = response.status_code
    expected = 404
    if returned == expected:
        print("PASS")
    else:
        print("FAIL")

except:
    # print(response.json)
    # print(response.json())
    print("Test Failed to Execute")


# test 2 good request --------------------
response = requests.get(
    BASE + "device/andrew_merrin",
)
try:
    returned = response.status_code
    expected = 200
    if returned == expected:
        print("PASS")
    else:
        print("FAIL")
    # test 3 returned results --------------------
    if len(response.json()) == 4:
        print("PASS")
    else:
        print("FAIL")

except:
    # print(response.json)
    # print(response.json())
    print("Test Failed to Execute")

# --------------------Test API endpoint /device/full--------------------


# test 4 good request --------------------
response = requests.get(
    BASE + "device/full/4",
)
try:
    returned = response.status_code
    expected = 200
    if returned == expected:
        print("PASS")
    else:
        print("FAIL")
    # test 5 length of response --------------------
    if len(response.json()) == 21:
        print("PASS 5")
    else:
        print("FAIL 5")
    # test 6 correct user returned --------------------
    if response.json()["owner_ref"] == "first_last":
        print("PASS")
    else:
        print("FAIL")

except:
    # print(response.json)
    # print(response.json())
    print("4,5,or 6 Test Failed to Execute")

# --------------------Test API endpoint /device/control--------------------

# test 7 good request --------------------
response = requests.get(
    BASE + "device/control/2",
)
try:
    returned = response.status_code
    expected = 200
    if returned == expected:
        print("PASS")
    else:
        print("FAIL")
    # test 8 length of response --------------------
    if len(response.json()) == 7:
        print("PASS")
    else:
        print("FAIL")
    # test 9 correct flow_limit returned --------------------
    if response.json()["flow_limit"] == 20:
        print("PASS")
    else:
        print("FAIL")

except:
    # print(response.json)
    # print(response.json())
    print("Test Failed to Execute")

# test 10 patch returned success--------------------
data1 = {"flow_limit": 30}
data2 = {"flow_limit": 15}
response = requests.patch(BASE + "device/control/1", data1)
try:
    returned = response.status_code
    expected = 200
    if returned == expected:
        print("PASS 10")
    else:
        print("FAIL 10")

    # test 11 correct flow_limit returned --------------------
    if response.json()["flow_limit"] == 30:
        print("PASS")
    else:
        print("FAIL")

except:
    # print(response.json)
    # print(response.json())
    print("10 or 11: Test Failed to Execute")

# reset data
requests.patch(BASE + "device/control/1", data2)

# --------------------Test API endpoint /device/history--------------------

# test 12 request too many data_points --------------------
response = requests.get(
    BASE + "device/history/1,month,temp,100",
)
try:
    returned = response.status_code
    expected = 400
    if returned == expected:
        print("PASS")
    else:
        print("FAIL")

except:
    # print(response.json)
    # print(response.json())
    print("Test Failed to Execute")


# test 13 request too many data_points --------------------
response = requests.get(
    BASE + "device/history/1,month,temp,5",
)
try:
    returned = response.status_code
    expected = 200
    if returned == expected:
        print("PASS")
    else:
        print("FAIL")

except:
    # print(response.json)
    # print(response.json())
    print("Test Failed to Execute")
